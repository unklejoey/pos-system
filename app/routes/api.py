"""
API endpoints for AJAX calls
"""
from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from app.models import db, Product, Category
from sqlalchemy import func

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/products/search', methods=['GET'])
@login_required
def search_products():
    """Search products by name or barcode"""
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', None)
    
    if not query:
        return jsonify({'products': []})
    
    products_query = Product.query.filter(
        Product.is_active == True,
        (
            (Product.name.ilike(f'%{query}%')) |
            (Product.barcode.ilike(f'%{query}%'))
        )
    )
    
    if category_id:
        products_query = products_query.filter_by(category_id=category_id)
    
    products = products_query.limit(20).all()
    
    return jsonify({
        'products': [
            {
                'id': p.id,
                'name': p.name,
                'barcode': p.barcode,
                'price': p.selling_price,
                'stock': p.stock_quantity,
                'image': f'/static/uploads/{p.image}' if p.image else '/static/img/placeholder.png'
            }
            for p in products
        ]
    })

@api_bp.route('/products/<int:product_id>', methods=['GET'])
@login_required
def get_product(product_id):
    """Get product details"""
    product = Product.query.get_or_404(product_id)
    
    return jsonify({
        'id': product.id,
        'name': product.name,
        'barcode': product.barcode,
        'price': product.selling_price,
        'stock': product.stock_quantity,
        'category': product.category.name,
        'image': f'/static/uploads/{product.image}' if product.image else '/static/img/placeholder.png'
    })

@api_bp.route('/categories', methods=['GET'])
@login_required
def get_categories():
    """Get all categories"""
    categories = Category.query.all()
    return jsonify({
        'categories': [
            {'id': c.id, 'name': c.name}
            for c in categories
        ]
    })

@api_bp.route('/stats/low-stock', methods=['GET'])
@login_required
def low_stock_stats():
    """Get low stock products count"""
    low_stock = Product.query.filter(
        Product.stock_quantity <= Product.low_stock_threshold
    ).count()
    return jsonify({'low_stock': low_stock})

@api_bp.route('/validate-barcode', methods=['POST'])
@login_required
def validate_barcode():
    """Check if barcode exists"""
    barcode = request.json.get('barcode', '')
    product = Product.query.filter_by(barcode=barcode).first()
    return jsonify({'exists': product is not None})
