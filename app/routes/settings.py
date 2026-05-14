"""
Settings management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from app.models import db, Settings
from app.utils import admin_required, get_setting, set_setting, save_picture, allowed_file
import os

settings_bp = Blueprint('settings', __name__, url_prefix='/settings')

@settings_bp.route('/', methods=['GET', 'POST'])
@login_required
@admin_required
def index():
    """Settings page"""
    if request.method == 'POST':
        store_name = request.form.get('store_name')
        currency_symbol = request.form.get('currency_symbol', '$')
        tax_rate = request.form.get('tax_rate', type=float, default=0)
        receipt_footer = request.form.get('receipt_footer')
        
        set_setting('store_name', store_name, 'Store name displayed on receipts')
        set_setting('currency_symbol', currency_symbol, 'Currency symbol for display')
        set_setting('tax_rate', str(tax_rate), 'Default tax rate as percentage')
        set_setting('receipt_footer', receipt_footer, 'Footer text on receipts')
        
        # Handle logo upload
        if 'logo' in request.files:
            file = request.files['logo']
            if file and file.filename and allowed_file(file.filename):
                upload_folder = os.path.join(os.path.dirname(__file__), 
                                            '../static/uploads')
                logo_file = save_picture(file, upload_folder)
                set_setting('store_logo', logo_file, 'Store logo for receipts')
        
        flash('Settings updated successfully!', 'success')
        return redirect(url_for('settings.index'))
    
    store_name = get_setting('store_name', 'My Store')
    currency_symbol = get_setting('currency_symbol', '$')
    tax_rate = get_setting('tax_rate', '0')
    receipt_footer = get_setting('receipt_footer', 'Thank you for your purchase!')
    store_logo = get_setting('store_logo')
    
    return render_template('settings/index.html',
                         store_name=store_name,
                         currency_symbol=currency_symbol,
                         tax_rate=tax_rate,
                         receipt_footer=receipt_footer,
                         store_logo=store_logo)
