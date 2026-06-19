# TelegramGifts Complete API Reference

Welcome to the full documentation for `TelegramGifts`, your offline-first solution for fetching Telegram Gift data. This library requires no API keys, auto-updates from a GitHub database, and uses smart ETag caching to prevent rate limits.

---

## 1. Client Initialization

The main entry point for the library is the `TelegramGifts` class.

```python
from TelegramGifts import TelegramGifts

gifts = TelegramGifts(
    repo_url="https://raw.githubusercontent.com/ssamy2/TelegramGiftsAssests/main",
    cache_dir="~/.telegramgifts_cache", # Optional: Specify a custom cache directory
    ttl_seconds=600,                    # Cache Time-To-Live in seconds (10 minutes default)
    enable_cache=True                   # Set to False to force real-time network requests
)
```

---

## 2. Comprehensive Gift Data

### `get_gift(identifier: str) -> Optional[dict]`
The most powerful method. It dynamically resolves the identifier and returns a rich dictionary containing all details.
**Arguments:**
- `identifier`: The gift's ID (e.g., `"6005797617768858105"`), short name (e.g., `"artisan_brick"`), or full name (e.g., `"Artisan Brick"`).
**Returns:**
```python
{
    "id": "6005797617768858105",
    "short_name": "artisan_brick",
    "full_name": "Artisan Brick",
    "type": "UPGRADED", # "UPGRADED", "UNUPGRADED", or "REGULAR"
    "supply": 10000,
    "prices": {
        "floor_price_ton": 51.75,
        "portal_price_ton": 51.75,
        "getgems_price_ton": 59.0,
        "tgmrkt_price_ton": 49.41
    },
    "links": {
        "webp": "https://.../by_id/6005797617768858105.webp",
        "tgs": "https://.../by_id/6005797617768858105.tgs"
    },
    "custom_emoji_id": "5886603410492366880"
}
```

---

## 3. Models and Attributes (For Upgraded Gifts)

### `get_model_details(identifier: str, model_name: Optional[str] = None) -> Union[list, dict, None]`
Fetches intricate details for upgraded models, injecting real-time market prices and WebP/TGS links.
**Arguments:**
- `identifier`: Gift identifier.
- `model_name`: Exact name of the model (case-insensitive). If omitted, returns a list of all models.
**Example Output:**
```python
{
  'name': 'pro_gamer', 
  'rarity_permille': 2.0, 
  'custom_emoji_id': '5881734231838695549', 
  'model_id': '5195366267158033241', 
  'price_ton': 110.0,
  'links': {'webp': '...', 'tgs': '...'}
}
```

### `get_attribute_price(identifier: str, attribute_type: Optional[str] = None, item_name: Optional[str] = None) -> Union[dict, float, None]`
Query specific prices for underlying NFT attributes.
**Arguments:**
- `attribute_type`: Can be `"models"`, `"backdrops"`, or `"symbols"`.
- `item_name`: The specific attribute name (e.g., `"Diamond"`, `"Amber"`).

---

## 4. Bulk Data Retrieval (Lists)

These methods return lists of Python Dataclasses (`GiftDetail` and `RegularGift`).

### `get_upgraded_gifts() -> List[GiftDetail]`
Returns a list of all **Upgraded** (NFT) gifts.

### `get_unupgraded_gifts() -> List[GiftDetail]`
Returns a list of all **Unupgraded** gifts (gifts with limited supply that haven't been minted yet).

### `get_regular_gifts() -> List[RegularGift]`
Returns a list of all **Regular** gifts (standard Telegram gifts).

### `get_all_gifts_details() -> List[GiftDetail]`
Returns a combined list of all upgraded and unupgraded gift details.

### `raw_gifts_details() -> dict`
Returns the raw parsed JSON dictionary from `Gifts_Details.json`.
**Example Output Structure:**
```python
{
  "upgraded": [
    {
      "full_name": "Artisan Brick",
      "short_name": "artisan_brick",
      "regular_id": "6005797617768858105",
      "custom_emoji_id": "5886603410492366880",
      "floor_price_ton": 51.75,
      "models": [ ... ]
    }
  ],
  "unupgraded": [ ... ]
}
```

### `raw_ss_data() -> list`
Returns the raw parsed JSON list from `ss.json`.
**Example Output Structure:**
```python
[
  {
    "id": "5956308547863052791",
    "short_name": "Trojan Horse",
    "full_name": "Trojan Horse",
    "type": "REGULAR",
    "floor_price": "0",
    "supply": 10000
  }
]
```

---

## 5. Market Prices

### `get_upgraded_price(identifier: str, source: str = "tgmrkt") -> Optional[float]`
Fetches the floor price for an upgraded gift from a specific marketplace.
**Arguments:**
- `source`: `"floor"` (overall lowest), `"portal"`, `"getgems"`, or `"tgmrkt"`.

### `get_unupgraded_price(identifier: str) -> Optional[float]`
Returns the standard floor price of an unupgraded gift.

---

## 6. Image and Asset Management

### `get_image_url(identifier: str, ext: str = "webp") -> str`
### `get_image_url_by_id(gift_id: str, ext: str = "webp") -> str`
Returns the direct GitHub URL for the image or animation. Valid extensions: `"webp"`, `"tgs"`.

### `download_image(identifier: str, ext: str = "webp") -> str`
Downloads the asset by name, caches it locally safely (using `.tmp` atomic writes to prevent corruption), and returns the **absolute local path**.
**Returns:** `/home/user/.telegramgifts_cache/webp/artisan_brick.webp`

### `download_image_by_id(gift_id: str, ext: str = "webp") -> str`
Downloads the asset by its numeric ID and returns the absolute local path.

### `download_model_image(short_name: str, model_short_name: str, ext: str = "webp") -> str`
Downloads the specific variant asset for a model (e.g., `pro_gamer.webp` for `artisan_brick`) and returns the local path.

---

## 7. Data Structures (Types)

The library uses Dataclasses for structured data.

### `GiftDetail` (Upgraded & Unupgraded)
- `full_name` (str)
- `short_name` (str)
- `regular_id` (str)
- `custom_emoji_id` (Optional[str])
- `prices` (`GiftPrices` object)
- `models` (List of `ModelInfo` objects)

### `RegularGift`
- `id` (str)
- `short_name` (str)
- `full_name` (str)
- `type` (str)
- `supply` (int)
- `floor_price` (str)
- `is_active` (bool)

---

## 8. Custom Exceptions

Handle errors safely by importing from `TelegramGifts.exceptions`.

```python
from TelegramGifts.exceptions import GitHubFetchError, CacheError

try:
    gifts.download_image("artisan_brick")
except GitHubFetchError as e:
    print(f"Internet connection issue: {e}")
except CacheError as e:
    print(f"Filesystem/Cache issue: {e}")
```

- **`TelegramGiftsError`**: Base class for all library errors.
- **`GitHubFetchError`**: Raised on HTTP/Network failures when pulling data.
- **`CacheError`**: Raised when disk operations fail or cache is misconfigured.
- **`GiftNotFoundError`**: Raised when searching for a gift fails.
- **`InvalidExtensionError`**: Raised if a file extension other than `webp` or `tgs` is requested.
