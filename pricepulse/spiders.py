import hashlib
import json
import re
from datetime import date, datetime, timezone
from urllib.parse import urljoin, urlsplit

import scrapy
from scrapy.exceptions import CloseSpider
from pricepulse.contracts import parse_csv

def safe_url(base, url, host):
    result = urljoin(base, url)
    parts = urlsplit(result)
    if parts.scheme != "https" or parts.hostname != host or parts.username or parts.password or parts.port not in (None, 443):
        raise ValueError("unapproved URL")
    return result

class BaseSpider(scrapy.Spider):
    custom_settings = {"ROBOTSTXT_OBEY": True, "CONCURRENT_REQUESTS": 1, "DOWNLOAD_DELAY": 1, "RETRY_TIMES": 2, "DOWNLOAD_MAXSIZE": 50000000, "REDIRECT_ENABLED": False, "COOKIES_ENABLED": False}
    def __init__(self, date=None, **kwargs):
        super().__init__(**kwargs)
        self.day = __import__('datetime').date.fromisoformat(date)
        self.selected = self.day.isoformat()

    def file_request(self, base, path, sha=None):
        url = safe_url(base, path, self.host)
        yield scrapy.Request(url, callback=self.parse_file, cb_kwargs={"expected_sha": sha}, errback=self.failed)

    def failed(self, failure):
        self.logger.error("Acquisition failed: %s", failure.getErrorMessage())
        raise CloseSpider("acquisition_failed")

    def parse_file(self, response, expected_sha):
        digest = hashlib.sha256(response.body).hexdigest()
        if expected_sha and digest.lower() != expected_sha.lower():
            raise CloseSpider("source_hash_mismatch")
        try:
            rows = list(parse_csv(response.body, self.name, self.store, self.selected, response.url, digest))
        except (ValueError, UnicodeError) as exc:
            raise CloseSpider(f"schema_error: {exc}") from exc
        yield {"type": "manifest", "source": self.name, "store_id": self.store, "publication_date": self.selected, "source_url": response.url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "http_status": response.status, "sha256": digest, "source_sha256": expected_sha, "encoding": self.encoding, "delimiter": self.delimiter, "row_count": len(rows)}
        for row in rows:
            yield {"type": "record", **row}

class SparSpider(BaseSpider):
    name, store, host, encoding, delimiter = "spar", "8702", "www.spar.hr", "cp1250", ";"
    async def start(self):
        url = f"https://www.spar.hr/datoteke_cjenici/Cjenik{self.day:%Y%m%d}.json"
        yield scrapy.Request(url, callback=self.parse_index, errback=self.failed)

    def parse_index(self, response):
        entries = response.json()["files"]
        matches = [x for x in entries if re.search(rf"_{self.store}_", x["name"]) and re.search(rf"_{self.day:%Y%m%d}_\d+\.csv$", x["name"], re.I)]
        if len(matches) != 1:
            raise CloseSpider("expected_one_spar_file")
        yield from self.file_request(response.url, matches[0]["URL"], matches[0].get("SHA"))

class KauflandSpider(BaseSpider):
    name, store, host, encoding, delimiter = "kaufland", "5630", "www.kaufland.hr", "utf-8-sig", "tab"
    async def start(self):
        yield scrapy.Request("https://www.kaufland.hr/akcije-novosti/popis-mpc.html", callback=self.parse, errback=self.failed)

    def parse(self, response):
        props = response.css('[data-component="AssetList"]::attr(data-props)').getall()
        if len(props) != 1:
            raise CloseSpider("expected_one_asset_list")
        path = json.loads(props[0])["settings"]["dataUrlAssets"]
        yield scrapy.Request(safe_url(response.url, path, self.host), callback=self.parse_index, errback=self.failed)

    def parse_index(self, response):
        matches = [x for x in response.json() if re.search(rf"_{self.store}_{self.day:%d%m%Y}_.*\.csv$", x["label"], re.I)]
        if len(matches) != 1:
            raise CloseSpider("expected_one_kaufland_file")
        yield from self.file_request(response.url, matches[0]["path"])
