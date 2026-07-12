# super-duper-octo-meme

Online selling automation. First marketplace: **eBay**.

`ebay-seller` is a small Python CLI that publishes live eBay listings using
eBay's [Sell Inventory API](https://developer.ebay.com/api-docs/sell/inventory/resources/methods),
the modern REST API that replaced the old Trading API's `AddItem` call.

## How it works

Publishing a listing on eBay via this API is a 3-step process, all handled by
`ebay-seller create-listing`:

1. **Inventory item** - the product data for a SKU (title, description, images, aspects, quantity).
2. **Offer** - price, category, and listing policies for that SKU on a specific marketplace.
3. **Publish** - turns the offer into a live listing and returns a `listingId`.

## Setup

### 1. Get eBay developer credentials

1. Create a developer account at [developer.ebay.com](https://developer.ebay.com).
2. Under **My Account -> Application Keys**, create a keyset (start with the
   **Sandbox** keyset so you can test without touching real listings). Note
   the Client ID and Client Secret.
3. Under **My Account -> User Access Tokens** (developer.ebay.com/my/auth/),
   generate a **User Access Token** for your own sandbox seller account with
   the `sell.inventory` scope, and copy the **refresh token** it gives you
   (valid for ~18 months, so you only need to do this once).
4. In **Seller Hub / Business Policies**, create (or note the IDs of) a
   fulfillment policy, payment policy, and return policy - the Inventory API
   requires these on every offer.

### 2. Install

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### 3. Configure

```bash
cp .env.example .env
# then fill in EBAY_CLIENT_ID, EBAY_CLIENT_SECRET, EBAY_REFRESH_TOKEN, etc.
```

### 4. Register a shipping location (once per account)

```bash
ebay-seller create-location --key warehouse-1 --country US --postal-code 94105
```

Copy the key into `EBAY_MERCHANT_LOCATION_KEY` in `.env`.

### 5. Publish a listing

Edit `examples/listing.json` (or create your own) with your product details
and real business policy IDs, then:

```bash
ebay-seller create-listing examples/listing.json
```

## Other commands

```bash
ebay-seller get-offer <offer-id>   # inspect an existing offer
```

## Running tests

```bash
pytest
```

## Project layout

```
src/ebay_seller/
  config.py   - loads settings from environment / .env
  auth.py     - OAuth2 refresh_token flow, caches the access token
  client.py   - thin wrapper over the Sell Inventory API endpoints
  listing.py  - builds inventory item / offer payloads from a listing spec
  cli.py      - the `ebay-seller` command-line entrypoint
examples/listing.json - example listing spec
tests/                - unit tests (HTTP calls mocked with `responses`)
```

## Roadmap

This starts with eBay; the config/client/listing split is meant to make room
for additional marketplaces (Amazon, Etsy, ...) as separate modules later.
