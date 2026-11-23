from pricepulse.matching import comparison_flags


def row(**changes):
    return {"gtin_normalized": "04006381333931", "title": "Example 2 x 1 L", "brand": "Example", "quantity": "2", "unit": "L", **changes}


def test_conservative_matching_flags_and_aliases():
    assert comparison_flags(row(), row()) == []
    assert "description_variant_or_pack_review" in comparison_flags(row(), row(title="Example 1 L"))
    assert "quantity_or_unit_review" in comparison_flags(row(), row(quantity="1"))
    assert "quantity_or_unit_review" in comparison_flags(row(), row(quantity="", unit=""))
    assert "gtin_mismatch_or_invalid" in comparison_flags(row(), row(gtin_normalized=None))
    assert "brand_review" in comparison_flags(row(), row(brand="Other"))
    assert "brand_review" not in comparison_flags(row(), row(brand="Example Co"), {"example co": "example"})
    assert "description_variant_or_pack_review" in comparison_flags(row(title="Example 2 x 1 L"), row(title="Example 1 L"))
    assert "quantity_or_unit_review" in comparison_flags(row(quantity="660", unit="g"), row(quantity="330", unit="g"))
    assert "description_variant_or_pack_review" in comparison_flags(row(title="Example red"), row(title="Example blue"))


def test_cross_retailer_mass_respects_source_columns():
    spar = row(quantity="0,2000", unit="kg")
    kaufland = row(quantity="0.200", unit="KOM")
    chains = ("spar", "kaufland")
    assert comparison_flags(spar, kaufland, cross_retailer_chains=chains) == []
    assert comparison_flags(kaufland, spar, cross_retailer_chains=chains[::-1]) == []
    assert comparison_flags(row(quantity="200", unit="g"), kaufland, cross_retailer_chains=chains) == []
    assert comparison_flags(row(quantity="0,2001", unit="kg"), kaufland, cross_retailer_chains=chains) == [
        "declared_mass_difference_review"
    ]
    for source_unit in ("L", "kom"):
        assert comparison_flags(row(quantity="0,2000", unit=source_unit), kaufland, cross_retailer_chains=chains) == [
            "declared_mass_not_comparable"
        ]
    assert comparison_flags(spar, row(quantity="0", unit="KOM"), cross_retailer_chains=chains) == [
        "declared_mass_not_comparable"
    ]
