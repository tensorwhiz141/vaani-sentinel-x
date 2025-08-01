# 🧪 **Complete API Testing Commands - All FastAPI Endpoints**

## 🔗 **Base URL:** `http://localhost:8000`

---

## 📋 **System Endpoints**

### **1. Health Check**
```bash
curl -X GET "http://localhost:8000/health"
```

### **2. System Information**
```bash
curl -X GET "http://localhost:8000/"
```

### **3. List All Agents**
```bash
curl -X GET "http://localhost:8000/api/agents/list"
```

---

## 🌍 **Translation Agent API**

### **Basic Translation**
```bash
curl -X POST "http://localhost:8000/api/agents/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "original_text": "Hello, how are you today?",
    "source_language": "en",
    "target_languages": ["hi", "sa", "es"],
    "tone": "formal",
    "preserve_formatting": true,
    "include_confidence": true
  }'
```

### **Casual Tone Translation**
```bash
curl -X POST "http://localhost:8000/api/agents/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "original_text": "Hey! What'\''s up? This is awesome!",
    "source_language": "en",
    "target_languages": ["hi", "fr", "de"],
    "tone": "casual",
    "preserve_formatting": true,
    "include_confidence": true
  }'
```

### **Devotional Translation**
```bash
curl -X POST "http://localhost:8000/api/agents/translate" \
  -H "Content-Type: application/json" \
  -d '{
    "original_text": "May peace and blessings be with you always",
    "source_language": "en",
    "target_languages": ["hi", "sa"],
    "tone": "devotional",
    "preserve_formatting": true,
    "include_confidence": true
  }'
```

### **Batch Translation**
```bash
curl -X POST "http://localhost:8000/api/agents/translate/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "texts": [
      "Good morning!",
      "How are you?",
      "Have a great day!"
    ],
    "source_language": "en",
    "target_languages": ["hi", "sa"],
    "tone": "formal"
  }'
```

### **Get Supported Languages**
```bash
curl -X GET "http://localhost:8000/api/agents/translate/languages"
```

---

## 📝 **Content Generation Agent API**

### **Instagram Content Generation**
```bash
curl -X POST "http://localhost:8000/api/agents/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_content": "Artificial Intelligence is transforming healthcare by enabling early disease detection and personalized treatment plans",
    "content_type": "fact",
    "platforms": ["instagram"],
    "languages": ["en", "hi"],
    "tone": "casual",
    "target_audience": "tech enthusiasts",
    "include_hashtags": true,
    "max_length": 500
  }'
```

### **Multi-Platform Content**
```bash
curl -X POST "http://localhost:8000/api/agents/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_content": "Meditation brings inner peace and clarity to the mind",
    "content_type": "devotional",
    "platforms": ["instagram", "twitter", "linkedin", "sanatan"],
    "languages": ["en", "hi", "sa"],
    "tone": "devotional",
    "include_hashtags": true
  }'
```

### **Quote Content Generation**
```bash
curl -X POST "http://localhost:8000/api/agents/generate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "raw_content": "The journey of a thousand miles begins with a single step",
    "content_type": "quote",
    "platforms": ["twitter", "linkedin"],
    "languages": ["en"],
    "tone": "formal",
    "include_hashtags": true
  }'
```

### **Get Content Templates**
```bash
curl -X GET "http://localhost:8000/api/agents/generate-content/templates"
```

---

## 👤 **Personalization Agent API**

### **Basic Personalization**
```bash
curl -X POST "http://localhost:8000/api/agents/personalize" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is an amazing article about the latest technology trends and innovations",
    "user_id": "user_123",
    "user_preferences": {
      "tone": "casual",
      "language": "en",
      "platform": "instagram",
      "interests": ["technology", "innovation", "AI"],
      "engagement_history": {
        "tech_posts": 0.85,
        "casual_tone": 0.92
      }
    },
    "personalization_level": 0.8
  }'
```

### **Devotional Personalization**
```bash
curl -X POST "http://localhost:8000/api/agents/personalize" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Find peace in meditation and spiritual practice",
    "user_id": "spiritual_user_456",
    "user_preferences": {
      "tone": "devotional",
      "language": "hi",
      "platform": "sanatan",
      "interests": ["spirituality", "meditation", "yoga"]
    },
    "personalization_level": 0.9
  }'
```

### **Get Personalization Factors**
```bash
curl -X GET "http://localhost:8000/api/agents/personalize/factors"
```

---

## 🎤 **Text-to-Speech Agent API**

### **Basic TTS Simulation**
```bash
curl -X POST "http://localhost:8000/api/agents/tts-simulate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "Welcome to Vaani Sentinel-X, your multilingual AI content generation system",
    "language": "en",
    "voice_preference": "female",
    "tone": "neutral",
    "speed": 1.0,
    "include_quality_metrics": true
  }'
```

### **Hindi TTS**
```bash
curl -X POST "http://localhost:8000/api/agents/tts-simulate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते! आपका स्वागत है",
    "language": "hi",
    "voice_preference": "male",
    "tone": "formal",
    "speed": 0.8,
    "include_quality_metrics": true
  }'
```

### **Sanskrit Devotional TTS**
```bash
curl -X POST "http://localhost:8000/api/agents/tts-simulate" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "ॐ शान्ति शान्ति शान्तिः",
    "language": "sa",
    "voice_preference": "neutral",
    "tone": "devotional",
    "speed": 0.7,
    "include_quality_metrics": true
  }'
```

### **Get Available Voices**
```bash
curl -X GET "http://localhost:8000/api/agents/tts-simulate/voices"
```

---

## 📊 **Analytics Agent API**

### **Content Analysis**
```bash
curl -X POST "http://localhost:8000/api/agents/analyze-content" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "post_001",
    "content_text": "🚀 Exciting news! Our new AI technology is revolutionizing the way we create content. Join us on this amazing journey! #AI #Innovation #Technology",
    "platform": "instagram",
    "language": "en",
    "metadata": {
      "posting_time": "2024-01-15T10:00:00Z",
      "target_audience": "tech_enthusiasts"
    },
    "analysis_depth": "detailed"
  }'
```

### **LinkedIn Content Analysis**
```bash
curl -X POST "http://localhost:8000/api/agents/analyze-content" \
  -H "Content-Type: application/json" \
  -d '{
    "content_text": "In today'\''s rapidly evolving business landscape, artificial intelligence is becoming a crucial competitive advantage. Companies that embrace AI-driven solutions are seeing significant improvements in efficiency and customer satisfaction.",
    "platform": "linkedin",
    "language": "en",
    "analysis_depth": "standard"
  }'
```

### **Get Platform Benchmarks**
```bash
curl -X GET "http://localhost:8000/api/agents/analyze-content/benchmarks"
```

---

## 🌐 **Multilingual Processing Agent API**

### **Language Detection & Processing**
```bash
curl -X POST "http://localhost:8000/api/agents/process-multilingual" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Bonjour! Comment allez-vous aujourd'\''hui?",
    "auto_detect_language": true,
    "processing_options": {
      "quality_check": true,
      "encoding_validation": true,
      "character_analysis": true
    }
  }'
```

### **Hindi Content Processing**
```bash
curl -X POST "http://localhost:8000/api/agents/process-multilingual" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "आज का दिन बहुत सुंदर है। मैं बहुत खुश हूं।",
    "auto_detect_language": false,
    "source_language": "hi",
    "processing_options": {
      "quality_check": true,
      "unicode_validation": true
    }
  }'
```

### **Get Supported Languages**
```bash
curl -X GET "http://localhost:8000/api/agents/process-multilingual/languages"
```

---

## 📅 **Scheduler Agent API**

### **Schedule Instagram Post**
```bash
curl -X POST "http://localhost:8000/api/agents/schedule-content" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "ig_post_001",
    "content": "🌟 Amazing sunset today! Nature never fails to inspire us. #sunset #nature #inspiration",
    "platform": "instagram",
    "language": "en",
    "preferred_time": "2024-01-20T19:00:00Z",
    "timezone": "UTC",
    "auto_optimize": true
  }'
```

### **Auto-Optimized Scheduling**
```bash
curl -X POST "http://localhost:8000/api/agents/schedule-content" \
  -H "Content-Type: application/json" \
  -d '{
    "content_id": "linkedin_post_002",
    "content": "Key insights from today'\''s industry conference on digital transformation",
    "platform": "linkedin",
    "language": "en",
    "timezone": "America/New_York",
    "auto_optimize": true
  }'
```

### **Get Optimal Times**
```bash
curl -X GET "http://localhost:8000/api/agents/schedule-content/optimal-times/instagram"
```

---

## 🎯 **Strategy Agent API**

### **Strategy Recommendations**
```bash
curl -X POST "http://localhost:8000/api/agents/recommend-strategy" \
  -H "Content-Type: application/json" \
  -d '{
    "content_history": [
      {
        "content_type": "fact",
        "platform": "instagram",
        "engagement_rate": 0.85,
        "language": "en"
      },
      {
        "content_type": "quote",
        "platform": "twitter",
        "engagement_rate": 0.72,
        "language": "hi"
      }
    ],
    "performance_data": {
      "avg_engagement": 0.78,
      "best_performing_platform": "instagram",
      "growth_rate": 0.15
    },
    "target_goals": {
      "engagement_rate": 0.90,
      "follower_growth": 0.20
    },
    "time_period": "week"
  }'
```

### **Monthly Strategy Analysis**
```bash
curl -X POST "http://localhost:8000/api/agents/recommend-strategy" \
  -H "Content-Type: application/json" \
  -d '{
    "performance_data": {
      "total_posts": 45,
      "avg_engagement": 0.65,
      "top_language": "en",
      "best_time": "19:00"
    },
    "target_goals": {
      "engagement_rate": 0.80,
      "reach_increase": 0.25
    },
    "time_period": "month"
  }'
```

### **Get Strategy Templates**
```bash
curl -X GET "http://localhost:8000/api/agents/recommend-strategy/templates"
```

---

## 🛡️ **Security Agent API**

### **Content Validation**
```bash
curl -X POST "http://localhost:8000/api/agents/validate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Check out this amazing product! Contact us at info@company.com for more details.",
    "platform": "instagram",
    "language": "en",
    "strict_mode": false,
    "custom_rules": ["no_email_addresses", "no_phone_numbers"]
  }'
```

### **Strict Mode Validation**
```bash
curl -X POST "http://localhost:8000/api/agents/validate-content" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "AMAZING DEAL!!! Contact me at john.doe@email.com or call 555-123-4567 NOW!!!",
    "platform": "twitter",
    "language": "en",
    "strict_mode": true
  }'
```

### **Get Security Rules**
```bash
curl -X GET "http://localhost:8000/api/agents/validate-content/rules"
```

---

## ❤️ **Sentiment Agent API**

### **Sentiment Analysis**
```bash
curl -X POST "http://localhost:8000/api/agents/tune-sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "I am feeling really happy and grateful today! This is such a wonderful experience.",
    "language": "en",
    "adjustment_level": 0.5
  }'
```

### **Sentiment Adjustment**
```bash
curl -X POST "http://localhost:8000/api/agents/tune-sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "This is okay, I guess. Nothing special about it.",
    "target_sentiment": "positive",
    "language": "en",
    "adjustment_level": 0.8
  }'
```

### **Hindi Sentiment Analysis**
```bash
curl -X POST "http://localhost:8000/api/agents/tune-sentiment" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "मैं बहुत खुश हूं और आभारी हूं। यह एक अद्भुत दिन है।",
    "language": "hi",
    "adjustment_level": 0.6
  }'
```

### **Get Emotion Keywords**
```bash
curl -X GET "http://localhost:8000/api/agents/tune-sentiment/emotions"
```

---

## 🧪 **Testing All Endpoints Script**

Save this as `test_all_apis.sh`:

```bash
#!/bin/bash

BASE_URL="http://localhost:8000"

echo "🧪 Testing all Vaani Sentinel-X API endpoints..."

# Test system endpoints
echo "📋 Testing system endpoints..."
curl -s "$BASE_URL/health" | jq .
curl -s "$BASE_URL/" | jq .

# Test translation
echo "🌍 Testing translation..."
curl -s -X POST "$BASE_URL/api/agents/translate" \
  -H "Content-Type: application/json" \
  -d '{"original_text":"Hello","source_language":"en","target_languages":["hi"],"tone":"formal"}' | jq .

# Test content generation
echo "📝 Testing content generation..."
curl -s -X POST "$BASE_URL/api/agents/generate-content" \
  -H "Content-Type: application/json" \
  -d '{"raw_content":"AI is amazing","content_type":"fact","platforms":["instagram"],"languages":["en"],"tone":"casual"}' | jq .

# Add more tests as needed...

echo "✅ API testing complete!"
```

---

## 🎯 **Quick Test Commands**

### **Test Everything at Once:**
```bash
# Health check
curl http://localhost:8000/health

# Basic translation
curl -X POST "http://localhost:8000/api/agents/translate" -H "Content-Type: application/json" -d '{"original_text":"Hello","source_language":"en","target_languages":["hi"],"tone":"formal"}'

# Content generation
curl -X POST "http://localhost:8000/api/agents/generate-content" -H "Content-Type: application/json" -d '{"raw_content":"AI is transforming the world","content_type":"fact","platforms":["instagram"],"languages":["en"],"tone":"casual"}'

# Sentiment analysis
curl -X POST "http://localhost:8000/api/agents/tune-sentiment" -H "Content-Type: application/json" -d '{"content":"I am very happy today!","language":"en"}'
```

**All these commands are ready to use! Just make sure your FastAPI server is running on http://localhost:8000** 🚀
