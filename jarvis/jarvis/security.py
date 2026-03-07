"""Safety & Security utilities for Jarvis.

Implements:
- Dangerous intent detection
- Keyword filtering
- API rate limiting
- Audit logging
- Prompt injection prevention
"""

import re
import time
from typing import Tuple, Dict, Any
from .database import log_command

# DANGEROUS KEYWORDS that indicate destructive intent
DANGEROUS_KEYWORDS = {
    # Shutdown/restart
    "shutdown", "restart", "reboot", "power off", "turn off",
    # File operations
    "delete", "remove", "rm -rf", "format", "wipe", "erase",
    # System attacks
    "hack", "crack", "breach", "exploit", "malware", "virus",
    # Sensitive operations
    "password", "bitcoin", "cryptocurrency", "private key", "token",
    "credit card", "ssn", "social security",
    # Process control
    "kill process", "terminate", "force close",
    # Network
    "firewall", "vpn", "proxy", "tunnel",
}

# Keywords that are generally safe
SAFE_KEYWORDS = {
    "time", "date", "weather", "news", "search", "open", "play",
    "pause", "stop", "volume", "music", "show", "tell", "joke",
    "reminder", "note", "task", "calendar", "schedule",
}

# Prompt injection patterns (to prevent users from overriding system prompt)
INJECTION_PATTERNS = [
    r"system.*prompt",
    r"ignore.*instruction",
    r"forget.*previous",
    r"override.*system",
    r"act as.*admin",
    r"you.*are.*now",
    r"new.*instructions",
]

class SafetyFilter:
    def __init__(self, rate_limit_requests=100, rate_limit_window_sec=60):
        """Initialize safety filter with rate limiting."""
        self.rate_limit_requests = rate_limit_requests
        self.rate_limit_window_sec = rate_limit_window_sec
        self.request_history = {}  # {user_id: [timestamp, timestamp, ...]}
        
    def detect_dangerous_intent(self, text: str) -> Tuple[bool, str]:
        """
        Detect if command contains dangerous/destructive intent.
        
        Returns:
            (is_dangerous: bool, reason: str)
        """
        text_lower = text.lower()
        
        # Check for explicit dangerous keywords
        for keyword in DANGEROUS_KEYWORDS:
            if keyword in text_lower:
                return True, f"Dangerous keyword detected: '{keyword}'"
        
        # Check for prompt injection attempts
        for pattern in INJECTION_PATTERNS:
            if re.search(pattern, text_lower, re.IGNORECASE):
                return True, "Prompt injection attempt detected"
        
        # Check for SQL injection patterns
        if re.search(r"(union|select|insert|update|delete|drop|exec|script)", text_lower):
            if "query" not in text_lower:  # Allow in context of search queries
                return True, "SQL injection pattern detected"
        
        # Check for command injection
        if any(char in text for char in ['|', ';', '`', '$(', '${', '&', '>']):
            return True, "Command injection pattern detected"
        
        return False, ""
    
    def filter_user_input(self, text: str) -> Tuple[bool, str]:
        """
        Apply comprehensive input validation.
        
        Returns:
            (is_safe: bool, reason_if_unsafe: str)
        """
        # Check length
        if len(text) > 1000:
            return False, "Command too long (>1000 chars)"
        
        # Check for null bytes
        if '\x00' in text:
            return False, "Null byte detected"
        
        # Check dangerous intent
        is_dangerous, reason = self.detect_dangerous_intent(text)
        if is_dangerous:
            return False, reason
        
        return True, ""
    
    def check_rate_limit(self, user_id: str = "default") -> Tuple[bool, str]:
        """
        Check if user has exceeded rate limit.
        
        Returns:
            (is_within_limit: bool, reason_if_exceeded: str)
        """
        now = time.time()
        
        if user_id not in self.request_history:
            self.request_history[user_id] = []
        
        # Clean old requests outside window
        self.request_history[user_id] = [
            ts for ts in self.request_history[user_id]
            if now - ts < self.rate_limit_window_sec
        ]
        
        # Check limit
        if len(self.request_history[user_id]) >= self.rate_limit_requests:
            return False, f"Rate limit exceeded ({self.rate_limit_requests} requests per {self.rate_limit_window_sec}s)"
        
        # Record this request
        self.request_history[user_id].append(now)
        return True, ""
    
    def sanitize_for_ai(self, text: str) -> str:
        """
        Sanitize user input before sending to AI.
        Removes potentially malicious content while preserving meaning.
        """
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters that could be dangerous (but keep common punctuation)
        text = re.sub(r'[^\w\s\-\.\,\?\!\:\'\"]', '', text)
        
        # Limit to ASCII range (prevents some Unicode-based attacks)
        text = text.encode('ascii', errors='ignore').decode('ascii')
        
        return text.strip()

# Global safety filter instance
_safety_filter = SafetyFilter(
    rate_limit_requests=100,
    rate_limit_window_sec=60
)

def validate_and_sanitize(user_input: str, user_id: str = "default") -> Dict[str, Any]:
    """
    Main validation function - checks all security layers.
    
    Returns dict with:
        - is_safe: bool
        - reason: str (if unsafe)
        - sanitized: str (if safe)
        - blocked: bool
    """
    result = {
        "is_safe": True,
        "reason": "",
        "sanitized": "",
        "blocked": False,
    }
    
    # Layer 1: Input validation
    is_safe, reason = _safety_filter.filter_user_input(user_input)
    if not is_safe:
        result["is_safe"] = False
        result["reason"] = reason
        result["blocked"] = True
        return result
    
    # Layer 2: Rate limiting
    is_within_limit, reason = _safety_filter.check_rate_limit(user_id)
    if not is_within_limit:
        result["is_safe"] = False
        result["reason"] = reason
        result["blocked"] = True
        return result
    
    # Layer 3: Sanitization
    sanitized = _safety_filter.sanitize_for_ai(user_input)
    result["sanitized"] = sanitized
    
    return result

def log_blocked_command(input_text: str, reason: str, user_id: str = "default"):
    """Log a blocked command attempt to audit trail."""
    log_command(
        input_text=input_text,
        stage="security",
        intent="blocked_command",
        success=False,
        execution_time_ms=0,
        blocked=1,
        meta=f"user={user_id},reason={reason}"
    )

def create_safe_ai_prompt(user_query: str, system_prompt: str = None) -> str:
    """
    Create a safe AI prompt with guardrails.
    
    Prevents prompt injection by:
    - Using explicit structure
    - Sanitizing user input
    - Clearly separating system/user messages
    """
    if system_prompt is None:
        system_prompt = (
            "You are Jarvis, an Uzbek AI assistant. "
            "You respond concisely and helpfully. "
            "You NEVER provide instructions for harmful, illegal, or destructive actions. "
            "You ALWAYS respond in Uzbek when possible."
        )
    
    sanitized_query = _safety_filter.sanitize_for_ai(user_query)
    
    # Use clear delimiters to prevent prompt injection
    safe_prompt = f"""[SYSTEM MESSAGE]
{system_prompt}

[USER QUERY]
{sanitized_query}

[RESPONSE]
Please provide a helpful and safe response:"""
    
    return safe_prompt

# Export public functions
__all__ = [
    'validate_and_sanitize',
    'log_blocked_command',
    'create_safe_ai_prompt',
    'SafetyFilter',
    'DANGEROUS_KEYWORDS',
]
