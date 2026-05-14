#!/usr/bin/env python
"""
Main entry point for the POS application
"""

import os
from app import create_app, db
from app.models import User, Category, Product, Sale, SaleItem, Settings


# Create app using environment config
app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Create shell context for Flask CLI"""
    return {
        'db': db,
        'User': User,
        'Category': Category,
        'Product': Product,
        'Sale': Sale,
        'SaleItem': SaleItem,
        'Settings': Settings
    }


# =========================
# INIT DATA (ONLY RUN ON STARTUP)
# =========================
with app.app_context():

    # =========================
    # CREATE UPLOAD FOLDER
    # =========================
    upload_folder = app.config.get('UPLOAD_FOLDER')
    if upload_folder and not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    # =========================
    # INITIALIZE DATABASE
    # =========================
    db.create_all()

    # =========================
    # CREATE DEFAULT ADMIN USER
    # =========================
    if not User.query.filter_by(username='admin').first():
        admin = User(
            username='admin',
            email='admin@pos.local',
            full_name='Administrator',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)

    # Owner account
    if not User.query.filter_by(username='sandra').first():
        owner = User(
            username='sandra',
            email='owner@pos.local',
            full_name='Sandra',
            role='admin',
            is_active=True
        )
        owner.set_password('Owner123')
        db.session.add(owner)

    # Cashier account
    if not User.query.filter_by(username='cashier1').first():
        cashier = User(
            username='cashier1',
            email='cashier@pos.local',
            full_name='Main Cashier',
            role='cashier',
            is_active=True
        )
        cashier.set_password('Cash123')
        db.session.add(cashier)

    # =========================
    # DEFAULT SETTINGS
    # =========================
    if not Settings.query.first():
        settings_data = [
            Settings(
                key='store_name',
                value='My Store',
                description='Store name'
            ),
            Settings(
                key='currency_symbol',
                value='₵',
                description='Currency symbol'
            ),
            Settings(
                key='currency_code',
                value='GHS',
                description='Currency code'
            ),
            Settings(
                key='tax_rate',
                value='0',
                description='Default tax rate'
            ),
            Settings(
                key='receipt_footer',
                value='Thank you for your purchase!',
                description='Receipt footer text'
            ),
        ]

        for setting in settings_data:
            db.session.add(setting)

    db.session.commit()

    print('✓ Default users created')
    print('✓ Default settings initialized (GHS ₵ enabled)')


# =========================
# RUN APP (LOCAL ONLY)
# =========================
if __name__ == '__main__':
    app.run(
        debug=app.config.get('DEBUG', False),
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000))
    )
