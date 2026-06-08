import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///flower_shop.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = False
    
    # Upload folders
    UPLOAD_FOLDER = 'static/uploads'
    BARCODE_FOLDER = 'static/uploads/barcodes'
    
    # Shop settings
    SHOP_NAME_TA = 'மல்லிகை மலர்க் கடை'
    SHOP_NAME_EN = 'Malligai Flower Shop'
    
    # Ensure folders exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(BARCODE_FOLDER, exist_ok=True)