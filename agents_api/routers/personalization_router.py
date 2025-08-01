"""
Personalization Agent API Router
Converts the static personalization agent into dynamic API endpoints
"""

from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any, Optional
import logging
import time
import uuid
from datetime import datetime
import asyncio

# Import models
from ..models.request_models import (
    PersonalizationRequest,
    UserPreferences,
    LanguageCode,
    ToneType,
    PlatformType
)
from ..models.response_models import (
    PersonalizationResponse,
    PersonalizationResult,
    ErrorResponse
)

router = APIRouter()
logger = logging.getLogger(__name__)

# Personalization factors and weights
PERSONALIZATION_FACTORS = {
    'tone': 0.3,
    'language': 0.25,
    'platform': 0.2,
    'interests': 0.15,
    'engagement_history': 0.1
}

# Tone-based content modifications
TONE_MODIFICATIONS = {
    'formal': {
        'prefixes': ['Please note that', 'It is important to understand', 'Research indicates'],
        'replacements': {
            'awesome': 'excellent',
            'cool': 'impressive',
            'great': 'outstanding',
            'amazing': 'remarkable'
        }
    },
    'casual': {
        'prefixes': ['Hey there!', 'Check this out:', 'You know what?'],
        'replacements': {
            'excellent': 'awesome',
            'outstanding': 'great',
            'remarkable': 'amazing',
            'significant': 'big'
        }
    },
    'devotional': {
        'prefixes': ['Blessed souls,', 'Dear devotees,', 'In divine grace,'],
        'replacements': {
            'good': 'blessed',
            'happy': 'blissful',
            'peaceful': 'serene',
            'wise': 'enlightened'
        },
        'suffixes': ['🙏', 'Om Shanti', 'Blessed be']
    },
    'neutral': {
        'prefixes': [],
        'replacements': {},
        'suffixes': []
    }
}

# Platform-specific personalization
PLATFORM_PERSONALIZATION = {
    'instagram': {
        'emoji_factor': 1.2,
        'hashtag_emphasis': True,
        'visual_language': True
    },
    'twitter': {
        'brevity_factor': 1.5,
        'trending_awareness': True,
        'engagement_hooks': True
    },
    'linkedin': {
        'professional_tone': 1.3,
        'industry_relevance': True,
        'networking_focus': True
    },
    'sanatan': {
        'spiritual_emphasis': 1.4,
        'cultural_sensitivity': True,
        'devotional_language': True
    }
}

async def analyze_user_preferences(user_preferences: UserPreferences) -> Dict[str, Any]:
    """Analyze user preferences to create personalization profile."""
    await asyncio.sleep(0.05)  # Simulate analysis time
    
    profile = {
        'primary_tone': user_preferences.tone.value if user_preferences.tone else 'neutral',
        'preferred_language': user_preferences.language.value if user_preferences.language else 'en',
        'main_platform': user_preferences.platform.value if user_preferences.platform else 'instagram',
        'interest_categories': user_preferences.interests or [],
        'engagement_patterns': user_preferences.engagement_history or {},
        'personalization_strength': 0.7
    }
    
    # Calculate personalization strength based on available data
    data_points = 0
    if user_preferences.tone:
        data_points += 1
    if user_preferences.language:
        data_points += 1
    if user_preferences.platform:
        data_points += 1
    if user_preferences.interests:
        data_points += len(user_preferences.interests) * 0.1
    if user_preferences.engagement_history:
        data_points += len(user_preferences.engagement_history) * 0.2
    
    profile['personalization_strength'] = min(1.0, data_points * 0.2)
    
    return profile

async def apply_tone_personalization(content: str, tone: str, language: str) -> str:
    """Apply tone-based personalization to content."""
    await asyncio.sleep(0.02)
    
    if tone not in TONE_MODIFICATIONS:
        return content
    
    modifications = TONE_MODIFICATIONS[tone]
    personalized_content = content
    
    # Apply word replacements
    for old_word, new_word in modifications.get('replacements', {}).items():
        personalized_content = personalized_content.replace(old_word, new_word)
    
    # Add prefixes for certain tones
    prefixes = modifications.get('prefixes', [])
    if prefixes and len(personalized_content) > 50:
        import random
        prefix = random.choice(prefixes)
        personalized_content = f"{prefix} {personalized_content}"
    
    # Add suffixes for devotional tone
    suffixes = modifications.get('suffixes', [])
    if suffixes and tone == 'devotional':
        import random
        suffix = random.choice(suffixes)
        personalized_content = f"{personalized_content} {suffix}"
    
    return personalized_content

async def apply_platform_personalization(
    content: str, 
    platform: str, 
    user_profile: Dict[str, Any]
) -> str:
    """Apply platform-specific personalization."""
    await asyncio.sleep(0.03)
    
    if platform not in PLATFORM_PERSONALIZATION:
        return content
    
    platform_config = PLATFORM_PERSONALIZATION[platform]
    personalized_content = content
    
    # Instagram: Add visual language and emojis
    if platform == 'instagram' and platform_config.get('visual_language'):
        if 'beautiful' in content.lower():
            personalized_content = personalized_content.replace('beautiful', '✨ beautiful ✨')
        if 'amazing' in content.lower():
            personalized_content = personalized_content.replace('amazing', '🌟 amazing 🌟')
    
    # Twitter: Add engagement hooks
    elif platform == 'twitter' and platform_config.get('engagement_hooks'):
        if not personalized_content.startswith(('What', 'How', 'Why', 'Did you know')):
            personalized_content = f"💭 {personalized_content}"
    
    # LinkedIn: Professional enhancement
    elif platform == 'linkedin' and platform_config.get('professional_tone'):
        professional_starters = [
            'In my experience,', 'Industry insights show that', 'Professional perspective:'
        ]
        if len(personalized_content) > 100:
            import random
            starter = random.choice(professional_starters)
            personalized_content = f"{starter} {personalized_content}"
    
    # Sanatan: Spiritual emphasis
    elif platform == 'sanatan' and platform_config.get('spiritual_emphasis'):
        if not any(word in personalized_content.lower() for word in ['divine', 'blessed', 'sacred', 'spiritual']):
            personalized_content = f"🕉️ {personalized_content}"
    
    return personalized_content

async def apply_interest_personalization(
    content: str, 
    interests: List[str], 
    language: str
) -> str:
    """Apply interest-based personalization."""
    await asyncio.sleep(0.02)
    
    if not interests:
        return content
    
    # Interest-based content enhancements
    interest_enhancements = {
        'technology': ['innovation', 'digital transformation', 'future tech'],
        'spirituality': ['inner peace', 'mindfulness', 'divine wisdom'],
        'health': ['wellness', 'vitality', 'healthy living'],
        'education': ['learning', 'knowledge', 'growth mindset'],
        'business': ['entrepreneurship', 'leadership', 'success strategies'],
        'art': ['creativity', 'artistic expression', 'beauty'],
        'nature': ['natural harmony', 'environmental awareness', 'earth connection']
    }
    
    personalized_content = content
    
    # Add relevant context based on interests
    for interest in interests:
        if interest.lower() in interest_enhancements:
            relevant_terms = interest_enhancements[interest.lower()]
            # Add contextual relevance (simplified for demo)
            if len(personalized_content) > 50:
                personalized_content += f" This resonates with {interest} enthusiasts."
                break
    
    return personalized_content

@router.post("/personalize", response_model=PersonalizationResponse)
async def personalize_content(request: PersonalizationRequest):
    """
    Personalize content based on user preferences and behavior.
    
    This endpoint takes base content and user preferences to create
    personalized versions optimized for individual users.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing personalization request for user: {request.user_id}")
        
        # Analyze user preferences
        user_profile = await analyze_user_preferences(request.user_preferences)
        
        # Start with original content
        personalized_text = request.content
        modifications_made = []
        
        # Apply tone personalization
        if request.user_preferences.tone:
            tone_personalized = await apply_tone_personalization(
                personalized_text,
                request.user_preferences.tone.value,
                request.user_preferences.language.value if request.user_preferences.language else 'en'
            )
            if tone_personalized != personalized_text:
                modifications_made.append(f"Applied {request.user_preferences.tone.value} tone")
                personalized_text = tone_personalized
        
        # Apply platform personalization
        if request.user_preferences.platform:
            platform_personalized = await apply_platform_personalization(
                personalized_text,
                request.user_preferences.platform.value,
                user_profile
            )
            if platform_personalized != personalized_text:
                modifications_made.append(f"Optimized for {request.user_preferences.platform.value}")
                personalized_text = platform_personalized
        
        # Apply interest-based personalization
        if request.user_preferences.interests:
            interest_personalized = await apply_interest_personalization(
                personalized_text,
                request.user_preferences.interests,
                request.user_preferences.language.value if request.user_preferences.language else 'en'
            )
            if interest_personalized != personalized_text:
                modifications_made.append("Added interest-based context")
                personalized_text = interest_personalized
        
        # Calculate personalization effectiveness
        personalization_score = user_profile['personalization_strength'] * request.personalization_level
        
        # Calculate recommendation score based on user profile match
        recommendation_score = 0.7
        if request.user_preferences.tone:
            recommendation_score += 0.1
        if request.user_preferences.platform:
            recommendation_score += 0.1
        if request.user_preferences.interests:
            recommendation_score += 0.1
        
        recommendation_score = min(1.0, recommendation_score)
        
        # Create personalization result
        personalization_result = PersonalizationResult(
            personalized_text=personalized_text,
            personalization_score=round(personalization_score, 3),
            applied_preferences={
                'tone': request.user_preferences.tone.value if request.user_preferences.tone else None,
                'language': request.user_preferences.language.value if request.user_preferences.language else None,
                'platform': request.user_preferences.platform.value if request.user_preferences.platform else None,
                'interests': request.user_preferences.interests,
                'personalization_level': request.personalization_level
            },
            modifications_made=modifications_made
        )
        
        processing_time = time.time() - start_time
        
        # Create response
        response = PersonalizationResponse(
            success=True,
            processing_time=round(processing_time, 3),
            original_content=request.content,
            user_id=request.user_id,
            personalization_result=personalization_result,
            recommendation_score=round(recommendation_score, 3)
        )
        
        logger.info(f"Personalization completed in {processing_time:.3f}s with score {personalization_score:.3f}")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Personalization failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Personalization processing failed: {str(e)}"
        )

@router.get("/personalize/factors")
async def get_personalization_factors():
    """Get available personalization factors and their weights."""
    return {
        "personalization_factors": PERSONALIZATION_FACTORS,
        "tone_modifications": {k: {"available_tones": list(v.get('replacements', {}).keys())} for k, v in TONE_MODIFICATIONS.items()},
        "platform_features": PLATFORM_PERSONALIZATION,
        "supported_interests": [
            "technology", "spirituality", "health", "education", 
            "business", "art", "nature", "music", "sports", "travel"
        ]
    }

@router.get("/personalize/preview")
async def preview_personalization(
    content: str,
    tone: Optional[str] = None,
    platform: Optional[str] = None
):
    """Preview how content would be personalized with given parameters."""
    if not content:
        raise HTTPException(status_code=400, detail="Content is required")
    
    preview_result = {"original": content}
    
    if tone and tone in TONE_MODIFICATIONS:
        tone_preview = await apply_tone_personalization(content, tone, 'en')
        preview_result[f"tone_{tone}"] = tone_preview
    
    if platform and platform in PLATFORM_PERSONALIZATION:
        platform_preview = await apply_platform_personalization(content, platform, {})
        preview_result[f"platform_{platform}"] = platform_preview
    
    return preview_result
