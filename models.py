from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Category(db.Model):
    __tablename__ = 'category'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ta = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    icon = db.Column(db.String(50), default='fas fa-box')  # FontAwesome icon
    color = db.Column(db.String(20), default='#2ecc71')    # Category color
    keywords = db.Column(db.Text)  # Search keywords
    description = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    products = db.relationship('Product', backref='category', lazy=True)

class Product(db.Model):
    __tablename__ = 'product'
    
    id = db.Column(db.Integer, primary_key=True)
    name_ta = db.Column(db.String(100), nullable=False)
    name_en = db.Column(db.String(100), nullable=False)
    description_ta = db.Column(db.String(200))
    description_en = db.Column(db.String(200))
    price = db.Column(db.Float, nullable=False)
    mrp = db.Column(db.Float, nullable=False)  # Maximum Retail Price
    unit = db.Column(db.String(20), nullable=False)  # கிராம், கிலோ, லிட்டர், பீஸ், சிறு பாக்கெட்
    stock_quantity = db.Column(db.Integer, default=0)
    min_stock_alert = db.Column(db.Integer, default=10)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
    brand = db.Column(db.String(100), index=True)  # Brand name
    gst_percentage = db.Column(db.Float, default=5)  # GST rate
    is_active = db.Column(db.Boolean, default=True)
    barcode = db.Column(db.String(50), unique=True, index=True) # Added index for fast scanning
    barcode_image = db.Column(db.String(200))
    expiry_date = db.Column(db.Date)  # For expiry tracking
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Customer(db.Model):
    __tablename__ = 'customer'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(15), unique=True, nullable=False, index=True) # Index for fast lookup at billing
    email = db.Column(db.String(100))
    address = db.Column(db.Text)
    gst_no = db.Column(db.String(20))
    loyalty_points = db.Column(db.Integer, default=0)  # Loyalty points
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    orders = db.relationship('Order', backref='customer', lazy=True)

class Order(db.Model):
    __tablename__ = 'order'
    
    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    bill_number = db.Column(db.String(50), unique=True, nullable=False, index=True)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    order_date = db.Column(db.DateTime, default=datetime.utcnow)
    total_amount = db.Column(db.Float, default=0)
    discount = db.Column(db.Float, default=0)
    tax_amount = db.Column(db.Float, default=0)
    grand_total = db.Column(db.Float, default=0)
    payment_method = db.Column(db.String(20), nullable=False)  # Cash, Card, UPI
    payment_status = db.Column(db.String(20), default='Completed')
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float, nullable=False)
    gst_amount = db.Column(db.Float, default=0) 
    total = db.Column(db.Float, nullable=False)
    
    product = db.relationship('Product')

class ShopSettings(db.Model):
    __tablename__ = 'shop_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    shop_name_ta = db.Column(db.String(200), default='ALWAR ஸ்டோர்') 
    shop_name_en = db.Column(db.String(200), default='ALWAR Store')
    address_ta = db.Column(db.Text, default='உங்கள் முகவரி இங்கே')
    address_en = db.Column(db.Text, default='Your Address Here')
    phone = db.Column(db.String(20), default='+91 98765 43210')
    phone_alt = db.Column(db.String(20), default='')
    email = db.Column(db.String(100), default='contact@alwarstore.com')
    gst_no = db.Column(db.String(20), default='')
    default_gst = db.Column(db.Float, default=0) # Groceries often have 0% or specific GST
    loyalty_points_ratio = db.Column(db.Float, default=0.01)  # 1 point per ₹100
    bill_footer_ta = db.Column(db.Text, default='நன்றி! மீண்டும் வருக')
    bill_footer_en = db.Column(db.Text, default='Thank you! Visit again')