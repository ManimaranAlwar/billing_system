from app import app, db
from models import Category, Product, User, ShopSettings
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def init_categories():
    """Initialize all product categories"""
    categories = [
        {
            'name_ta': 'மளிகை பொருட்கள்',
            'name_en': 'Groceries',
            'icon': 'fas fa-shopping-basket',
            'color': '#2ecc71',
            'keywords': 'rice, wheat, oil, sugar, spices, dal, groceries, staples, அரிசி, எண்ணெய், சர்க்கரை, மசாலா'
        },
        {
            'name_ta': 'தின்பண்டங்கள்',
            'name_en': 'Snacks',
            'icon': 'fas fa-cookie-bite',
            'color': '#e67e22',
            'keywords': 'biscuits, chips, mixture, namkeen, noodles, snacks, பிஸ்கட், சிப்ஸ், நூடுல்ஸ்'
        },
        {
            'name_ta': 'பானங்கள்',
            'name_en': 'Beverages',
            'icon': 'fas fa-wine-bottle',
            'color': '#3498db',
            'keywords': 'soft drinks, juice, tea, coffee, milk, drinks, பானங்கள், டீ, காபி, ஜூஸ்'
        },
        {
            'name_ta': 'தனிப்பட்ட பராமரிப்பு',
            'name_en': 'Personal Care',
            'icon': 'fas fa-hand-sparkles',
            'color': '#e84393',
            'keywords': 'soap, shampoo, toothpaste, cream, lotion, hair oil, personal care, சோப், ஷாம்பு'
        },
        {
            'name_ta': 'வீட்டு பராமரிப்பு',
            'name_en': 'Household',
            'icon': 'fas fa-broom',
            'color': '#f1c40f',
            'keywords': 'detergent, cleaner, cleaning, household, வீட்டு பராமரிப்பு, டிடர்ஜெண்ட்'
        },
        {
            'name_ta': 'பால் பொருட்கள்',
            'name_en': 'Dairy',
            'icon': 'fas fa-cheese',
            'color': '#95a5a6',
            'keywords': 'milk, curd, butter, cheese, paneer, dairy, பால், தயிர், வெண்ணெய்'
        },
        {
            'name_ta': 'பழங்கள் & காய்கறிகள்',
            'name_en': 'Fruits & Vegetables',
            'icon': 'fas fa-apple-alt',
            'color': '#27ae60',
            'keywords': 'vegetables, fruits, fresh, produce, காய்கறிகள், பழங்கள்'
        },
        {
            'name_ta': 'இனிப்புகள் & சாக்லேட்',
            'name_en': 'Sweets & Chocolates',
            'icon': 'fas fa-candy-cane',
            'color': '#e84393',
            'keywords': 'chocolate, candy, sweets, ice cream, சாக்லேட், இனிப்புகள்'
        },
        {
            'name_ta': 'குழந்தை பராமரிப்பு',
            'name_en': 'Baby Care',
            'icon': 'fas fa-baby-carriage',
            'color': '#3498db',
            'keywords': 'baby food, diapers, baby care, குழந்தை பராமரிப்பு, டயப்பர்'
        },
        {
            'name_ta': 'செல்லப்பிராணி பொருட்கள்',
            'name_en': 'Pet Supplies',
            'icon': 'fas fa-paw',
            'color': '#f39c12',
            'keywords': 'pet food, pet care, dog food, cat food, செல்லப்பிராணி'
        },
        {
            'name_ta': 'அடிப்படை மருந்துகள்',
            'name_en': 'Health & OTC',
            'icon': 'fas fa-medkit',
            'color': '#e74c3c',
            'keywords': 'medicine, health, first aid, bandage, மருந்து, சுகாதாரம்'
        },
        {
            'name_ta': 'அன்றாட தேவைகள்',
            'name_en': 'Daily Essentials',
            'icon': 'fas fa-box-open',
            'color': '#7f8c8d',
            'keywords': 'matchbox, candles, batteries, tissues, essentials, தினசரி தேவைகள்'
        }
    ]
    
    for cat_data in categories:
        existing = Category.query.filter_by(name_en=cat_data['name_en']).first()
        if not existing:
            category = Category(**cat_data)
            db.session.add(category)
    
    db.session.commit()
    print("✅ Categories initialized successfully!")

def init_products():
    """Initialize sample products"""
    # Get category references
    groceries = Category.query.filter_by(name_en='Groceries').first()
    snacks = Category.query.filter_by(name_en='Snacks').first()
    beverages = Category.query.filter_by(name_en='Beverages').first()
    personal_care = Category.query.filter_by(name_en='Personal Care').first()
    household = Category.query.filter_by(name_en='Household').first()
    dairy = Category.query.filter_by(name_en='Dairy').first()
    
    products = [
        # Groceries
        {'name_ta': 'பாஸ்மதி அரிசி', 'name_en': 'Basmati Rice', 'price': 120.00, 'mrp': 130.00, 'unit': 'கிலோ', 
         'stock': 100, 'brand': 'India Gate', 'gst': 5, 'category': groceries},
        {'name_ta': 'சூரியகாந்தி எண்ணெய்', 'name_en': 'Sunflower Oil', 'price': 110.00, 'mrp': 120.00, 'unit': 'லிட்டர்',
         'stock': 50, 'brand': 'Fortune', 'gst': 5, 'category': groceries},
        {'name_ta': 'துவரம் பருப்பு', 'name_en': 'Toor Dal', 'price': 90.00, 'mrp': 95.00, 'unit': 'கிலோ',
         'stock': 80, 'brand': 'Local', 'gst': 5, 'category': groceries},
        {'name_ta': 'சர்க்கரை', 'name_en': 'Sugar', 'price': 45.00, 'mrp': 48.00, 'unit': 'கிலோ',
         'stock': 150, 'brand': 'Dhampure', 'gst': 5, 'category': groceries},
        
        # Snacks
        {'name_ta': 'குட் டே பிஸ்கட்', 'name_en': 'Good Day Biscuit', 'price': 25.00, 'mrp': 30.00, 'unit': 'பாக்கெட்',
         'stock': 200, 'brand': 'Britannia', 'gst': 12, 'category': snacks},
        {'name_ta': 'லேஸ் சிப்ஸ்', 'name_en': 'Lays Chips', 'price': 20.00, 'mrp': 20.00, 'unit': 'பாக்கெட்',
         'stock': 150, 'brand': 'PepsiCo', 'gst': 12, 'category': snacks},
        {'name_ta': 'முருக்கு', 'name_en': 'Murukku', 'price': 40.00, 'mrp': 45.00, 'unit': 'பாக்கெட்',
         'stock': 100, 'brand': 'Local', 'gst': 5, 'category': snacks},
        
        # Beverages
        {'name_ta': 'கோகோ கோலா', 'name_en': 'Coca Cola', 'price': 40.00, 'mrp': 40.00, 'unit': 'பாட்டில்',
         'stock': 120, 'brand': 'Coca Cola', 'gst': 12, 'category': beverages},
        {'name_ta': 'ரெட் லேபிள் டீ', 'name_en': 'Red Label Tea', 'price': 180.00, 'mrp': 200.00, 'unit': 'பாக்கெட்',
         'stock': 60, 'brand': 'Brooke Bond', 'gst': 5, 'category': beverages},
        
        # Personal Care
        {'name_ta': 'லக்ஸ் சோப்', 'name_en': 'Lux Soap', 'price': 35.00, 'mrp': 40.00, 'unit': 'பீஸ்',
         'stock': 150, 'brand': 'HUL', 'gst': 12, 'category': personal_care},
        {'name_ta': 'க்ளோஸ் அப் பற்பசை', 'name_en': 'Close Up Toothpaste', 'price': 65.00, 'mrp': 75.00, 'unit': 'பீஸ்',
         'stock': 100, 'brand': 'HUL', 'gst': 12, 'category': personal_care},
        
        # Household
        {'name_ta': 'சர்ஃப் எக்சல் டிடர்ஜெண்ட்', 'name_en': 'Surf Excel Detergent', 'price': 120.00, 'mrp': 130.00, 'unit': 'கிலோ',
         'stock': 80, 'brand': 'HUL', 'gst': 12, 'category': household},
        {'name_ta': 'விம் டிஷ் வாஷ்', 'name_en': 'Vim Dish Wash', 'price': 45.00, 'mrp': 50.00, 'unit': 'பாட்டில்',
         'stock': 90, 'brand': 'HUL', 'gst': 12, 'category': household},
        
        # Dairy
        {'name_ta': 'பால் பாக்கெட்', 'name_en': 'Milk Packet', 'price': 28.00, 'mrp': 28.00, 'unit': 'லிட்டர்',
         'stock': 50, 'brand': 'Aavin', 'gst': 5, 'category': dairy},
        {'name_ta': 'தயிர்', 'name_en': 'Curd', 'price': 30.00, 'mrp': 32.00, 'unit': 'பாக்கெட்',
         'stock': 40, 'brand': 'Aavin', 'gst': 5, 'category': dairy},
    ]
    
    for prod_data in products:
        existing = Product.query.filter_by(name_en=prod_data['name_en']).first()
        if not existing:
            product = Product(
                name_ta=prod_data['name_ta'],
                name_en=prod_data['name_en'],
                price=prod_data['price'],
                mrp=prod_data['mrp'],
                unit=prod_data['unit'],
                stock_quantity=prod_data['stock'],
                brand=prod_data['brand'],
                gst_percentage=prod_data['gst'],
                category_id=prod_data['category'].id,
                is_active=True
            )
            db.session.add(product)
    
    db.session.commit()
    print(f"✅ Added {len(products)} sample products!")

def init_database():
    """Initialize the entire database"""
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Create admin user
        if not User.query.first():
            admin = User(username='admin')
            admin.set_password('admin123')
            db.session.add(admin)
            print("✅ Admin user created!")
        
        # Create shop settings
        if not ShopSettings.query.first():
            settings = ShopSettings()
            db.session.add(settings)
            print("✅ Shop settings created!")
        
        db.session.commit()
        
        # Initialize categories and products
        init_categories()
        init_products()
        
        print("\n🎉 Database initialization completed successfully!")
        print("📝 Login with: admin / admin123")

if __name__ == '__main__':
    init_database()