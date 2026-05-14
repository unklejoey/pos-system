"""
Helper functions for the POS system
"""
import os
import secrets
from datetime import datetime
from functools import wraps
from flask import redirect, url_for, flash
from flask_login import current_user
from werkzeug.utils import secure_filename
from PIL import Image
from app.models import Settings, db

def generate_transaction_id():
    """Generate unique transaction ID"""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_suffix = secrets.token_hex(3)
    return f'TXN{timestamp}{random_suffix}'

def allowed_file(filename, allowed_extensions={'png', 'jpg', 'jpeg', 'gif'}):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_picture(form_picture, upload_folder, size=(200, 200)):
    """Save and resize picture"""
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
    
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(upload_folder, picture_fn)
    
    img = Image.open(form_picture)
    img.thumbnail(size)
    img.save(picture_path)
    
    return picture_fn

def get_setting(key, default=None):
    """Get a setting value from database"""
    setting = Settings.query.filter_by(key=key).first()
    return setting.value if setting else default

def set_setting(key, value, description=''):
    """Set a setting value in database"""
    setting = Settings.query.filter_by(key=key).first()
    if setting:
        setting.value = value
    else:
        setting = Settings(key=key, value=value, description=description)
        db.session.add(setting)
    db.session.commit()
    return setting

def format_currency(amount, currency_symbol='GHS'):
    """Format amount as Ghana Cedis currency"""
    try:
        return f"{currency_symbol} {float(amount):.2f}"
    except (ValueError, TypeError):
        return f"{currency_symbol} 0.00"

def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You need to log in first.', 'warning')
            return redirect(url_for('auth.login'))
        if current_user.role != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function

def manager_required(f):
    """Decorator to require manager or admin role"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('You need to log in first.', 'warning')
            return redirect(url_for('auth.login'))
        if current_user.role not in ['admin', 'manager']:
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('dashboard.index'))
        return f(*args, **kwargs)
    return decorated_function
