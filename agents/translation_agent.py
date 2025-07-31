import os
import json
import logging
import requests
from datetime import datetime
from typing import Dict, List, Optional

# Logging setup
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'translation_agent.txt')

logger = logging.getLogger('translation_agent')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.info("Initializing translation_agent.py")

# File paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
CONTENT_BLOCKS_FILE = os.path.join(BASE_DIR, 'content', 'structured', 'content_blocks.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'translated_content.json')
LANGUAGE_MAP_FILE = os.path.join(CONFIG_DIR, 'language_voice_map.json')

# Supported languages
SUPPORTED_LANGUAGES = [
    'en', 'hi', 'mr', 'ta', 'te', 'kn', 'ml', 'bn', 'gu', 'pa', 'od',
    'es', 'fr', 'de', 'ja', 'zh', 'ru', 'ar', 'pt', 'it', 'ko'
]

# Language names for better prompts
LANGUAGE_NAMES = {
    'en': 'English', 'hi': 'Hindi', 'mr': 'Marathi', 'ta': 'Tamil', 'te': 'Telugu',
    'kn': 'Kannada', 'ml': 'Malayalam', 'bn': 'Bengali', 'gu': 'Gujarati', 'pa': 'Punjabi',
    'od': 'Odia', 'es': 'Spanish', 'fr': 'French', 'de': 'German', 'ja': 'Japanese',
    'zh': 'Chinese', 'ru': 'Russian', 'ar': 'Arabic', 'pt': 'Portuguese', 'it': 'Italian',
    'ko': 'Korean'
}

def load_config(file_path: str) -> Dict:
    """Load JSON configuration file."""
    logger.debug(f"Loading config: {file_path}")
    if not os.path.exists(file_path):
        logger.error(f"Config file not found: {file_path}")
        raise FileNotFoundError(f"Config file not found: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Failed to load {file_path}: {str(e)}")
        raise

def simulate_llm_translation(text: str, target_language: str, tone: str = 'formal') -> Dict:
    """Simulate LLM-powered translation with confidence scoring."""
    logger.info(f"Simulating translation to {target_language} with tone: {tone}")
    
    # Simulate different translation quality based on language complexity
    confidence_scores = {
        'en': 0.98, 'hi': 0.95, 'mr': 0.92, 'ta': 0.90, 'te': 0.89,
        'kn': 0.88, 'ml': 0.87, 'bn': 0.93, 'gu': 0.91, 'pa': 0.90,
        'od': 0.85, 'es': 0.96, 'fr': 0.95, 'de': 0.94, 'ja': 0.88,
        'zh': 0.86, 'ru': 0.89, 'ar': 0.84, 'pt': 0.95, 'it': 0.94, 'ko': 0.87
    }
    
    # Simulate tone-aware translation
    tone_prefixes = {
        'formal': f"[{LANGUAGE_NAMES[target_language]} - Formal]:",
        'casual': f"[{LANGUAGE_NAMES[target_language]} - Casual]:",
        'devotional': f"[{LANGUAGE_NAMES[target_language]} - Devotional]:"
    }
    
    translated_text = f"{tone_prefixes.get(tone, tone_prefixes['formal'])} {text}"
    confidence = confidence_scores.get(target_language, 0.80)
    
    # Simulate slight confidence reduction for complex tones
    if tone == 'devotional' and target_language in ['hi', 'mr', 'ta', 'te', 'kn', 'ml', 'bn', 'gu', 'pa', 'od']:
        confidence += 0.02  # Higher confidence for devotional content in Indian languages
    elif tone == 'casual':
        confidence -= 0.03  # Slightly lower confidence for casual tone
    
    return {
        'translated_text': translated_text,
        'confidence_score': round(confidence, 3),
        'translation_method': 'simulated_llm',
        'tone_applied': tone,
        'timestamp': datetime.now().isoformat()
    }

def translate_content_blocks(content_blocks: List[Dict]) -> List[Dict]:
    """Translate all content blocks to all supported languages."""
    logger.info(f"Starting translation of {len(content_blocks)} content blocks to {len(SUPPORTED_LANGUAGES)} languages")
    
    translated_content = []
    
    for block in content_blocks:
        content_id = block['id']
        original_text = block['text']
        original_language = block.get('language', 'en')
        content_type = block.get('type', 'unknown')
        
        logger.info(f"Translating content ID {content_id} from {original_language}")
        
        # Determine tone based on content type
        tone_mapping = {
            'fact': 'formal',
            'micro-article': 'casual',
            'quote': 'devotional'
        }
        base_tone = tone_mapping.get(content_type, 'formal')
        
        for target_lang in SUPPORTED_LANGUAGES:
            # Skip if same language
            if target_lang == original_language:
                translation_result = {
                    'translated_text': original_text,
                    'confidence_score': 1.0,
                    'translation_method': 'original',
                    'tone_applied': base_tone,
                    'timestamp': datetime.now().isoformat()
                }
            else:
                translation_result = simulate_llm_translation(original_text, target_lang, base_tone)
            
            translated_item = {
                'content_id': content_id,
                'original_language': original_language,
                'target_language': target_lang,
                'language_name': LANGUAGE_NAMES[target_lang],
                'content_type': content_type,
                'original_text': original_text,
                **translation_result
            }
            
            translated_content.append(translated_item)
    
    logger.info(f"Generated {len(translated_content)} translations")
    return translated_content

def save_translated_content(translated_content: List[Dict]) -> None:
    """Save translated content to JSON file."""
    logger.info(f"Saving {len(translated_content)} translations to {OUTPUT_FILE}")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(translated_content, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved translations to {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Failed to save translations: {str(e)}")
        raise

def main():
    """Main function for translation agent."""
    logger.info("Starting Translation Agent")
    print("Starting AI-Powered Translation Agent...")
    
    try:
        # Load content blocks
        content_blocks = load_config(CONTENT_BLOCKS_FILE)
        print(f"Loaded {len(content_blocks)} content blocks")
        
        # Translate content
        translated_content = translate_content_blocks(content_blocks)
        print(f"Generated {len(translated_content)} translations")
        
        # Save results
        save_translated_content(translated_content)
        print(f"Saved translations to {OUTPUT_FILE}")
        
        # Display sample results
        print("\nSample Translations:")
        for i, item in enumerate(translated_content[:5]):
            print(f"{i+1}. ID {item['content_id']} -> {item['language_name']}: {item['translated_text'][:100]}...")
            print(f"   Confidence: {item['confidence_score']}, Tone: {item['tone_applied']}")
        
        logger.info("Translation Agent completed successfully")
        
    except Exception as e:
        logger.error(f"Translation Agent failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
