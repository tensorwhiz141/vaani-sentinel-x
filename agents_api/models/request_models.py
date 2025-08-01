"""
Pydantic models for API request validation
Defines input schemas for all agent endpoints
"""

from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any, Union
from enum import Enum
from datetime import datetime

# Enums for validation
class LanguageCode(str, Enum):
    ENGLISH = "en"
    HINDI = "hi"
    SANSKRIT = "sa"
    SPANISH = "es"
    FRENCH = "fr"
    GERMAN = "de"
    JAPANESE = "ja"
    CHINESE = "zh"
    ARABIC = "ar"
    PORTUGUESE = "pt"
    ITALIAN = "it"
    RUSSIAN = "ru"
    KOREAN = "ko"
    MARATHI = "mr"
    TAMIL = "ta"
    TELUGU = "te"
    KANNADA = "kn"
    MALAYALAM = "ml"
    BENGALI = "bn"
    GUJARATI = "gu"
    PUNJABI = "pa"
    ODIA = "od"

class ToneType(str, Enum):
    FORMAL = "formal"
    CASUAL = "casual"
    DEVOTIONAL = "devotional"
    NEUTRAL = "neutral"

class PlatformType(str, Enum):
    INSTAGRAM = "instagram"
    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    SANATAN = "sanatan"

class ContentType(str, Enum):
    FACT = "fact"
    QUOTE = "quote"
    MICRO_ARTICLE = "micro-article"
    DEVOTIONAL = "devotional"

class VoiceType(str, Enum):
    MALE = "male"
    FEMALE = "female"
    NEUTRAL = "neutral"

# Translation Agent Request Models
class TranslationRequest(BaseModel):
    original_text: str = Field(..., min_length=1, max_length=5000, description="Text to translate")
    source_language: LanguageCode = Field(..., description="Source language code")
    target_languages: List[LanguageCode] = Field(..., min_items=1, max_items=10, description="Target language codes")
    tone: Optional[ToneType] = Field(ToneType.NEUTRAL, description="Desired tone for translation")
    preserve_formatting: Optional[bool] = Field(True, description="Whether to preserve text formatting")
    include_confidence: Optional[bool] = Field(True, description="Include confidence scores in response")

    @validator('target_languages')
    def validate_target_languages(cls, v, values):
        if 'source_language' in values and values['source_language'] in v:
            raise ValueError('Target languages cannot include source language')
        return v

class BatchTranslationRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=50, description="List of texts to translate")
    source_language: LanguageCode = Field(..., description="Source language code")
    target_languages: List[LanguageCode] = Field(..., min_items=1, max_items=5, description="Target language codes")
    tone: Optional[ToneType] = Field(ToneType.NEUTRAL, description="Desired tone for translation")

# Content Generation Request Models
class ContentGenerationRequest(BaseModel):
    raw_content: str = Field(..., min_length=10, max_length=2000, description="Raw content to process")
    content_type: ContentType = Field(..., description="Type of content to generate")
    platforms: List[PlatformType] = Field(..., min_items=1, max_items=4, description="Target platforms")
    languages: List[LanguageCode] = Field(..., min_items=1, max_items=5, description="Target languages")
    tone: Optional[ToneType] = Field(ToneType.NEUTRAL, description="Desired tone")
    target_audience: Optional[str] = Field(None, max_length=200, description="Target audience description")
    include_hashtags: Optional[bool] = Field(True, description="Include relevant hashtags")
    max_length: Optional[int] = Field(None, ge=50, le=2000, description="Maximum content length")

class BulkContentGenerationRequest(BaseModel):
    content_items: List[Dict[str, Any]] = Field(..., min_items=1, max_items=20, description="Multiple content items")
    default_platforms: List[PlatformType] = Field(..., description="Default platforms for all items")
    default_languages: List[LanguageCode] = Field(..., description="Default languages for all items")
    default_tone: Optional[ToneType] = Field(ToneType.NEUTRAL, description="Default tone")

# Personalization Request Models
class UserPreferences(BaseModel):
    tone: Optional[ToneType] = Field(None, description="Preferred tone")
    language: Optional[LanguageCode] = Field(None, description="Preferred language")
    platform: Optional[PlatformType] = Field(None, description="Preferred platform")
    interests: Optional[List[str]] = Field(None, max_items=10, description="User interests")
    engagement_history: Optional[Dict[str, float]] = Field(None, description="Historical engagement data")

class PersonalizationRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Base content to personalize")
    user_id: Optional[str] = Field(None, max_length=100, description="User identifier")
    user_preferences: UserPreferences = Field(..., description="User preferences")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")
    personalization_level: Optional[float] = Field(0.7, ge=0.0, le=1.0, description="Personalization intensity")

# TTS Simulation Request Models
class TTSRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=3000, description="Text to convert to speech")
    language: LanguageCode = Field(..., description="Language for TTS")
    voice_preference: VoiceType = Field(VoiceType.NEUTRAL, description="Voice type preference")
    tone: Optional[ToneType] = Field(ToneType.NEUTRAL, description="Desired tone")
    speed: Optional[float] = Field(1.0, ge=0.5, le=2.0, description="Speech speed multiplier")
    include_quality_metrics: Optional[bool] = Field(True, description="Include quality assessment")

class BatchTTSRequest(BaseModel):
    texts: List[str] = Field(..., min_items=1, max_items=20, description="Multiple texts for TTS")
    language: LanguageCode = Field(..., description="Language for all texts")
    voice_preference: VoiceType = Field(VoiceType.NEUTRAL, description="Voice type preference")

# Analytics Request Models
class ContentAnalysisRequest(BaseModel):
    content_id: Optional[str] = Field(None, max_length=100, description="Content identifier")
    content_text: str = Field(..., min_length=1, max_length=5000, description="Content to analyze")
    platform: PlatformType = Field(..., description="Target platform")
    language: LanguageCode = Field(..., description="Content language")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    analysis_depth: Optional[str] = Field("standard", pattern="^(basic|standard|detailed)$", description="Analysis depth")

class PerformancePredictionRequest(BaseModel):
    content: str = Field(..., description="Content for performance prediction")
    platform: PlatformType = Field(..., description="Target platform")
    language: LanguageCode = Field(..., description="Content language")
    posting_time: Optional[datetime] = Field(None, description="Planned posting time")
    historical_data: Optional[Dict[str, Any]] = Field(None, description="Historical performance data")

# Multilingual Processing Request Models
class MultilingualProcessingRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Content to process")
    auto_detect_language: Optional[bool] = Field(True, description="Auto-detect source language")
    source_language: Optional[LanguageCode] = Field(None, description="Source language if known")
    processing_options: Optional[Dict[str, bool]] = Field(None, description="Processing options")

# Scheduling Request Models
class SchedulingRequest(BaseModel):
    content_id: str = Field(..., max_length=100, description="Content identifier")
    content: str = Field(..., description="Content to schedule")
    platform: PlatformType = Field(..., description="Target platform")
    language: LanguageCode = Field(..., description="Content language")
    preferred_time: Optional[datetime] = Field(None, description="Preferred posting time")
    timezone: Optional[str] = Field("UTC", description="Timezone for scheduling")
    auto_optimize: Optional[bool] = Field(True, description="Auto-optimize posting time")

# Strategy Request Models
class StrategyRequest(BaseModel):
    content_history: Optional[List[Dict[str, Any]]] = Field(None, description="Historical content data")
    performance_data: Optional[Dict[str, Any]] = Field(None, description="Performance metrics")
    target_goals: Optional[Dict[str, float]] = Field(None, description="Target performance goals")
    # time_period: Optional[str] = Field("week", pattern="^(day|week|month)$", description="Analysis time period")

# Security Validation Request Models
class SecurityValidationRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Content to validate")
    platform: PlatformType = Field(..., description="Target platform")
    language: LanguageCode = Field(..., description="Content language")
    strict_mode: Optional[bool] = Field(False, description="Enable strict validation mode")
    custom_rules: Optional[List[str]] = Field(None, description="Custom validation rules")

# Sentiment Analysis Request Models
class SentimentRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=5000, description="Content for sentiment analysis")
    target_sentiment: Optional[str] = Field(None, description="Desired sentiment")
    language: LanguageCode = Field(..., description="Content language")
    adjustment_level: Optional[float] = Field(0.5, ge=0.0, le=1.0, description="Sentiment adjustment intensity")
