import json

import pytest
from scrapy.crawler import Crawler
from scrapy.downloadermiddlewares.retry import RetryMiddleware
from scrapy.downloadermiddlewares.robotstxt import RobotsTxtMiddleware
from scrapy.exceptions import CloseSpider, IgnoreRequest, ResponseDataLossError
from scrapy.http import Request, Response, TextResponse
from scrapy.robotstxt import ProtegoRobotParser
from scrapy.settings import Settings
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.statscollectors import MemoryStatsCollector
from twisted.internet.error import TimeoutError
from twisted.python.failure import Failure
from twisted.internet.defer import Deferred

from pricepulse.robots import StrictRobotsMiddleware
from pricepulse.contracts import KONZUM_CDN_HOST
from pricepulse.spiders import KauflandSpider, KonzumSpider, SparSpider, safe_url


@pytest.fixture
def crawler():
    settings = Settings()
    for key, value in SparSpider.custom_settings.items():
        settings.set(key, value, priority="spider")
    instance = Crawler(SparSpider, settings)
    instance.stats = MemoryStatsCollector(instance)
    instance.spider = SparSpider(date="2026-11-17")
    instance.spider.crawler = instance
    return instance


def test_bounded_retry_and_access_responses(crawler):
    middleware = RetryMiddleware.from_crawler(crawler)
    request = Request("https://www.spar.hr/test")
    for status in (403, 404, 429):
        response = Response(request.url, status=status, request=request)
        assert middleware.process_response(request, response) is response
    response = Response(request.url, status=503, request=request)
    retry1 = middleware.process_response(request, response)
    retry2 = middleware.process_response(retry1, response)
    assert retry1.meta["retry_times"] == 1
    assert retry2.meta["retry_times"] == 2
    assert middleware.process_response(retry2, response) is response
    assert crawler.stats.get_value("retry/count") == 2
    assert crawler.stats.get_value("retry/max_reached") == 1
    assert isinstance(middleware.process_exception(request, TimeoutError()), Request)
    assert isinstance(middleware.process_exception(request, ResponseDataLossError()), Request)


@pytest.mark.parametrize("status,reason", [(403, "http_forbidden"), (404, "http_not_found"), (429, "http_rate_limited"), (500, "http_error")])
def test_failure_classification_and_logging(status, reason, caplog):
    spider = SparSpider(date="2026-11-17")
    response = Response("https://www.spar.hr/test", status=status)
    with pytest.raises(CloseSpider) as exc:
        spider.failed(Failure(HttpError(response)))
    assert exc.value.reason == reason
    assert reason in caplog.text and str(status) in caplog.text


def test_robots_denial_is_classified_as_blocked(caplog):
    spider = SparSpider(date="2026-11-17")
    with pytest.raises(CloseSpider) as exc:
        spider.failed(Failure(IgnoreRequest("Forbidden by robots.txt")))
    assert exc.value.reason == "request_blocked"
    assert "Forbidden by robots.txt" in caplog.text


def test_request_controls_and_robots(crawler):
    settings = crawler.settings
    assert settings.getbool("ROBOTSTXT_OBEY")
    assert settings.getint("CONCURRENT_REQUESTS_PER_DOMAIN") == 1
    assert settings.getfloat("DOWNLOAD_DELAY") == 1
    assert settings.getfloat("DOWNLOAD_DELAY_JITTER") == 0
    assert settings.getint("DOWNLOAD_TIMEOUT") == 30
    assert settings.getbool("DOWNLOAD_FAIL_ON_DATALOSS")
    assert not settings.getbool("REDIRECT_ENABLED")
    robots = RobotsTxtMiddleware.from_crawler(crawler)
    parser = ProtegoRobotParser.from_crawler(crawler, b"User-agent: *\nDisallow: /private\n")
    robots.process_request_2(parser, Request("https://www.spar.hr/public"))
    with pytest.raises(IgnoreRequest):
        robots.process_request_2(parser, Request("https://www.spar.hr/private"))
    assert crawler.stats.get_value("robotstxt/forbidden") == 1


@pytest.mark.parametrize("url", ["http://www.spar.hr/a", "https://evil.test/a", "https://www.spar.hr.evil.test/a", "https://user@www.spar.hr/a", "https://www.spar.hr:444/a"])
def test_disallowed_hosts(url):
    with pytest.raises(ValueError):
        safe_url("https://www.spar.hr/", url, "www.spar.hr")


def test_invalid_indexes_and_bounded_selection(caplog):
    spider = SparSpider(date="2026-11-17")
    for data in (b"{", b'{"files":{}}', b'{"files":[{}]}'):
        with pytest.raises(CloseSpider) as exc:
            list(spider.parse_index(TextResponse("https://www.spar.hr/index", body=data, encoding="utf-8")))
        assert exc.value.reason == "index_schema_error"
    for entries in ([], [{"name": "x_8702_x_20261116_1000.csv"}], [{"name": "x_8702_x_20261117_1000.csv"}] * 2):
        data = json.dumps({"files": entries}).encode()
        with pytest.raises(CloseSpider) as exc:
            list(spider.parse_index(TextResponse("https://www.spar.hr/index", body=data, encoding="utf-8")))
        assert exc.value.reason == "expected_one_spar_file"
    assert "index_schema_error" in caplog.text
    kauf = KauflandSpider(date="2026-11-17")
    with pytest.raises(CloseSpider) as exc:
        list(kauf.parse_index(TextResponse("https://www.kaufland.hr/index", body=b"{}", encoding="utf-8")))
    assert exc.value.reason == "index_schema_error"


@pytest.mark.parametrize("flag", ["partial", "dataloss"])
def test_partial_file_stops_before_manifest(flag, caplog):
    spider = SparSpider(date="2026-11-17")
    response = Response("https://www.spar.hr/file.csv", body=b"partial", flags=[flag])
    with pytest.raises(CloseSpider) as exc:
        list(spider.parse_file(response, expected_sha=None))
    assert exc.value.reason == "incomplete_response"
    assert "incomplete_response" in caplog.text


def test_kaufland_rejects_unsafe_index():
    spider = KauflandSpider(date="2026-11-17")
    body = b'''<div data-component="AssetList" data-props='{"settings":{"dataUrlAssets":"https://evil.test/index"}}'></div>'''
    from scrapy.http import HtmlResponse
    response = HtmlResponse("https://www.kaufland.hr/page", body=body, encoding="utf-8")
    with pytest.raises(CloseSpider) as exc:
        list(spider.parse(response))
    assert exc.value.reason == "index_schema_error"


@pytest.mark.parametrize("failure_mode", ["http", "transport"])
def test_robots_unavailable_denies_requests(crawler, failure_mode, monkeypatch):
    middleware = StrictRobotsMiddleware.from_crawler(crawler)
    request = Request("https://www.spar.hr/robots.txt")
    middleware._parsers["www.spar.hr"] = Deferred()
    if failure_mode == "http":
        async def parse_fixture(self, response, netloc, req):
            self._parsers[netloc] = ProtegoRobotParser.from_crawler(crawler, response.body)
        monkeypatch.setattr(RobotsTxtMiddleware, "_parse_robots", parse_fixture)
        response = Response(request.url, status=403, body=b"", request=request)
        coroutine = middleware._parse_robots(response, "www.spar.hr", request)
        with pytest.raises(StopIteration):
            coroutine.send(None)
    else:
        middleware._robots_error(TimeoutError(), "www.spar.hr", request)
    parser = middleware._parsers["www.spar.hr"]
    assert not parser.allowed("https://www.spar.hr/file", "PricePulse")
    assert crawler.stats.get_value("pricepulse/robots_unavailable") == 1


@pytest.mark.parametrize("status,spider_class,allowed", [
    (403, KonzumSpider, True),
    (403, SparSpider, False),
    (404, KonzumSpider, False),
    (429, KonzumSpider, False),
    (503, KonzumSpider, False),
    (200, KonzumSpider, False),
])
def test_konzum_cdn_robots_policy(crawler, monkeypatch, status, spider_class, allowed):
    crawler.spider = spider_class(date="2026-11-27")
    middleware = StrictRobotsMiddleware.from_crawler(crawler)
    url = f"https://{KONZUM_CDN_HOST}"
    request = Request(url + "/robots.txt")

    async def parse_fixture(self, response, netloc, request):
        self._parsers[netloc] = ProtegoRobotParser.from_crawler(crawler, response.body)

    monkeypatch.setattr(RobotsTxtMiddleware, "_parse_robots", parse_fixture)
    response = Response(request.url, status=status, body=b"User-agent: *\nDisallow: /\n")
    coroutine = middleware._parse_robots(response, KONZUM_CDN_HOST, request)
    with pytest.raises(StopIteration):
        coroutine.send(None)
    assert middleware._parsers[KONZUM_CDN_HOST].allowed(url + "/file.csv", "PricePulse") is allowed
    assert crawler.stats.get_value("pricepulse/konzum_cdn_robots_unavailable", 0) == int(allowed)
