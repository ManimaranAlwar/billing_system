from app import app, db
from models import Category

def init_categories():
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
    print("Categories initialized successfully!")

if __name__ == '__main__':
    with app.app_context():
        init_categories()