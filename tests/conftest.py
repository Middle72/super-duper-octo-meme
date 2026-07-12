import pytest

from ebay_seller.config import EbayConfig


@pytest.fixture
def config() -> EbayConfig:
    return EbayConfig(
        env="SANDBOX",
        client_id="test-client-id",
        client_secret="test-client-secret",
        refresh_token="test-refresh-token",
        marketplace_id="EBAY_US",
        merchant_location_key="warehouse-1",
    )
