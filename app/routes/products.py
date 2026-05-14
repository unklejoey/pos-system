"""
Product management routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, Product, Category, SaleItem
from app.utils import allowed_file, save_picture, admin_required, manager_required
import os

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
@login_required
def index():
    """List all products"""
    page = request.args.get('page', 1, type=int)
    category = request.args.get('category', None)
    search = request.args.get('search', '')
    
    query = Product.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            (Product.name.ilike(f'%{search}%')) |
            (Product.barcode.ilike(f'%{search}%'))
        )
    
    if category:
        query = query.filter_by(category_id=category)
    
    products = query.paginate(page=page, per_page=15)
    categories = Category.query.all()
    
    return render_template('products/index.html',
                         products=products,
                         categories=categories,
                         search=search,
                         selected_category=category)

@products_bp.route('/add', methods=['GET', 'POST'])
@login_required
@manager_required
def add():
    """Add new product"""
    if request.method == 'POST':
        name = request.form.get('name')
        barcode = request.form.get('barcode')
        category_id = request.form.get('category_id')
        cost_price = request.form.get('cost_price', type=float)
        selling_price = request.form.get('selling_price', type=float)
        stock_quantity = request.form.get('stock_quantity', type=int)
        low_stock_threshold = request.form.get('low_stock_threshold', type=int, default=5)
        description = request.form.get('description')
        
        # Validation
        if not all([name, category_id, cost_price, selling_price]):
            flash('Please fill in all required fields.', 'warning')
            return redirect(url_for('products.add'))
        
        if Product.query.filter_by(barcode=barcode).first() and barcode:
            flash('Barcode already exists.', 'warning')
            return redirect(url_for('products.add'))
        
        # Handle image upload
        image_file = None
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                upload_folder = os.path.join(os.path.dirname(__file__), 
                                            '../static/uploads')
                image_file = save_picture(file, upload_folder)
        
        product = Product(
            name=name,
            barcode=barcode,
            category_id=category_id,
            cost_price=cost_price,
            selling_price=selling_price,
            stock_quantity=stock_quantity or 0,
            low_stock_threshold=low_stock_threshold or 5,
            description=description,
            image=image_file
        )
        
        db.session.add(product)
        db.session.commit()
        
        flash(f'Product "{name}" added successfully!', 'success')
        return redirect(url_for('products.index'))
    
    categories = Category.query.all()
    return render_template('products/add.html', categories=categories)

@products_bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
@manager_required
def edit(product_id):
    """Edit product"""
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        product.name = request.form.get('name')
        product.barcode = request.form.get('barcode')
        product.category_id = request.form.get('category_id')
        product.cost_price = request.form.get('cost_price', type=float)
        product.selling_price = request.form.get('selling_price', type=float)
        product.stock_quantity = request.form.get('stock_quantity', type=int)
        product.low_stock_threshold = request.form.get('low_stock_threshold', type=int)
        product.description = request.form.get('description')
        
        # Handle image upload
        if 'image' in request.files:
            file = request.files['image']
            if file and file.filename and allowed_file(file.filename):
                upload_folder = os.path.join(os.path.dirname(__file__), 
                                            '../static/uploads')
                product.image = save_picture(file, upload_folder)
        
        db.session.commit()
        flash(f'Product "{product.name}" updated successfully!', 'success')
        return redirect(url_for('products.index'))
    
    categories = Category.query.all()
    return render_template('products/edit.html', product=product, categories=categories)

@products_bp.route('/<int:product_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete(product_id):
    """Delete product"""
    product = Product.query.get_or_404(product_id)
    name = product.name

    if SaleItem.query.filter_by(product_id=product.id).first():
        product.is_active = False
        flash(f'Product "{name}" has sales history, so it was deactivated instead of deleted.', 'info')
    else:
        db.session.delete(product)
        flash(f'Product "{name}" deleted successfully!', 'success')

    db.session.commit()
    return redirect(url_for('products.index'))

@products_bp.route('/categories', methods=['GET'])
@login_required
@manager_required
def categories():
    """Manage categories"""
    page = request.args.get('page', 1, type=int)
    cats = Category.query.paginate(page=page, per_page=15)
    return render_template('products/categories.html', categories=cats)

@products_bp.route('/categories/add', methods=['GET', 'POST'])
@login_required
@manager_required
def add_category():
    """Add category"""
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        
        if not name:
            flash('Category name is required.', 'warning')
            return redirect(url_for('products.add_category'))
        
        if Category.query.filter_by(name=name).first():
            flash('Category already exists.', 'warning')
            return redirect(url_for('products.add_category'))
        
        category = Category(name=name, description=description)
        db.session.add(category)
        db.session.commit()
        
        flash(f'Category "{name}" added successfully!', 'success')
        return redirect(url_for('products.categories'))
    
    return render_template('products/add_category.html')

@products_bp.route('/categories/<int:category_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_category(category_id):
    """Delete category"""
    category = Category.query.get_or_404(category_id)
    
    if category.products:
        flash('Cannot delete category with products.', 'warning')
        return redirect(url_for('products.categories'))
    
    name = category.name
    db.session.delete(category)
    db.session.commit()
    flash(f'Category "{name}" deleted successfully!', 'success')
    return redirect(url_for('products.categories'))
