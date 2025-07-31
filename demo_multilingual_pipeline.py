#!/usr/bin/env python3
"""
Vaani Sentinel-X Multilingual Content Personalization Demo
==========================================================

This script demonstrates the complete multilingual content pipeline:
1. Language metadata enhancement
2. Simulated translation previews  
3. AI-powered translation with confidence scoring
4. Personalization based on user preferences
5. TTS voice tag assignment with tone mapping
6. Weekly strategy recommendations

Author: Vaani Sentinel-X Team
Date: 2025-07-30
"""

import os
import json
import subprocess
import sys
from datetime import datetime
from typing import Dict, List

def print_header(title: str) -> None:
    """Print a formatted header."""
    print("\n" + "="*60)
    print(f" {title}")
    print("="*60)

def print_section(title: str) -> None:
    """Print a formatted section header."""
    print(f"\n--- {title} ---")

def run_agent(script_path: str, description: str) -> bool:
    """Run an agent script and return success status."""
    print(f"\n🚀 Running {description}...")
    try:
        result = subprocess.run([sys.executable, script_path], 
                              capture_output=True, text=True, cwd=os.getcwd())
        if result.returncode == 0:
            print(f"✅ {description} completed successfully")
            return True
        else:
            print(f"❌ {description} failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error running {description}: {str(e)}")
        return False

def load_json_file(file_path: str) -> Dict:
    """Load and return JSON file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Error loading {file_path}: {str(e)}")
        return {}

def display_sample_data(data: List[Dict], title: str, sample_count: int = 3) -> None:
    """Display sample data from a list."""
    print_section(f"Sample {title}")
    for i, item in enumerate(data[:sample_count], 1):
        print(f"\n{i}. {title} Sample:")
        for key, value in list(item.items())[:5]:  # Show first 5 fields
            if isinstance(value, str) and len(value) > 100:
                value = value[:100] + "..."
            print(f"   {key}: {value}")
        if len(item) > 5:
            print(f"   ... and {len(item) - 5} more fields")

def display_strategy_summary(strategy_data: Dict) -> None:
    """Display strategy recommendation summary."""
    print_section("Weekly Strategy Summary")
    
    if 'executive_summary' in strategy_data:
        summary = strategy_data['executive_summary']
        print(f"📊 Overall engagement average: {summary.get('overall_engagement_average', 'N/A')}")
        print(f"📋 Total recommendations: {summary.get('total_recommendations', 'N/A')}")
        print(f"🔥 High priority actions: {summary.get('high_priority_actions', 'N/A')}")
        print(f"⚡ Medium priority actions: {summary.get('medium_priority_actions', 'N/A')}")
        print(f"📈 Low priority actions: {summary.get('low_priority_actions', 'N/A')}")
        
        if 'key_insights' in summary:
            print(f"\n🔍 Key Insights:")
            for insight in summary['key_insights']:
                print(f"   • {insight}")
    
    if 'strategic_recommendations' in strategy_data:
        recommendations = strategy_data['strategic_recommendations'][:3]
        print(f"\n🎯 Top 3 Recommendations:")
        for i, rec in enumerate(recommendations, 1):
            priority = rec.get('priority', 'unknown').upper()
            recommendation = rec.get('recommendation', 'N/A')
            print(f"   {i}. [{priority}] {recommendation}")

def display_language_coverage(translated_data: List[Dict]) -> None:
    """Display language coverage statistics."""
    print_section("Language Coverage Analysis")
    
    languages = {}
    for item in translated_data:
        lang = item.get('target_language', 'unknown')
        lang_name = item.get('language_name', lang)
        if lang not in languages:
            languages[lang] = {'name': lang_name, 'count': 0, 'avg_confidence': 0}
        languages[lang]['count'] += 1
        languages[lang]['avg_confidence'] += item.get('confidence_score', 0)
    
    # Calculate averages
    for lang_data in languages.values():
        if lang_data['count'] > 0:
            lang_data['avg_confidence'] = round(lang_data['avg_confidence'] / lang_data['count'], 3)
    
    print(f"🌍 Total languages supported: {len(languages)}")
    print(f"📝 Total translations generated: {len(translated_data)}")
    
    print(f"\n🏆 Top 5 Languages by Content Volume:")
    sorted_langs = sorted(languages.items(), key=lambda x: x[1]['count'], reverse=True)
    for i, (lang_code, data) in enumerate(sorted_langs[:5], 1):
        print(f"   {i}. {data['name']} ({lang_code}): {data['count']} items, {data['avg_confidence']} avg confidence")

def display_voice_mapping_stats(tts_data: List[Dict]) -> None:
    """Display TTS voice mapping statistics."""
    print_section("Voice Mapping Statistics")
    
    voice_usage = {}
    tone_distribution = {}
    
    for item in tts_data:
        voice = item.get('voice_tag', 'unknown')
        tone = item.get('tone', 'unknown')
        
        voice_usage[voice] = voice_usage.get(voice, 0) + 1
        tone_distribution[tone] = tone_distribution.get(tone, 0) + 1
    
    print(f"🎤 Total unique voices used: {len(voice_usage)}")
    print(f"🎭 Total tone variations: {len(tone_distribution)}")
    
    print(f"\n🎵 Top 5 Most Used Voices:")
    sorted_voices = sorted(voice_usage.items(), key=lambda x: x[1], reverse=True)
    for i, (voice, count) in enumerate(sorted_voices[:5], 1):
        print(f"   {i}. {voice}: {count} uses")
    
    print(f"\n🎨 Tone Distribution:")
    for tone, count in sorted(tone_distribution.items(), key=lambda x: x[1], reverse=True):
        print(f"   • {tone}: {count} items")

def main():
    """Main demo function."""
    print_header("Vaani Sentinel-X Multilingual Content Personalization Demo")
    print("🌟 Demonstrating AI-powered multilingual content pipeline")
    print(f"📅 Demo Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Check if we're in the right directory
    if not os.path.exists('agents') or not os.path.exists('config'):
        print("❌ Please run this demo from the Vaani Sentinel-X root directory")
        return
    
    print_section("Pipeline Overview")
    print("This demo will execute the following pipeline:")
    print("1. 🔤 Language Metadata Enhancement")
    print("2. 🌐 AI-Powered Translation (21 languages)")
    print("3. 👤 Content Personalization (10 user profiles)")
    print("4. 🎤 TTS Voice Tag Assignment")
    print("5. 📊 Adaptive Strategy Recommendations")
    print("6. 📋 Comprehensive Results Analysis")
    
    # Step 1: Run Translation Agent
    success = run_agent('agents/translation_agent.py', 'AI-Powered Translation Agent')
    if not success:
        print("❌ Translation failed, stopping demo")
        return
    
    # Step 2: Run Personalization Agent
    success = run_agent('agents/personalization_agent.py', 'Content Personalization Agent')
    if not success:
        print("❌ Personalization failed, stopping demo")
        return
    
    # Step 3: Run TTS Simulator
    success = run_agent('agents/tts_simulator.py', 'TTS Voice Assignment Simulator')
    if not success:
        print("❌ TTS simulation failed, stopping demo")
        return
    
    # Step 4: Run Strategy Engine
    success = run_agent('agents/adaptive_strategy_engine.py', 'Adaptive Strategy Engine')
    if not success:
        print("❌ Strategy generation failed, stopping demo")
        return
    
    print_header("Pipeline Results Analysis")
    
    # Load and analyze results
    print("📂 Loading generated data files...")
    
    translated_data = load_json_file('data/translated_content.json')
    personalized_data = load_json_file('data/personalized_content.json')
    tts_data = load_json_file('data/tts_simulation_output.json')
    strategy_data = load_json_file('data/weekly_strategy_recommendation.json')
    
    if not all([translated_data, personalized_data, tts_data, strategy_data]):
        print("❌ Some data files could not be loaded")
        return
    
    # Display comprehensive analysis
    display_language_coverage(translated_data)
    display_sample_data(translated_data, "Translated Content")
    
    display_sample_data(personalized_data, "Personalized Content")
    
    display_voice_mapping_stats(tts_data)
    display_sample_data(tts_data, "TTS Simulation Output")
    
    display_strategy_summary(strategy_data)
    
    print_header("Demo Completion Summary")
    print("✅ All pipeline components executed successfully!")
    print(f"📊 Generated {len(translated_data)} translations")
    print(f"👤 Created {len(personalized_data)} personalized content items")
    print(f"🎤 Simulated {len(tts_data)} TTS outputs")
    print(f"📋 Produced comprehensive strategy recommendations")
    
    print_section("Next Steps")
    print("🔗 Integration Points:")
    print("   • API endpoints added to Next.js backend server")
    print("   • Data available at /api/translated-content")
    print("   • Data available at /api/personalized-content")
    print("   • Data available at /api/tts-simulation")
    print("   • Data available at /api/strategy-recommendations")
    
    print("\n🚀 To test the API integration:")
    print("   1. Start the backend server: cd web-ui/nextjs-voice-panel && npm run server")
    print("   2. Start the frontend: npm start (or npm run dev)")
    print("   3. Login with test@vaani.com / password123")
    print("   4. Access the new multilingual features in the dashboard")
    
    print("\n🎯 Deliverables Completed:")
    print("   ✅ 20+ language support with voice mapping")
    print("   ✅ AI-powered translation with confidence scoring")
    print("   ✅ Tone-based personalization")
    print("   ✅ TTS voice tag assignment")
    print("   ✅ Weekly strategy recommendations")
    print("   ✅ Complete API integration")
    
    print(f"\n🌟 Vaani Sentinel-X Multilingual Pipeline Demo Complete! 🌟")

if __name__ == "__main__":
    main()
