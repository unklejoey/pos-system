"""
Sales (POS) routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models import db, Product, Sale, SaleItem, Category
from app.utils import generate_transaction_id, get_setting
from decimal import Decimal
import json


sales_bp = Blueprint('sales', __name__, url_prefix='/sales')

@sales_bp.route('/pos', methods=['GET'])
@login_required
def pos():
    """POS sales screen"""
    categories = Category.query.all()
    return render_template(
        'sales/pos.html',
        categories=categories,
        currency_symbol=get_setting('currency_symbol', 'GHS'),
        subtotal=0,
        total=0,
        tax=0,
        discount=0,
        cash_received=0,
        change=0
    )


@sales_bp.route('/checkout', methods=['GET', 'POST'])
@login_required
def checkout():
    """Process sale checkout"""
    if request.method == 'POST':
        data = request.get_json()
        
        items = data.get('items', [])
        discount = float(data.get('discount', 0))
        tax = float(data.get('tax', 0))
        cash_received = float(data.get('cash_received', 0))
        payment_method = data.get('payment_method', 'cash')
        notes = data.get('notes', '')
        
        # Validation
        if not items:
            return jsonify({'success': False, 'message': 'Cart is empty'}), 400
        
        try:
            validated_items = []
            subtotal = 0

            for item in items:
                product_id = item.get('product_id')
                quantity = int(item.get('quantity', 0))

                product = Product.query.get(product_id)
                if not product or not product.is_active:
                    return jsonify({'success': False, 'message': 'Product not found'}), 400

                if quantity <= 0:
                    return jsonify({'success': False, 'message': f'Invalid quantity for {product.name}'}), 400

                if product.stock_quantity < quantity:
                    return jsonify({'success': False, 'message': f'Insufficient stock for {product.name}'}), 400

                unit_price = round(float(product.selling_price), 2)
                total_price = round(unit_price * quantity, 2)
                subtotal = round(subtotal + total_price, 2)
                validated_items.append((product, quantity, unit_price, total_price))

            discount = max(0, round(discount, 2))
            tax = max(0, round(tax, 2))
            total = round(subtotal - discount + tax, 2)

            if total < 0:
                return jsonify({'success': False, 'message': 'Discount cannot exceed sale total'}), 400

            if cash_received < total:
                return jsonify({'success': False, 'message': 'Insufficient payment'}), 400

            # Create sale record
            transaction_id = generate_transaction_id()
            change = round(cash_received - total, 2)
            
            sale = Sale(
                transaction_id=transaction_id,
                user_id=current_user.id,
                subtotal=subtotal,
                discount=discount,
                tax=tax,
                total=total,
                cash_received=cash_received,
                change=change,
                payment_method=payment_method,
                notes=notes
            )
            db.session.add(sale)
            db.session.flush()  # Get the sale ID
            
            # Add items and reduce stock
            for product, quantity, unit_price, total_price in validated_items:
                # Reduce stock
                product.stock_quantity -= quantity
                
                # Create sale item record
                sale_item = SaleItem(
                    sale_id=sale.id,
                    product_id=product_id,
                    quantity=quantity,
                    unit_price=unit_price,
                    total_price=total_price
                )
                db.session.add(sale_item)
            
            db.session.commit()
            
            return jsonify({
                'success': True,
                'message': 'Sale completed successfully',
                'transaction_id': transaction_id,
                'receipt_url': url_for('sales.receipt', sale_id=sale.id)
            })
            
        except Exception as e:
            db.session.rollback()
            return jsonify({'success': False, 'message': str(e)}), 500

@sales_bp.route('/receipt/<int:sale_id>', methods=['GET'])
@login_required
def receipt(sale_id):
    """View receipt"""
    sale = Sale.query.get_or_404(sale_id)
    return render_template('sales/receipt.html', sale=sale)

@sales_bp.route('/receipt/<int:sale_id>/print', methods=['GET'])
@login_required
def print_receipt(sale_id):
    """Print receipt (thermal style)"""
    sale = Sale.query.get_or_404(sale_id)
    auto_print = request.args.get('auto_print') == '1'
    return render_template('sales/receipt_print.html', sale=sale, auto_print=auto_print)
