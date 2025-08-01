"""
Scheduler Agent API Router
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
import time
import asyncio
from datetime import datetime, timedelta
import pytz

from models.request_models import SchedulingRequest, PlatformType, LanguageCode
from models.response_models import SchedulingResponse, SchedulingResult

router = APIRouter()
logger = logging.getLogger(__name__)

# Optimal posting times by platform (UTC hours)
OPTIMAL_TIMES = {
    'instagram': [6, 9, 12, 17, 19, 21],  # 6AM, 9AM, 12PM, 5PM, 7PM, 9PM
    'twitter': [8, 12, 17, 20],           # 8AM, 12PM, 5PM, 8PM
    'linkedin': [7, 8, 12, 17, 18],       # 7AM, 8AM, 12PM, 5PM, 6PM
    'sanatan': [5, 6, 18, 19, 20]         # 5AM, 6AM, 6PM, 7PM, 8PM (prayer times)
}

# Audience activity levels by hour
AUDIENCE_ACTIVITY = {
    'instagram': {6: 0.7, 9: 0.8, 12: 0.9, 17: 0.95, 19: 1.0, 21: 0.85},
    'twitter': {8: 0.8, 12: 0.9, 17: 0.95, 20: 1.0},
    'linkedin': {7: 0.75, 8: 0.9, 12: 0.85, 17: 1.0, 18: 0.95},
    'sanatan': {5: 0.9, 6: 1.0, 18: 0.95, 19: 0.9, 20: 0.85}
}

async def calculate_optimal_time(
    platform: str, 
    preferred_time: datetime = None, 
    timezone: str = 'UTC'
) -> Dict[str, Any]:
    """Calculate optimal posting time for platform."""
    await asyncio.sleep(0.05)
    
    # Get current time in specified timezone
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    
    # Get optimal hours for platform
    optimal_hours = OPTIMAL_TIMES.get(platform, [9, 12, 17])
    
    # If preferred time is specified, check if it's optimal
    if preferred_time:
        preferred_hour = preferred_time.hour
        if preferred_hour in optimal_hours:
            optimization_score = AUDIENCE_ACTIVITY.get(platform, {}).get(preferred_hour, 0.7)
            return {
                'scheduled_time': preferred_time,
                'optimization_score': optimization_score,
                'is_optimal': True
            }
    
    # Find next optimal time
    current_hour = now.hour
    next_optimal_hours = [h for h in optimal_hours if h > current_hour]
    
    if next_optimal_hours:
        next_hour = min(next_optimal_hours)
        scheduled_time = now.replace(hour=next_hour, minute=0, second=0, microsecond=0)
    else:
        # Next day's first optimal time
        next_hour = min(optimal_hours)
        scheduled_time = (now + timedelta(days=1)).replace(hour=next_hour, minute=0, second=0, microsecond=0)
    
    optimization_score = AUDIENCE_ACTIVITY.get(platform, {}).get(next_hour, 0.8)
    
    return {
        'scheduled_time': scheduled_time,
        'optimization_score': optimization_score,
        'is_optimal': True
    }

async def estimate_audience_reach(platform: str, scheduled_time: datetime, language: str) -> int:
    """Estimate audience reach for scheduled content."""
    await asyncio.sleep(0.02)
    
    # Base audience by platform
    base_audience = {
        'instagram': 5000,
        'twitter': 3000,
        'linkedin': 2000,
        'sanatan': 1500
    }
    
    # Language multipliers
    language_multipliers = {
        'en': 1.0,
        'hi': 0.8,
        'sa': 0.6
    }
    
    base = base_audience.get(platform, 2000)
    lang_mult = language_multipliers.get(language, 0.7)
    
    # Time-based multiplier
    hour = scheduled_time.hour
    time_mult = AUDIENCE_ACTIVITY.get(platform, {}).get(hour, 0.7)
    
    estimated_reach = int(base * lang_mult * time_mult)
    return estimated_reach

@router.post("/schedule-content", response_model=SchedulingResponse)
async def schedule_content(request: SchedulingRequest):
    """Schedule content for optimal posting time."""
    start_time = time.time()
    
    try:
        # Calculate optimal scheduling
        scheduling_data = await calculate_optimal_time(
            request.platform.value,
            request.preferred_time,
            request.timezone
        )
        
        # Estimate audience reach
        estimated_reach = await estimate_audience_reach(
            request.platform.value,
            scheduling_data['scheduled_time'],
            request.language.value
        )
        
        # Determine competition level (simplified)
        hour = scheduling_data['scheduled_time'].hour
        if hour in [12, 17, 19]:  # Peak hours
            competition_level = "high"
        elif hour in [9, 15, 21]:  # Medium hours
            competition_level = "medium"
        else:
            competition_level = "low"
        
        # Create scheduling result
        scheduling_result = SchedulingResult(
            content_id=request.content_id,
            scheduled_time=scheduling_data['scheduled_time'],
            platform=request.platform,
            optimization_score=scheduling_data['optimization_score'],
            audience_reach_estimate=estimated_reach,
            competition_level=competition_level
        )
        
        # Generate alternative times
        alternative_times = []
        optimal_hours = OPTIMAL_TIMES.get(request.platform.value, [9, 12, 17])
        for hour in optimal_hours[:3]:  # Top 3 alternatives
            alt_time = scheduling_data['scheduled_time'].replace(hour=hour)
            alt_reach = await estimate_audience_reach(request.platform.value, alt_time, request.language.value)
            alternative_times.append({
                'time': alt_time.isoformat(),
                'optimization_score': AUDIENCE_ACTIVITY.get(request.platform.value, {}).get(hour, 0.7),
                'estimated_reach': alt_reach
            })
        
        processing_time = time.time() - start_time
        
        return SchedulingResponse(
            success=True,
            processing_time=round(processing_time, 3),
            scheduling_result=scheduling_result,
            alternative_times=alternative_times,
            scheduling_rationale=f"Scheduled for optimal {request.platform.value} engagement time with {competition_level} competition"
        )
        
    except Exception as e:
        logger.error(f"Content scheduling failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Scheduling failed: {str(e)}")

@router.get("/schedule-content/optimal-times/{platform}")
async def get_optimal_times(platform: str):
    """Get optimal posting times for a specific platform."""
    if platform not in OPTIMAL_TIMES:
        raise HTTPException(status_code=404, detail=f"Platform '{platform}' not supported")
    
    return {
        "platform": platform,
        "optimal_hours_utc": OPTIMAL_TIMES[platform],
        "audience_activity": AUDIENCE_ACTIVITY.get(platform, {}),
        "timezone_note": "All times are in UTC. Adjust for your local timezone."
    }
