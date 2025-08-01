"""
Translation Agent API Router
Converts the static translation agent into dynamic API endpoints
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Dict, Any
import logging
import time
from datetime import datetime
import asyncio

# Import models
from ..models.request_models import (
    TranslationRequest, 
    BatchTranslationRequest,
    LanguageCode,
    ToneType
)
from ..models.response_models import (
    TranslationResponse,
    TranslationResult,
    BatchTranslationResponse,
    ErrorResponse
)

# Import original agent functions (adapted)
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))

router = APIRouter()
logger = logging.getLogger(__name__)

# Language names mapping (from original agent)
LANGUAGE_NAMES = {
    'en': 'English', 'hi': 'Hindi', 'mr': 'Marathi', 'ta': 'Tamil', 'te': 'Telugu',
    'kn': 'Kannada', 'ml': 'Malayalam', 'bn': 'Bengali', 'gu': 'Gujarati', 'pa': 'Punjabi',
    'od': 'Odia', 'es': 'Spanish', 'fr': 'French', 'de': 'German', 'ja': 'Japanese',
    'zh': 'Chinese', 'ru': 'Russian', 'ar': 'Arabic', 'pt': 'Portuguese', 'it': 'Italian',
    'ko': 'Korean', 'sa': 'Sanskrit'
}

# Confidence scores for different languages (from original agent)
CONFIDENCE_SCORES = {
    'en': 0.98, 'hi': 0.95, 'mr': 0.92, 'ta': 0.90, 'te': 0.89,
    'kn': 0.88, 'ml': 0.87, 'bn': 0.93, 'gu': 0.91, 'pa': 0.90,
    'od': 0.85, 'es': 0.96, 'fr': 0.95, 'de': 0.94, 'ja': 0.88,
    'zh': 0.86, 'ru': 0.89, 'ar': 0.84, 'pt': 0.95, 'it': 0.94, 
    'ko': 0.87, 'sa': 0.92
}

async def simulate_llm_translation(
    text: str, 
    source_lang: str,
    target_language: str, 
    tone: str = 'formal'
) -> Dict[str, Any]:
    """
    Simulate LLM-powered translation with confidence scoring.
    Adapted from original agent for real-time API use.
    """
    logger.info(f"Translating '{text[:50]}...' from {source_lang} to {target_language} with tone: {tone}")
    
    # Simulate processing time
    await asyncio.sleep(0.1)  # Simulate API call delay
    
    # Get language names
    target_lang_name = LANGUAGE_NAMES.get(target_language, target_language.upper())
    
    # Simulate tone-aware translation
    tone_prefixes = {
        'formal': f"[{target_lang_name} - Formal]:",
        'casual': f"[{target_lang_name} - Casual]:",
        'devotional': f"[{target_lang_name} - Devotional]:",
        'neutral': f"[{target_lang_name}]:"
    }
    
    # For demonstration, we'll simulate translation by adding language prefix
    # In production, this would call actual translation APIs
    if source_lang == target_language:
        translated_text = text
        confidence = 1.0
        method = 'original'
    else:
        translated_text = f"{tone_prefixes.get(tone, tone_prefixes['neutral'])} {text}"
        confidence = CONFIDENCE_SCORES.get(target_language, 0.80)
        method = 'simulated_llm'
    
    # Adjust confidence based on tone complexity
    if tone == 'devotional' and target_language in ['hi', 'mr', 'ta', 'te', 'kn', 'ml', 'bn', 'gu', 'pa', 'od', 'sa']:
        confidence += 0.02  # Higher confidence for devotional content in Indian languages
    elif tone == 'casual':
        confidence -= 0.03  # Slightly lower confidence for casual tone
    
    # Ensure confidence is within bounds
    confidence = max(0.0, min(1.0, confidence))
    
    return {
        'translated_text': translated_text,
        'confidence_score': round(confidence, 3),
        'translation_method': method,
        'tone_applied': tone,
        'word_count': len(translated_text.split()),
        'timestamp': datetime.now().isoformat()
    }

@router.post("/translate", response_model=TranslationResponse)
async def translate_text(request: TranslationRequest):
    """
    Translate text from source language to multiple target languages.
    
    This endpoint accepts user input and returns real-time translations
    with confidence scores and tone adjustments.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing translation request: {request.source_language} -> {request.target_languages}")
        
        # Validate that source language is not in target languages
        if request.source_language in request.target_languages:
            raise HTTPException(
                status_code=400,
                detail="Source language cannot be included in target languages"
            )
        
        # Process translations for each target language
        translation_results = []
        
        for target_lang in request.target_languages:
            try:
                # Perform translation
                translation_data = await simulate_llm_translation(
                    text=request.original_text,
                    source_lang=request.source_language.value,
                    target_language=target_lang.value,
                    tone=request.tone.value
                )
                
                # Create translation result
                translation_result = TranslationResult(
                    target_language=target_lang,
                    language_name=LANGUAGE_NAMES.get(target_lang.value, target_lang.value.upper()),
                    translated_text=translation_data['translated_text'],
                    confidence_score=translation_data['confidence_score'],
                    tone_applied=ToneType(translation_data['tone_applied']),
                    word_count=translation_data['word_count']
                )
                
                translation_results.append(translation_result)
                
            except Exception as e:
                logger.error(f"Failed to translate to {target_lang}: {str(e)}")
                # Continue with other languages, but log the error
                continue
        
        if not translation_results:
            raise HTTPException(
                status_code=500,
                detail="Failed to generate any translations"
            )
        
        processing_time = time.time() - start_time
        
        # Create response
        response = TranslationResponse(
            success=True,
            processing_time=round(processing_time, 3),
            original_text=request.original_text,
            source_language=request.source_language,
            translations=translation_results,
            total_translations=len(translation_results)
        )
        
        logger.info(f"Translation completed successfully in {processing_time:.3f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Translation request failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Translation processing failed: {str(e)}"
        )

@router.post("/translate/batch", response_model=BatchTranslationResponse)
async def translate_batch(request: BatchTranslationRequest):
    """
    Translate multiple texts in batch mode.
    
    Efficiently processes multiple texts with the same source and target languages.
    """
    start_time = time.time()
    
    try:
        logger.info(f"Processing batch translation: {len(request.texts)} texts, {request.source_language} -> {request.target_languages}")
        
        # Process each text
        batch_results = []
        
        for i, text in enumerate(request.texts):
            try:
                # Create individual translation request
                individual_request = TranslationRequest(
                    original_text=text,
                    source_language=request.source_language,
                    target_languages=request.target_languages,
                    tone=request.tone
                )
                
                # Process translation
                translation_response = await translate_text(individual_request)
                batch_results.append(translation_response)
                
            except Exception as e:
                logger.error(f"Failed to process text {i+1}: {str(e)}")
                continue
        
        if not batch_results:
            raise HTTPException(
                status_code=500,
                detail="Failed to process any texts in batch"
            )
        
        # Calculate average confidence
        all_confidences = []
        for result in batch_results:
            for translation in result.translations:
                all_confidences.append(translation.confidence_score)
        
        average_confidence = sum(all_confidences) / len(all_confidences) if all_confidences else 0.0
        processing_time = time.time() - start_time
        
        # Create batch response
        response = BatchTranslationResponse(
            success=True,
            processing_time=round(processing_time, 3),
            results=batch_results,
            total_processed=len(batch_results),
            average_confidence=round(average_confidence, 3)
        )
        
        logger.info(f"Batch translation completed: {len(batch_results)} texts processed in {processing_time:.3f}s")
        return response
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch translation failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Batch translation processing failed: {str(e)}"
        )

@router.get("/translate/languages")
async def get_supported_languages():
    """
    Get list of supported languages for translation.
    """
    return {
        "supported_languages": [
            {
                "code": code,
                "name": name,
                "confidence_score": CONFIDENCE_SCORES.get(code, 0.80)
            }
            for code, name in LANGUAGE_NAMES.items()
        ],
        "total_languages": len(LANGUAGE_NAMES),
        "supported_tones": ["formal", "casual", "devotional", "neutral"]
    }

@router.get("/translate/confidence/{language_code}")
async def get_language_confidence(language_code: str):
    """
    Get confidence score for a specific language.
    """
    if language_code not in LANGUAGE_NAMES:
        raise HTTPException(
            status_code=404,
            detail=f"Language '{language_code}' not supported"
        )
    
    return {
        "language_code": language_code,
        "language_name": LANGUAGE_NAMES[language_code],
        "confidence_score": CONFIDENCE_SCORES.get(language_code, 0.80),
        "supported": True
    }
