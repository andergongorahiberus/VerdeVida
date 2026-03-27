"""Verde Vida Nursery Agent — customer service agent for the LLMOps course."""

from __future__ import annotations

from verde_vida_agent.agent import create_agent
from verde_vida_agent.config import SYSTEM_PROMPT, load_catalog, load_faqs
from verde_vida_agent.tools import get_faq_answer, search_catalog

__version__ = "0.1.0"
__all__ = [
    "SYSTEM_PROMPT",
    "create_agent",
    "get_faq_answer",
    "load_catalog",
    "load_faqs",
    "search_catalog",
]
