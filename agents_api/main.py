#!/usr/bin/env python3
"""
Vaani Sentinel-X Dynamic Agent API Server
FastAPI server that converts all static agents into user-driven API endpoints

Author: Vaani Sentinel-X Team
Date: 2025-08-01
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
import logging
import sys
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

# Add the parent directory to the path to import agents
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Import Pydantic models for request/response validation
from models.request_models import *
from models.response_models import *

# Import agent routers
from routers import (
    translation_router,
    content_generation_router,
    personalization_router,
    tts_router,
    analytics_router,
    multilingual_router,
    scheduler_router,
    strategy_router,
    security_router,
    sentiment_router
)

# Import WebSocket handler
from websocket_handler import websocket_endpoint

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('agents_api.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Create FastAPI application
app = FastAPI(
    title="Vaani Sentinel-X Dynamic Agent API",
    description="Real-time multilingual AI content generation system with user-driven agent interactions",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include agent routers
app.include_router(translation_router.router, prefix="/api/agents", tags=["Translation"])
app.include_router(content_generation_router.router, prefix="/api/agents", tags=["Content Generation"])
app.include_router(personalization_router.router, prefix="/api/agents", tags=["Personalization"])
app.include_router(tts_router.router, prefix="/api/agents", tags=["Text-to-Speech"])
app.include_router(analytics_router.router, prefix="/api/agents", tags=["Analytics"])
app.include_router(multilingual_router.router, prefix="/api/agents", tags=["Multilingual Processing"])
app.include_router(scheduler_router.router, prefix="/api/agents", tags=["Scheduling"])
app.include_router(strategy_router.router, prefix="/api/agents", tags=["Strategy"])
app.include_router(security_router.router, prefix="/api/agents", tags=["Security"])
app.include_router(sentiment_router.router, prefix="/api/agents", tags=["Sentiment"])

@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "Vaani Sentinel-X Dynamic Agent API",
        "version": "2.0.0",
        "description": "Real-time multilingual AI content generation system",
        "docs": "/docs",
        "agents_available": [
            "translation",
            "content-generation", 
            "personalization",
            "tts-simulation",
            "analytics",
            "multilingual-processing",
            "scheduling",
            "strategy",
            "security",
            "sentiment"
        ],
        "timestamp": datetime.now().isoformat()
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "service": "Vaani Sentinel-X Agent API",
        "version": "2.0.0"
    }

@app.get("/api/agents/list")
async def list_agents():
    """List all available agents and their capabilities"""
    return {
        "agents": {
            "translation": {
                "endpoint": "/api/agents/translate",
                "description": "Real-time multilingual translation with confidence scores",
                "supported_languages": ["en", "hi", "sa", "es", "fr", "de", "ja", "zh", "ar", "pt", "it", "ru", "ko"],
                "input_formats": ["text", "json"],
                "features": ["tone_adjustment", "confidence_scoring", "batch_translation"]
            },
            "content_generation": {
                "endpoint": "/api/agents/generate-content",
                "description": "AI-powered content generation for multiple platforms",
                "supported_platforms": ["instagram", "twitter", "linkedin", "sanatan"],
                "content_types": ["fact", "quote", "micro-article", "devotional"],
                "features": ["platform_optimization", "multi_language", "tone_adjustment"]
            },
            "personalization": {
                "endpoint": "/api/agents/personalize",
                "description": "User-specific content personalization and optimization",
                "personalization_factors": ["tone", "language", "platform", "user_preferences"],
                "features": ["real_time_adaptation", "preference_learning", "context_awareness"]
            },
            "tts_simulation": {
                "endpoint": "/api/agents/tts-simulate",
                "description": "Text-to-speech simulation with voice quality metrics",
                "supported_voices": ["male", "female", "neutral"],
                "languages": ["en", "hi", "sa"],
                "features": ["voice_quality_scoring", "duration_estimation", "tone_matching"]
            },
            "analytics": {
                "endpoint": "/api/agents/analyze-content",
                "description": "Content performance analysis and engagement prediction",
                "metrics": ["engagement_score", "sentiment_analysis", "platform_optimization"],
                "features": ["real_time_analysis", "performance_prediction", "trend_identification"]
            },
            "multilingual_processing": {
                "endpoint": "/api/agents/process-multilingual",
                "description": "Advanced multilingual content processing and routing",
                "features": ["language_detection", "content_routing", "quality_assessment"]
            },
            "scheduling": {
                "endpoint": "/api/agents/schedule-content",
                "description": "Intelligent content scheduling and timing optimization",
                "features": ["optimal_timing", "platform_specific_scheduling", "audience_analysis"]
            },
            "strategy": {
                "endpoint": "/api/agents/recommend-strategy",
                "description": "AI-driven content strategy recommendations",
                "features": ["performance_analysis", "trend_prediction", "optimization_suggestions"]
            },
            "security": {
                "endpoint": "/api/agents/validate-content",
                "description": "Content security validation and filtering",
                "features": ["content_filtering", "safety_scoring", "compliance_checking"]
            },
            "sentiment": {
                "endpoint": "/api/agents/tune-sentiment",
                "description": "Sentiment analysis and tone adjustment",
                "features": ["sentiment_detection", "tone_modification", "emotional_scoring"]
            }
        },
        "total_agents": 10,
        "api_version": "2.0.0",
        "timestamp": datetime.now().isoformat()
    }

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Custom HTTP exception handler"""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.now().isoformat()
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """General exception handler"""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "An unexpected error occurred",
            "timestamp": datetime.now().isoformat()
        }
    )

@app.websocket("/ws")
async def websocket_endpoint_route(websocket: WebSocket):
    """WebSocket endpoint for real-time agent processing."""
    await websocket_endpoint(websocket)

@app.websocket("/ws/{user_id}")
async def websocket_endpoint_with_user(websocket: WebSocket, user_id: str):
    """WebSocket endpoint with user identification."""
    await websocket_endpoint(websocket, user_id)

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
