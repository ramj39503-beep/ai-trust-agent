from typing import List, Dict

POSITIVE_WORDS = {'amazing', 'excellent', 'great', 'good', 'awesome', 'love', 'best', 'perfect', 'wonderful', 'fantastic', 'beautiful', 'recommend', 'happy', 'satisfied', 'quality', 'fast', 'reliable', 'worth'}
NEGATIVE_WORDS = {'bad', 'terrible', 'awful', 'poor', 'hate', 'worst', 'broken', 'useless', 'waste', 'disappointed', 'cheap', 'slow', 'unreliable', 'scam', 'fraud', 'defective', 'overpriced'}

def analyze_sentiment(reviews: List[Dict]) -> Dict:
    if not reviews:
        return {"positive": 0, "neutral": 0, "negative": 0, "average_rating": 0}
    
    positive_count = negative_count = neutral_count = total_rating = 0
    
    for review in reviews:
        text = review.get('text', '').lower()
        rating = review.get('rating', 0)
        total_rating += rating
        
        pos_score = sum(1 for word in POSITIVE_WORDS if word in text)
        neg_score = sum(1 for word in NEGATIVE_WORDS if word in text)
        
        if pos_score > neg_score:
            positive_count += 1
        elif neg_score > pos_score:
            negative_count += 1
        else:
            neutral_count += 1
    
    total = len(reviews)
    return {"positive": positive_count, "neutral": neutral_count, "negative": negative_count, "average_rating": round(total_rating / total, 2), "summary": f"{positive_count}/{total} positive reviews"}
