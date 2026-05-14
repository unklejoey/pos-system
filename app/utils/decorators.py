"""
Role-based access control decorators for POS system
"""

from functools import wraps
from flask import abort
from flask_login import current_user


def admin_required(f):
    """
    Restrict access to admin users only
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)

        if getattr(current_user, "role", None) != "admin":
            abort(403)

        return f(*args, **kwargs)

    return wrapper


def manager_required(f):
    """
    Allow admin and manager users only
    """
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)

        if getattr(current_user, "role", None) not in ["admin", "manager"]:
            abort(403)

        return f(*args, **kwargs)

    return wrapper