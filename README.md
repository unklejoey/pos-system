# Modern POS System

A lightweight, responsive Point of Sale (POS) system built with Python Flask, SQLite, and Bootstrap 5. Perfect for small businesses, shops, and supermarkets.

## Features

### ✅ Core Features
- **Admin Authentication** - Secure login with session management
- **Dashboard** - Real-time sales analytics and key metrics
- **Product Management** - Add, edit, delete products with images
- **Category Management** - Organize products by categories
- **POS Sales Screen** - Fast, responsive checkout interface
- **Inventory Management** - Track stock levels with low-stock alerts
- **Sales History** - Complete transaction records with filtering
- **Receipt System** - Printable thermal-style receipts
- **Settings Management** - Configure store name, logo, and defaults

### 🎨 User Interface
- Modern, clean design inspired by SaaS dashboards
- Mobile-responsive layout
- Fast AJAX-based cart updates
- Real-time search with autocomplete
- Soft shadows and rounded cards
- Smooth animations and transitions

### 🛠️ Technical Features
- **Backend**: Flask with SQLAlchemy ORM
- **Database**: SQLite with proper migrations
- **Frontend**: HTML5, CSS3, JavaScript ES6+
- **Architecture**: MVC-style with Blueprints
- **Security**: Password hashing, session handling
- **Performance**: Optimized queries and caching

## System Requirements

- Python 3.7 or higher
- pip (Python package manager)
- Modern web browser

## Installation & Setup

### 1. Clone or Download the Project

```bash
cd pos-system
```

### 2. Create Virtual Environment

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Initialize Database

```bash
python run.py
```

The application will:
- Create the SQLite database
- Initialize all tables
- Create a default admin user

### 5. Start the Application

```bash
python run.py
```

Open your browser and navigate to:
```
http://localhost:5000
```

## Default Login Credentials

- **Username**: `admin`
- **Password**: `admin123`

⚠️ **Important**: Change the default password immediately after first login!

## Project Structure

```
pos-system/
├── app/
│   ├── __init__.py           # Flask app factory
│   ├── config.py             # Configuration settings
│   ├── models/
│   │   └── __init__.py       # Database models
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py           # Authentication
│   │   ├── dashboard.py      # Dashboard
│   │   ├── products.py       # Product management
│   │   ├── sales.py          # Sales/POS
│   │   ├── inventory.py      # Inventory
│   │   ├── history.py        # Sales history
│   │   ├── settings.py       # Settings
│   │   └── api.py            # API endpoints
│   ├── templates/            # Jinja2 templates
│   │   ├── base.html
│   │   ├── auth/
│   │   ├── dashboard/
│   │   ├── products/
│   │   ├── sales/
│   │   ├── inventory/
│   │   ├── history/
│   │   └── settings/
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css
│   │   ├── js/
│   │   │   ├── main.js
│   │   │   └── pos.js
│   │   └── uploads/          # Product images
│   └── utils/
│       ├── __init__.py
│       └── helpers.py        # Helper functions
├── run.py                    # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## Usage Guide

### Dashboard
- View daily sales metrics
- Check low stock items
- See recent transactions
- Monitor stock value

### Product Management
- Add products with images, barcodes, and pricing
- Set cost and selling prices
- Configure stock quantities
- Create and manage categories
- Track profit margins

### POS Screen
1. Search for products by name or barcode
2. Click on a product card
3. Set quantity in the modal
4. Add to cart
5. Modify quantities or remove items
6. Enter cash received
7. Click "Complete Sale"
8. Print receipt if needed

### Inventory Management
- View all products with current stock
- Sort by low stock first
- Filter by category
- See stock value calculations
- Identify items needing reorder

### Sales History
- Filter transactions by date range
- Search by transaction ID
- View detailed receipts
- Export to CSV for accounting

### Settings
- Configure store name and logo
- Set default tax rate
- Customize currency symbol
- Add receipt footer text

## Keyboard Shortcuts

| Key | Action |
|-----|--------|
| `Ctrl+F` | Focus search |
| `Enter` | Add to cart |
| `Escape` | Clear search |
| `Ctrl+P` | Print receipt |

## Database Models

### User
- Admin, Manager, Cashier roles
- Secure password hashing

### Product
- Barcode support
- Category assignment
- Cost and selling prices
- Stock quantity tracking
- Image upload

### Sale
- Transaction ID
- Subtotal, discount, tax, total
- Payment method
- Cash received and change
- Timestamp

### Category
- Product organization
- Product count tracking

### Settings
- Key-value store for configuration
- Store name, logo, tax rate, etc.

## API Endpoints

### Products
- `GET /api/products/search` - Search products
- `GET /api/products/<id>` - Get product details

### Categories
- `GET /api/categories` - Get all categories

### Statistics
- `GET /api/stats/low-stock` - Low stock count

### Validation
- `POST /api/validate-barcode` - Check barcode uniqueness

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection (Flask-WTF)
- SQL injection prevention (SQLAlchemy ORM)
- Input validation on forms
- Secure file upload handling

## Deployment

### Local Network Access

To access from other computers on your network:

```bash
python run.py
```

Then access from another machine using:
```
http://YOUR_IP:5000
```

### Production Deployment

For production, consider:

1. Use a production WSGI server (Gunicorn, Waitress)
2. Set `DEBUG = False` in config
3. Use environment variables for secrets
4. Set `SESSION_COOKIE_SECURE = True`
5. Configure HTTPS/SSL
6. Use PostgreSQL instead of SQLite
7. Implement proper backup strategy

Example with Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# macOS/Linux
lsof -i :5000
kill -9 <PID>
```

### Database Errors
Delete `pos_system.db` to reset:
```bash
rm pos_system.db
python run.py
```

### Module Import Errors
Reinstall dependencies:
```bash
pip install -r requirements.txt --force-reinstall
```

## Future Enhancements

- [ ] Multi-language support
- [ ] Dark mode toggle
- [ ] Barcode scanner integration
- [ ] Customer loyalty program
- [ ] Advanced reporting
- [ ] Invoice generation
- [ ] Employee management
- [ ] Real-time sync
- [ ] Mobile app
- [ ] Payment gateway integration

## File Size & Performance

- Database: ~50MB (typical)
- Images: Optimized to 200x200px
- Load time: <2 seconds average
- Supports 10,000+ products
- Suitable for single-location shops

## Browser Support

- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Responsive on tablets

## Keyboard Shortcuts (POS Screen)

- `Ctrl+L` - Clear cart
- `Ctrl+S` - Complete sale
- `Escape` - Clear search focus

## License

Open source for educational and commercial use.

## Support & Contributing

For issues, suggestions, or improvements, please refer to the documentation or contact support.

## Version

**v1.0.0** - Initial Release

---

**Built with ❤️ for small businesses**

Happy selling!
