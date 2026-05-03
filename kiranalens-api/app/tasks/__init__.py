"""
Background tasks for async processing
"""
from app.tasks.assessment_processor import process_assessment_async

__all__ = ["process_assessment_async"]