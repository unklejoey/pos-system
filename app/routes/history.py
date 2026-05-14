"""
Sales history and reports routes
"""
from flask import Blueprint, render_template, request, jsonify, send_file
from flask_login import login_required
from app.models import Sale, SaleItem, Product
from datetime import datetime, timedelta
import csv
import io

history_bp = Blueprint('history', __name__, url_prefix='/history')

@history_bp.route('/', methods=['GET'])
@login_required
def index():
    """Sales history"""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = Sale.query
    
    if search:
        query = query.filter(Sale.transaction_id.ilike(f'%{search}%'))
    
    if date_from:
        date_obj = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(Sale.created_at >= date_obj)
    
    if date_to:
        date_obj = datetime.strptime(date_to, '%Y-%m-%d')
        date_obj = date_obj.replace(hour=23, minute=59, second=59)
        query = query.filter(Sale.created_at <= date_obj)
    
    sales = query.order_by(Sale.created_at.desc()).paginate(page=page, per_page=15)
    
    # Summary
    total_revenue = sum(s.get_calculated_total() for s in query.all())
    total_transactions = query.count()
    
    return render_template('history/index.html',
                         sales=sales,
                         search=search,
                         date_from=date_from,
                         date_to=date_to,
                         total_revenue=total_revenue,
                         total_transactions=total_transactions)

@history_bp.route('/export', methods=['GET'])
@login_required
def export_csv():
    """Export sales to CSV"""
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    
    query = Sale.query
    
    if date_from:
        date_obj = datetime.strptime(date_from, '%Y-%m-%d')
        query = query.filter(Sale.created_at >= date_obj)
    
    if date_to:
        date_obj = datetime.strptime(date_to, '%Y-%m-%d')
        date_obj = date_obj.replace(hour=23, minute=59, second=59)
        query = query.filter(Sale.created_at <= date_obj)
    
    sales = query.order_by(Sale.created_at.desc()).all()
    
    # Create CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Transaction ID', 'Date', 'Time', 'Subtotal', 'Discount', 'Tax', 'Total', 'Payment Method', 'Cashier'])
    
    for sale in sales:
        writer.writerow([
            sale.transaction_id,
            sale.created_at.strftime('%Y-%m-%d'),
            sale.created_at.strftime('%H:%M:%S'),
            f'${sale.get_items_subtotal():.2f}',
            f'${sale.discount:.2f}',
            f'${sale.tax:.2f}',
            f'${sale.get_calculated_total():.2f}',
            sale.payment_method,
            sale.user.full_name or sale.user.username
        ])
    
    output.seek(0)
    return send_file(
        io.BytesIO(output.getvalue().encode()),
        mimetype='text/csv',
        as_attachment=True,
        download_name=f'sales_report_{datetime.now().strftime("%Y%m%d")}.csv'
    )
