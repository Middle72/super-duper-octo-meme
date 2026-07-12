"""Environment-based configuration for the eBay Seller tools."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv

_SANDBOX_API_BASE = "https://api.sandbox.ebay.com"
_PRODUCTION_API_BASE = "https://api.ebay.com"

_SANDBOX_OAUTH_URL = "https://api.sandbox.ebay.com/identity/v1/oauth2/token"
_PRODUCTION_OAUTH_URL = "https://api.ebay.com/identity/v1/oauth2/token"


@dataclass(frozen=True)
class EbayConfig:
    env: str
    client_id: str
    client_secret: str
    refresh_token: str
    marketplace_id: str
    merchant_location_key: str | None

    @property
    def api_base(self) -> str:
        return _SANDBOX_API_BASE if self.env == "SANDBOX" else _PRODUCTION_API_BASE

    @property
    def oauth_url(self) -> str:
        return _SANDBOX_OAUTH_URL if self.env == "SANDBOX" else _PRODUCTION_OAUTH_URL


def load_config() -> EbayConfig:
    """Load configuration from environment variables (and a local .env file, if present)."""
    load_dotenv()

    env = os.environ.get("EBAY_ENV", "SANDBOX").upper()
    if env not in ("SANDBOX", "PRODUCTION"):
        raise ValueError(f"EBAY_ENV must be SANDBOX or PRODUCTION, got {env!r}")

    def require(name: str) -> str:
        value = os.environ.get(name)
        if not value:
            raise ValueError(f"Missing required environment variable: {name}")
        return value

    return EbayConfig(
        env=env,
        client_id=require("EBAY_CLIENT_ID"),
        client_secret=require("EBAY_CLIENT_SECRET"),
        refresh_token=require("EBAY_REFRESH_TOKEN"),
        marketplace_id=os.environ.get("EBAY_MARKETPLACE_ID", "EBAY_US"),
        merchant_location_key=os.environ.get("EBAY_MERCHANT_LOCATION_KEY") or None,
    )
