"""
Pydantic models for API response validation
Defines output schemas for all agent endpoints
"""

from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from .request_models import LanguageCode, ToneType, PlatformType, ContentType, VoiceType

# Base Response Model
class BaseResponse(BaseModel):
    success: bool = Field(..., description="Whether the operation was successful")
    timestamp: datetime = Field(default_factory=datetime.now, description="Response timestamp")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    agent_version: str = Field("2.0.0", description="Agent version")

# Translation Response Models
class TranslationResult(BaseModel):
    target_language: LanguageCode = Field(..., description="Target language code")
    language_name: str = Field(..., description="Human-readable language name")
    translated_text: str = Field(..., description="Translated content")
    confidence_score: float = Field(..., ge=0.0, le=1.0, description="Translation confidence score")
    tone_applied: ToneType = Field(..., description="Applied tone")
    word_count: int = Field(..., description="Word count of translation")

class TranslationResponse(BaseResponse):
    original_text: str = Field(..., description="Original input text")
    source_language: LanguageCode = Field(..., description="Source language")
    translations: List[TranslationResult] = Field(..., description="Translation results")
    total_translations: int = Field(..., description="Number of translations generated")

class BatchTranslationResponse(BaseResponse):
    results: List[TranslationResponse] = Field(..., description="Batch translation results")
    total_processed: int = Field(..., description="Total texts processed")
    average_confidence: float = Field(..., description="Average confidence score")

# Content Generation Response Models
class GeneratedContent(BaseModel):
    platform: PlatformType = Field(..., description="Target platform")
    language: LanguageCode = Field(..., description="Content language")
    content_type: ContentType = Field(..., description="Type of generated content")
    generated_text: str = Field(..., description="Generated content")
    hashtags: Optional[List[str]] = Field(None, description="Relevant hashtags")
    character_count: int = Field(..., description="Character count")
    word_count: int = Field(..., description="Word count")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Content quality score")
    engagement_prediction: Optional[float] = Field(None, description="Predicted engagement score")

class ContentGenerationResponse(BaseResponse):
    original_content: str = Field(..., description="Original input content")
    generated_content: List[GeneratedContent] = Field(..., description="Generated content variations")
    total_variations: int = Field(..., description="Number of content variations")
    content_id: str = Field(..., description="Unique content identifier")

# Personalization Response Models
class PersonalizationResult(BaseModel):
    personalized_text: str = Field(..., description="Personalized content")
    personalization_score: float = Field(..., ge=0.0, le=1.0, description="Personalization effectiveness score")
    applied_preferences: Dict[str, Any] = Field(..., description="Applied user preferences")
    modifications_made: List[str] = Field(..., description="List of modifications applied")

class PersonalizationResponse(BaseResponse):
    original_content: str = Field(..., description="Original content")
    user_id: Optional[str] = Field(None, description="User identifier")
    personalization_result: PersonalizationResult = Field(..., description="Personalization result")
    recommendation_score: float = Field(..., description="Content recommendation score")

# TTS Response Models
class TTSResult(BaseModel):
    text: str = Field(..., description="Input text")
    language: LanguageCode = Field(..., description="TTS language")
    voice_type: VoiceType = Field(..., description="Applied voice type")
    estimated_duration: float = Field(..., description="Estimated audio duration in seconds")
    quality_score: float = Field(..., ge=0.0, le=1.0, description="Voice quality score")
    audio_url: Optional[str] = Field(None, description="URL to generated audio file")
    phonetic_transcription: Optional[str] = Field(None, description="Phonetic transcription")

class TTSResponse(BaseResponse):
    tts_result: TTSResult = Field(..., description="TTS processing result")
    audio_format: str = Field("mp3", description="Audio file format")
    sample_rate: int = Field(22050, description="Audio sample rate")

class BatchTTSResponse(BaseResponse):
    results: List[TTSResult] = Field(..., description="Batch TTS results")
    total_duration: float = Field(..., description="Total estimated duration")
    average_quality: float = Field(..., description="Average quality score")

# Analytics Response Models
class ContentMetrics(BaseModel):
    engagement_score: float = Field(..., ge=0.0, le=1.0, description="Predicted engagement score")
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Sentiment analysis score")
    readability_score: float = Field(..., ge=0.0, le=1.0, description="Content readability score")
    platform_optimization: float = Field(..., ge=0.0, le=1.0, description="Platform optimization score")
    viral_potential: float = Field(..., ge=0.0, le=1.0, description="Viral potential score")

class AnalyticsResponse(BaseResponse):
    content_id: Optional[str] = Field(None, description="Content identifier")
    analysis_type: str = Field(..., description="Type of analysis performed")
    metrics: ContentMetrics = Field(..., description="Content performance metrics")
    recommendations: List[str] = Field(..., description="Improvement recommendations")
    competitive_analysis: Optional[Dict[str, Any]] = Field(None, description="Competitive analysis data")

# Multilingual Processing Response Models
class LanguageDetectionResult(BaseModel):
    detected_language: LanguageCode = Field(..., description="Detected language")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence")
    alternative_languages: List[Dict[str, float]] = Field(..., description="Alternative language possibilities")

class MultilingualProcessingResponse(BaseResponse):
    original_content: str = Field(..., description="Original input content")
    language_detection: LanguageDetectionResult = Field(..., description="Language detection results")
    processing_results: Dict[str, Any] = Field(..., description="Processing results")
    quality_assessment: float = Field(..., ge=0.0, le=1.0, description="Content quality assessment")

# Scheduling Response Models
class SchedulingResult(BaseModel):
    content_id: str = Field(..., description="Content identifier")
    scheduled_time: datetime = Field(..., description="Scheduled posting time")
    platform: PlatformType = Field(..., description="Target platform")
    optimization_score: float = Field(..., ge=0.0, le=1.0, description="Timing optimization score")
    audience_reach_estimate: int = Field(..., description="Estimated audience reach")
    competition_level: str = Field(..., description="Competition level at scheduled time")

class SchedulingResponse(BaseResponse):
    scheduling_result: SchedulingResult = Field(..., description="Scheduling result")
    alternative_times: List[Dict[str, Any]] = Field(..., description="Alternative optimal times")
    scheduling_rationale: str = Field(..., description="Explanation for chosen time")

# Strategy Response Models
class StrategyRecommendation(BaseModel):
    recommendation_type: str = Field(..., description="Type of recommendation")
    priority: str = Field(..., pattern="^(high|medium|low)$", description="Recommendation priority")
    description: str = Field(..., description="Detailed recommendation")
    expected_impact: float = Field(..., ge=0.0, le=1.0, description="Expected impact score")
    implementation_difficulty: str = Field(..., pattern="^(easy|medium|hard)$", description="Implementation difficulty")
    timeline: str = Field(..., description="Recommended implementation timeline")

class StrategyResponse(BaseResponse):
    analysis_period: str = Field(..., description="Analysis time period")
    recommendations: List[StrategyRecommendation] = Field(..., description="Strategy recommendations")
    performance_trends: Dict[str, Any] = Field(..., description="Performance trend analysis")
    competitive_insights: Optional[Dict[str, Any]] = Field(None, description="Competitive insights")
    next_review_date: datetime = Field(..., description="Recommended next review date")

# Security Validation Response Models
class SecurityIssue(BaseModel):
    issue_type: str = Field(..., description="Type of security issue")
    severity: str = Field(..., pattern="^(low|medium|high|critical)$", description="Issue severity")
    description: str = Field(..., description="Issue description")
    suggested_fix: str = Field(..., description="Suggested resolution")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Detection confidence")

class SecurityValidationResponse(BaseResponse):
    content_safe: bool = Field(..., description="Whether content passed security validation")
    overall_risk_score: float = Field(..., ge=0.0, le=1.0, description="Overall risk assessment score")
    issues_found: List[SecurityIssue] = Field(..., description="Security issues identified")
    compliance_status: Dict[str, bool] = Field(..., description="Compliance check results")
    sanitized_content: Optional[str] = Field(None, description="Sanitized version of content")

# Sentiment Analysis Response Models
class SentimentAnalysis(BaseModel):
    overall_sentiment: str = Field(..., pattern="^(positive|negative|neutral)$", description="Overall sentiment")
    sentiment_score: float = Field(..., ge=-1.0, le=1.0, description="Sentiment score (-1 to 1)")
    emotional_tone: str = Field(..., description="Detected emotional tone")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Analysis confidence")
    key_emotions: List[Dict[str, float]] = Field(..., description="Key emotions detected")

class SentimentResponse(BaseResponse):
    original_content: str = Field(..., description="Original content")
    sentiment_analysis: SentimentAnalysis = Field(..., description="Sentiment analysis results")
    adjusted_content: Optional[str] = Field(None, description="Sentiment-adjusted content")
    adjustment_applied: bool = Field(..., description="Whether adjustment was applied")

# Error Response Models
class ErrorResponse(BaseModel):
    success: bool = Field(False, description="Operation success status")
    error_code: str = Field(..., description="Error code")
    error_message: str = Field(..., description="Human-readable error message")
    details: Optional[Dict[str, Any]] = Field(None, description="Additional error details")
    timestamp: datetime = Field(default_factory=datetime.now, description="Error timestamp")
    request_id: Optional[str] = Field(None, description="Request identifier for tracking")
