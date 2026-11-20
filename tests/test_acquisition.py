import hashlib
import json
import pytest
from scrapy.http import HtmlResponse, TextResponse
from pricepulse.contracts import FIELDS, amount, gtin, parse_csv
from pricepulse.spiders import KauflandSpider, SparSpider, safe_url

@pytest.mark.parametrize("source,encoding,sep", [("spar", "cp1250", ";"), ("kaufland", "utf-8-sig", "\t")])
def test_prices_and_dialect(source, encoding, sep):
    fields = FIELDS[source]
    def row(regular, special):
        values = {name: "" for name in fields}
        values.update(title="Čaj", gtin="4006381333931", regular=regular, special=special)
        return sep.join(values[name] for name in fields)
    data = (sep.join(fields.values()) + "\n" + "\n".join([row("2,00", ""), row("", "1,20"), row("2,00", "2,00"), row("2,00", "1,00"), row("x", "")]) + "\n").encode(encoding)
    result = list(parse_csv(data, source, "8702", "2026-11-17", "https://example.test", hashlib.sha256(data).hexdigest()))
    assert [r["price_origin"] for r in result] == ["regular", "special", "both_equal", None, None]
    assert result[1]["effective_price_eur"] == "1.20"
    assert result[0]["gtin_normalized"] == "04006381333931"
    assert result[3]["ingestion_status"] == "conflicting prices"
    assert result[4]["ingestion_status"] == "invalid price"
    with pytest.raises(ValueError, match="headers"):
        list(parse_csv(b"unknown\n", source, "1", "2026-11-17", "x", "x"))

def test_gtin():
    assert str(amount(",99")) == "0.99"
    assert gtin("4006381333931") == "04006381333931"
    assert gtin("4006381333932") is None
    assert gtin("123") is None

def test_selection_and_url_safety():
    spar = SparSpider(date="2026-11-17")
    body = json.dumps({"files": [{"name": "test_8702_x_20261117_0330.csv", "URL": "/data.csv"}, {"name": "test_8703_x_20261117_0330.csv", "URL": "/other.csv"}]}).encode()
    response = TextResponse("https://www.spar.hr/index", body=body, encoding="utf-8")
    assert list(spar.parse_index(response))[0].url == "https://www.spar.hr/data.csv"
    spider = KauflandSpider(date="2026-11-17")
    html = b'''<div data-component="AssetList" data-props='{"settings":{"dataUrlAssets":"/index.json"}}'></div>'''
    response = HtmlResponse("https://www.kaufland.hr/page", body=html, encoding="utf-8")
    assert list(spider.parse(response))[0].url == "https://www.kaufland.hr/index.json"
    data = json.dumps([{"label": "Store_5630_17112026_7-30.csv", "path": "/file.csv"}]).encode()
    response = TextResponse("https://www.kaufland.hr/index.json", body=data, encoding="utf-8")
    assert list(spider.parse_index(response))[0].url == "https://www.kaufland.hr/file.csv"
    with pytest.raises(ValueError):
        safe_url(response.url, "https://evil.test/file.csv", spider.host)
