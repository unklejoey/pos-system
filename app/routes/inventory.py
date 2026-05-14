"""
Inventory management routes
"""
from flask import Blueprint, render_template, request
from flask_login import login_required
from app.models import Product, Category
from app.utils import manager_required

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/', methods=['GET'])
@login_required
@manager_required
def index():
    """Inventory management page"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', '')
    sort = request.args.get('sort', 'name')
    
    active_products = Product.query.filter_by(is_active=True)
    query = active_products
    
    if search:
        query = query.filter(
            (Product.name.ilike(f'%{search}%')) |
            (Product.barcode.ilike(f'%{search}%'))
        )
    
    if category:
        query = query.filter(Product.category_id == category)

    
    # Sorting
    if sort == 'stock':
        query = query.order_by(Product.stock_quantity.asc())
    elif sort == 'low':
        query = query.filter(Product.stock_quantity <= Product.low_stock_threshold)
    
    products = query.paginate(page=page, per_page=15)
    categories = Category.query.all()
    
    # Summary stats
    total_stock_value = sum(p.stock_quantity * p.cost_price for p in active_products.all())
    low_stock_count = active_products.filter(
        Product.stock_quantity <= Product.low_stock_threshold
    ).count()
    
    return render_template('inventory/index.html',
                         products=products,
                         categories=categories,
                         search=search,
                         selected_category=category,
                         sort=sort,
                         total_stock_value=total_stock_value,
                         low_stock_count=low_stock_count)
