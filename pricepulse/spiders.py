import csv
import hashlib
import json
import re
from datetime import datetime, timezone
from pathlib import Path
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
    custom_settings = {
        "ROBOTSTXT_OBEY": True, "CONCURRENT_REQUESTS": 1,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 1, "DOWNLOAD_DELAY": 1,
        "DOWNLOAD_DELAY_JITTER": 0, "DOWNLOAD_TIMEOUT": 30,
        "RETRY_TIMES": 2, "RETRY_HTTP_CODES": [408, 500, 502, 503, 504],
        "DOWNLOAD_MAXSIZE": 50000000, "DOWNLOAD_FAIL_ON_DATALOSS": True,
        "REDIRECT_ENABLED": False, "METAREFRESH_ENABLED": False,
        "COOKIES_ENABLED": False,
        "DOWNLOADER_MIDDLEWARES": {
            "scrapy.downloadermiddlewares.robotstxt.RobotsTxtMiddleware": None,
            "pricepulse.robots.StrictRobotsMiddleware": 100,
        },
    }
    def __init__(self, date=None, raw_path=None, **kwargs):
        super().__init__(**kwargs)
        self.day = __import__('datetime').date.fromisoformat(date)
        self.selected = self.day.isoformat()
        self.raw_path = Path(raw_path) if raw_path else None

    def file_request(self, base, path, sha=None):
        try:
            url = safe_url(base, path, self.host)
        except (ValueError, TypeError) as exc:
            self.stop("unsafe_url", str(exc))
        yield scrapy.Request(url, callback=self.parse_file, cb_kwargs={"expected_sha": sha}, errback=self.failed)

    def stop(self, reason, detail):
        self.logger.error("Acquisition stopped [%s]: %s", reason, detail)
        raise CloseSpider(reason)

    def require_complete(self, response):
        if "partial" in response.flags or "dataloss" in response.flags:
            self.stop("incomplete_response", "Source response is incomplete")

    def failed(self, failure):
        response = getattr(failure.value, "response", None)
        status = response.status if response is not None else None
        reason = {403: "http_forbidden", 404: "http_not_found", 429: "http_rate_limited"}.get(status, "http_error" if status else "download_error")
        self.stop(reason, f"HTTP {status}" if status else failure.getErrorMessage())

    def parse_file(self, response, expected_sha):
        self.require_complete(response)
        digest = hashlib.sha256(response.body).hexdigest()
        if expected_sha and digest.lower() != expected_sha.lower():
            self.stop("source_hash_mismatch", "Downloaded file does not match source SHA-256")
        try:
            rows = list(parse_csv(response.body, self.name, self.store, self.selected, response.url, digest))
        except (csv.Error, ValueError, UnicodeError) as exc:
            self.stop("schema_error", str(exc))
        if self.raw_path is not None:
            try:
                with self.raw_path.open("xb") as raw:
                    raw.write(response.body)
            except OSError as exc:
                self.stop("raw_storage_error", str(exc))
        yield {"type": "manifest", "source": self.name, "store_id": self.store, "publication_date": self.selected, "source_url": response.url, "retrieved_at_utc": datetime.now(timezone.utc).isoformat(), "http_status": response.status, "sha256": digest, "source_sha256": expected_sha, "encoding": self.encoding, "delimiter": self.delimiter, "row_count": len(rows)}
        for row in rows:
            yield {"type": "record", **row}

class SparSpider(BaseSpider):
    name, store, host, encoding, delimiter = "spar", "8702", "www.spar.hr", "cp1250", ";"
    async def start(self):
        url = f"https://www.spar.hr/datoteke_cjenici/Cjenik{self.day:%Y%m%d}.json"
        yield scrapy.Request(url, callback=self.parse_index, errback=self.failed)

    def parse_index(self, response):
        self.require_complete(response)
        try:
            entries = response.json()["files"]
            if not isinstance(entries, list) or any(not isinstance(x, dict) or not isinstance(x.get("name"), str) for x in entries):
                raise ValueError("invalid SPAR file list")
            matches = [x for x in entries if re.search(rf"_{self.store}_", x["name"]) and re.search(rf"_{self.day:%Y%m%d}_\d+\.csv$", x["name"], re.I)]
        except (ValueError, KeyError, TypeError) as exc:
            self.stop("index_schema_error", str(exc))
        if len(matches) != 1:
            self.stop("expected_one_spar_file", f"Found {len(matches)} files for selected store and date")
        if not isinstance(matches[0].get("URL"), str) or (matches[0].get("SHA") is not None and not re.fullmatch(r"[0-9a-fA-F]{64}", str(matches[0]["SHA"]))):
            self.stop("index_schema_error", "Invalid SPAR file URL or hash")
        yield from self.file_request(response.url, matches[0]["URL"], matches[0].get("SHA"))

class KauflandSpider(BaseSpider):
    name, store, host, encoding, delimiter = "kaufland", "5630", "www.kaufland.hr", "utf-8-sig", "tab"
    async def start(self):
        yield scrapy.Request("https://www.kaufland.hr/akcije-novosti/popis-mpc.html", callback=self.parse, errback=self.failed)

    def parse(self, response):
        self.require_complete(response)
        props = response.css('[data-component="AssetList"]::attr(data-props)').getall()
        if len(props) != 1:
            self.stop("expected_one_asset_list", f"Found {len(props)} asset lists")
        try:
            path = json.loads(props[0])["settings"]["dataUrlAssets"]
            url = safe_url(response.url, path, self.host)
        except (KeyError, TypeError, ValueError) as exc:
            self.stop("index_schema_error", str(exc))
        yield scrapy.Request(url, callback=self.parse_index, errback=self.failed)

    def parse_index(self, response):
        self.require_complete(response)
        try:
            entries = response.json()
            if not isinstance(entries, list) or any(not isinstance(x, dict) or not isinstance(x.get("label"), str) for x in entries):
                raise ValueError("invalid Kaufland asset list")
            matches = [x for x in entries if re.search(rf"_{self.store}_{self.day:%d%m%Y}_.*\.csv$", x["label"], re.I)]
        except (ValueError, TypeError) as exc:
            self.stop("index_schema_error", str(exc))
        if len(matches) != 1:
            self.stop("expected_one_kaufland_file", f"Found {len(matches)} files for selected store and date")
        if not isinstance(matches[0].get("path"), str):
            self.stop("index_schema_error", "Missing Kaufland file path")
        yield from self.file_request(response.url, matches[0]["path"])
