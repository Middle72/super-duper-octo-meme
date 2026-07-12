import responses

from ebay_seller.auth import EbayAuth


@responses.activate
def test_get_access_token_fetches_and_caches(config):
    responses.add(
        responses.POST,
        config.oauth_url,
        json={"access_token": "token-1", "expires_in": 7200},
        status=200,
    )

    auth = EbayAuth(config)

    assert auth.get_access_token() == "token-1"
    assert auth.get_access_token() == "token-1"
    assert len(responses.calls) == 1  # cached, no second request


@responses.activate
def test_get_access_token_refreshes_after_expiry(config):
    responses.add(
        responses.POST,
        config.oauth_url,
        json={"access_token": "token-1", "expires_in": -1},
        status=200,
    )
    responses.add(
        responses.POST,
        config.oauth_url,
        json={"access_token": "token-2", "expires_in": 7200},
        status=200,
    )

    auth = EbayAuth(config)

    assert auth.get_access_token() == "token-1"
    assert auth.get_access_token() == "token-2"
    assert len(responses.calls) == 2
