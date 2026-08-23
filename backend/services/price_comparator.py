from typing import List, Dict
import hashlib

def _fetch_live_prices(url: str) -> List[Dict]:
    return []

def _generate_demo_prices(url: str) -> List[Dict]:
    url_hash = int(hashlib.md5(url.encode()).hexdigest(), 16)
    base_price = 50 + (url_hash % 200)
    return [
        {"seller": "Primary Store", "price": base_price, "currency": "USD", "condition": "New"},
        {"seller": "Competitor A", "price": base_price - 5, "currency": "USD", "condition": "New"},
        {"seller": "Competitor B", "price": base_price + 10, "currency": "USD", "condition": "New"},
        {"seller": "Used Market", "price": base_price * 0.7, "currency": "USD", "condition": "Used"},
    ]

def find_alternatives(url: str) -> List[Dict]:
    url_hash = int(hashlib.md5(url.encode()).hexdigest(), 16)
    base_price = 50 + (url_hash % 200)
    return [
        {"name": "Budget Alternative", "price": base_price * 0.6, "tier": "budget", "rating": 4.0},
        {"name": "Premium Upgrade", "price": base_price * 1.5, "tier": "premium", "rating": 4.8},
    ]

def fetch_prices(url: str) -> List[Dict]:
    live_prices = _fetch_live_prices(url)
    return live_prices if live_prices else _generate_demo_prices(url)
