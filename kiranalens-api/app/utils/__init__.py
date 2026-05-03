"""
Utility functions and helpers.

Note: Heavy dependencies (anthropic, httpx) are imported lazily so that
pure utility modules (economic_variables, sales_estimation, scoring) can
be imported in unit tests without requiring external API clients.
"""


def get_address_from_coordinates(*args, **kwargs):
    """Lazy-load geocoding to avoid pulling httpx into every import."""
    from app.utils.geocoding import get_address_from_coordinates as _fn
    return _fn(*args, **kwargs)


def process_assessment_images(*args, **kwargs):
    """Lazy-load AI processor to avoid pulling anthropic into every import."""
    from app.utils.ai_processor import process_assessment_images as _fn
    return _fn(*args, **kwargs)


__all__ = ["get_address_from_coordinates", "process_assessment_images"]