from typing import List, Dict

FAKE_INDICATORS = {
    'hype_language': ['MUST BUY', 'EXCELLENT', 'AMAZING', '!!!', '10/10', 'BEST EVER'],
    'generic_usernames': ['reviewer_', 'user_', 'customer_', 'amazon', 'verified_'],
}

def detect_fake_reviews(reviews: List[Dict]) -> Dict:
    if not reviews:
        return {"suspicious_count": 0, "total_reviews": 0, "risk_level": "low"}
    
    suspicious_reviews = []
    for i, review in enumerate(reviews):
        text = review.get('text', '')
        author = review.get('author', '')
        rating = review.get('rating', 0)
        
        flags = 0
        details = []
        
        if any(phrase in text for phrase in FAKE_INDICATORS['hype_language']):
            flags += 1
            details.append("Excessive hype language")
        
        if any(pattern in author.lower() for pattern in FAKE_INDICATORS['generic_usernames']):
            flags += 1
            details.append("Generic/bot-like username")
        
        if rating >= 5 and len(text) < 50:
            flags += 1
            details.append("Very high rating with minimal text")
        
        if flags >= 2:
            suspicious_reviews.append({"index": i, "author": author, "text": text[:100], "flags": flags, "details": details})
    
    total = len(reviews)
    suspicious = len(suspicious_reviews)
    risk = "low" if suspicious == 0 else ("medium" if suspicious <= total * 0.2 else "high")
    
    return {"suspicious_count": suspicious, "total_reviews": total, "risk_level": risk, "details": suspicious_reviews[:3]}
