from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, send_file, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from datetime import datetime, timedelta
from sqlalchemy import func, and_
import json
import os
import uuid

from config import Config
from models import db, User, Category, Product, Customer, Order, OrderItem, ShopSettings
from forms import LoginForm, ProductForm, CategoryForm, CustomerForm, ShopSettingsForm
from utils import generate_barcode, generate_pdf_bill, export_to_excel

import pandas as pd
import io

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Create default admin user and shop settings
def create_default_data():
    """Create default data if it doesn't exist"""
    with app.app_context():
        db.create_all()
        
        # Create admin user if not exists
        if not User.query.first():
            admin = User(username='admin')
            admin.set_password('admin123') # Note: Change this after first login!
            db.session.add(admin)
            db.session.commit()
            print("Admin user created successfully!")
        
        # Create default shop settings if not exists
        if not ShopSettings.query.first():
            settings = ShopSettings()
            db.session.add(settings)
            db.session.commit()
            print("Default shop settings created!")
        
        # Supermarket Categories
       # Supermarket Categories (Updated based on your image)
        if not Category.query.first():
            categories = [
                Category(name_ta='அரிசி & தானியங்கள்', name_en='Rice & Grains', icon='fas fa-seedling', color='#f1c40f', keywords='அரிசி, நெல், தானியம், சிறுதானியம், rice, grains'),
                Category(name_ta='பருப்பு வகைகள்', name_en='Dals & Pulses', icon='fas fa-leaf', color='#e67e22', keywords='பருப்பு, துவரம், உளுத்தம், கடலை, dal, dhal, pulses'),
                Category(name_ta='சமையல் எண்ணெய்கள்', name_en='Cooking Oils', icon='fas fa-tint', color='#f39c12', keywords='எண்ணெய், ஆயில், சன் பிளவர், நல்லெண்ணெய், கடலெண்ணெய், oil'),
                Category(name_ta='மசாலா பொருட்கள்', name_en='Spices & Masalas', icon='fas fa-pepper-hot', color='#e74c3c', keywords='மசாலா, தூள், காரம், மிளகு, சீரகம், கடுகு, masala, spice, spices'),
                Category(name_ta='சிற்றுண்டி & தொகுக்கப்பட்ட உணவுகள்', name_en='Snacks & Packaged Foods', icon='fas fa-cookie', color='#d35400', keywords='பிஸ்கட், மிக்சர், முறுக்கு, ஸ்நாக்ஸ், திண்பண்டம், snacks, biscuit, chips'),
                Category(name_ta='பானங்கள்', name_en='Beverages', icon='fas fa-wine-bottle', color='#3498db', keywords='ஜூஸ், டீ, காபி, பானம், பால், juice, drinks, beverage, tea, coffee, milk'),
                Category(name_ta='வீட்டு சுத்தம்', name_en='Household Cleaning', icon='fas fa-pump-soap', color='#9b59b6', keywords='சோப், பவுடர், லிக்விட், பிரஷ், கிளீனிங், soap, detergent, liquid, clean'),
                Category(name_ta='தனிப்பட்ட பராமரிப்பு', name_en='Personal Care', icon='fas fa-bath', color='#1abc9c', keywords='ஷாம்பு, பேஸ்ட், பிரஷ், ஹேர் ஆயில், shampoo, paste, brush, care'),
                
                # NEW CATEGORIES ADDED
                Category(name_ta='காய்கறிகள் & பழங்கள்', name_en='Vegetables & Fruits', icon='fas fa-carrot', color='#2ecc71', keywords='காய்கறி, பழம், தக்காளி, வெங்காயம், veg, fruits, fresh'),
                Category(name_ta='பால் பொருட்கள் & முட்டை', name_en='Dairy & Eggs', icon='fas fa-egg', color='#f39c12', keywords='பால், தயிர், முட்டை, நெய், வெண்ணெய், milk, curd, egg, dairy')
            ]
            db.session.add_all(categories)
            db.session.commit()
            print("Updated supermarket categories created!")

# Call the function to create default data
create_default_data()

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            return redirect(url_for('admin_dashboard'))
        flash('தவறான பயனர்பெயர் அல்லது கடவுச்சொல் (Invalid username or password)', 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Admin Routes
@app.route('/admin/dashboard')
@login_required
def admin_dashboard():
    total_orders = Order.query.count()
    total_products = Product.query.count()
    total_customers = Customer.query.count()
    
    today = datetime.now().date()
    today_sales = db.session.query(func.sum(Order.grand_total)).filter(
        func.date(Order.order_date) == today
    ).scalar() or 0
    
    low_stock = Product.query.filter(Product.stock_quantity <= Product.min_stock_alert).count()
    recent_orders = Order.query.order_by(Order.order_date.desc()).limit(10).all()
    
    sales_data = []
    for i in range(6, -1, -1):
        date = today - timedelta(days=i)
        daily_sales = db.session.query(func.sum(Order.grand_total)).filter(
            func.date(Order.order_date) == date
        ).scalar() or 0
        sales_data.append({
            'date': date.strftime('%d/%m'),
            'amount': float(daily_sales)
        })
    
    return render_template('admin/dashboard.html', 
                         total_orders=total_orders,
                         total_products=total_products,
                         total_customers=total_customers,
                         today_sales=today_sales,
                         low_stock=low_stock,
                         recent_orders=recent_orders,
                         sales_data=json.dumps(sales_data))

@app.route('/admin/products')
@login_required
def admin_products():
    products = Product.query.all()
    return render_template('admin/products.html', products=products)

@app.route('/admin/products/add', methods=['GET', 'POST'])
@login_required
def add_product():
    form = ProductForm()
    form.category_id.choices = [(c.id, f"{c.name_ta} - {c.name_en}") for c in Category.query.all()]
    
    if form.validate_on_submit():
        product = Product(
            name_ta=form.name_ta.data,
            name_en=form.name_en.data,
            description_ta=form.description_ta.data,
            description_en=form.description_en.data,
            price=form.price.data,
            mrp=form.mrp.data,
            unit=form.unit.data,
            stock_quantity=form.stock_quantity.data,
            min_stock_alert=form.min_stock_alert.data,
            category_id=form.category_id.data,
            brand=form.brand.data,
            gst_percentage=form.gst_percentage.data,
            is_active=form.is_active.data
        )
        
        db.session.add(product)
        db.session.commit()
        
        barcode_file = generate_barcode(product.id, product.name_en)
        if barcode_file:
            product.barcode = str(product.id).zfill(12)
            product.barcode_image = barcode_file
            db.session.commit()
        
        flash('பொருள் வெற்றிகரமாக சேர்க்கப்பட்டது! (Product added successfully!)', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/add_product.html', form=form)

@app.route('/admin/products/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_product(id):
    product = Product.query.get_or_404(id)
    form = ProductForm(obj=product)
    form.category_id.choices = [(c.id, f"{c.name_ta} - {c.name_en}") for c in Category.query.all()]
    
    if form.validate_on_submit():
        product.name_ta = form.name_ta.data
        product.name_en = form.name_en.data
        product.description_ta = form.description_ta.data
        product.description_en = form.description_en.data
        product.price = form.price.data
        product.mrp = form.mrp.data
        product.unit = form.unit.data
        product.stock_quantity = form.stock_quantity.data
        product.min_stock_alert = form.min_stock_alert.data
        product.category_id = form.category_id.data
        product.brand = form.brand.data
        product.gst_percentage = form.gst_percentage.data
        product.is_active = form.is_active.data
        
        db.session.commit()
        flash('பொருள் வெற்றிகரமாக புதுப்பிக்கப்பட்டது! (Product updated successfully!)', 'success')
        return redirect(url_for('admin_products'))
    
    return render_template('admin/edit_product.html', form=form, product=product)

@app.route('/admin/products/delete/<int:id>', methods=['POST'])
@login_required
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        flash(f'"{product.name_ta}" வெற்றிகரமாக நீக்கப்பட்டது!', 'success')
    except Exception as e:
        db.session.rollback()
        # ஏற்கனவே ஏதேனும் பில்லில் இந்த பொருள் விற்கப்பட்டிருந்தால், இதை Database-ல் இருந்து மொத்தமாக அழிக்க முடியாது (Foreign Key Error).
        # எனவே அந்த சமயத்தில் பொருளை 'Hidden' ஆக மாற்றிவிடுகிறோம்.
        product.is_active = False 
        db.session.commit()
        flash(f'இந்த பொருள் பழைய பில்களில் உள்ளதால் முழுமையாக நீக்க முடியாது. ஆனால் பட்டியலில் இருந்து மறைக்கப்பட்டுள்ளது (Hidden).', 'info')
        
    return redirect(url_for('admin_products'))


@app.route('/admin/categories')
@login_required
def admin_categories():
    categories = Category.query.all()
    form = CategoryForm()
    return render_template('admin/categories.html', categories=categories, form=form)

@app.route('/admin/categories/add', methods=['POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        existing = Category.query.filter_by(name_ta=form.name_ta.data).first()
        if existing:
            flash('இந்த வகை ஏற்கனவே உள்ளது!', 'danger')
        else:
            category = Category(
                name_ta=form.name_ta.data,
                name_en=form.name_en.data,
                description=form.description.data
            )
            db.session.add(category)
            db.session.commit()
            flash('வகை வெற்றிகரமாக சேர்க்கப்பட்டது!', 'success')
    else:
        flash('பிழை: அனைத்து கட்டாய புலங்களையும் நிரப்பவும்', 'danger')
    return redirect(url_for('admin_categories'))

@app.route('/admin/customers')
@login_required
def admin_customers():
    customers = Customer.query.order_by(Customer.created_at.desc()).all()
    return render_template('admin/customers.html', customers=customers)

@app.route('/admin/customers/add', methods=['POST'])
@login_required
def add_customer():
    try:
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        email = request.form.get('email', '').strip()
        address = request.form.get('address', '').strip()
        gst_no = request.form.get('gst_no', '').strip()
        
        if not name or not phone:
            flash('பெயர் மற்றும் தொலைபேசி எண் கட்டாயம்!', 'danger')
            return redirect(url_for('admin_customers'))
        
        if not phone.isdigit() or len(phone) != 10:
            flash('தொலைபேசி எண் 10 இலக்கங்கள் கொண்டதாக இருக்க வேண்டும்!', 'danger')
            return redirect(url_for('admin_customers'))
        
        existing = Customer.query.filter_by(phone=phone).first()
        if existing:
            flash(f'இந்த தொலைபேசி எண் ({phone}) ஏற்கனவே {existing.name} என்ற வாடிக்கையாளருக்கு பதிவு செய்யப்பட்டுள்ளது!', 'danger')
            return redirect(url_for('admin_customers'))
        
        customer = Customer(name=name, phone=phone, email=email or None, address=address or None, gst_no=gst_no or None)
        db.session.add(customer)
        db.session.commit()
        flash(f'வாடிக்கையாளர் "{name}" வெற்றிகரமாக சேர்க்கப்பட்டது!', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'பிழை: {str(e)}', 'danger')
    
    return redirect(url_for('admin_customers'))

@app.route('/admin/customer/<int:id>')
@login_required
def customer_detail(id):
    customer = Customer.query.get_or_404(id)
    orders = Order.query.filter_by(customer_id=id).order_by(Order.order_date.desc()).all()
    total_spent = sum(order.grand_total for order in orders)
    avg_bill = total_spent / len(orders) if orders else 0
    return render_template('admin/customer_detail.html', customer=customer, orders=orders, total_spent=total_spent, avg_bill=avg_bill)

@app.route('/admin/orders')
@login_required
def admin_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('admin/orders.html', orders=orders)

@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
def admin_settings():
    settings = ShopSettings.query.first()
    form = ShopSettingsForm(obj=settings)
    
    if form.validate_on_submit():
        settings.shop_name_ta = form.shop_name_ta.data
        settings.shop_name_en = form.shop_name_en.data
        settings.address_ta = form.address_ta.data
        settings.address_en = form.address_en.data
        settings.phone = form.phone.data
        settings.email = form.email.data
        settings.gst_no = form.gst_no.data
        settings.default_gst = form.default_gst.data 
        settings.bill_footer_ta = form.bill_footer_ta.data
        settings.bill_footer_en = form.bill_footer_en.data
        
        db.session.commit()
        flash('கடை அமைப்புகள் வெற்றிகரமாக புதுப்பிக்கப்பட்டது!', 'success')
        return redirect(url_for('admin_settings'))
    
    return render_template('admin/settings.html', form=form, settings=settings)

# ==========================================
# BILLING ROUTES (UPDATED WITH PREVIOUS/NEXT)
# ==========================================

@app.route('/billing/new')
@login_required
def new_bill():
    products = Product.query.filter_by(is_active=True).all()
    settings = ShopSettings.query.first()
    categories = Category.query.all()
    return render_template('billing/new_bill.html', products=products, settings=settings, categories=categories)

@app.route('/billing/previous/', defaults={'current_id': None})
@app.route('/billing/previous/<int:current_id>')
@login_required
def previous_bill(current_id):
    """புதிய பில் பக்கத்தில் இருந்து முந்தைய பில்லை பார்க்க"""
    if current_id:
        # குறிப்பிட்ட பில்-க்கு முந்தைய பில்
        order = Order.query.filter(Order.id < current_id).order_by(Order.id.desc()).first()
    else:
        # கடைசியாக போடப்பட்ட பில்
        order = Order.query.order_by(Order.id.desc()).first()
        
    if order:
        return redirect(url_for('view_bill', id=order.id))
    
    flash('முந்தைய பில்கள் எதுவும் இல்லை! (No previous bills found)', 'warning')
    return redirect(request.referrer or url_for('new_bill'))

@app.route('/billing/next/', defaults={'current_id': None})
@app.route('/billing/next/<int:current_id>')
@login_required
def next_bill(current_id):
    """பழைய பில்லில் இருந்து அடுத்த பில்லை பார்க்க"""
    if current_id:
        order = Order.query.filter(Order.id > current_id).order_by(Order.id.asc()).first()
        if order:
            return redirect(url_for('view_bill', id=order.id))
        # அடுத்த பில் இல்லை என்றால், புதிய பில் பக்கத்திற்கு செல்லவும்
        return redirect(url_for('new_bill'))
    
    # 'New Bill' பக்கத்தில் இருக்கும் போது Next அழுத்தினால்
    flash('நீங்கள் புதிய பில் பக்கத்தில் தான் உள்ளீர்கள்!', 'info')
    return redirect(url_for('new_bill'))

@app.route('/api/hold-bill', methods=['POST'])
@login_required
def hold_bill_api():
    """தற்காலிகமாக பில்லை நிறுத்திவைக்க (Hold Bill API)"""
    try:
        data = request.json
        if 'held_bills' not in session:
            session['held_bills'] = []
            
        hold_id = str(uuid.uuid4())[:6] # Unique ID for hold
        data['hold_id'] = hold_id
        data['timestamp'] = datetime.now().strftime('%I:%M %p')
        
        held = session['held_bills']
        held.append(data)
        session['held_bills'] = held
        session.modified = True
        
        return jsonify({'success': True, 'message': 'பில் தற்காலிகமாக சேமிக்கப்பட்டது (Bill Held)!', 'hold_id': hold_id})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})

# ==========================================
# API ROUTES
# ==========================================

@app.route('/api/search-products')
def search_products():
    query = request.args.get('q', '').strip()
    category_id = request.args.get('category', type=int)
    
    if not query and not category_id:
        return jsonify([])
    
    # Active ஆக உள்ள பொருட்களை மட்டும் தேட
    product_query = Product.query.filter(Product.is_active == True)
    
    if category_id:
        product_query = product_query.filter(Product.category_id == category_id)
    
    if query:
        search_term = f"%{query}%"
        
        # CATEGORY NO (Category ID) மூலம் தேடுவதற்கான லாஜிக்
        category_id_match = None
        if query.isdigit():
            category_id_match = Product.category_id == int(query)

        # Advanced Search Logic:
        # பொருளின் பெயர் (தமிழ், ஆங்கிலம்), பார்கோடு, பிராண்ட், கேடகரி பெயர் மற்றும் கேடகரி ID.
        or_conditions = [
            Product.name_ta.ilike(search_term),
            Product.name_en.ilike(search_term),
            Product.barcode.ilike(search_term),
            Product.brand.ilike(search_term),
            Product.category.has(Category.name_ta.ilike(search_term)),
            Product.category.has(Category.name_en.ilike(search_term))
        ]
        
        # பயனர் டைப் செய்தது ஒரு எண்ணாக இருந்தால் (Category No), அதையும் தேடலில் சேர்ப்போம்
        if category_id_match is not None:
            or_conditions.append(category_id_match)
            
        product_query = product_query.filter(db.or_(*or_conditions))
    
    products = product_query.limit(50).all()
    
    results = []
    for p in products:
        results.append({
            'id': p.id,
            'name_ta': p.name_ta,
            'name_en': p.name_en,
            'price': p.price,
            'mrp': p.mrp,
            'unit': p.unit,
            'stock': p.stock_quantity,
            'brand': p.brand,
            'gst_percentage': p.gst_percentage,
            'category': p.category.name_ta if p.category else 'Other'
        })
    
    return jsonify(results)

@app.route('/api/scan-barcode', methods=['POST'])
def scan_barcode():
    data = request.json
    barcode = data.get('barcode')
    
    product = Product.query.filter_by(barcode=barcode).first()
    if product:
        return jsonify({
            'success': True,
            'product': {
                'id': product.id,
                'name_ta': product.name_ta,
                'name_en': product.name_en,
                'price': product.price,
                'unit': product.unit,
                'stock': product.stock_quantity,
                'gst_percentage': product.gst_percentage
            }
        })
    return jsonify({'success': False, 'message': 'பொருள் கிடைக்கவில்லை'})

@app.route('/api/create-order', methods=['POST'])
@login_required
def create_order():
    try:
        data = request.json
        if not data.get('items') or len(data['items']) == 0:
            return jsonify({'success': False, 'message': 'பொருட்கள் எதுவும் இல்லை'}), 400
        
        customer = None
        if data.get('customer_phone'):
            customer = Customer.query.filter_by(phone=data['customer_phone']).first()
            if not customer and data.get('customer_name'):
                customer = Customer(
                    name=data['customer_name'],
                    phone=data['customer_phone'],
                    email=data.get('customer_email', ''),
                    address=data.get('customer_address', '')
                )
                db.session.add(customer)
                db.session.commit()
        
        order_number = f"ORD{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4]}"
        bill_number = f"BILL{datetime.now().strftime('%Y%m%d%H%M%S')}{uuid.uuid4().hex[:4]}"
        
        order = Order(
            order_number=order_number,
            bill_number=bill_number,
            customer_id=customer.id if customer else None,
            total_amount=data['total_amount'],
            discount=data.get('discount', 0),
            tax_amount=data.get('gst_amount', 0),
            grand_total=data['grand_total'],
            payment_method=data['payment_method'],
            created_by=current_user.id
        )
        
        db.session.add(order)
        db.session.flush()
        
        for item in data['items']:
            product = Product.query.get(item['product_id'])
            if product:
                gst_amount = (item['price'] * item['quantity'] * product.gst_percentage) / 100
                
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item['product_id'],
                    quantity=item['quantity'],
                    price=item['price'],
                    gst_amount=gst_amount,
                    total=(item['quantity'] * item['price']) + gst_amount
                )
                db.session.add(order_item)
                product.stock_quantity -= item['quantity']
        
        db.session.commit()
        
        if customer:
            points_earned = int(order.grand_total / 100)
            customer.loyalty_points = (customer.loyalty_points or 0) + points_earned
            db.session.commit()
        
        return jsonify({
            'success': True,
            'order_id': order.id,
            'bill_number': order.bill_number
        })
        
    except Exception as e:
        db.session.rollback()
        print(f"Error creating order: {str(e)}")
        return jsonify({'success': False, 'message': str(e)}), 500

@app.route('/billing/history')
@login_required
def bill_history():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    return render_template('billing/bill_history.html', orders=orders)

@app.route('/billing/view/<int:id>')
@login_required
def view_bill(id):
    order = Order.query.get_or_404(id)
    settings = ShopSettings.query.first()
    return render_template('billing/view_bill.html', order=order, settings=settings)

@app.route('/billing/download-pdf/<int:id>')
@login_required
def download_pdf(id):
    order = Order.query.get_or_404(id)
    settings = ShopSettings.query.first()
    customer = order.customer
    
    pdf_buffer = generate_pdf_bill(order, order.items, settings, customer, request.args.get('lang', 'ta'))
    
    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=f"bill_{order.bill_number}.pdf",
        mimetype='application/pdf'
    )

@app.route('/api/search-customers')
def search_customers():
    query = request.args.get('q', '')
    customers = Customer.query.filter(
        Customer.name.contains(query) | Customer.phone.contains(query)
    ).limit(10).all()
    
    results = [{'id': c.id, 'name': c.name, 'phone': c.phone, 'email': c.email, 'address': c.address} for c in customers]
    return jsonify(results)

@app.route('/api/customer/<int:id>/history')
def customer_history(id):
    customer = Customer.query.get_or_404(id)
    orders = Order.query.filter_by(customer_id=id).order_by(Order.order_date.desc()).all()
    
    history = [{
        'id': order.id,
        'order_number': order.order_number,
        'bill_number': order.bill_number,
        'date': order.order_date.strftime('%d/%m/%Y %H:%M'),
        'total': order.grand_total,
        'payment_method': order.payment_method
    } for order in orders]
    
    return jsonify({
        'customer': {'name': customer.name, 'phone': customer.phone, 'email': customer.email, 'address': customer.address},
        'orders': history
    })

# Export Routes
@app.route('/api/export/products')
@login_required
def export_products():
    products = Product.query.all()
    data = [[idx, p.name_ta, p.name_en, p.price, p.unit, p.stock_quantity, p.category.name_ta if p.category else '-'] for idx, p in enumerate(products, 1)]
    headers = ['வ.எண்', 'பெயர் (தமிழ்)', 'பெயர் (ஆங்கிலம்)', 'விலை (₹)', 'அலகு', 'இருப்பு', 'வகை']
    buffer = export_to_excel(data, headers, 'products.xlsx')
    return send_file(buffer, as_attachment=True, download_name='products.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/api/export/orders')
@login_required
def export_orders():
    orders = Order.query.order_by(Order.order_date.desc()).all()
    data = [[idx, o.bill_number, o.order_date.strftime('%d/%m/%Y %H:%M'), o.customer.name if o.customer else 'பொது', o.grand_total, o.payment_method] for idx, o in enumerate(orders, 1)]
    headers = ['வ.எண்', 'பில் எண்', 'தேதி', 'வாடிக்கையாளர்', 'மொத்தம் (₹)', 'பணம் செலுத்திய முறை']
    buffer = export_to_excel(data, headers, 'orders.xlsx')
    return send_file(buffer, as_attachment=True, download_name='orders.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/api/export/daily-sales')
@login_required
def export_daily_sales():
    today = datetime.now().date()
    orders = Order.query.filter(func.date(Order.order_date) == today).all()
    data = [[o.bill_number, o.order_date.strftime('%H:%M'), o.customer.name if o.customer else 'பொது', o.grand_total] for o in orders]
    headers = ['பில் எண்', 'நேரம்', 'வாடிக்கையாளர்', 'மொத்தம் (₹)']
    buffer = export_to_excel(data, headers, f'daily_sales_{today}.xlsx')
    return send_file(buffer, as_attachment=True, download_name=f'daily_sales_{today}.xlsx', mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/admin/products/download-template')
@login_required
def download_product_template():
    """பயனர்களுக்கான மாதிரி Excel டெம்ப்ளேட்டை உருவாக்குகிறது"""
    # டெம்ப்ளேட்டிற்கான தலைப்புகள்
    df = pd.DataFrame(columns=[
        'Name_Tamil', 'Name_English', 'Category_ID', 'Price', 'MRP', 
        'Unit', 'Stock', 'Min_Alert', 'GST_Percentage', 'Brand'
    ])
    
    # மாதிரி டேட்டா (உதாரணத்திற்காக)
    df.loc[0] = ['பாஸ்மதி அரிசி', 'Basmati Rice', 1, 120, 150, 'கிலோ', 50, 5, 5, 'India Gate']
    df.loc[1] = ['சர்க்கரை', 'Sugar', 1, 40, 45, 'கிலோ', 100, 10, 0, 'Parrys']
    
    # Excel ஃபைலாக மாற்ற
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Products')
    output.seek(0)
    
    return send_file(output, as_attachment=True, download_name="Product_Import_Template.xlsx", mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")

@app.route('/admin/products/import', methods=['POST'])
@login_required
def import_products():
    """Excel அல்லது CSV-யிலிருந்து பொருட்களை Bulk Upload செய்தல்"""
    if 'file' not in request.files:
        flash('கோப்பு எதுவும் தேர்ந்தெடுக்கப்படவில்லை!', 'danger')
        return redirect(url_for('admin_products'))
        
    file = request.files['file']
    if file.filename == '':
        flash('கோப்பு காலியாக உள்ளது!', 'danger')
        return redirect(url_for('admin_products'))

    try:
        # File type-ஐ பொறுத்து Pandas மூலம் படிக்கவும்
        if file.filename.endswith('.csv'):
            df = pd.read_csv(file)
        elif file.filename.endswith(('.xls', '.xlsx')):
            df = pd.read_excel(file)
        else:
            flash('தவறான கோப்பு வடிவம். Excel அல்லது CSV கோப்பை மட்டும் பயன்படுத்தவும்.', 'danger')
            return redirect(url_for('admin_products'))

        added_count = 0
        
        # ஒவ்வொரு வரியாக (Row) டேட்டாபேஸில் சேர்க்க
        for index, row in df.iterrows():
            # அடிப்படை கட்டாய டேட்டா உள்ளதா என சோதிக்க
            if pd.isna(row.get('Name_Tamil')) or pd.isna(row.get('Price')):
                continue

            product = Product(
                name_ta=str(row.get('Name_Tamil', '')).strip(),
                name_en=str(row.get('Name_English', '')).strip() if not pd.isna(row.get('Name_English')) else "",
                category_id=int(row.get('Category_ID', 1)) if not pd.isna(row.get('Category_ID')) else 1,
                price=float(row.get('Price', 0)),
                mrp=float(row.get('MRP', row.get('Price', 0))),
                unit=str(row.get('Unit', 'எண்ணிக்கை')).strip(),
                stock_quantity=float(row.get('Stock', 0)),
                min_stock_alert=float(row.get('Min_Alert', 5)),
                gst_percentage=float(row.get('GST_Percentage', 0)),
                brand=str(row.get('Brand', '')).strip() if not pd.isna(row.get('Brand')) else "",
                is_active=True
            )
            db.session.add(product)
            db.session.flush() # ID-ஐ உருவாக்க Flush செய்கிறோம்
            
            # பார்கோடு உருவாக்க (தேவைப்பட்டால்)
            barcode_file = generate_barcode(product.id, product.name_en)
            if barcode_file:
                product.barcode = str(product.id).zfill(12)
                product.barcode_image = barcode_file
                
            added_count += 1
            
        db.session.commit()
        flash(f'வெற்றி! {added_count} பொருட்கள் வெற்றிகரமாக பதிவேற்றப்பட்டன.', 'success')
        
    except Exception as e:
        db.session.rollback()
        flash(f'பதிவேற்றத்தில் பிழை: {str(e)}. டெம்ப்ளேட்டை சரியாக நிரப்பியுள்ளீர்களா என சரிபார்க்கவும்.', 'danger')

    return redirect(url_for('admin_products'))


# Vercel serverless mode - ensure DB and defaults on startup
# The create_default_data() function already runs at module level

if __name__ == '__main__':
    app.run(debug=True)
