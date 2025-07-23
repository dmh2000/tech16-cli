"""System prompt strings for different command types."""

from typing import Dict

system_query = "system_query"
system_code = "system_code"
system_plan = "system_plan"
system_review = "system_review"

SYSTEM_PROMPTS: Dict[str, str] = {
    "query": system_query,
    "code": system_code,
    "plan": system_plan,
    "review": system_review,
}


def get_system_prompt(command_type: str) -> str:
    """
    Get the system prompt for a given command type.
    
    Args:
        command_type: The command type (query, code, plan, review)
        
    Returns:
        str: The system prompt string
        
    Raises:
        KeyError: If the command type is not supported
    """
    if command_type not in SYSTEM_PROMPTS:
        raise KeyError(f"Unknown command type: {command_type}")
    
    return SYSTEM_PROMPTS[command_type]