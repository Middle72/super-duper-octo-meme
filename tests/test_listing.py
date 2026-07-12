import json
from unittest.mock import MagicMock

from ebay_seller.listing import publish_listing_from_spec


def test_publish_listing_from_spec_calls_client_in_order(config):
    with open("examples/listing.json") as f:
        spec = json.load(f)

    client = MagicMock()
    client.create_offer.return_value = "offer-123"
    client.publish_offer.return_value = "listing-456"

    listing_id = publish_listing_from_spec(client, config, spec)

    assert listing_id == "listing-456"

    client.create_or_replace_inventory_item.assert_called_once()
    sku_arg, inventory_item = client.create_or_replace_inventory_item.call_args.args
    assert sku_arg == "WIDGET-001"
    assert inventory_item["product"]["title"] == spec["title"]

    client.create_offer.assert_called_once()
    (offer_arg,) = client.create_offer.call_args.args
    assert offer_arg["sku"] == "WIDGET-001"
    assert offer_arg["merchantLocationKey"] == "warehouse-1"

    client.publish_offer.assert_called_once_with("offer-123")


def test_publish_listing_requires_merchant_location(config):
    import dataclasses

    import pytest

    from ebay_seller.listing import _build_offer

    config_without_location = dataclasses.replace(config, merchant_location_key=None)
    spec = {
        "sku": "SKU-1",
        "quantity": 1,
        "category_id": "1",
        "description": "d",
        "listing_policies": {},
        "price": {"value": "1.00"},
    }

    with pytest.raises(ValueError, match="merchant_location_key"):
        _build_offer(spec, config_without_location)
