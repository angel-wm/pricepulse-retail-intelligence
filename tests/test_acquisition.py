import hashlib
import json
import pytest
from scrapy.http import HtmlResponse, TextResponse
from scrapy.exceptions import CloseSpider
from pricepulse.contracts import FIELDS, amount, gtin, parse_csv
from pricepulse.spiders import KauflandSpider, KonzumSpider, SparSpider, safe_url

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


def test_spar_accepts_a_missing_category_but_requires_price_headers():
    fields = FIELDS["spar"]
    values = dict(title="Čaj", code="101", brand="Example", quantity="0,1",
                  unit="kg", regular="2,40", special="", gtin="4006381333931")

    def parse(fields_to_emit):
        headers = ";".join(fields[key] for key in fields_to_emit)
        row = ";".join(values[key] for key in fields_to_emit)
        body = f"{headers}\n{row}\n".encode("cp1250")
        return list(parse_csv(body, "spar", "8702", "2026-11-25", "x", "x"))

    (record,) = parse(list(values))
    assert record["category"] is None
    assert record["effective_price_eur"] == "2.40"
    assert record["gtin_normalized"] == "04006381333931"
    with pytest.raises(ValueError, match="headers"):
        parse([key for key in values if key != "special"])
    with pytest.raises(ValueError, match="headers"):
        parse([*values, "regular"])
    values["category"] = "Čajevi"
    assert parse(list(values))[0]["category"] == "Čajevi"


def test_spar_routes_the_listed_price_from_the_new_promotion_flag_layout():
    fields = FIELDS["spar"]
    header = ";".join(
        [fields[key] for key in ("title", "code", "brand", "quantity", "unit", "regular", "special")]
        + ["cijena za jedinicu mjere (EUR)", fields["gtin"], "sidrena cijena (EUR)"]
    )
    body = (
        header + "\n"
        "Čaj;101;Example;0,1;kg;2,40;NE;24,00;4006381333931;3,10\n"
        "Čaj;102;Example;0,1;kg;1,80;DA;18,00;4006381333931;3,10\n"
        "Čaj;103;Example;0,1;kg;1,80;UNKNOWN;18,00;4006381333931;3,10\n"
    ).encode("cp1250")

    regular, special, unknown = parse_csv(body, "spar", "8702", "2026-11-25", "x", "x")
    assert (regular["price_origin"], regular["regular_price_eur"]) == ("regular", "2.40")
    assert (special["price_origin"], special["effective_price_eur"]) == ("special", "1.80")
    assert special["regular_price_eur"] is None and special["category"] is None
    assert special["raw_row"]["sidrena cijena (EUR)"] == "3,10"
    assert unknown["ingestion_status"] == "unknown promotion indicator"
    assert unknown["effective_price_eur"] is None


def test_gtin():
    assert str(amount(",99")) == "0.99"
    assert gtin("4006381333931") == "04006381333931"
    assert gtin("4006381333932") is None
    assert gtin("123") is None

def test_selection_and_url_safety():
    spar = SparSpider(date="2026-11-17")
    body = json.dumps({"files": [{"name": "test_8702_x_20261117_0330.csv", "URL": "/data.csv"}, {"name": "test_8703_x_20261117_0330.csv", "URL": "/other.csv"}]}).encode()
    response = TextResponse("https://www.spar.hr/index", body=body, encoding="utf-8")
    request = list(spar.parse_index(response))[0]
    assert request.url == "https://www.spar.hr/data.csv"
    assert request.cb_kwargs["discovery"] == {"index_url": response.url, "index_item_count": 2, "selected_file_count": 1, "fetched_file_count": 1}
    spider = KauflandSpider(date="2026-11-17")
    html = b'''<div data-component="AssetList" data-props='{"settings":{"dataUrlAssets":"/index.json"}}'></div>'''
    response = HtmlResponse("https://www.kaufland.hr/page", body=html, encoding="utf-8")
    assert list(spider.parse(response))[0].url == "https://www.kaufland.hr/index.json"
    data = json.dumps([{"label": "Store_5630_17112026_7-30.csv", "path": "/file.csv"}]).encode()
    response = TextResponse("https://www.kaufland.hr/index.json", body=data, encoding="utf-8")
    request = list(spider.parse_index(response))[0]
    assert request.url == "https://www.kaufland.hr/file.csv"
    assert request.cb_kwargs["discovery"]["index_item_count"] == 1
    with pytest.raises(ValueError):
        safe_url(response.url, "https://evil.test/file.csv", spider.host)


def test_kaufland_selects_new_filename_for_exact_store_and_date():
    spider = KauflandSpider(date="2026-11-23")
    entries = [
        {"label": "123_Example_5630_cjenik robe_1_20261122_0730.csv", "path": "/prior-day.csv"},
        {"label": "123_Example_5631_cjenik robe_1_20261123_0730.csv", "path": "/other-store.csv"},
        {"label": "123_Example_5630_cjenik robe_1_20261123_0730.csv", "path": "/correct.csv"},
    ]
    response = TextResponse("https://www.kaufland.hr/index", body=json.dumps(entries).encode(), encoding="utf-8")
    (request,) = spider.parse_index(response)
    assert request.url == "https://www.kaufland.hr/correct.csv"


def test_konzum_preserves_listed_price_origin_and_promotion_metadata():
    header = ",".join([*FIELDS["konzum"].values(), "NAZIV POSEBNOG OBLIKA PRODAJE", "BAZNA CIJENA"])
    body = (
        header + "\n"
        "Čaj,101,Example,0.1,kg,2.40,NE,4006381333931,,3.10\n"
        'Čaj,102,Example,0.1,kg,"1,80",DA,0000000000000,Akcijska prodaja,3.10\n'
        "Čaj,103,Example,0.1,kg,2.40,UNKNOWN,4006381333931,,3.10\n"
    ).encode("utf-8-sig")
    regular, special, unknown = parse_csv(body, "konzum", "1280", "2026-11-23", "x", "x")
    assert (regular["price_origin"], regular["effective_price_eur"]) == ("regular", "2.40")
    assert (special["price_origin"], special["effective_price_eur"]) == ("special", "1.80")
    assert special["regular_price_eur"] is None and special["gtin_normalized"] is None
    assert special["raw_row"]["BAZNA CIJENA"] == "3.10"
    assert unknown["ingestion_status"] == "unknown promotion indicator"
    assert unknown["effective_price_eur"] is None


def test_konzum_selects_unique_store_and_date_from_download_links():
    spider = KonzumSpider(date="2026-11-23")
    link = "/cjenici/download?title=SUPER%2CEXAMPLE%2C1280%2C1000%2C23.11.2026%2C+10-45.CSV"
    other_store = link.replace("1280", "1281")
    prior_day = link.replace("23.11.2026", "22.11.2026")

    def response(*links):
        body = "".join(f'<a href="{href}">Download</a>' for href in links).encode()
        return HtmlResponse("https://www.konzum.hr/cjenici?date=2026-11-23", body=body)

    (request,) = spider.parse_index(response(other_store, prior_day, link, link))
    assert request.url == "https://www.konzum.hr" + link
    assert request.cb_kwargs["discovery"]["index_item_count"] == 3
    with pytest.raises(CloseSpider) as missing:
        list(spider.parse_index(response(other_store, prior_day)))
    assert missing.value.reason == "expected_one_konzum_file"
    with pytest.raises(CloseSpider) as ambiguous:
        list(spider.parse_index(response(link, link.replace("1000", "1001"))))
    assert ambiguous.value.reason == "expected_one_konzum_file"
    with pytest.raises(CloseSpider) as unsafe:
        list(spider.parse_index(response("https://example.test" + link)))
    assert unsafe.value.reason == "unsafe_url"

    cdn = "https://d2depcln7eup0h.cloudfront.net/20261123-SUPER%2CEXAMPLE%2C1280%2C1000%2C23.11.2026%2C%2010-45.CSV"
    (request,) = spider.parse_index(response(cdn, cdn, other_store, cdn.replace("20261123-", "20261122-")))
    assert request.url == cdn
    assert request.cb_kwargs["discovery"]["selected_file_count"] == 1
    assert not request.meta.get("dont_obey_robotstxt")
    with pytest.raises(CloseSpider) as mixed:
        list(spider.parse_index(response(link, cdn)))
    assert mixed.value.reason == "expected_one_konzum_file"
