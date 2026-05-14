# Installation & Setup Guide

## System Requirements

- **Python**: 3.7 or higher
- **RAM**: 512MB minimum
- **Disk Space**: 100MB minimum
- **Browser**: Chrome, Firefox, Safari, or Edge (latest versions)
- **OS**: Windows, macOS, Linux

## Step-by-Step Installation

### 1. Download/Clone the Project

```bash
# Navigate to your projects folder
cd ~/projects
# or
cd C:\Users\YourName\Documents
```

### 2. Create Python Virtual Environment

Virtual environment isolates project dependencies:

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### 3. Install Python Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Wait for installation to complete (2-3 minutes).

### 4. Initialize the Application

```bash
python run.py
```

**First run will:**
- Create `pos_system.db` database
- Create all tables
- Create default admin user
- Display confirmation messages

### 5. Access the Application

Open your web browser and go to:
```
http://localhost:5000
```

### 6. Login

**Default Credentials:**
- Username: `admin`
- Password: `admin123`

⚠️ **IMPORTANT**: Change password after first login!

## Optional: Load Sample Data

To populate database with sample products and users:

```bash
python seed_data.py
```

This adds:
- 30+ sample products
- 6 product categories
- Additional test users (cashier, manager)
- Ready-to-use inventory

**Sample Users:**
- admin / admin123
- cashier1 / password123
- cashier2 / password123
- manager / password123

## Configuration

### Environment Variables

Create `.env` file in project root:

```env
FLASK_ENV=development
FLASK_APP=run.py
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///pos_system.db
```

See `.env.example` for template.

### Application Config

Edit `app/config.py` to customize:
- Debug mode
- Upload folder location
- Session timeout
- Pagination settings
- File upload size limits

## Troubleshooting

### Issue: Python Not Found

```bash
# Check Python version
python --version
# or
python3 --version

# Windows: Use Python from Microsoft Store or python.org
# macOS: brew install python3
# Linux: sudo apt-get install python3
```

### Issue: Port 5000 Already in Use

**Windows:**
```bash
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**macOS/Linux:**
```bash
lsof -i :5000
kill -9 <PID>
```

Or change port in `run.py`:
```python
app.run(host='0.0.0.0', port=8000)  # Use 8000 instead
```

### Issue: Module Import Errors

```bash
# Ensure virtual environment is activated
# Check for (venv) in terminal prompt

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# Verify installation
pip list
```

### Issue: Database Errors

```bash
# Delete and recreate database
rm pos_system.db
# or on Windows: del pos_system.db

# Reinitialize
python run.py
```

### Issue: Permission Denied on Linux/macOS

```bash
chmod +x run.py
chmod -R 755 app/static/uploads
```

## Project Structure

```
pos-system/
├── app/
│   ├── __init__.py              # Flask factory
│   ├── config.py                # Configuration
│   │
│   ├── models/
│   │   └── __init__.py          # DB Models
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py              # Login/Logout
│   │   ├── dashboard.py         # Dashboard
│   │   ├── products.py          # Products CRUD
│   │   ├── sales.py             # POS Sales
│   │   ├── inventory.py         # Stock Management
│   │   ├── history.py           # Transactions
│   │   ├── settings.py          # Settings
│   │   └── api.py               # API Endpoints
│   │
│   ├── templates/               # HTML Templates
│   │   ├── base.html
│   │   ├── auth/
│   │   │   └── login.html
│   │   ├── dashboard/
│   │   │   └── index.html
│   │   ├── products/
│   │   │   ├── index.html
│   │   │   ├── add.html
│   │   │   ├── edit.html
│   │   │   └── categories.html
│   │   ├── sales/
│   │   │   ├── pos.html
│   │   │   ├── receipt.html
│   │   │   └── receipt_print.html
│   │   ├── inventory/
│   │   │   └── index.html
│   │   ├── history/
│   │   │   └── index.html
│   │   └── settings/
│   │       └── index.html
│   │
│   ├── static/
│   │   ├── css/
│   │   │   └── style.css        # Main styles
│   │   ├── js/
│   │   │   ├── main.js          # Utilities
│   │   │   └── pos.js           # POS logic
│   │   └── uploads/             # Product images
│   │
│   └── utils/
│       ├── __init__.py
│       └── helpers.py           # Helper functions
│
├── run.py                       # Entry point
├── requirements.txt             # Dependencies
├── seed_data.py                # Sample data
├── QUICKSTART.py               # Quick start
├── .env.example                # Env template
├── .gitignore                  # Git ignore
└── README.md                   # Documentation
```

## Starting the Application

### Development Mode
```bash
python run.py
```

Server runs on `http://localhost:5000`

### Production Mode (Local Network)

Edit `run.py`:
```python
if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0', port=5000)
```

Access from other computers:
```
http://YOUR_COMPUTER_IP:5000
```

Find your IP:
```bash
# Windows
ipconfig

# macOS/Linux
ifconfig
```

### Production Deployment

For public deployment, use Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

## Database

### SQLite (Default)

File-based database (`pos_system.db`):
- No server required
- Suitable for small to medium businesses
- Easy backup (copy file)

### Backup Database

```bash
# Simple copy
cp pos_system.db pos_system.db.backup

# Or use tar
tar -czf pos_system.db.$(date +%Y%m%d).tar.gz pos_system.db
```

### Restore Database

```bash
cp pos_system.db.backup pos_system.db
```

## First Run Checklist

- [ ] Python installed and virtual environment activated
- [ ] Dependencies installed (`pip list` shows Flask, SQLAlchemy, etc.)
- [ ] Application starts without errors (`python run.py`)
- [ ] Can access dashboard at `http://localhost:5000`
- [ ] Can login with admin/admin123
- [ ] Settings page loads correctly
- [ ] Can add a product
- [ ] Can access POS screen
- [ ] Can perform test transaction

## Security Setup for Production

### 1. Change Secret Key

Edit `app/config.py`:
```python
SECRET_KEY = os.environ.get('SECRET_KEY') or 'very-secure-random-key-here'
```

### 2. Environment Variables

Create `.env`:
```env
FLASK_ENV=production
SECRET_KEY=your-super-secure-key
```

### 3. Enable HTTPS

- Use Let's Encrypt for free SSL
- Configure reverse proxy (Nginx)
- Set `SESSION_COOKIE_SECURE = True`

### 4. Database Security

- Use PostgreSQL for production
- Regular backups
- Strong database password

### 5. File Permissions

```bash
chmod 600 pos_system.db
chmod 755 app/
chmod -R 755 app/static/
```

## Performance Optimization

### Database Queries
- Indexes automatically created on ForeignKeys
- Pagination set to 15 items per page
- Lazy loading for relationships

### Caching
- Browser caching enabled
- CSS/JS minification (Bootstrap CDN)
- Image optimization

### Load Testing

```bash
# With Apache Bench
ab -n 1000 -c 10 http://localhost:5000/

# With wrk
wrk -t4 -c100 -d30s http://localhost:5000/
```

## Maintenance

### Regular Tasks

- Daily: Check low stock alerts
- Weekly: Backup database
- Monthly: Review sales reports
- Quarterly: Update Python packages

### Updating Dependencies

```bash
pip list --outdated
pip install --upgrade package-name
```

### Monitoring

Check server logs:
```bash
# Gunicorn logs
journalctl -u gunicorn

# Application logs
tail -f app.log
```

## Support & Help

1. Read README.md for feature overview
2. Check inline code comments
3. Review error messages in browser console (F12)
4. Check application logs
5. Ensure database integrity

## Next Steps

1. ✅ Complete installation
2. ✅ Load sample data
3. ✅ Explore dashboard
4. ✅ Configure store settings
5. ✅ Add your products
6. ✅ Test POS screen
7. ✅ Train staff
8. ✅ Deploy to production

Happy selling! 🎉
