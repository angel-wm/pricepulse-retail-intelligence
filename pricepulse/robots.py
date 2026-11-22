"""Fail closed when robots.txt cannot be obtained successfully."""
import logging

from scrapy.downloadermiddlewares.robotstxt import RobotsTxtMiddleware
from scrapy.utils.misc import build_from_crawler

logger = logging.getLogger(__name__)
DENY_ALL = b"User-agent: *\nDisallow: /\n"


class StrictRobotsMiddleware(RobotsTxtMiddleware):
    async def _parse_robots(self, response, netloc, request):
        if response.status != 200:
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
