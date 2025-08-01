"""
Sentiment Analysis and Tuning Agent API Router
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
import time
import asyncio
import re

from ..models.request_models import SentimentRequest, LanguageCode
from ..models.response_models import SentimentResponse, SentimentAnalysis

router = APIRouter()
logger = logging.getLogger(__name__)

# Emotion keywords for different languages
EMOTION_KEYWORDS = {
    'en': {
        'joy': ['happy', 'joyful', 'delighted', 'cheerful', 'blissful', 'elated'],
        'peace': ['peaceful', 'calm', 'serene', 'tranquil', 'quiet', 'still'],
        'love': ['love', 'affection', 'compassion', 'kindness', 'caring', 'warmth'],
        'gratitude': ['grateful', 'thankful', 'blessed', 'appreciative', 'thankfulness'],
        'wisdom': ['wise', 'wisdom', 'enlightened', 'insightful', 'understanding'],
        'fear': ['afraid', 'scared', 'anxious', 'worried', 'fearful', 'nervous'],
        'anger': ['angry', 'furious', 'mad', 'irritated', 'annoyed', 'frustrated'],
        'sadness': ['sad', 'depressed', 'melancholy', 'sorrowful', 'grief', 'mourning']
    },
    'hi': {
        'joy': ['खुश', 'प्रसन्न', 'आनंदित', 'हर्षित', 'खुशी', 'आनंद'],
        'peace': ['शांत', 'शांति', 'स्थिर', 'निर्मल', 'प्रशांत'],
        'love': ['प्रेम', 'प्यार', 'स्नेह', 'करुणा', 'दया', 'ममता'],
        'gratitude': ['कृतज्ञ', 'धन्यवाद', 'आभार', 'कृतज्ञता'],
        'wisdom': ['ज्ञान', 'बुद्धि', 'विवेक', 'समझ', 'प्रज्ञा'],
        'fear': ['डर', 'भय', 'चिंता', 'घबराहट', 'आशंका'],
        'anger': ['गुस्सा', 'क्रोध', 'रोष', 'कोप', 'चिढ़'],
        'sadness': ['दुख', 'शोक', 'उदासी', 'विषाद', 'मलाल']
    },
    'sa': {
        'joy': ['आनन्द', 'हर्ष', 'प्रमोद', 'उल्लास', 'प्रसन्नता'],
        'peace': ['शान्ति', 'प्रशान्ति', 'निर्वाण', 'स्थिरता'],
        'love': ['प्रेम', 'स्नेह', 'करुणा', 'दया', 'अनुराग'],
        'gratitude': ['कृतज्ञता', 'धन्यवाद', 'आभार'],
        'wisdom': ['ज्ञान', 'प्रज्ञा', 'विद्या', 'बुद्धि', 'विवेक'],
        'fear': ['भय', 'त्रास', 'आशङ्का', 'चिन्ता'],
        'anger': ['क्रोध', 'कोप', 'रोष', 'अमर्ष'],
        'sadness': ['दुःख', 'शोक', 'विषाद', 'खेद']
    }
}

# Sentiment adjustment patterns
SENTIMENT_ADJUSTMENTS = {
    'positive': {
        'replacements': {
            'good': 'wonderful',
            'nice': 'beautiful',
            'okay': 'great',
            'fine': 'excellent'
        },
        'prefixes': ['Beautifully', 'Wonderfully', 'Amazingly'],
        'suffixes': ['✨', '🌟', '💫']
    },
    'negative': {
        'replacements': {
            'bad': 'challenging',
            'terrible': 'difficult',
            'awful': 'tough',
            'horrible': 'demanding'
        },
        'prefixes': ['Despite challenges', 'Through difficulties'],
        'suffixes': ['💪', '🙏']
    },
    'neutral': {
        'replacements': {},
        'prefixes': [],
        'suffixes': []
    }
}

async def analyze_sentiment(content: str, language: str) -> Dict[str, Any]:
    """Analyze sentiment and emotions in content."""
    await asyncio.sleep(0.1)
    
    # Get emotion keywords for language
    emotions = EMOTION_KEYWORDS.get(language, EMOTION_KEYWORDS['en'])
    
    # Count emotion occurrences
    emotion_scores = {}
    total_emotional_words = 0
    
    for emotion, keywords in emotions.items():
        count = sum(1 for keyword in keywords if keyword.lower() in content.lower())
        if count > 0:
            emotion_scores[emotion] = count / len(keywords)  # Normalize by keyword count
            total_emotional_words += count
    
    # Calculate overall sentiment score
    positive_emotions = ['joy', 'peace', 'love', 'gratitude', 'wisdom']
    negative_emotions = ['fear', 'anger', 'sadness']
    
    positive_score = sum(emotion_scores.get(emotion, 0) for emotion in positive_emotions)
    negative_score = sum(emotion_scores.get(emotion, 0) for emotion in negative_emotions)
    
    if positive_score + negative_score > 0:
        sentiment_score = (positive_score - negative_score) / (positive_score + negative_score)
    else:
        sentiment_score = 0.0
    
    # Determine overall sentiment
    if sentiment_score > 0.3:
        overall_sentiment = 'positive'
    elif sentiment_score < -0.3:
        overall_sentiment = 'negative'
    else:
        overall_sentiment = 'neutral'
    
    # Determine dominant emotional tone
    if emotion_scores:
        emotional_tone = max(emotion_scores.keys(), key=lambda k: emotion_scores[k])
    else:
        emotional_tone = 'neutral'
    
    # Calculate confidence based on emotional word density
    word_count = len(content.split())
    confidence = min(1.0, total_emotional_words / max(1, word_count) * 5)
    
    # Convert emotion scores to list format
    key_emotions = [
        {'emotion': emotion, 'score': score}
        for emotion, score in emotion_scores.items()
        if score > 0
    ]
    
    return {
        'overall_sentiment': overall_sentiment,
        'sentiment_score': round(sentiment_score, 3),
        'emotional_tone': emotional_tone,
        'confidence': round(confidence, 3),
        'key_emotions': key_emotions
    }

async def adjust_sentiment(
    content: str, 
    current_sentiment: str, 
    target_sentiment: str, 
    language: str,
    adjustment_level: float
) -> str:
    """Adjust content sentiment towards target sentiment."""
    await asyncio.sleep(0.05)
    
    if current_sentiment == target_sentiment or adjustment_level == 0:
        return content
    
    adjusted_content = content
    adjustments = SENTIMENT_ADJUSTMENTS.get(target_sentiment, SENTIMENT_ADJUSTMENTS['neutral'])
    
    # Apply word replacements
    for old_word, new_word in adjustments['replacements'].items():
        if adjustment_level > 0.5:  # Only apply if adjustment level is significant
            adjusted_content = re.sub(
                rf'\b{old_word}\b', 
                new_word, 
                adjusted_content, 
                flags=re.IGNORECASE
            )
    
    # Add prefixes for strong adjustments
    if adjustment_level > 0.7 and adjustments['prefixes']:
        import random
        prefix = random.choice(adjustments['prefixes'])
        adjusted_content = f"{prefix}, {adjusted_content}"
    
    # Add suffixes for positive sentiment
    if target_sentiment == 'positive' and adjustment_level > 0.6 and adjustments['suffixes']:
        import random
        suffix = random.choice(adjustments['suffixes'])
        adjusted_content = f"{adjusted_content} {suffix}"
    
    return adjusted_content

@router.post("/tune-sentiment", response_model=SentimentResponse)
async def tune_sentiment(request: SentimentRequest):
    """Analyze and optionally adjust content sentiment."""
    start_time = time.time()
    
    try:
        # Analyze current sentiment
        sentiment_data = await analyze_sentiment(request.content, request.language.value)
        
        # Create sentiment analysis object
        sentiment_analysis = SentimentAnalysis(
            overall_sentiment=sentiment_data['overall_sentiment'],
            sentiment_score=sentiment_data['sentiment_score'],
            emotional_tone=sentiment_data['emotional_tone'],
            confidence=sentiment_data['confidence'],
            key_emotions=sentiment_data['key_emotions']
        )
        
        # Adjust sentiment if target is specified
        adjusted_content = None
        adjustment_applied = False
        
        if request.target_sentiment and request.target_sentiment != sentiment_data['overall_sentiment']:
            adjusted_content = await adjust_sentiment(
                request.content,
                sentiment_data['overall_sentiment'],
                request.target_sentiment,
                request.language.value,
                request.adjustment_level
            )
            adjustment_applied = adjusted_content != request.content
        
        processing_time = time.time() - start_time
        
        return SentimentResponse(
            success=True,
            processing_time=round(processing_time, 3),
            original_content=request.content,
            sentiment_analysis=sentiment_analysis,
            adjusted_content=adjusted_content,
            adjustment_applied=adjustment_applied
        )
        
    except Exception as e:
        logger.error(f"Sentiment analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Sentiment processing failed: {str(e)}")

@router.get("/tune-sentiment/emotions")
async def get_emotion_keywords():
    """Get emotion keywords for different languages."""
    return {
        "supported_languages": list(EMOTION_KEYWORDS.keys()),
        "emotion_categories": list(EMOTION_KEYWORDS['en'].keys()),
        "emotion_keywords": EMOTION_KEYWORDS,
        "sentiment_types": ["positive", "negative", "neutral"]
    }

@router.get("/tune-sentiment/preview")
async def preview_sentiment_adjustment(
    content: str,
    target_sentiment: str,
    language: str = 'en',
    adjustment_level: float = 0.5
):
    """Preview how content sentiment would be adjusted."""
    if not content:
        raise HTTPException(status_code=400, detail="Content is required")
    
    # Analyze current sentiment
    current_analysis = await analyze_sentiment(content, language)
    
    # Generate adjusted version
    adjusted = await adjust_sentiment(
        content,
        current_analysis['overall_sentiment'],
        target_sentiment,
        language,
        adjustment_level
    )
    
    return {
        "original_content": content,
        "current_sentiment": current_analysis['overall_sentiment'],
        "current_score": current_analysis['sentiment_score'],
        "target_sentiment": target_sentiment,
        "adjusted_content": adjusted,
        "adjustment_applied": adjusted != content
    }
