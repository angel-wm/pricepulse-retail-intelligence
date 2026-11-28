"""Enforce robots rules and the scoped Konzum CDN unavailable-file policy."""
import logging

from scrapy.downloadermiddlewares.robotstxt import RobotsTxtMiddleware
from scrapy.utils.misc import build_from_crawler

from pricepulse.contracts import KONZUM_CDN_HOST

logger = logging.getLogger(__name__)
DENY_ALL = b"User-agent: *\nDisallow: /\n"


class StrictRobotsMiddleware(RobotsTxtMiddleware):
    async def _parse_robots(self, response, netloc, request):
        if (response.status == 403 and netloc in (KONZUM_CDN_HOST, KONZUM_CDN_HOST + ":443")
                and self.crawler.spider.name == "konzum"):
            # Konzum's public index advertises its CDN CSVs for automated processing.
            # RFC 9309 §2.3.1.3 permits requests when robots.txt itself is unavailable.
            logger.warning("Konzum CDN robots.txt returned HTTP 403; applying the scoped unavailable-file policy")
            self._stats.inc_value("pricepulse/konzum_cdn_robots_unavailable")
            response = response.replace(body=b"")
        elif response.status != 200:
            logger.error("robots.txt returned HTTP %s; denying source requests", response.status)
            self._stats.inc_value("pricepulse/robots_unavailable")
            response = response.replace(body=DENY_ALL)
        await super()._parse_robots(response, netloc, request)

    def _robots_error(self, exc, netloc, request):
        logger.error("robots.txt retrieval failed; denying source requests: %s", exc)
        self._stats.inc_value("pricepulse/robots_unavailable")
        pending = self._parsers[netloc]
        parser = build_from_crawler(self._parserimpl, self.crawler, DENY_ALL)
        self._parsers[netloc] = parser
        pending.callback(parser)
