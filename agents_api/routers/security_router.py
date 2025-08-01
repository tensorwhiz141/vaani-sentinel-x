"""
Security Validation Agent API Router
"""

from fastapi import APIRouter, HTTPException
from typing import Dict, Any, List
import logging
import time
import asyncio
import re

from models.request_models import SecurityValidationRequest, PlatformType, LanguageCode
from models.response_models import SecurityValidationResponse, SecurityIssue

router = APIRouter()
logger = logging.getLogger(__name__)

# Security patterns and rules
SECURITY_PATTERNS = {
    'inappropriate_content': [
        r'\b(hate|violence|abuse|harassment)\b',
        r'\b(spam|scam|fraud)\b'
    ],
    'personal_info': [
        r'\b\d{3}-\d{2}-\d{4}\b',  # SSN pattern
        r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b',  # Credit card pattern
        r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  # Email pattern
    ],
    'platform_violations': {
        'twitter': [r'#\w+' * 10],  # Too many hashtags
        'instagram': [r'follow\s+for\s+follow', r'like\s+for\s+like'],
        'linkedin': [r'get\s+rich\s+quick', r'make\s+money\s+fast']
    }
}

# Compliance rules
COMPLIANCE_RULES = {
    'content_length': True,
    'appropriate_language': True,
    'no_personal_info': True,
    'platform_guidelines': True,
    'cultural_sensitivity': True
}

async def scan_for_security_issues(
    content: str, 
    platform: str, 
    language: str, 
    strict_mode: bool = False
) -> List[Dict[str, Any]]:
    """Scan content for security and compliance issues."""
    await asyncio.sleep(0.08)
    
    issues = []
    
    # Check for inappropriate content
    for pattern in SECURITY_PATTERNS['inappropriate_content']:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append({
                'type': 'inappropriate_content',
                'severity': 'high',
                'description': 'Content contains potentially inappropriate language',
                'suggested_fix': 'Remove or replace flagged terms with appropriate alternatives',
                'confidence': 0.85
            })
    
    # Check for personal information
    for pattern in SECURITY_PATTERNS['personal_info']:
        if re.search(pattern, content):
            issues.append({
                'type': 'personal_information',
                'severity': 'critical',
                'description': 'Content contains personal information that should be removed',
                'suggested_fix': 'Remove or mask personal information',
                'confidence': 0.95
            })
    
    # Platform-specific violations
    platform_patterns = SECURITY_PATTERNS['platform_violations'].get(platform, [])
    for pattern in platform_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            issues.append({
                'type': 'platform_violation',
                'severity': 'medium',
                'description': f'Content may violate {platform} community guidelines',
                'suggested_fix': f'Adjust content to comply with {platform} best practices',
                'confidence': 0.75
            })
    
    # Strict mode additional checks
    if strict_mode:
        # Check for excessive capitalization
        if len(re.findall(r'[A-Z]{3,}', content)) > 2:
            issues.append({
                'type': 'formatting_issue',
                'severity': 'low',
                'description': 'Excessive use of capital letters detected',
                'suggested_fix': 'Use normal capitalization for better readability',
                'confidence': 0.70
            })
        
        # Check for excessive punctuation
        if len(re.findall(r'[!?]{2,}', content)) > 0:
            issues.append({
                'type': 'formatting_issue',
                'severity': 'low',
                'description': 'Excessive punctuation detected',
                'suggested_fix': 'Use standard punctuation for professional appearance',
                'confidence': 0.65
            })
    
    return issues

async def check_compliance(content: str, platform: str, language: str) -> Dict[str, bool]:
    """Check content compliance against various rules."""
    await asyncio.sleep(0.03)
    
    compliance_status = {}
    
    # Content length check
    platform_limits = {'twitter': 280, 'instagram': 2200, 'linkedin': 3000, 'sanatan': 1500}
    max_length = platform_limits.get(platform, 1000)
    compliance_status['content_length'] = len(content) <= max_length
    
    # Appropriate language check (simplified)
    inappropriate_words = ['spam', 'scam', 'hate', 'violence']
    compliance_status['appropriate_language'] = not any(word in content.lower() for word in inappropriate_words)
    
    # No personal info check
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    compliance_status['no_personal_info'] = not re.search(email_pattern, content)
    
    # Platform guidelines (simplified)
    compliance_status['platform_guidelines'] = True  # Assume compliant unless issues found
    
    # Cultural sensitivity (basic check)
    sensitive_terms = ['offensive', 'discriminatory', 'inappropriate']
    compliance_status['cultural_sensitivity'] = not any(term in content.lower() for term in sensitive_terms)
    
    return compliance_status

async def sanitize_content(content: str, issues: List[Dict[str, Any]]) -> str:
    """Sanitize content by fixing identified issues."""
    await asyncio.sleep(0.05)
    
    sanitized = content
    
    # Remove personal information
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    sanitized = re.sub(email_pattern, '[EMAIL_REMOVED]', sanitized)
    
    # Fix excessive capitalization
    sanitized = re.sub(r'[A-Z]{4,}', lambda m: m.group().capitalize(), sanitized)
    
    # Fix excessive punctuation
    sanitized = re.sub(r'[!?]{2,}', '!', sanitized)
    
    # Remove inappropriate content (basic)
    inappropriate_words = ['spam', 'scam']
    for word in inappropriate_words:
        sanitized = re.sub(rf'\b{word}\b', '[REMOVED]', sanitized, flags=re.IGNORECASE)
    
    return sanitized

@router.post("/validate-content", response_model=SecurityValidationResponse)
async def validate_content(request: SecurityValidationRequest):
    """Validate content for security and compliance issues."""
    start_time = time.time()
    
    try:
        # Scan for security issues
        security_issues_data = await scan_for_security_issues(
            request.content,
            request.platform.value,
            request.language.value,
            request.strict_mode
        )
        
        # Create security issue objects
        security_issues = []
        for issue_data in security_issues_data:
            issue = SecurityIssue(
                issue_type=issue_data['type'],
                severity=issue_data['severity'],
                description=issue_data['description'],
                suggested_fix=issue_data['suggested_fix'],
                confidence=issue_data['confidence']
            )
            security_issues.append(issue)
        
        # Check compliance
        compliance_status = await check_compliance(
            request.content,
            request.platform.value,
            request.language.value
        )
        
        # Determine if content is safe
        critical_issues = [issue for issue in security_issues if issue.severity == 'critical']
        high_issues = [issue for issue in security_issues if issue.severity == 'high']
        content_safe = len(critical_issues) == 0 and len(high_issues) == 0
        
        # Calculate overall risk score
        risk_score = 0.0
        for issue in security_issues:
            if issue.severity == 'critical':
                risk_score += 0.4
            elif issue.severity == 'high':
                risk_score += 0.3
            elif issue.severity == 'medium':
                risk_score += 0.2
            else:  # low
                risk_score += 0.1
        
        risk_score = min(1.0, risk_score)
        
        # Generate sanitized content if issues exist
        sanitized_content = None
        if security_issues:
            sanitized_content = await sanitize_content(request.content, security_issues_data)
        
        processing_time = time.time() - start_time
        
        return SecurityValidationResponse(
            success=True,
            processing_time=round(processing_time, 3),
            content_safe=content_safe,
            overall_risk_score=risk_score,
            issues_found=security_issues,
            compliance_status=compliance_status,
            sanitized_content=sanitized_content
        )
        
    except Exception as e:
        logger.error(f"Security validation failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Validation failed: {str(e)}")

@router.get("/validate-content/rules")
async def get_security_rules():
    """Get available security rules and compliance checks."""
    return {
        "security_categories": list(SECURITY_PATTERNS.keys()),
        "compliance_rules": list(COMPLIANCE_RULES.keys()),
        "severity_levels": ["low", "medium", "high", "critical"],
        "supported_platforms": ["instagram", "twitter", "linkedin", "sanatan"]
    }
