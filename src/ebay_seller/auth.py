"""OAuth2 token handling for the eBay Sell APIs.

The Sell Inventory API acts on behalf of a seller, so it needs a *user* access
token. Those are minted by exchanging a long-lived refresh token (obtained once
via eBay's "User Access Token" tool at developer.ebay.com/my/auth/) for a
short-lived access token via the refresh_token grant.
"""

from __future__ import annotations

import time

import requests

from ebay_seller.config import EbayConfig

SELL_INVENTORY_SCOPE = "https://api.ebay.com/oauth/api_scope/sell.inventory"


class EbayAuth:
    """Fetches and caches user access tokens for a given config."""

    def __init__(self, config: EbayConfig):
        self._config = config
        self._access_token: str | None = None
        self._expires_at: float = 0.0

    def get_access_token(self) -> str:
        if self._access_token is None or time.time() >= self._expires_at:
            self._refresh()
        assert self._access_token is not None
        return self._access_token

    def _refresh(self) -> None:
        config = self._config
        response = requests.post(
            config.oauth_url,
            auth=(config.client_id, config.client_secret),
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={
                "grant_type": "refresh_token",
                "refresh_token": config.refresh_token,
                "scope": SELL_INVENTORY_SCOPE,
            },
            timeout=30,
        )
        response.raise_for_status()
        payload = response.json()

        self._access_token = payload["access_token"]
        # Refresh a little early to avoid racing against expiry.
        self._expires_at = time.time() + payload["expires_in"] - 60
