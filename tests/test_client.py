import pytest
import responses

from ebay_seller.auth import EbayAuth
from ebay_seller.client import EbayApiError, EbayInventoryClient


class FakeAuth(EbayAuth):
    def get_access_token(self) -> str:
        return "fake-token"


@pytest.fixture
def client(config) -> EbayInventoryClient:
    return EbayInventoryClient(config, auth=FakeAuth(config))


@responses.activate
def test_create_offer_returns_offer_id(client, config):
    responses.add(
        responses.POST,
        f"{config.api_base}/sell/inventory/v1/offer",
        json={"offerId": "offer-123"},
        status=201,
    )

    offer_id = client.create_offer({"sku": "SKU-1"})

    assert offer_id == "offer-123"
    assert responses.calls[0].request.headers["Authorization"] == "Bearer fake-token"


@responses.activate
def test_publish_offer_returns_listing_id(client, config):
    responses.add(
        responses.POST,
        f"{config.api_base}/sell/inventory/v1/offer/offer-123/publish/",
        json={"listingId": "listing-456"},
        status=200,
    )

    listing_id = client.publish_offer("offer-123")

    assert listing_id == "listing-456"


@responses.activate
def test_api_error_raises_with_details(client, config):
    responses.add(
        responses.GET,
        f"{config.api_base}/sell/inventory/v1/offer/bad-offer",
        json={"errors": [{"message": "Offer not found"}]},
        status=404,
    )

    with pytest.raises(EbayApiError) as exc_info:
        client.get_offer("bad-offer")

    assert exc_info.value.status_code == 404
    assert "Offer not found" in str(exc_info.value)
