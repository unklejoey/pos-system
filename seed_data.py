"""
Seed data script for POS system
Run this to populate the database with sample data
"""
import os
import sys
from app import create_app, db
from app.models import User, Category, Product, Settings

def seed_database():
    """Populate database with sample data"""
    
    app = create_app()
    
    with app.app_context():
        # Check if data already exists
        if Category.query.first():
            print("Database already has data. Skipping seed.")
            return
        
        print("Seeding database...")
        
        # Create categories
        categories = [
            Category(name='Beverages', description='Soft drinks, juices, water'),
            Category(name='Snacks', description='Chips, cookies, candy'),
            Category(name='Dairy', description='Milk, cheese, yogurt'),
            Category(name='Bakery', description='Bread, pastries, cakes'),
            Category(name='Frozen Foods', description='Ice cream, frozen meals'),
            Category(name='Household', description='Cleaning supplies, toiletries'),
        ]
        
        for category in categories:
            db.session.add(category)
        
        db.session.commit()
        print(f"✓ Created {len(categories)} categories")
        
        # Create products
        products_data = [
            # Beverages
            ('Coca Cola 500ml', 'Beverages', '5001234500001', 0.75, 1.99, 100),
            ('Sprite 500ml', 'Beverages', '5001234500002', 0.75, 1.99, 95),
            ('Orange Juice 1L', 'Beverages', '5001234500003', 1.50, 3.99, 50),
            ('Mineral Water 1L', 'Beverages', '5001234500004', 0.30, 0.99, 200),
            ('Iced Tea 500ml', 'Beverages', '5001234500005', 0.50, 1.49, 80),
            
            # Snacks
            ('Lay\'s Chips 50g', 'Snacks', '5001234600001', 0.40, 1.29, 150),
            ('Doritos 50g', 'Snacks', '5001234600002', 0.45, 1.49, 130),
            ('Pringles 100g', 'Snacks', '5001234600003', 0.90, 2.49, 100),
            ('Oreo Cookies 100g', 'Snacks', '5001234600004', 0.80, 2.29, 120),
            ('Candy Mix Pack', 'Snacks', '5001234600005', 1.50, 3.99, 80),
            
            # Dairy
            ('Milk 1L', 'Dairy', '5001234700001', 1.20, 2.99, 100),
            ('Cheese 200g', 'Dairy', '5001234700002', 2.50, 5.99, 60),
            ('Yogurt 500g', 'Dairy', '5001234700003', 1.80, 3.99, 75),
            ('Butter 200g', 'Dairy', '5001234700004', 2.00, 4.99, 50),
            ('Cream 250ml', 'Dairy', '5001234700005', 1.50, 3.49, 40),
            
            # Bakery
            ('Bread Loaf 500g', 'Bakery', '5001234800001', 1.00, 2.49, 80),
            ('Croissant Pack', 'Bakery', '5001234800002', 1.50, 3.99, 60),
            ('Donuts 6 Pack', 'Bakery', '5001234800003', 1.80, 4.99, 50),
            ('Cake Slice', 'Bakery', '5001234800004', 2.00, 4.99, 40),
            ('Muffins 4 Pack', 'Bakery', '5001234800005', 1.60, 3.99, 55),
            
            # Frozen Foods
            ('Ice Cream 500ml', 'Frozen Foods', '5001234900001', 2.50, 5.99, 100),
            ('Frozen Pizza', 'Frozen Foods', '5001234900002', 3.50, 7.99, 45),
            ('Frozen Vegetables 500g', 'Frozen Foods', '5001234900003', 1.50, 3.49, 70),
            ('Frozen Fries 500g', 'Frozen Foods', '5001234900004', 1.20, 2.99, 90),
            ('Frozen Chicken 1kg', 'Frozen Foods', '5001234900005', 4.00, 8.99, 60),
            
            # Household
            ('Dish Soap 500ml', 'Household', '5001235000001', 0.80, 1.99, 100),
            ('Laundry Detergent 1L', 'Household', '5001235000002', 1.50, 3.99, 80),
            ('Toilet Paper 4 Pack', 'Household', '5001235000003', 1.20, 2.99, 150),
            ('Paper Towels 2 Pack', 'Household', '5001235000004', 1.00, 2.49, 120),
            ('Trash Bags 20 Pack', 'Household', '5001235000005', 1.50, 3.49, 100),
        ]
        
        for name, category_name, barcode, cost, price, stock in products_data:
            category = Category.query.filter_by(name=category_name).first()
            product = Product(
                name=name,
                barcode=barcode,
                category_id=category.id,
                cost_price=cost,
                selling_price=price,
                stock_quantity=stock,
                low_stock_threshold=10,
                is_active=True
            )
            db.session.add(product)
        
        db.session.commit()
        print(f"✓ Created {len(products_data)} products")
        
        # Create additional users
        users_data = [
            ('cashier1', 'Cashier', 'John Smith', 'cashier1@pos.local'),
            ('cashier2', 'Cashier', 'Jane Doe', 'cashier2@pos.local'),
            ('manager', 'Manager', 'Mike Johnson', 'manager@pos.local'),
        ]
        
        for username, role, full_name, email in users_data:
            if not User.query.filter_by(username=username).first():
                user = User(
                    username=username,
                    email=email,
                    full_name=full_name,
                    role=role.lower(),
                    is_active=True
                )
                user.set_password('password123')  # Default password
                db.session.add(user)
        
        db.session.commit()
        print("✓ Created additional users")
        
        print("\n✅ Database seeded successfully!")
        print("\nSample Users Created:")
        print("  Admin: admin / admin123")
        print("  Cashier: cashier1 / password123")
        print("  Cashier: cashier2 / password123")
        print("  Manager: manager / password123")
        print("\n⚠️  Change all passwords in production!")

if __name__ == '__main__':
    seed_database()
