import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional

# Logging setup
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'personalization_agent.txt')

logger = logging.getLogger('personalization_agent')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.info("Initializing personalization_agent.py")

# File paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
CONFIG_DIR = os.path.join(BASE_DIR, 'config')
USER_PROFILES_FILE = os.path.join(CONFIG_DIR, 'user_profiles.json')
TRANSLATED_CONTENT_FILE = os.path.join(BASE_DIR, 'data', 'translated_content.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'personalized_content.json')

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

def simulate_tone_personalization(text: str, original_tone: str, target_tone: str, language: str) -> Dict:
    """Simulate LLM-powered tone personalization."""
    logger.debug(f"Personalizing tone from {original_tone} to {target_tone} in {language}")
    
    # Tone transformation templates
    tone_transformations = {
        ('formal', 'casual'): {
            'prefix': '[Casual Style]',
            'confidence_modifier': -0.02
        },
        ('formal', 'devotional'): {
            'prefix': '[Devotional Style]',
            'confidence_modifier': 0.03 if language in ['hi', 'mr', 'ta', 'te', 'kn', 'ml', 'bn', 'gu', 'pa', 'od'] else -0.01
        },
        ('casual', 'formal'): {
            'prefix': '[Formal Style]',
            'confidence_modifier': 0.01
        },
        ('casual', 'devotional'): {
            'prefix': '[Devotional Style]',
            'confidence_modifier': 0.02 if language in ['hi', 'mr', 'ta', 'te', 'kn', 'ml', 'bn', 'gu', 'pa', 'od'] else -0.02
        },
        ('devotional', 'formal'): {
            'prefix': '[Formal Style]',
            'confidence_modifier': -0.01
        },
        ('devotional', 'casual'): {
            'prefix': '[Casual Style]',
            'confidence_modifier': -0.03
        }
    }
    
    # If same tone, no change needed
    if original_tone == target_tone:
        return {
            'personalized_text': text,
            'tone_confidence': 0.98,
            'personalization_applied': False
        }
    
    # Apply tone transformation
    transformation = tone_transformations.get((original_tone, target_tone), {
        'prefix': f'[{target_tone.title()} Style]',
        'confidence_modifier': -0.05
    })
    
    personalized_text = f"{transformation['prefix']} {text}"
    base_confidence = 0.90
    tone_confidence = base_confidence + transformation['confidence_modifier']
    
    return {
        'personalized_text': personalized_text,
        'tone_confidence': round(max(0.70, min(0.99, tone_confidence)), 3),
        'personalization_applied': True
    }

def personalize_content_for_users(translated_content: List[Dict], user_profiles: List[Dict]) -> List[Dict]:
    """Personalize translated content based on user preferences."""
    logger.info(f"Personalizing content for {len(user_profiles)} users")
    
    personalized_content = []
    
    for user in user_profiles:
        user_id = user['user_id']
        preferred_languages = user['preferred_languages']
        tone_preference = user.get('tone_preference', 'formal')
        content_types = user.get('content_types', [])
        
        logger.info(f"Processing user {user_id} with tone preference: {tone_preference}")
        
        for content_item in translated_content:
            content_id = content_item['content_id']
            target_language = content_item['target_language']
            content_type = content_item['content_type']
            original_tone = content_item['tone_applied']
            translated_text = content_item['translated_text']
            
            # Skip if language not in user preferences
            if target_language not in preferred_languages:
                continue
            
            # Skip if content type not in user preferences (if specified)
            if content_types and content_type not in content_types:
                continue
            
            # Apply tone personalization
            personalization_result = simulate_tone_personalization(
                translated_text, original_tone, tone_preference, target_language
            )
            
            personalized_item = {
                'user_id': user_id,
                'content_id': content_id,
                'language': target_language,
                'language_name': content_item['language_name'],
                'content_type': content_type,
                'original_tone': original_tone,
                'target_tone': tone_preference,
                'original_text': content_item['original_text'],
                'translated_text': translated_text,
                'personalized_text': personalization_result['personalized_text'],
                'translation_confidence': content_item['confidence_score'],
                'tone_confidence': personalization_result['tone_confidence'],
                'overall_confidence': round(
                    (content_item['confidence_score'] + personalization_result['tone_confidence']) / 2, 3
                ),
                'personalization_applied': personalization_result['personalization_applied'],
                'timestamp': datetime.now().isoformat()
            }
            
            personalized_content.append(personalized_item)
    
    logger.info(f"Generated {len(personalized_content)} personalized content items")
    return personalized_content

def save_personalized_content(personalized_content: List[Dict]) -> None:
    """Save personalized content to JSON file."""
    logger.info(f"Saving {len(personalized_content)} personalized items to {OUTPUT_FILE}")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(personalized_content, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved personalized content to {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Failed to save personalized content: {str(e)}")
        raise

def generate_personalization_summary(personalized_content: List[Dict]) -> Dict:
    """Generate summary statistics for personalization."""
    logger.info("Generating personalization summary")
    
    total_items = len(personalized_content)
    users = set(item['user_id'] for item in personalized_content)
    languages = set(item['language'] for item in personalized_content)
    content_types = set(item['content_type'] for item in personalized_content)
    
    # Calculate average confidence scores
    translation_confidences = [item['translation_confidence'] for item in personalized_content]
    tone_confidences = [item['tone_confidence'] for item in personalized_content]
    overall_confidences = [item['overall_confidence'] for item in personalized_content]
    
    # Count personalization applications
    personalized_count = sum(1 for item in personalized_content if item['personalization_applied'])
    
    summary = {
        'total_personalized_items': total_items,
        'unique_users': len(users),
        'unique_languages': len(languages),
        'unique_content_types': len(content_types),
        'personalization_applied_count': personalized_count,
        'personalization_rate': round(personalized_count / total_items * 100, 2) if total_items > 0 else 0,
        'average_translation_confidence': round(sum(translation_confidences) / len(translation_confidences), 3) if translation_confidences else 0,
        'average_tone_confidence': round(sum(tone_confidences) / len(tone_confidences), 3) if tone_confidences else 0,
        'average_overall_confidence': round(sum(overall_confidences) / len(overall_confidences), 3) if overall_confidences else 0,
        'users_list': list(users),
        'languages_list': list(languages),
        'content_types_list': list(content_types),
        'timestamp': datetime.now().isoformat()
    }
    
    return summary

def main():
    """Main function for personalization agent."""
    logger.info("Starting Personalization Agent")
    print("Starting AI-Powered Personalization Agent...")
    
    try:
        # Load user profiles
        user_profiles = load_config(USER_PROFILES_FILE)
        print(f"Loaded {len(user_profiles)} user profiles")
        
        # Load translated content
        translated_content = load_config(TRANSLATED_CONTENT_FILE)
        print(f"Loaded {len(translated_content)} translated content items")
        
        # Personalize content
        personalized_content = personalize_content_for_users(translated_content, user_profiles)
        print(f"Generated {len(personalized_content)} personalized content items")
        
        # Save results
        save_personalized_content(personalized_content)
        print(f"Saved personalized content to {OUTPUT_FILE}")
        
        # Generate and display summary
        summary = generate_personalization_summary(personalized_content)
        print(f"\nPersonalization Summary:")
        print(f"- Total items: {summary['total_personalized_items']}")
        print(f"- Users: {summary['unique_users']}")
        print(f"- Languages: {summary['unique_languages']}")
        print(f"- Personalization rate: {summary['personalization_rate']}%")
        print(f"- Average confidence: {summary['average_overall_confidence']}")
        
        # Display sample results
        print("\nSample Personalized Content:")
        for i, item in enumerate(personalized_content[:3]):
            print(f"{i+1}. User {item['user_id']} - {item['language_name']} ({item['target_tone']}):")
            print(f"   {item['personalized_text'][:100]}...")
            print(f"   Confidence: {item['overall_confidence']}")
        
        logger.info("Personalization Agent completed successfully")
        
    except Exception as e:
        logger.error(f"Personalization Agent failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
