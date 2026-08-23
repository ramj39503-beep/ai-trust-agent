from pydantic import BaseModel
from typing import List, Dict, Optional

class Review(BaseModel):
    platform: str
    author: str
    rating: float
    text: str

class AnalyzeRequest(BaseModel):
    url: str

class AnalyzeResponse(BaseModel):
    url: str
    reviews: List[Dict]
    sentiment: Dict
    fake_reviews: Dict
    prices: List[Dict]
    alternatives: List[Dict]
    trust_signals: List[Dict]
    recommendation: Dict
    demo_mode: bool
