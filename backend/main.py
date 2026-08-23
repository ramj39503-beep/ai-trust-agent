from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Dict
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from services.review_aggregator import fetch_reviews
from services.sentiment import analyze_sentiment
from services.fake_review_detector import detect_fake_reviews
from services.price_comparator import fetch_prices, find_alternatives
from services.trust_checker import check_trust
from services.recommendation import build_recommendation

app = FastAPI()

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

@app.get("/")
async def serve_frontend():
    return FileResponse(os.path.join(os.path.dirname(__file__), "../frontend/index.html"))

@app.post("/api/analyze")
async def analyze(request: AnalyzeRequest) -> AnalyzeResponse:
    url = request.url
    if not url.startswith(("http://", "https://")):
        raise HTTPException(status_code=400, detail="URL must start with http:// or https://")
    
    reviews = fetch_reviews(url)
    sentiment = analyze_sentiment(reviews)
    fake_reviews = detect_fake_reviews(reviews)
    prices = fetch_prices(url)
    alternatives = find_alternatives(url)
    trust_signals = check_trust(url)
    recommendation = build_recommendation(sentiment, fake_reviews, prices, trust_signals)
    
    return AnalyzeResponse(
        url=url,
        reviews=reviews,
        sentiment=sentiment,
        fake_reviews=fake_reviews,
        prices=prices,
        alternatives=alternatives,
        trust_signals=trust_signals,
        recommendation=recommendation,
        demo_mode=True
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
