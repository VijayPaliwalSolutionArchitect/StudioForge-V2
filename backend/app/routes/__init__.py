"""app/routes/__init__.py — API route exports."""
from .brands import router as brands_router
from .campaigns import router as campaigns_router
from .briefs import router as briefs_router
from .assets import router as assets_router
from .calendar import router as calendar_router
from .approvals import router as approvals_router
from .admin import router as admin_router

__all__ = [
    "brands_router",
    "campaigns_router",
    "briefs_router",
    "assets_router",
    "calendar_router",
    "approvals_router",
    "admin_router",
]
