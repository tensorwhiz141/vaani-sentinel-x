"""
Analytics Agent API Router
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
import time
import asyncio
from datetime import datetime

from ..models.request_models import ContentAnalysisRequest, PerformancePredictionRequest, PlatformType, LanguageCode
from ..models.response_models import AnalyticsResponse, ContentMetrics

router = APIRouter()
logger = logging.getLogger(__name__)

# Platform engagement baselines
PLATFORM_BASELINES = {
    'instagram': {'engagement': 0.75, 'viral_potential': 0.65},
    'twitter': {'engagement': 0.68, 'viral_potential': 0.72},
    'linkedin': {'engagement': 0.62, 'viral_potential': 0.45},
    'sanatan': {'engagement': 0.80, 'viral_potential': 0.55}
}

async def analyze_content_metrics(content: str, platform: str, language: str) -> Dict[str, float]:
    """Analyze content and generate performance metrics."""
    await asyncio.sleep(0.15)  # Simulate analysis
    
    # Basic content analysis
    word_count = len(content.split())
    char_count = len(content)
    
    # Platform baseline
    baseline = PLATFORM_BASELINES.get(platform, {'engagement': 0.65, 'viral_potential': 0.50})
    
    # Engagement score calculation
    engagement_score = baseline['engagement']
    if 50 <= word_count <= 150:  # Optimal length
        engagement_score += 0.1
    if any(word in content.lower() for word in ['amazing', 'incredible', 'beautiful', 'inspiring']):
        engagement_score += 0.05
    
    # Sentiment analysis (simplified)
    positive_words = ['good', 'great', 'amazing', 'beautiful', 'wonderful', 'blessed', 'peaceful']
    negative_words = ['bad', 'terrible', 'awful', 'sad', 'angry', 'frustrated']
    
    positive_count = sum(1 for word in positive_words if word in content.lower())
    negative_count = sum(1 for word in negative_words if word in content.lower())
    
    sentiment_score = (positive_count - negative_count) / max(1, positive_count + negative_count)
    sentiment_score = max(-1.0, min(1.0, sentiment_score))
    
    # Readability (simplified)
    avg_word_length = sum(len(word) for word in content.split()) / max(1, word_count)
    readability_score = max(0.0, min(1.0, 1.0 - (avg_word_length - 5) / 10))
    
    # Platform optimization
    platform_optimization = baseline['engagement']
    if platform == 'twitter' and char_count <= 280:
        platform_optimization += 0.1
    elif platform == 'instagram' and 100 <= char_count <= 500:
        platform_optimization += 0.1
    elif platform == 'linkedin' and 200 <= char_count <= 1000:
        platform_optimization += 0.1
    
    # Viral potential
    viral_potential = baseline['viral_potential']
    if sentiment_score > 0.5:
        viral_potential += 0.1
    if any(word in content.lower() for word in ['share', 'tag', 'comment', 'follow']):
        viral_potential += 0.05
    
    return {
        'engagement_score': min(1.0, engagement_score),
        'sentiment_score': sentiment_score,
        'readability_score': readability_score,
        'platform_optimization': min(1.0, platform_optimization),
        'viral_potential': min(1.0, viral_potential)
    }

@router.post("/analyze-content", response_model=AnalyticsResponse)
async def analyze_content(request: ContentAnalysisRequest):
    """Analyze content performance and provide insights."""
    start_time = time.time()
    
    try:
        # Perform content analysis
        metrics_data = await analyze_content_metrics(
            request.content_text, 
            request.platform.value, 
            request.language.value
        )
        
        # Create metrics object
        metrics = ContentMetrics(
            engagement_score=metrics_data['engagement_score'],
            sentiment_score=metrics_data['sentiment_score'],
            readability_score=metrics_data['readability_score'],
            platform_optimization=metrics_data['platform_optimization'],
            viral_potential=metrics_data['viral_potential']
        )
        
        # Generate recommendations
        recommendations = []
        if metrics.engagement_score < 0.7:
            recommendations.append("Consider adding more engaging language and call-to-action phrases")
        if metrics.sentiment_score < 0.2:
            recommendations.append("Try incorporating more positive and uplifting language")
        if metrics.readability_score < 0.6:
            recommendations.append("Simplify language and use shorter sentences for better readability")
        if metrics.platform_optimization < 0.7:
            recommendations.append(f"Optimize content length and format for {request.platform.value}")
        if metrics.viral_potential < 0.5:
            recommendations.append("Add shareable elements like questions, quotes, or trending topics")
        
        if not recommendations:
            recommendations.append("Content is well-optimized! Consider A/B testing different variations.")
        
        processing_time = time.time() - start_time
        
        return AnalyticsResponse(
            success=True,
            processing_time=round(processing_time, 3),
            content_id=request.content_id,
            analysis_type=request.analysis_depth,
            metrics=metrics,
            recommendations=recommendations
        )
        
    except Exception as e:
        logger.error(f"Content analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@router.get("/analyze-content/benchmarks")
async def get_platform_benchmarks():
    """Get performance benchmarks for different platforms."""
    return {
        "platform_benchmarks": PLATFORM_BASELINES,
        "metric_descriptions": {
            "engagement_score": "Predicted user engagement rate (0-1)",
            "sentiment_score": "Content sentiment analysis (-1 to 1)",
            "readability_score": "Content readability assessment (0-1)",
            "platform_optimization": "Platform-specific optimization score (0-1)",
            "viral_potential": "Likelihood of content going viral (0-1)"
        }
    }
