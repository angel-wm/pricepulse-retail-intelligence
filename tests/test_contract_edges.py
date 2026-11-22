"""Synthetic source contracts and provenance; no retailer records."""
import csv
import hashlib
import io

import pytest
from scrapy.exceptions import CloseSpider
from scrapy.http import Response

from pricepulse.contracts import FIELDS, parse_csv
from pricepulse.spiders import KauflandSpider, SparSpider


@pytest.fixture(params=[("spar", "cp1250", ";", "8702"), ("kaufland", "utf-8-sig", "\t", "5630")])
def source(request):
    return request.param


def make_csv(source, rows, extra_header=None):
    name, encoding, delimiter, _ = source
    headers = list(FIELDS[name].values())
    if extra_header:
        headers.append(extra_header)
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fieldnames=headers, delimiter=delimiter, lineterminator="\n")
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode(encoding)


def test_missing_prices_and_invalid_identifiers(source):
    name, _, _, store = source
    fields = FIELDS[name]
    body = make_csv(source, [{fields["gtin"]: "00000000000000", fields["regular"]: "", fields["special"]: ""},
                             {fields["gtin"]: "4006381333932", fields["regular"]: "1,25"}])
    records = list(parse_csv(body, name, store, "2026-11-17", "https://example.test/file", "abc"))
    assert records[0]["ingestion_status"] == "missing price"
    assert records[0]["effective_price_eur"] is None
    assert records[1]["gtin_raw"] == "4006381333932"
    assert records[1]["gtin_normalized"] is None
    assert records[1]["source_store_id"] == store
    assert records[1]["price_list_date"] == "2026-11-17"
    assert records[1]["source_file_hash"] == "abc"


def test_header_drift_and_malformed_rows(source):
    name, encoding, delimiter, store = source
    header = delimiter.join(FIELDS[name].values())
    for text in (header + delimiter + list(FIELDS[name].values())[0] + "\n", header + "\n" + delimiter.join(["x"] * (len(FIELDS[name]) - 1)) + "\n"):
        with pytest.raises(ValueError):
            list(parse_csv(text.encode(encoding), name, store, "2026-11-17", "url", "hash"))
    with pytest.raises(csv.Error):
        list(parse_csv((header + '\n"unclosed').encode(encoding), name, store, "2026-11-17", "url", "hash"))
    body = make_csv(source, [{FIELDS[name]["regular"]: "1,00", "new column": "retained"}], extra_header="new column")
    assert list(parse_csv(body, name, store, "2026-11-17", "url", "hash"))[0]["raw_row"]["new column"] == "retained"


def test_manifest_provenance_and_hash_failure(source):
    name, _, _, store = source
    spider = (SparSpider if name == "spar" else KauflandSpider)(date="2026-11-17")
    body = make_csv(source, [{FIELDS[name]["regular"]: "1,00"}])
    digest = hashlib.sha256(body).hexdigest()
    response = Response(f"https://www.{name}.hr/file.csv", body=body, status=200)
    output = list(spider.parse_file(response, expected_sha=digest))
    manifest, row = output
    assert manifest["sha256"] == digest == row["source_file_hash"]
    assert manifest["store_id"] == row["source_store_id"] == store
    assert manifest["publication_date"] == row["price_list_date"] == "2026-11-17"
    assert manifest["source_url"] == row["source_url"] == response.url
    assert manifest["row_count"] == 1 and manifest["http_status"] == 200
    with pytest.raises(CloseSpider) as exc:
        list(spider.parse_file(response, expected_sha="0" * 64))
    assert exc.value.reason == "source_hash_mismatch"


def test_invalid_csv_fails_closed(source):
    name, encoding, delimiter, _ = source
    spider = (SparSpider if name == "spar" else KauflandSpider)(date="2026-11-17")
    header = delimiter.join(FIELDS[name].values())
    response = Response(f"https://www.{name}.hr/file.csv", body=(header + '\n"unclosed').encode(encoding))
    with pytest.raises(CloseSpider) as exc:
        list(spider.parse_file(response, expected_sha=None))
    assert exc.value.reason == "schema_error"
