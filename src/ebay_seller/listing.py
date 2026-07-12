"""Turns a simple listing spec (see examples/listing.json) into a live eBay listing."""

from __future__ import annotations

from typing import Any

from ebay_seller.client import EbayInventoryClient
from ebay_seller.config import EbayConfig


def _build_inventory_item(spec: dict[str, Any]) -> dict[str, Any]:
    return {
        "condition": spec["condition"],
        "product": {
            "title": spec["title"],
            "description": spec["description"],
            "aspects": spec.get("aspects", {}),
            "imageUrls": spec["image_urls"],
        },
        "availability": {
            "shipToLocationAvailability": {"quantity": spec["quantity"]},
        },
    }


def _build_offer(spec: dict[str, Any], config: EbayConfig) -> dict[str, Any]:
    merchant_location_key = spec.get("merchant_location_key") or config.merchant_location_key
    if not merchant_location_key:
        raise ValueError(
            "No merchant_location_key in the listing spec and no "
            "EBAY_MERCHANT_LOCATION_KEY configured. Run `ebay-seller create-location` first."
        )

    return {
        "sku": spec["sku"],
        "marketplaceId": config.marketplace_id,
        "format": "FIXED_PRICE",
        "availableQuantity": spec["quantity"],
        "categoryId": spec["category_id"],
        "listingDescription": spec["description"],
        "listingPolicies": spec["listing_policies"],
        "merchantLocationKey": merchant_location_key,
        "pricingSummary": {
            "price": {
                "value": spec["price"]["value"],
                "currency": spec["price"].get("currency", "USD"),
            }
        },
    }


def publish_listing_from_spec(
    client: EbayInventoryClient, config: EbayConfig, spec: dict[str, Any]
) -> str:
    """Create the inventory item + offer for `spec` and publish it. Returns the listing ID."""
    sku = spec["sku"]

    client.create_or_replace_inventory_item(sku, _build_inventory_item(spec))
    offer_id = client.create_offer(_build_offer(spec, config))
    return client.publish_offer(offer_id)
