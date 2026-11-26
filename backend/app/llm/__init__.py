"""app/llm/__init__.py — LLM layer exports."""
from .router import ModelRouter, global_router

__all__ = ["ModelRouter", "global_router"]
