import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils.dataframe import dataframe_to_rows
from datetime import datetime
import os

class ExcelExporter:
    def __init__(self):
        self.export_dir = os.path.join('static', 'exports')
        os.makedirs(self.export_dir, exist_ok=True)
    
    def export_products(self, products):
        """Export products to Excel"""
        data = []
        for p in products:
            data.append({
                'பொருள் ID': p.id,
                'பெயர் (தமிழ்)': p.name_ta,
                'பெயர் (ஆங்கிலம்)': p.name_en,
                'விலை': p.price,
                'அளவு': p.unit,
                'இருப்பு': p.stock_quantity,
                'வகை': p.category.name_ta if p.category else '',
                'நிலை': 'செயலில்' if p.is_active else 'செயலற்று'
            })
        
        df = pd.DataFrame(data)
        filename = f"products_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(self.export_dir, filename)
        
        # Create Excel with formatting
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            df.to_excel(writer, sheet_name='பொருட்கள்', index=False)
            
            # Get workbook and worksheet
            workbook = writer.book
            worksheet = writer.sheets['பொருட்கள்']
            
            # Format header
            header_font = Font(bold=True, color="FFFFFF")
            header_fill = PatternFill(start_color="28A745", end_color="28A745", fill_type="solid")
            
            for cell in worksheet[1]:
                cell.font = header_font
                cell.fill = header_fill
                cell.alignment = Alignment(horizontal="center")
            
            # Adjust column widths
            for column in worksheet.columns:
                max_length = 0
                column_letter = column[0].column_letter
                for cell in column:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = min(max_length + 2, 50)
                worksheet.column_dimensions[column_letter].width = adjusted_width
        
        return filename
    
    def export_orders(self, orders):
        """Export orders to Excel"""
        data = []
        for o in orders:
            data.append({
                'ஆர்டர் எண்': o.order_number,
                'பில் எண்': o.bill_number,
                'தேதி': o.order_date.strftime('%d/%m/%Y %H:%M'),
                'வாடிக்கையாளர்': o.customer.name if o.customer else 'பொது',
                'மொத்தம்': o.total_amount,
                'தள்ளுபடி': o.discount,
                'வரி': o.tax_amount,
                'இறுதித் தொகை': o.grand_total,
                'செலுத்தும் முறை': o.payment_method
            })
        
        df = pd.DataFrame(data)
        filename = f"orders_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        filepath = os.path.join(self.export_dir, filename)
        
        df.to_excel(filepath, index=False)
        return filename
    
    def export_customer_history(self, customer, orders):
        """Export customer purchase history"""
        data = []
        for o in orders:
            data.append({
                'பில் எண்': o.bill_number,
                'தேதி': o.order_date.strftime('%d/%m/%Y'),
                'பொருட்கள்': len(o.items),
                'மொத்தம்': o.total_amount,
                'தள்ளுபடி': o.discount,
                'இறுதித் தொகை': o.grand_total
            })
        
        df = pd.DataFrame(data)
        
        # Summary
        summary = pd.DataFrame([{
            'மொத்த பில்கள்': len(orders),
            'மொத்த செலவு': sum(o.grand_total for o in orders),
            'சராசரி பில்': sum(o.grand_total for o in orders) / len(orders) if orders else 0
        }])
        
        filename = f"customer_{customer.id}_{customer.name}_{datetime.now().strftime('%Y%m%d')}.xlsx"
        filepath = os.path.join(self.export_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            summary.to_excel(writer, sheet_name='சுருக்கம்', index=False)
            df.to_excel(writer, sheet_name='பில் வரலாறு', index=False)
        
        return filename
    
    def export_daily_sales(self, date, orders):
        """Export daily sales report"""
        data = []
        for o in orders:
            for item in o.items:
                data.append({
                    'பில் எண்': o.bill_number,
                    'நேரம்': o.order_date.strftime('%H:%M'),
                    'வாடிக்கையாளர்': o.customer.name if o.customer else 'பொது',
                    'பொருள்': item.product.name_ta,
                    'அளவு': f"{item.quantity} {item.product.unit}",
                    'விலை': item.price,
                    'மொத்தம்': item.total
                })
        
        df = pd.DataFrame(data)
        
        # Summary
        summary = pd.DataFrame([{
            'மொத்த விற்பனை': sum(o.grand_total for o in orders),
            'மொத்த பில்கள்': len(orders),
            'மொத்த பொருட்கள்': sum(len(o.items) for o in orders)
        }])
        
        filename = f"daily_sales_{date.strftime('%Y%m%d')}.xlsx"
        filepath = os.path.join(self.export_dir, filename)
        
        with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
            summary.to_excel(writer, sheet_name='சுருக்கம்', index=False)
            df.to_excel(writer, sheet_name='விற்பனை விவரம்', index=False)
        
        return filename