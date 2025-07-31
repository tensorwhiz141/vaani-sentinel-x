import os
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

# Logging setup
LOG_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, 'adaptive_strategy_engine.txt')

logger = logging.getLogger('adaptive_strategy_engine')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(LOG_FILE, encoding='utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
logger.addHandler(handler)
logger.info("Initializing adaptive_strategy_engine.py")

# File paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
ANALYTICS_FILE = os.path.join(BASE_DIR, 'analytics_db', 'post_metrics.json')
TTS_OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'tts_simulation_output.json')
PERSONALIZED_CONTENT_FILE = os.path.join(BASE_DIR, 'data', 'personalized_content.json')
OUTPUT_FILE = os.path.join(BASE_DIR, 'data', 'weekly_strategy_recommendation.json')

def load_config(file_path: str) -> List[Dict]:
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

def analyze_performance_metrics(analytics_data: List[Dict]) -> Dict:
    """Analyze performance metrics to identify top-performing content."""
    logger.info(f"Analyzing performance metrics for {len(analytics_data)} posts")
    
    # Group by platform, language, and sentiment
    performance_groups = defaultdict(list)
    
    for post in analytics_data:
        platform = post.get('platform', 'unknown')
        language = post.get('language', 'en')
        sentiment = post.get('sentiment', 'neutral')
        
        # Calculate engagement score
        stats = post.get('stats', {})
        engagement_score = (
            stats.get('likes', 0) * 1.0 +
            stats.get('comments', 0) * 2.0 +
            stats.get('shares', 0) * 3.0 +
            stats.get('retweets', 0) * 2.5 +
            stats.get('views', 0) * 0.1
        )
        
        key = f"{platform}_{language}_{sentiment}"
        performance_groups[key].append({
            'post_id': post.get('post_id'),
            'content_id': post.get('content_id'),
            'engagement_score': engagement_score,
            'stats': stats,
            'timestamp': post.get('timestamp')
        })
    
    # Calculate averages and identify top performers
    performance_analysis = {}
    for key, posts in performance_groups.items():
        platform, language, sentiment = key.split('_')
        avg_engagement = sum(p['engagement_score'] for p in posts) / len(posts)
        top_post = max(posts, key=lambda x: x['engagement_score'])
        
        performance_analysis[key] = {
            'platform': platform,
            'language': language,
            'sentiment': sentiment,
            'post_count': len(posts),
            'average_engagement': round(avg_engagement, 2),
            'top_engagement': round(top_post['engagement_score'], 2),
            'top_content_id': top_post['content_id'],
            'improvement_potential': round(top_post['engagement_score'] - avg_engagement, 2)
        }
    
    logger.info(f"Analyzed {len(performance_analysis)} performance groups")
    return performance_analysis

def analyze_tts_effectiveness(tts_data: List[Dict]) -> Dict:
    """Analyze TTS voice effectiveness by language and tone."""
    logger.info(f"Analyzing TTS effectiveness for {len(tts_data)} outputs")
    
    voice_performance = defaultdict(list)
    
    for tts_item in tts_data:
        voice_tag = tts_item.get('voice_tag')
        language = tts_item.get('language')
        tone = tts_item.get('tone')
        quality_score = tts_item.get('voice_quality_score', 0)
        confidence = tts_item.get('overall_confidence', 0)
        
        # Combined effectiveness score
        effectiveness = (quality_score * 0.6 + confidence * 0.4)
        
        key = f"{language}_{tone}"
        voice_performance[key].append({
            'voice_tag': voice_tag,
            'effectiveness': effectiveness,
            'quality_score': quality_score,
            'confidence': confidence
        })
    
    # Calculate best voices for each language-tone combination
    voice_recommendations = {}
    for key, voices in voice_performance.items():
        language, tone = key.split('_')
        avg_effectiveness = sum(v['effectiveness'] for v in voices) / len(voices)
        best_voice = max(voices, key=lambda x: x['effectiveness'])
        
        voice_recommendations[key] = {
            'language': language,
            'tone': tone,
            'recommended_voice': best_voice['voice_tag'],
            'effectiveness_score': round(best_voice['effectiveness'], 3),
            'average_effectiveness': round(avg_effectiveness, 3),
            'voice_count': len(voices)
        }
    
    logger.info(f"Generated voice recommendations for {len(voice_recommendations)} combinations")
    return voice_recommendations

def generate_content_strategy_recommendations(performance_analysis: Dict, voice_recommendations: Dict, personalized_data: List[Dict]) -> List[Dict]:
    """Generate strategic recommendations based on analysis."""
    logger.info("Generating content strategy recommendations")
    
    recommendations = []
    
    # 1. Top-performing content recommendations
    top_performers = sorted(performance_analysis.values(), key=lambda x: x['average_engagement'], reverse=True)[:5]
    
    for performer in top_performers:
        recommendations.append({
            'type': 'content_amplification',
            'priority': 'high',
            'platform': performer['platform'],
            'language': performer['language'],
            'sentiment': performer['sentiment'],
            'recommendation': f"Increase {performer['sentiment']} content in {performer['language']} on {performer['platform']}",
            'reason': f"Average engagement: {performer['average_engagement']}, Top engagement: {performer['top_engagement']}",
            'expected_impact': 'high',
            'implementation_effort': 'medium'
        })
    
    # 2. Voice optimization recommendations
    high_effectiveness_voices = sorted(voice_recommendations.values(), key=lambda x: x['effectiveness_score'], reverse=True)[:3]
    
    for voice_rec in high_effectiveness_voices:
        recommendations.append({
            'type': 'voice_optimization',
            'priority': 'medium',
            'language': voice_rec['language'],
            'tone': voice_rec['tone'],
            'recommended_voice': voice_rec['recommended_voice'],
            'recommendation': f"Use {voice_rec['recommended_voice']} for {voice_rec['tone']} content in {voice_rec['language']}",
            'reason': f"Effectiveness score: {voice_rec['effectiveness_score']}",
            'expected_impact': 'medium',
            'implementation_effort': 'low'
        })
    
    # 3. Language expansion recommendations
    language_usage = defaultdict(int)
    for item in personalized_data:
        language_usage[item['language']] += 1
    
    underutilized_languages = [lang for lang, count in language_usage.items() if count < 5]
    
    for lang in underutilized_languages[:3]:
        recommendations.append({
            'type': 'language_expansion',
            'priority': 'low',
            'language': lang,
            'recommendation': f"Increase content production in {lang}",
            'reason': f"Currently underutilized with only {language_usage[lang]} content items",
            'expected_impact': 'medium',
            'implementation_effort': 'high'
        })
    
    # 4. Tone diversification recommendations
    tone_distribution = defaultdict(int)
    for item in personalized_data:
        tone_distribution[item['target_tone']] += 1
    
    if tone_distribution['devotional'] < tone_distribution['formal'] * 0.3:
        recommendations.append({
            'type': 'tone_diversification',
            'priority': 'medium',
            'tone': 'devotional',
            'recommendation': "Increase devotional content production",
            'reason': "Devotional content is underrepresented compared to formal content",
            'expected_impact': 'high',
            'implementation_effort': 'medium'
        })
    
    logger.info(f"Generated {len(recommendations)} strategic recommendations")
    return recommendations

def create_weekly_strategy_report(recommendations: List[Dict], performance_analysis: Dict, voice_recommendations: Dict) -> Dict:
    """Create comprehensive weekly strategy report."""
    logger.info("Creating weekly strategy report")
    
    # Calculate summary metrics
    total_platforms = len(set(p['platform'] for p in performance_analysis.values()))
    total_languages = len(set(p['language'] for p in performance_analysis.values()))
    avg_engagement = sum(p['average_engagement'] for p in performance_analysis.values()) / len(performance_analysis)
    
    high_priority_recs = [r for r in recommendations if r['priority'] == 'high']
    medium_priority_recs = [r for r in recommendations if r['priority'] == 'medium']
    low_priority_recs = [r for r in recommendations if r['priority'] == 'low']
    
    report = {
        'report_metadata': {
            'generated_at': datetime.now().isoformat(),
            'report_period': f"{(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} to {datetime.now().strftime('%Y-%m-%d')}",
            'analysis_scope': {
                'platforms_analyzed': total_platforms,
                'languages_analyzed': total_languages,
                'performance_groups': len(performance_analysis),
                'voice_combinations': len(voice_recommendations)
            }
        },
        'executive_summary': {
            'overall_engagement_average': round(avg_engagement, 2),
            'total_recommendations': len(recommendations),
            'high_priority_actions': len(high_priority_recs),
            'medium_priority_actions': len(medium_priority_recs),
            'low_priority_actions': len(low_priority_recs),
            'key_insights': [
                f"Top performing platform-language combination shows {max(p['average_engagement'] for p in performance_analysis.values()):.1f} average engagement",
                f"Voice optimization opportunities identified for {len(voice_recommendations)} language-tone combinations",
                f"{len([r for r in recommendations if r['type'] == 'content_amplification'])} content amplification opportunities identified"
            ]
        },
        'strategic_recommendations': recommendations,
        'performance_insights': performance_analysis,
        'voice_optimization_data': voice_recommendations,
        'implementation_timeline': {
            'immediate_actions': [r for r in recommendations if r['priority'] == 'high'],
            'short_term_actions': [r for r in recommendations if r['priority'] == 'medium'],
            'long_term_actions': [r for r in recommendations if r['priority'] == 'low']
        }
    }
    
    return report

def save_strategy_report(report: Dict) -> None:
    """Save strategy report to JSON file."""
    logger.info(f"Saving strategy report to {OUTPUT_FILE}")
    
    # Ensure data directory exists
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    try:
        with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        logger.info(f"Successfully saved strategy report to {OUTPUT_FILE}")
    except Exception as e:
        logger.error(f"Failed to save strategy report: {str(e)}")
        raise

def main():
    """Main function for adaptive strategy engine."""
    logger.info("Starting Adaptive Strategy Engine")
    print("Starting Adaptive Strategy Engine...")
    
    try:
        # Load analytics data
        analytics_data = load_config(ANALYTICS_FILE)
        print(f"Loaded {len(analytics_data)} analytics records")
        
        # Load TTS simulation data
        tts_data = load_config(TTS_OUTPUT_FILE)
        print(f"Loaded {len(tts_data)} TTS simulation outputs")
        
        # Load personalized content data
        personalized_data = load_config(PERSONALIZED_CONTENT_FILE)
        print(f"Loaded {len(personalized_data)} personalized content items")
        
        # Analyze performance metrics
        performance_analysis = analyze_performance_metrics(analytics_data)
        print(f"Analyzed {len(performance_analysis)} performance groups")
        
        # Analyze TTS effectiveness
        voice_recommendations = analyze_tts_effectiveness(tts_data)
        print(f"Generated {len(voice_recommendations)} voice recommendations")
        
        # Generate strategic recommendations
        recommendations = generate_content_strategy_recommendations(
            performance_analysis, voice_recommendations, personalized_data
        )
        print(f"Generated {len(recommendations)} strategic recommendations")
        
        # Create comprehensive report
        strategy_report = create_weekly_strategy_report(
            recommendations, performance_analysis, voice_recommendations
        )
        
        # Save report
        save_strategy_report(strategy_report)
        print(f"Saved strategy report to {OUTPUT_FILE}")
        
        # Display summary
        summary = strategy_report['executive_summary']
        print(f"\nWeekly Strategy Summary:")
        print(f"- Overall engagement average: {summary['overall_engagement_average']}")
        print(f"- Total recommendations: {summary['total_recommendations']}")
        print(f"- High priority actions: {summary['high_priority_actions']}")
        print(f"- Medium priority actions: {summary['medium_priority_actions']}")
        print(f"- Low priority actions: {summary['low_priority_actions']}")
        
        print(f"\nTop Recommendations:")
        for i, rec in enumerate(recommendations[:3], 1):
            print(f"{i}. [{rec['priority'].upper()}] {rec['recommendation']}")
        
        logger.info("Adaptive Strategy Engine completed successfully")
        
    except Exception as e:
        logger.error(f"Adaptive Strategy Engine failed: {str(e)}")
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main()
