from typing import List, Dict
import hashlib

# EXTENSION POINT: Replace with real API calls to Trustpilot, Google Reviews, etc.
def _fetch_live_reviews(platform: str, url: str) -> List[Dict]:
    return []

def _generate_demo_reviews(url: str) -> List[Dict]:
    url_hash = int(hashlib.md5(url.encode()).hexdigest(), 16)
    demo_templates = [
        {"platform": "Trustpilot", "author": "John_M", "rating": 5, "text": "Absolutely amazing product! Fast shipping and great quality."},
        {"platform": "Trustpilot", "author": "Sarah_K", "rating": 4, "text": "Good product but packaging could be better."},
        {"platform": "Amazon", "author": "Mike D.", "rating": 5, "text": "Best purchase ever! Highly recommend!"},
        {"platform": "Amazon", "author": "reviewer_12345", "rating": 5, "text": "EXCELLENT VALUE!!! MUST BUY!!! 10/10!!!"},
        {"platform": "Google", "author": "Alex P.", "rating": 3, "text": "Average experience. Nothing special."},
    ]
    num_reviews = (url_hash % 4) + 3
    start_idx = (url_hash // 5) % len(demo_templates)
    return [demo_templates[(start_idx + i) % len(demo_templates)] for i in range(num_reviews)]

def fetch_reviews(url: str) -> List[Dict]:
    live_reviews = _fetch_live_reviews("all", url)
    if live_reviews:
        return live_reviews
    return _generate_demo_reviews(url)
