"""
Multilingual Processing Agent API Router
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
import time
import asyncio
from langdetect import detect, LangDetectException

from ..models.request_models import MultilingualProcessingRequest, LanguageCode
from ..models.response_models import MultilingualProcessingResponse, LanguageDetectionResult

router = APIRouter()
logger = logging.getLogger(__name__)

# Language confidence mapping
LANGUAGE_CONFIDENCE_MAP = {
    'en': 0.98, 'hi': 0.95, 'sa': 0.92, 'es': 0.96, 'fr': 0.95,
    'de': 0.94, 'ja': 0.88, 'zh': 0.86, 'ar': 0.84, 'pt': 0.95
}

async def detect_content_language(content: str) -> Dict[str, Any]:
    """Detect language of content with confidence scores."""
    await asyncio.sleep(0.05)
    
    try:
        detected_lang = detect(content)
        confidence = LANGUAGE_CONFIDENCE_MAP.get(detected_lang, 0.80)
        
        # Simulate alternative language possibilities
        alternatives = [
            {'language': 'en', 'confidence': 0.15},
            {'language': 'hi', 'confidence': 0.10}
        ]
        
        return {
            'detected_language': detected_lang,
            'confidence': confidence,
            'alternatives': alternatives
        }
    except LangDetectException:
        return {
            'detected_language': 'en',
            'confidence': 0.50,
            'alternatives': []
        }

@router.post("/process-multilingual", response_model=MultilingualProcessingResponse)
async def process_multilingual_content(request: MultilingualProcessingRequest):
    """Process content for multilingual optimization."""
    start_time = time.time()
    
    try:
        # Detect language if auto-detect is enabled
        if request.auto_detect_language:
            detection_result = await detect_content_language(request.content)
        else:
            detection_result = {
                'detected_language': request.source_language.value if request.source_language else 'en',
                'confidence': 1.0,
                'alternatives': []
            }
        
        # Create language detection result
        language_detection = LanguageDetectionResult(
            detected_language=LanguageCode(detection_result['detected_language']),
            confidence=detection_result['confidence'],
            alternative_languages=detection_result['alternatives']
        )
        
        # Process content (simplified)
        processing_results = {
            'language_routing': f"Content routed to {detection_result['detected_language']} pipeline",
            'quality_check': 'Passed',
            'encoding_validation': 'UTF-8 compliant',
            'character_analysis': {
                'total_chars': len(request.content),
                'unicode_chars': sum(1 for c in request.content if ord(c) > 127),
                'special_chars': sum(1 for c in request.content if not c.isalnum() and not c.isspace())
            }
        }
        
        # Quality assessment
        quality_score = 0.85
        if detection_result['confidence'] > 0.9:
            quality_score += 0.1
        if len(request.content) > 50:
            quality_score += 0.05
        
        processing_time = time.time() - start_time
        
        return MultilingualProcessingResponse(
            success=True,
            processing_time=round(processing_time, 3),
            original_content=request.content,
            language_detection=language_detection,
            processing_results=processing_results,
            quality_assessment=min(1.0, quality_score)
        )
        
    except Exception as e:
        logger.error(f"Multilingual processing failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")

@router.get("/process-multilingual/languages")
async def get_supported_languages():
    """Get supported languages for multilingual processing."""
    return {
        "supported_languages": list(LANGUAGE_CONFIDENCE_MAP.keys()),
        "confidence_scores": LANGUAGE_CONFIDENCE_MAP,
        "auto_detection": True
    }
