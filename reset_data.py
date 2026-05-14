from app import create_app, db
from app.models import Product, Category, Sale, SaleItem

app = create_app()

def reset_data():
    with app.app_context():

        print("RESETTING BUSINESS DATA...")

        # delete in correct order
        SaleItem.query.delete()
        Sale.query.delete()
        Product.query.delete()
        Category.query.delete()

        db.session.commit()

        print("✅ Business data cleared successfully")

reset_data()
