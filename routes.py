"""Compatibility shim for older imports.

The route implementations now live in:
- auth_routes.py
- prediction_routes.py
- utility_routes.py
"""

from auth_routes import auth_bp
from prediction_routes import predictions_bp
from utility_routes import utility_bp

__all__ = ['auth_bp', 'predictions_bp', 'utility_bp']
