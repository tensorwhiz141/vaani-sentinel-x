"""
Comprehensive test suite for Vaani Sentinel-X Dynamic Agent API
Tests all agent endpoints with various user input scenarios
"""

import pytest
import asyncio
from fastapi.testclient import TestClient
from agents_api.main import app

# Create test client
client = TestClient(app)

class TestSystemEndpoints:
    """Test core system endpoints."""
    
    def test_root_endpoint(self):
        """Test root endpoint returns system information."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "agents_available" in data
        assert data["version"] == "2.0.0"
    
    def test_health_check(self):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
    
    def test_agents_list(self):
        """Test agents list endpoint."""
        response = client.get("/api/agents/list")
        assert response.status_code == 200
        data = response.json()
        assert "agents" in data
        assert data["total_agents"] == 10

class TestTranslationAgent:
    """Test translation agent endpoints."""
    
    def test_translate_single_language(self):
        """Test translation to single target language."""
        payload = {
            "original_text": "Hello, how are you?",
            "source_language": "en",
            "target_languages": ["hi"],
            "tone": "formal",
            "include_confidence": True
        }
        
        response = client.post("/api/agents/translate", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert len(data["translations"]) == 1
        assert data["translations"][0]["target_language"] == "hi"
        assert "confidence_score" in data["translations"][0]
    
    def test_translate_multiple_languages(self):
        """Test translation to multiple target languages."""
        payload = {
            "original_text": "Good morning!",
            "source_language": "en",
            "target_languages": ["hi", "sa", "es"],
            "tone": "casual"
        }
        
        response = client.post("/api/agents/translate", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert len(data["translations"]) == 3
        assert data["total_translations"] == 3
    
    def test_translate_invalid_input(self):
        """Test translation with invalid input."""
        payload = {
            "original_text": "",  # Empty text
            "source_language": "en",
            "target_languages": ["hi"]
        }
        
        response = client.post("/api/agents/translate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_translate_same_source_target(self):
        """Test translation with source language in target languages."""
        payload = {
            "original_text": "Hello",
            "source_language": "en",
            "target_languages": ["en", "hi"]  # Source in targets
        }
        
        response = client.post("/api/agents/translate", json=payload)
        assert response.status_code == 422  # Validation error
    
    def test_get_supported_languages(self):
        """Test getting supported languages."""
        response = client.get("/api/agents/translate/languages")
        assert response.status_code == 200
        
        data = response.json()
        assert "supported_languages" in data
        assert len(data["supported_languages"]) > 0
        assert "supported_tones" in data

class TestContentGenerationAgent:
    """Test content generation agent endpoints."""
    
    def test_generate_content_single_platform(self):
        """Test content generation for single platform."""
        payload = {
            "raw_content": "AI is revolutionizing healthcare",
            "content_type": "fact",
            "platforms": ["instagram"],
            "languages": ["en"],
            "tone": "neutral",
            "include_hashtags": True
        }
        
        response = client.post("/api/agents/generate-content", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert len(data["generated_content"]) == 1
        assert data["generated_content"][0]["platform"] == "instagram"
        assert "hashtags" in data["generated_content"][0]
    
    def test_generate_content_multiple_platforms(self):
        """Test content generation for multiple platforms."""
        payload = {
            "raw_content": "Meditation brings inner peace",
            "content_type": "devotional",
            "platforms": ["instagram", "twitter", "linkedin"],
            "languages": ["en", "hi"],
            "tone": "devotional"
        }
        
        response = client.post("/api/agents/generate-content", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert len(data["generated_content"]) == 6  # 3 platforms × 2 languages
        assert data["total_variations"] == 6
    
    def test_get_content_templates(self):
        """Test getting content templates."""
        response = client.get("/api/agents/generate-content/templates")
        assert response.status_code == 200
        
        data = response.json()
        assert "content_types" in data
        assert "platforms" in data
        assert "templates" in data

class TestPersonalizationAgent:
    """Test personalization agent endpoints."""
    
    def test_personalize_content(self):
        """Test content personalization."""
        payload = {
            "content": "This is a great article about technology",
            "user_id": "test_user_123",
            "user_preferences": {
                "tone": "casual",
                "language": "en",
                "platform": "instagram",
                "interests": ["technology", "innovation"]
            },
            "personalization_level": 0.8
        }
        
        response = client.post("/api/agents/personalize", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "personalization_result" in data
        assert data["user_id"] == "test_user_123"
    
    def test_get_personalization_factors(self):
        """Test getting personalization factors."""
        response = client.get("/api/agents/personalize/factors")
        assert response.status_code == 200
        
        data = response.json()
        assert "personalization_factors" in data
        assert "supported_interests" in data

class TestTTSAgent:
    """Test TTS agent endpoints."""
    
    def test_tts_simulation(self):
        """Test TTS simulation."""
        payload = {
            "text": "Hello, welcome to Vaani Sentinel-X",
            "language": "en",
            "voice_preference": "female",
            "tone": "neutral",
            "speed": 1.0,
            "include_quality_metrics": True
        }
        
        response = client.post("/api/agents/tts-simulate", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "tts_result" in data
        assert data["tts_result"]["language"] == "en"
        assert "estimated_duration" in data["tts_result"]
    
    def test_get_available_voices(self):
        """Test getting available voices."""
        response = client.get("/api/agents/tts-simulate/voices")
        assert response.status_code == 200
        
        data = response.json()
        assert "voices" in data
        assert "supported_languages" in data

class TestAnalyticsAgent:
    """Test analytics agent endpoints."""
    
    def test_analyze_content(self):
        """Test content analysis."""
        payload = {
            "content_text": "This is an amazing post about AI technology!",
            "platform": "instagram",
            "language": "en",
            "analysis_depth": "standard"
        }
        
        response = client.post("/api/agents/analyze-content", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert "metrics" in data
        assert "recommendations" in data
        assert len(data["recommendations"]) > 0
    
    def test_get_platform_benchmarks(self):
        """Test getting platform benchmarks."""
        response = client.get("/api/agents/analyze-content/benchmarks")
        assert response.status_code == 200
        
        data = response.json()
        assert "platform_benchmarks" in data
        assert "metric_descriptions" in data

class TestSecurityAgent:
    """Test security agent endpoints."""
    
    def test_validate_safe_content(self):
        """Test validation of safe content."""
        payload = {
            "content": "This is a wonderful day to learn something new!",
            "platform": "instagram",
            "language": "en",
            "strict_mode": False
        }
        
        response = client.post("/api/agents/validate-content", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["content_safe"] is True
        assert "compliance_status" in data
    
    def test_validate_unsafe_content(self):
        """Test validation of potentially unsafe content."""
        payload = {
            "content": "Contact me at test@email.com for spam offers",
            "platform": "twitter",
            "language": "en",
            "strict_mode": True
        }
        
        response = client.post("/api/agents/validate-content", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        # Should detect personal information
        assert len(data["issues_found"]) > 0

class TestSentimentAgent:
    """Test sentiment agent endpoints."""
    
    def test_analyze_positive_sentiment(self):
        """Test analysis of positive sentiment."""
        payload = {
            "content": "I am so happy and grateful for this wonderful day!",
            "language": "en",
            "adjustment_level": 0.5
        }
        
        response = client.post("/api/agents/tune-sentiment", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        assert data["sentiment_analysis"]["overall_sentiment"] == "positive"
        assert data["sentiment_analysis"]["sentiment_score"] > 0
    
    def test_sentiment_adjustment(self):
        """Test sentiment adjustment."""
        payload = {
            "content": "This is okay, I guess",
            "target_sentiment": "positive",
            "language": "en",
            "adjustment_level": 0.8
        }
        
        response = client.post("/api/agents/tune-sentiment", json=payload)
        assert response.status_code == 200
        
        data = response.json()
        assert data["success"] is True
        if data["adjustment_applied"]:
            assert data["adjusted_content"] != data["original_content"]

class TestErrorHandling:
    """Test error handling across all agents."""
    
    def test_invalid_json(self):
        """Test handling of invalid JSON."""
        response = client.post(
            "/api/agents/translate",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self):
        """Test handling of missing required fields."""
        payload = {
            "source_language": "en"
            # Missing original_text and target_languages
        }
        
        response = client.post("/api/agents/translate", json=payload)
        assert response.status_code == 422
    
    def test_invalid_enum_values(self):
        """Test handling of invalid enum values."""
        payload = {
            "original_text": "Hello",
            "source_language": "invalid_language",
            "target_languages": ["hi"]
        }
        
        response = client.post("/api/agents/translate", json=payload)
        assert response.status_code == 422

# Performance tests
class TestPerformance:
    """Test performance characteristics."""
    
    def test_translation_response_time(self):
        """Test translation response time is reasonable."""
        import time
        
        payload = {
            "original_text": "Hello world",
            "source_language": "en",
            "target_languages": ["hi"],
            "tone": "neutral"
        }
        
        start_time = time.time()
        response = client.post("/api/agents/translate", json=payload)
        end_time = time.time()
        
        assert response.status_code == 200
        assert (end_time - start_time) < 2.0  # Should complete within 2 seconds
    
    def test_concurrent_requests(self):
        """Test handling of concurrent requests."""
        import threading
        import time
        
        results = []
        
        def make_request():
            payload = {
                "original_text": "Test concurrent request",
                "source_language": "en",
                "target_languages": ["hi"]
            }
            response = client.post("/api/agents/translate", json=payload)
            results.append(response.status_code)
        
        # Create 5 concurrent requests
        threads = []
        for _ in range(5):
            thread = threading.Thread(target=make_request)
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
        
        # All requests should succeed
        assert all(status == 200 for status in results)
        assert len(results) == 5

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"])
