"""
Routes package initialization
"""
from app.routes.auth import auth_bp
from app.routes.dashboard import dashboard_bp
from app.routes.products import products_bp
from app.routes.sales import sales_bp
from app.routes.inventory import inventory_bp
from app.routes.history import history_bp
from app.routes.settings import settings_bp
from app.routes.api import api_bp

__all__ = [
    'auth_bp',
    'dashboard_bp',
    'products_bp',
    'sales_bp',
    'inventory_bp',
    'history_bp',
    'settings_bp',
    'api_bp'
]
