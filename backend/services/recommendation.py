from typing import Dict

def build_recommendation(sentiment: Dict, fake_reviews: Dict, prices: list, trust_signals: list) -> Dict:
    trust_score = 50
    passed_checks = sum(1 for s in trust_signals if s.get('passed', False))
    trust_score += (passed_checks / len(trust_signals)) * 30 if trust_signals else 0
    
    total_reviews = sentiment.get('positive', 0) + sentiment.get('negative', 0)
    if total_reviews > 0:
        sentiment_ratio = sentiment.get('positive', 0) / total_reviews
        trust_score += sentiment_ratio * 20
    
    if fake_reviews.get('risk_level') == 'high':
        trust_score -= 15
    elif fake_reviews.get('risk_level') == 'medium':
        trust_score -= 8
    
    trust_score = max(0, min(100, trust_score))
    
    if trust_score >= 75:
        verdict, color, emoji = "Recommended", "green", "✓"
    elif trust_score >= 50:
        verdict, color, emoji = "Proceed with Caution", "yellow", "⚠"
    else:
        verdict, color, emoji = "Not Recommended", "red", "✗"
    
    explanation = [
        f"Trust Score: {int(trust_score)}/100",
        f"Security: {passed_checks}/{len(trust_signals) if trust_signals else 0} checks passed",
        f"Sentiment: {sentiment.get('summary', 'No reviews')}",
        f"Fake Review Risk: {fake_reviews.get('risk_level', 'unknown')}",
    ]
    
    return {"verdict": verdict, "score": int(trust_score), "color": color, "emoji": emoji, "explanation": explanation}
