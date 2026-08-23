from typing import Tuple, Dict
import random

GREETING_RESPONSES = {
    "hello": "Hi there! 👋 I'm Scanline Bot, your AI shopping assistant. How can I help you today?",
    "hi": "Hello! Welcome to Scanline. I'm here to help you make smart purchasing decisions. What would you like to know?",
    "hey": "Hey! 👋 I'm your AI shopping expert. Ask me anything about products, reviews, prices, or safety!",
}

PRODUCT_QUESTIONS = {
    "review": "I can help you analyze product reviews! The analysis shows: {sentiment}% positive reviews, {fake_risk} risk of fake reviews, and a trust score of {trust_score}/100.",
    "safe": "Based on my analysis: {trust_signals}. Your trust score is {trust_score}/100. {verdict}",
    "buy": "Looking at the data: Average rating is {avg_rating}/5, {positive_count} positive reviews. {alternatives_info} Overall verdict: {verdict}",
    "price": "The current price is ${price}. I found {alt_count} alternatives ranging from ${min_price} to ${max_price}. Would you like recommendations?",
    "fake": "Fake review risk is {risk_level}. {suspicious_count} out of {total} reviews look suspicious. {details}",
    "trust": "Your trust score is {trust_score}/100 based on: {factors}",
    "recommend": "I recommend: {recommendation}. Based on the analysis, here's why: {reason}",
}

FALLBACK_RESPONSES = [
    "That's a great question! Based on the product analysis, I'd recommend checking the trust score and reviews first. What specific aspect are you concerned about?",
    "I understand your concern. Let me help you understand the data better. Are you worried about quality, authenticity, or price?",
    "Good question! The analysis shows strong indicators. Would you like me to break down the reviews, prices, or security checks?",
    "I'm here to help! Can you tell me more about what you're looking for? (Quality, Safety, Best price, etc.)",
    "Excellent point! Based on all the data, here's what stands out: The trust score, positive sentiment, and security checks all look good.",
]

def extract_analysis_data(analysis: Dict) -> Dict:
    """Extract useful data from analysis for chatbot responses"""
    if not analysis:
        return {}
    
    data = {
        "trust_score": analysis.get("recommendation", {}).get("score", 0),
        "sentiment": analysis.get("sentiment", {}),
        "fake_reviews": analysis.get("fake_reviews", {}),
        "prices": analysis.get("prices", []),
        "alternatives": analysis.get("alternatives", []),
        "trust_signals": analysis.get("trust_signals", []),
        "recommendation": analysis.get("recommendation", {}),
    }
    return data

def get_trust_verdict(score: int) -> str:
    """Get verdict based on trust score"""
    if score >= 75:
        return "✅ This looks very trustworthy! I'd recommend it."
    elif score >= 50:
        return "⚠️ Proceed with caution. There are some concerns."
    else:
        return "❌ I'd be careful. This doesn't look trustworthy."

def format_sentiment(sentiment: Dict) -> str:
    """Format sentiment data for response"""
    positive = sentiment.get("positive", 0)
    total = sentiment.get("positive", 0) + sentiment.get("negative", 0) + sentiment.get("neutral", 0)
    if total == 0:
        return "No reviews available"
    percent = int((positive / total) * 100)
    return f"{percent}% positive ({positive}/{total} reviews)"

def format_fake_review_info(fake_reviews: Dict) -> str:
    """Format fake review data"""
    risk = fake_reviews.get("risk_level", "unknown").upper()
    suspicious = fake_reviews.get("suspicious_count", 0)
    total = fake_reviews.get("total_reviews", 0)
    
    if risk == "HIGH":
        return f"🚨 HIGH RISK: {suspicious}/{total} reviews look suspicious"
    elif risk == "MEDIUM":
        return f"⚠️ MEDIUM RISK: {suspicious}/{total} reviews look suspicious"
    else:
        return f"✅ LOW RISK: Only {suspicious}/{total} reviews look suspicious"

def format_price_info(prices: List[Dict]) -> str:
    """Format price comparison"""
    if not prices:
        return "Price data unavailable"
    
    price_list = "\n".join([f"  • {p.get('seller', 'Unknown')}: ${p.get('price', 0):.2f}" for p in prices[:3]])
    return f"Current prices:\n{price_list}"

def chat_with_bot(user_message: str, analysis: Dict = None) -> Tuple[str, str]:
    """
    Main chatbot function that responds to user queries
    Returns: (reply, suggestion)
    """
    user_msg = user_message.lower().strip()
    
    # Extract analysis data
    analysis_data = extract_analysis_data(analysis) if analysis else {}
    trust_score = analysis_data.get("trust_score", 0)
    sentiment = analysis_data.get("sentiment", {})
    fake_reviews = analysis_data.get("fake_reviews", {})
    prices = analysis_data.get("prices", [])
    alternatives = analysis_data.get("alternatives", [])
    recommendation = analysis_data.get("recommendation", {})
    
    # Greeting handling
    for greeting, response in GREETING_RESPONSES.items():
        if greeting in user_msg:
            suggestion = "Ask me about reviews, prices, safety, or if you should buy this product!"
            return response, suggestion
    
    # Product quality/review questions
    if any(word in user_msg for word in ["review", "quality", "rating", "how is", "what about"]):
        sentiment_text = format_sentiment(sentiment)
        verdict = get_trust_verdict(trust_score)
        reply = f"📊 Review Analysis:\n{sentiment_text}\n\n{verdict}"
        suggestion = "Would you like to know about fake reviews or prices?"
        return reply, suggestion
    
    # Safety/authenticity questions
    if any(word in user_msg for word in ["safe", "authentic", "trust", "legit", "fake", "scam"]):
        fake_info = format_fake_review_info(fake_reviews)
        verdict = get_trust_verdict(trust_score)
        security_checks = sum(1 for s in analysis_data.get("trust_signals", []) if s.get("passed"))
        reply = f"🛡️ Safety Check:\n{fake_info}\nSecurity: {security_checks}/4 checks passed\n\n{verdict}"
        suggestion = "Want to compare prices or see alternative products?"
        return reply, suggestion
    
    # Price questions
    if any(word in user_msg for word in ["price", "cost", "cheap", "expensive", "how much"]):
        price_info = format_price_info(prices)
        if alternatives:
            alt_info = f"\n💡 Cheaper alternatives available: {alternatives[0].get('name')} at ${alternatives[0].get('price', 0):.2f}"
        else:
            alt_info = ""
        reply = f"💰 Pricing:\n{price_info}{alt_info}"
        suggestion = "Should I help you decide if it's worth buying?"
        return reply, suggestion
    
    # Buy/purchase decision questions
    if any(word in user_msg for word in ["should i buy", "worth", "recommend", "should i get", "good deal"]):
        verdict = recommendation.get("verdict", "Unknown")
        score = recommendation.get("score", 0)
        explanation = "\n".join(recommendation.get("explanation", []))
        reply = f"🎯 My Recommendation: {verdict}\n\nTrust Score: {score}/100\n\n{explanation}"
        suggestion = "Need more details about anything specific?"
        return reply, suggestion
    
    # Fake review questions
    if any(word in user_msg for word in ["fake", "suspicious", "bogus"]):
        fake_info = format_fake_review_info(fake_reviews)
        details = fake_reviews.get("details", [])
        if details:
            detail_text = "\n".join([f"  • {d.get('author')}: {d.get('text', '')[:50]}..." for d in details[:2]])
            reply = f"🚨 Fake Review Detection:\n{fake_info}\n\nExamples:\n{detail_text}"
        else:
            reply = f"🚨 Fake Review Detection:\n{fake_info}\n\nNo highly suspicious reviews found!"
        suggestion = "Want to see the real customer reviews?"
        return reply, suggestion
    
    # Alternatives/comparison questions
    if any(word in user_msg for word in ["alternative", "better", "compare", "similar", "other"]):
        if alternatives:
            alt_list = "\n".join([f"  • {a.get('name')}: ${a.get('price', 0):.2f} ({a.get('tier')} tier)" for a in alternatives])
            reply = f"🔄 Alternative Products:\n{alt_list}"
            suggestion = "Would you like to analyze any of these alternatives?"
        else:
            reply = "No alternative products found in our database. Would you like me to analyze something else?"
            suggestion = "Let me help with another question!"
        return reply, suggestion
    
    # Help/general questions
    if any(word in user_msg for word in ["help", "what can you", "how do i", "tell me"]):
        reply = "I can help you with:\n" \
                "✅ Review Analysis - See what people really say\n" \
                "✅ Fake Review Detection - Spot suspicious reviews\n" \
                "✅ Price Comparison - Find the best deals\n" \
                "✅ Safety Check - Verify if a product is trustworthy\n" \
                "✅ Buy Decision - Should you purchase this?"
        suggestion = "Ask me any of these questions!"
        return reply, suggestion
    
    # Fallback for unknown questions
    reply = random.choice(FALLBACK_RESPONSES)
    suggestion = "Try asking about reviews, prices, safety, or whether to buy!"
    return reply, suggestion
