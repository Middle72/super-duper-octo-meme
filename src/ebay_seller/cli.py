"""Command-line interface for the ebay-seller listing manager."""

from __future__ import annotations

import json

import click

from ebay_seller.client import EbayApiError, EbayInventoryClient
from ebay_seller.config import load_config
from ebay_seller.listing import publish_listing_from_spec


@click.group()
def main() -> None:
    """Manage eBay listings via the Sell Inventory API."""


@main.command("create-location")
@click.option("--key", required=True, help="A short identifier you choose for this location.")
@click.option("--country", required=True, help="ISO country code, e.g. US.")
@click.option("--postal-code", required=True)
@click.option("--city", default=None)
def create_location(key: str, country: str, postal_code: str, city: str | None) -> None:
    """Register the warehouse/location inventory ships from. Run this once per account."""
    config = load_config()
    client = EbayInventoryClient(config)

    address: dict[str, str] = {"country": country, "postalCode": postal_code}
    if city:
        address["city"] = city

    location = {
        "location": {"address": address},
        "locationTypes": ["WAREHOUSE"],
        "name": key,
    }

    try:
        client.create_merchant_location(key, location)
    except EbayApiError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Created merchant location {key!r}. Set EBAY_MERCHANT_LOCATION_KEY={key} in .env")


@main.command("create-listing")
@click.argument("spec_file", type=click.Path(exists=True, dir_okay=False))
def create_listing(spec_file: str) -> None:
    """Publish a live eBay listing from a JSON spec file (see examples/listing.json)."""
    config = load_config()
    client = EbayInventoryClient(config)

    with open(spec_file) as f:
        spec = json.load(f)

    try:
        listing_id = publish_listing_from_spec(client, config, spec)
    except EbayApiError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(f"Published listing {listing_id} for SKU {spec['sku']}")


@main.command("get-offer")
@click.argument("offer_id")
def get_offer(offer_id: str) -> None:
    """Look up an existing offer by ID."""
    config = load_config()
    client = EbayInventoryClient(config)

    try:
        offer = client.get_offer(offer_id)
    except EbayApiError as exc:
        raise click.ClickException(str(exc)) from exc

    click.echo(json.dumps(offer, indent=2))


if __name__ == "__main__":
    main()
