from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, FloatField, IntegerField, SelectField, TextAreaField
# InputRequired என்பதைப் புதிதாகச் சேர்த்துள்ளோம்
from wtforms.validators import DataRequired, InputRequired, Optional 

class LoginForm(FlaskForm):
    username = StringField('பயனர்பெயர்', validators=[DataRequired()])
    password = PasswordField('கடவுச்சொல்', validators=[DataRequired()])

class ProductForm(FlaskForm):
    name_ta = StringField('பெயர் (தமிழ்)', validators=[DataRequired()])
    name_en = StringField('பெயர் (ஆங்கிலம்)', validators=[DataRequired()])
    brand = StringField('பிராண்ட்', validators=[Optional()])
    
    # DataRequired-க்கு பதிலாக InputRequired பயன்படுத்தப்பட்டுள்ளது (0-வை அனுமதிக்க)
    mrp = FloatField('அசல் விலை (MRP)', default=0.0, validators=[InputRequired(message="அசல் விலையை உள்ளிடவும்")])
    gst_percentage = FloatField('GST வரி (%)', default=0.0, validators=[InputRequired(message="GST வரியை உள்ளிடவும் (0 எனலாம்)")])
    price = FloatField('விற்பனை விலை', default=0.0, validators=[InputRequired(message="விற்பனை விலையை உள்ளிடவும்")])
    
    description_ta = TextAreaField('விளக்கம் (தமிழ்)', validators=[Optional()])
    description_en = TextAreaField('விளக்கம் (ஆங்கிலம்)', validators=[Optional()])
    
    unit = SelectField('அளவீடு', choices=[
        ('கிலோ', 'கிலோ (Kg)'),
        ('கிராம்', 'கிராம் (g)'),
        ('லிட்டர்', 'லிட்டர் (L)'),
        ('மில்லி', 'மில்லி (ml)'),
        ('பீஸ்', 'பீஸ் (Piece)'),
        ('பாக்கெட்', 'பாக்கெட் (Packet)'),
        ('பாக்ஸ்', 'பாக்ஸ் (Box)'),
        ('டஜன்', 'டஜன் (Dozen)')
    ], validators=[DataRequired()])
    
    # இருப்பும் 0 ஆக இருக்கலாம் என்பதால் இதற்கும் InputRequired
    stock_quantity = IntegerField('தற்போதைய இருப்பு', default=0, validators=[InputRequired()])
    min_stock_alert = IntegerField('குறைந்தபட்ச எச்சரிக்கை', default=5, validators=[InputRequired()])
    
    category_id = SelectField('பொருள் வகை', coerce=int, validators=[DataRequired()])
    is_active = BooleanField('செயலில் உள்ளதா', default=True)

class CategoryForm(FlaskForm):
    name_ta = StringField('வகை பெயர் (தமிழ்)', validators=[DataRequired()])
    name_en = StringField('Category Name (English)', validators=[DataRequired()])
    description = TextAreaField('விளக்கம்', validators=[Optional()])

class CustomerForm(FlaskForm):
    name = StringField('பெயர்', validators=[DataRequired()])
    phone = StringField('தொலைபேசி', validators=[DataRequired()])
    email = StringField('மின்னஞ்சல்', validators=[Optional()])
    address = TextAreaField('முகவரி', validators=[Optional()])
    gst_no = StringField('GST எண்', validators=[Optional()])

class ShopSettingsForm(FlaskForm):
    shop_name_ta = StringField('கடையின் பெயர் (தமிழ்)', validators=[DataRequired()])
    shop_name_en = StringField('Shop Name (English)', validators=[DataRequired()])
    address_ta = TextAreaField('முகவரி (தமிழ்)', validators=[DataRequired()])
    address_en = TextAreaField('Address (English)', validators=[DataRequired()])
    phone = StringField('தொலைபேசி எண் 1', validators=[DataRequired()])
    phone_alt = StringField('தொலைபேசி எண் 2', validators=[Optional()])
    email = StringField('மின்னஞ்சல்', validators=[Optional()])
    gst_no = StringField('GST எண்', validators=[Optional()])
    default_gst = FloatField('டிஃபால்ட் GST (%)', validators=[Optional()])
    bill_footer_ta = TextAreaField('பில் முடிவுரை (தமிழ்)', validators=[Optional()])
    bill_footer_en = TextAreaField('Bill Footer (English)', validators=[Optional()])