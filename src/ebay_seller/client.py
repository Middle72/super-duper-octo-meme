"""Thin wrapper around the eBay Sell Inventory API.

Docs: https://developer.ebay.com/api-docs/sell/inventory/resources/methods

Creating a live listing is a three-step process against this API:
  1. Create (or replace) an inventory item for a SKU - the product data.
  2. Create an offer for that SKU - price, quantity, listing policies.
  3. Publish the offer - this is what actually creates the live eBay listing.
"""

from __future__ import annotations

from typing import Any

import requests

from ebay_seller.auth import EbayAuth
from ebay_seller.config import EbayConfig


class EbayApiError(RuntimeError):
    def __init__(self, response: requests.Response):
        self.status_code = response.status_code
        try:
            self.errors = response.json()
        except ValueError:
            self.errors = response.text
        super().__init__(f"eBay API error {self.status_code}: {self.errors}")


class EbayInventoryClient:
    def __init__(self, config: EbayConfig, auth: EbayAuth | None = None):
        self._config = config
        self._auth = auth or EbayAuth(config)

    def _headers(self, *, content_language: bool = False) -> dict[str, str]:
        headers = {
            "Authorization": f"Bearer {self._auth.get_access_token()}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        }
        if content_language:
            headers["Content-Language"] = "en-US"
        return headers

    def _url(self, path: str) -> str:
        return f"{self._config.api_base}/sell/inventory/v1{path}"

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        response = requests.request(method, self._url(path), timeout=30, **kwargs)
        if not response.ok:
            raise EbayApiError(response)
        return response

    def create_or_replace_inventory_item(self, sku: str, inventory_item: dict[str, Any]) -> None:
        self._request(
            "PUT",
            f"/inventory_item/{sku}",
            headers=self._headers(content_language=True),
            json=inventory_item,
        )

    def get_inventory_item(self, sku: str) -> dict[str, Any]:
        response = self._request("GET", f"/inventory_item/{sku}", headers=self._headers())
        return response.json()

    def create_merchant_location(self, location_key: str, location: dict[str, Any]) -> None:
        self._request(
            "POST",
            f"/location/{location_key}",
            headers=self._headers(),
            json=location,
        )

    def create_offer(self, offer: dict[str, Any]) -> str:
        response = self._request(
            "POST",
            "/offer",
            headers=self._headers(content_language=True),
            json=offer,
        )
        return response.json()["offerId"]

    def get_offer(self, offer_id: str) -> dict[str, Any]:
        response = self._request("GET", f"/offer/{offer_id}", headers=self._headers())
        return response.json()

    def update_offer(self, offer_id: str, offer: dict[str, Any]) -> None:
        self._request(
            "PUT",
            f"/offer/{offer_id}",
            headers=self._headers(content_language=True),
            json=offer,
        )

    def publish_offer(self, offer_id: str) -> str:
        response = self._request(
            "POST",
            f"/offer/{offer_id}/publish/",
            headers=self._headers(),
        )
        return response.json()["listingId"]

    def withdraw_offer(self, offer_id: str) -> None:
        self._request("POST", f"/offer/{offer_id}/withdraw/", headers=self._headers())
