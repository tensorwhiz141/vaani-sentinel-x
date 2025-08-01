"""
Content Generation Agent API Router
Converts the static content generation agent into dynamic API endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any, Optional
import logging
import time
import re
import uuid
from datetime import datetime
import asyncio

# Import models
from models.request_models import (
    ContentGenerationRequest,
    BulkContentGenerationRequest,
    LanguageCode,
    ToneType,
    PlatformType,
    ContentType
)
from models.response_models import (
    ContentGenerationResponse,
    GeneratedContent,
    ErrorResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)

# Platform-specific content templates and constraints
PLATFORM_CONSTRAINTS = {
    'instagram': {
        'max_chars': 2200,
        'hashtag_limit': 30,
        'style': 'visual_focused',
        'tone_preference': 'casual'
    },
    'twitter': {
        'max_chars': 280,
        'hashtag_limit': 2,
        'style': 'concise',
        'tone_preference': 'casual'
    },
    'linkedin': {
        'max_chars': 3000,
        'hashtag_limit': 5,
        'style': 'professional',
        'tone_preference': 'formal'
    },
    'sanatan': {
        'max_chars': 1500,
        'hashtag_limit': 10,
        'style': 'devotional',
        'tone_preference': 'devotional'
    }
}

# Content type templates
CONTENT_TEMPLATES = {
    'fact': {
        'structure': 'Did you know? {content} This shows us that {insight}.',
        'hashtags': ['#DidYouKnow', '#Facts', '#Learning', '#Knowledge']
    },
    'quote': {
        'structure': '"{content}" - {attribution}',
        'hashtags': ['#Wisdom', '#Inspiration', '#Quotes', '#Motivation']
    },
    'micro-article': {
        'structure': '{title}\n\n{content}\n\n{conclusion}',
        'hashtags': ['#Article', '#Insights', '#Learning', '#Knowledge']
    },
    'devotional': {
        'structure': '{content}\n\n🙏 {blessing}',
        'hashtags': ['#Devotion', '#Spirituality', '#Blessing', '#Peace']
    }
}

def clean_text_for_platform(text: str, platform: str) -> str:
    """Clean and format text for specific platform requirements."""
    # Remove emojis if needed for certain platforms
    if platform == 'linkedin':
        emoji_pattern = re.compile(
            "["
            "\U0001F600-\U0001F64F"
            "\U0001F300-\U0001F5FF"
            "\U0001F680-\U0001F6FF"
            "\U0001F700-\U0001F77F"
            "\U0001F780-\U0001F7FF"
            "\U0001F800-\U0001F8FF"
            "\U0001F900-\U0001F9FF"
            "\U0001FA00-\U0001FA6F"
            "\U0001FA70-\U0001FAFF"
            "\U00002700-\U0001F1FF"
            "]+",
            flags=re.UNICODE
        )
        text = emoji_pattern.sub('', text).strip()
    
    # Platform-specific formatting
    if platform == 'twitter':
        # Ensure conciseness for Twitter
        sentences = text.split('. ')
        if len(sentences) > 2:
            text = '. '.join(sentences[:2]) + '.'
    
    return text.strip()

def generate_hashtags(content: str, content_type: str, platform: str, language: str) -> List[str]:
    """Generate relevant hashtags based on content, type, platform, and language."""
    base_hashtags = CONTENT_TEMPLATES.get(content_type, {}).get('hashtags', [])
    
    # Language-specific hashtags
    if language == 'hi':
        base_hashtags.extend(['#हिंदी', '#भारत', '#ज्ञान'])
    elif language == 'sa':
        base_hashtags.extend(['#संस्कृत', '#वेद', '#धर्म'])
    elif language == 'en':
        base_hashtags.extend(['#English', '#Global', '#Universal'])
    
    # Platform-specific hashtags
    if platform == 'instagram':
        base_hashtags.extend(['#InstaDaily', '#Explore', '#Trending'])
    elif platform == 'linkedin':
        base_hashtags.extend(['#Professional', '#Career', '#Business'])
    elif platform == 'twitter':
        base_hashtags.extend(['#Twitter', '#Social'])
    elif platform == 'sanatan':
        base_hashtags.extend(['#Sanatan', '#Dharma', '#Spirituality'])
    
    # Limit hashtags based on platform constraints
    max_hashtags = PLATFORM_CONSTRAINTS.get(platform, {}).get('hashtag_limit', 10)
    return base_hashtags[:max_hashtags]

async def simulate_ai_content_generation(
    raw_content: str,
    content_type: str,
    platform: str,
    language: str,
    tone: str,
    target_audience: Optional[str] = None,
    max_length: Optional[int] = None
) -> Dict[str, Any]:
    """
    Simulate AI-powered content generation.
    In production, this would call actual AI APIs like GPT, Claude, etc.
    """
    logger.info(f"Generating {content_type} content for {platform} in {language} with {tone} tone")
    
    # Simulate processing time
    await asyncio.sleep(0.2)
    
    # Get platform constraints
    platform_info = PLATFORM_CONSTRAINTS.get(platform, {})
    max_chars = max_length or platform_info.get('max_chars', 1000)
    
    # Generate content based on type and platform
    if content_type == 'fact':
        if language == 'en':
            generated_text = f"Did you know? {raw_content} This fascinating insight shows us the incredible complexity of our world."
        elif language == 'hi':
            generated_text = f"क्या आप जानते हैं? {raw_content} यह दिलचस्प जानकारी हमें दुनिया की अविश्वसनीय जटिलता दिखाती है।"
        elif language == 'sa':
            generated_text = f"किं जानासि? {raw_content} एतत् आश्चर्यजनकं ज्ञानं अस्माकं जगतः अद्भुतं जटिलतां दर्शयति॥"
    
    elif content_type == 'quote':
        if language == 'en':
            generated_text = f'"{raw_content}" - Ancient Wisdom'
        elif language == 'hi':
            generated_text = f'"{raw_content}" - प्राचीन ज्ञान'
        elif language == 'sa':
            generated_text = f'"{raw_content}" - प्राचीनं ज्ञानम्॥'
    
    elif content_type == 'micro-article':
        if language == 'en':
            generated_text = f"Understanding Life's Lessons\n\n{raw_content}\n\nThis wisdom reminds us to stay mindful and present in our daily journey."
        elif language == 'hi':
            generated_text = f"जीवन के पाठ को समझना\n\n{raw_content}\n\nयह ज्ञान हमें अपनी दैनिक यात्रा में सचेत और उपस्थित रहने की याद दिलाता है।"
        elif language == 'sa':
            generated_text = f"जीवनस्य शिक्षाणां बोधः\n\n{raw_content}\n\nएतत् ज्ञानं अस्मान् स्वस्य दैनिकयात्रायां सचेतनं उपस्थितं च स्थातुं स्मारयति॥"
    
    elif content_type == 'devotional':
        if language == 'en':
            generated_text = f"{raw_content}\n\n🙏 May this wisdom bring peace and clarity to your path."
        elif language == 'hi':
            generated_text = f"{raw_content}\n\n🙏 यह ज्ञान आपके मार्ग में शांति और स्पष्टता लाए।"
        elif language == 'sa':
            generated_text = f"{raw_content}\n\n🙏 एतत् ज्ञानं भवतः पथे शान्तिं स्पष्टतां च आनयतु॥"
    
    else:
        # Default content generation
        generated_text = f"[{language.upper()}] {raw_content}"
    
    # Clean and format for platform
    generated_text = clean_text_for_platform(generated_text, platform)
    
    # Ensure content doesn't exceed platform limits
    if len(generated_text) > max_chars:
        generated_text = generated_text[:max_chars-3] + "..."
    
    # Generate hashtags
    hashtags = generate_hashtags(generated_text, content_type, platform, language)
    
    # Calculate quality metrics
    word_count = len(generated_text.split())
    char_count = len(generated_text)
    
    # Simulate quality scoring
    quality_score = 0.85
    if tone == platform_info.get('tone_preference', 'neutral'):
        quality_score += 0.1
    if char_count <= max_chars * 0.8:  # Good length utilization
        quality_score += 0.05
    
    # Simulate engagement prediction
    engagement_prediction = 0.75
    if content_type == 'quote' and platform == 'instagram':
        engagement_prediction += 0.1
    elif content_type == 'fact' and platform == 'twitter':
        engagement_prediction += 0.05
    
    return {
        'generated_text': generated_text,
        'hashtags': hashtags,
        'word_count': word_count,
        'character_count': char_count,
        'quality_score': min(1.0, quality_score),
        'engagement_prediction': min(1.0, engagement_prediction),
        'platform_optimized': True,
        'tone_applied': tone,
        'timestamp': datetime.now().isoformat()
    }

@router.post("/generate-content", response_model=ContentGenerationResponse)
async def generate_content(request: ContentGenerationRequest):
    """
    Generate platform-optimized content from raw input.
    
    This endpoint accepts user content and generates optimized versions
    for multiple platforms and languages with AI-powered enhancements.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing content generation request: {request.content_type} for {len(request.platforms)} platforms")
        
        generated_content_list = []
        content_id = str(uuid.uuid4())
        
        # Generate content for each platform and language combination
        for platform in request.platforms:
            for language in request.languages:
                try:
                    # Generate content
                    generation_data = await simulate_ai_content_generation(
                        raw_content=request.raw_content,
                        content_type=request.content_type.value,
                        platform=platform.value,
                        language=language.value,
                        tone=request.tone.value,
                        target_audience=request.target_audience,
                        max_length=request.max_length
                    )
                    
                    # Create generated content object
                    generated_content = GeneratedContent(
                        platform=platform,
                        language=language,
                        content_type=request.content_type,
                        generated_text=generation_data['generated_text'],
                        hashtags=generation_data['hashtags'] if request.include_hashtags else None,
                        character_count=generation_data['character_count'],
                        word_count=generation_data['word_count'],
                        quality_score=generation_data['quality_score'],
                        engagement_prediction=generation_data.get('engagement_prediction')
                    )
                    
                    generated_content_list.append(generated_content)
                    
                except Exception as e:
                    logger.error(f"Failed to generate content for {platform}-{language}: {str(e)}")
                    continue
        
        if not generated_content_list:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate any content variations"
            )
        
        processing_time = time.time() - start_time
        
        # Create response
        response = ContentGenerationResponse(
            success=True,
            processing_time=round(processing_time, 3),
            original_content=request.raw_content,
            generated_content=generated_content_list,
            total_variations=len(generated_content_list),
            content_id=content_id
        )
        
        logger.info(f"Content generation completed: {len(generated_content_list)} variations in {processing_time:.3f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Content generation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Content generation processing failed: {str(e)}"
        )

@router.get("/generate-content/templates")
async def get_content_templates():
    """Get available content templates and platform constraints."""
    return {
        "content_types": list(CONTENT_TEMPLATES.keys()),
        "platforms": list(PLATFORM_CONSTRAINTS.keys()),
        "templates": CONTENT_TEMPLATES,
        "platform_constraints": PLATFORM_CONSTRAINTS,
        "supported_tones": ["formal", "casual", "devotional", "neutral"]
    }

@router.get("/generate-content/platform/{platform}")
async def get_platform_info(platform: str):
    """Get detailed information about a specific platform."""
    if platform not in PLATFORM_CONSTRAINTS:
        raise HTTPException(
            status_code=404,
            detail=f"Platform '{platform}' not supported"
        )
    
    return {
        "platform": platform,
        "constraints": PLATFORM_CONSTRAINTS[platform],
        "recommended_content_types": ["fact", "quote", "micro-article", "devotional"],
        "optimization_tips": [
            f"Keep content under {PLATFORM_CONSTRAINTS[platform]['max_chars']} characters",
            f"Use maximum {PLATFORM_CONSTRAINTS[platform]['hashtag_limit']} hashtags",
            f"Prefer {PLATFORM_CONSTRAINTS[platform]['tone_preference']} tone"
        ]
    }
