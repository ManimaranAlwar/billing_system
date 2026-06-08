import barcode
from barcode.writer import ImageWriter
import os
import qrcode
from PIL import Image
import random
import string

class BarcodeGenerator:
    def __init__(self):
        self.barcode_dir = os.path.join('static', 'barcodes')
        os.makedirs(self.barcode_dir, exist_ok=True)
    
    def generate_product_barcode(self, product_id, product_name):
        """Generate barcode for product"""
        # Create unique barcode number
        barcode_number = f"PROD{product_id:06d}{random.randint(1000, 9999)}"
        
        try:
            # Generate barcode
            EAN = barcode.get_barcode_class('code128')
            ean = EAN(barcode_number, writer=ImageWriter())
            
            # Save barcode image
            filename = f"barcode_{product_id}_{product_name[:10]}"
            filepath = os.path.join(self.barcode_dir, filename)
            ean.save(filepath)
            
            return f"barcodes/{filename}.png", barcode_number
        except Exception as e:
            print(f"Error generating barcode: {e}")
            return None, None
    
    def generate_qr_code(self, data, filename):
        """Generate QR code for bill or customer"""
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(data)
        qr.make(fit=True)
        
        img = qr.make_image(fill_color="black", back_color="white")
        filepath = os.path.join(self.barcode_dir, f"qr_{filename}.png")
        img.save(filepath)
        
        return f"barcodes/qr_{filename}.png"

class BarcodeScanner:
    @staticmethod
    def parse_scanned_data(scanned_data):
        """Parse scanned barcode data"""
        try:
            # Check if it's our product barcode format
            if scanned_data.startswith('PROD'):
                product_id = int(scanned_data[4:10])
                return {
                    'type': 'product',
                    'product_id': product_id,
                    'barcode': scanned_data
                }
            elif scanned_data.startswith('BILL'):
                bill_number = scanned_data[4:]
                return {
                    'type': 'bill',
                    'bill_number': bill_number
                }
            elif scanned_data.startswith('CUST'):
                customer_id = int(scanned_data[4:10])
                return {
                    'type': 'customer',
                    'customer_id': customer_id
                }
            else:
                return {
                    'type': 'unknown',
                    'data': scanned_data
                }
        except:
            return {
                'type': 'unknown',
                'data': scanned_data
            }