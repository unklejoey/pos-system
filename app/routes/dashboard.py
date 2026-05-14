"""
Dashboard routes
"""
from flask import Blueprint, render_template
from flask_login import login_required
from datetime import datetime, timedelta
from app.models import db, Sale, Product, SaleItem, User
from sqlalchemy import func

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/')

@dashboard_bp.route('/', methods=['GET'])
@dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def index():
    """Display dashboard with analytics"""
    
    # Today's sales
    today = datetime.utcnow().date()
    today_sales = Sale.query.filter(
        func.date(Sale.created_at) == today
    ).all()
    
    today_revenue = sum(sale.get_calculated_total() for sale in today_sales)
    today_transactions = len(today_sales)
    today_items_sold = sum(sale.get_items_quantity() for sale in today_sales)
    
    # This week sales
    week_start = datetime.utcnow().date() - timedelta(days=7)
    week_sales = Sale.query.filter(
        func.date(Sale.created_at) >= week_start
    ).all()
    week_revenue = sum(sale.get_calculated_total() for sale in week_sales)
    
    # Product statistics
    active_products = Product.query.filter_by(is_active=True)
    total_products = active_products.count()
    low_stock_products = active_products.filter(
        Product.stock_quantity <= Product.low_stock_threshold
    ).all()
    total_stock_value = db.session.query(
        func.sum(Product.stock_quantity * Product.cost_price)
    ).filter(Product.is_active == True).scalar() or 0
    
    # Recent transactions (last 10)
    recent_sales = Sale.query.order_by(Sale.created_at.desc()).limit(10).all()
    
    # Staff count
    total_staff = User.query.count()
    
    return render_template('dashboard/index.html',
                         today_revenue=today_revenue,
                         today_transactions=today_transactions,
                         today_items_sold=today_items_sold,
                         week_revenue=week_revenue,
                         total_products=total_products,
                         low_stock_products=low_stock_products,
                         total_stock_value=total_stock_value,
                         recent_sales=recent_sales,
                         total_staff=total_staff)
