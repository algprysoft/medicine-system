import streamlit as st
import sqlite3
import pandas as pd
# import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import json
import os
import hashlib
import re

# إعداد صفحة Streamlit
st.set_page_config(
    page_title="نظام إدارة الأدوية",
    page_icon="💊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تثبيت الخط العربي (لتحسين العرض)
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Tajawal:wght@300;400;500;700&display=swap');

* {
    font-family: 'Tajawal', sans-serif;
}

.main-header {
    background: linear-gradient(135deg, #2E86DE 0%, #1B5FB3 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.sidebar-header {
    background: #2E86DE;
    padding: 1rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 1rem;
}

.metric-card {
    background: #192d2d;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    border-left: 4px solid #2E86DE;
    margin-bottom: 1rem;
}

.btn-primary {
    background-color: #2E86DE;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
}

.btn-danger {
    background-color: #E74C3C;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
}

.btn-warning {
    background-color: #F39C12;
    color: white;
    border: none;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    cursor: pointer;
}

.table-header {
    background-color: #2E86DE;
    color: white;
}

.stDataFrame {
    border: 1px solid #ddd;
    border-radius: 10px;
}

.st-emotion-cache-467cry h3{
    color: #00b1ff;
    text-align: center;
}

.st-emotion-cache-467cry h2{
    text-align:center;
}

/* تحسين عرض الجداول */
[data-testid="stDataFrame"] table {
    width: 100%;
    border-collapse: collapse;
}

[data-testid="stDataFrame"] th {
    background-color: #2E86DE;
    color: white;
    padding: 12px;
    text-align: right;
    font-weight: bold;
}

[data-testid="stDataFrame"] td {
    padding: 10px;
    border-bottom: 1px solid #ddd;
    text-align: right;
}

[data-testid="stDataFrame"] tr:hover {
    background-color: #f5f5f5;
}

/* جعل عمود اسم الدواء أعرض */
[data-testid="stDataFrame"] th:nth-child(2),
[data-testid="stDataFrame"] td:nth-child(2) {
    min-width: 200px !important;
    max-width: 300px !important;
    word-wrap: break-word;
}

/* تحسين الأعمدة الأخرى */
[data-testid="stDataFrame"] th:nth-child(1),
[data-testid="stDataFrame"] td:nth-child(1) {
    min-width: 60px !important;
    text-align: center;
}

[data-testid="stDataFrame"] th:nth-child(3),
[data-testid="stDataFrame"] td:nth-child(3) {
    min-width: 120px !important;
    text-align: center;
}

[data-testid="stDataFrame"] th:nth-child(4),
[data-testid="stDataFrame"] td:nth-child(4) {
    min-width: 100px !important;
    text-align: center;
}

[data-testid="stDataFrame"] th:nth-child(5),
[data-testid="stDataFrame"] td:nth-child(5) {
    min-width: 120px !important;
    text-align: center;
}

/* إخفاء رسائل التصحيح */
.debug-message {
    display: none;
}

/* تحسين الأزرار في الجداول */
.action-buttons {
    display: flex;
    gap: 5px;
    justify-content: center;
}

.action-buttons button {
    padding: 4px 8px;
    font-size: 12px;
}

/* تنسيقات إضافية لأزرار الحذف */
.stButton button {
    transition: all 0.3s ease;
}

.stButton button:hover {
    transform: scale(1.05);
}

/* تنسيق خاص لأزرار الحذف */
.stButton button[kind="secondary"] {
    background-color: #000000 !important;
    color: white !important;
    border: 1px solid #0f1e92 !important;
}

.stButton button[kind="secondary"]:hover {
    background-color: #337c4f !important;
    border-color: #0f1e92 !important;
}

/* تحسين مظهر dialog التأكيد */
.confirmation-dialog {
    background: white !important;
    border: 2px solid #dc3545 !important;
}

.overlay {
    background: rgba(0,0,0,0.5) !important;
}

/* تنسيقات للحذف عند Hover */
.medicine-row {
    transition: all 0.3s ease;
    position: relative;
}

.medicine-row:hover {
    background-color: #f8f9fa !important;
    transform: translateX(-5px);
}

.delete-btn {
    display: none;
    position: absolute;
    right: 10px;
    top: 50%;
    transform: translateY(-50%);
    background: #dc3545;
    color: white;
    border: none;
    padding: 5px 10px;
    border-radius: 4px;
    cursor: pointer;
    font-size: 12px;
    z-index: 1000;
}

.medicine-row:hover .delete-btn {
    display: block;
}

.confirmation-dialog {
    position: fixed;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    background: white;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    z-index: 10000;
    border: 2px solid #dc3545;
    min-width: 300px;
}

.overlay {
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0,0.5);
    z-index: 9999;
}

/* تحسينات للبيانات المعروضة */
.data-warning {
    background-color: #fff3cd;
    border: 1px solid #ffeaa7;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}

.data-success {
    background-color: #d1ecf1;
    border: 1px solid #bee5eb;
    border-radius: 5px;
    padding: 10px;
    margin: 10px 0;
}

/* تنسيقات جديدة للحذف */
.delete-animation {
    animation: fadeOut 0.5s ease-in-out;
}

@keyframes fadeOut {
    from { opacity: 1; transform: translateX(0); }
    to { opacity: 0; transform: translateX(-100px); }
}

.medicine-card {
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    padding: 15px;
    margin: 10px 0;
    background: white;
    transition: all 0.3s ease;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}

.medicine-card:hover {
    box-shadow: 0 4px 8px rgba(0,0,0,0.15);
    transform: translateY(-2px);
}

.medicine-card.deleting {
    background-color: #ffe6e6;
    border-color: #ffcccc;
}
.st-emotion-cache-1n6tfoc{
    direction: rtl !important;
}
</style>
""", unsafe_allow_html=True)

class AuthenticationSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.load_users()
    
    def load_users(self):
        """تحميل بيانات المستخدمين من ملف JSON"""
        try:
            if os.path.exists(self.users_file):
                with open(self.users_file, 'r', encoding='utf-8') as f:
                    self.users = json.load(f)
            else:
                # بيانات افتراضية
                self.users = {
                    "admin": {
                        "password": self.hash_password("admin123"),
                        "role": "admin",
                        "created_at": datetime.now().isoformat()
                    },
                    "user": {
                        "password": self.hash_password("user123"),
                        "role": "user",
                        "created_at": datetime.now().isoformat()
                    }
                }
                self.save_users()
        except Exception as e:
            self.users = {}
    
    def save_users(self):
        """حفظ بيانات المستخدمين في ملف JSON"""
        try:
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, ensure_ascii=False, indent=4)
        except Exception as e:
            pass
    
    def hash_password(self, password):
        """تشفير كلمة المرور"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password, hashed):
        """التحقق من كلمة المرور"""
        return self.hash_password(password) == hashed
    
    def login(self, username, password):
        """تسجيل الدخول"""
        if username in self.users and self.verify_password(password, self.users[username]["password"]):
            return self.users[username]["role"]
        return None
    
    def update_user(self, username, new_username, new_password, current_user_role):
        """تحديث بيانات المستخدم"""
        if current_user_role != "admin":
            return False, "غير مصرح به - تحتاج صلاحيات المدير"
        
        if username not in self.users:
            return False, "المستخدم غير موجود"
        
        # تحديث البيانات
        if new_username != username:
            self.users[new_username] = self.users.pop(username)
        
        if new_password:
            self.users[new_username]["password"] = self.hash_password(new_password)
        
        self.users[new_username]["updated_at"] = datetime.now().isoformat()
        self.save_users()
        return True, "تم تحديث بيانات المستخدم بنجاح"
    
    def create_user(self, username, password, role, current_user_role):
        """إنشاء مستخدم جديد"""
        if current_user_role != "admin":
            return False, "غير مصرح به - تحتاج صلاحيات المدير"
        
        if username in self.users:
            return False, "اسم المستخدم موجود مسبقاً"
        
        self.users[username] = {
            "password": self.hash_password(password),
            "role": role,
            "created_at": datetime.now().isoformat()
        }
        self.save_users()
        return True, "تم إنشاء المستخدم بنجاح"
    
    def delete_user(self, username, current_user_role):
        """حذف مستخدم"""
        if current_user_role != "admin":
            return False, "غير مصرح به - تحتاج صلاحيات المدير"
        
        if username not in self.users:
            return False, "المستخدم غير موجود"
        
        # منع حذف المستخدم الحالي
        if username == st.session_state.username:
            return False, "لا يمكن حذف المستخدم الحالي"
        
        # منع حذف آخر مدير في النظام
        admin_count = sum(1 for user_info in self.users.values() if user_info["role"] == "admin")
        if self.users[username]["role"] == "admin" and admin_count <= 1:
            return False, "لا يمكن حذف آخر مدير في النظام"
        
        del self.users[username]
        self.save_users()
        return True, f"تم حذف المستخدم {username} بنجاح"

class MedicineDatabase:
    def __init__(self):
        # استخدام نفس مسار قاعدة البيانات القديم من الكود 1
        self.db_path = "medicines.db"
        # إنشاء المجلد إذا لم يكن موجوداً
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """تهيئة قاعدة البيانات وإصلاح هيكل الجدول"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # التحقق من الجدول الموجود
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='medicines'")
            table_exists = cursor.fetchone()
            
            if table_exists:
                # التحقق من وجود الأعمدة المطلوبة وإضافتها إذا لم تكن موجودة
                cursor.execute("PRAGMA table_info(medicines)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                
                # إضافة الأعمدة المفقودة بدون DEFAULT values للمشاكل
                if 'created_at' not in column_names:
                    try:
                        cursor.execute("ALTER TABLE medicines ADD COLUMN created_at TIMESTAMP")
                    except:
                        cursor.execute("ALTER TABLE medicines ADD COLUMN created_at TEXT")
                
                if 'scientific_name' not in column_names:
                    cursor.execute("ALTER TABLE medicines ADD COLUMN scientific_name TEXT")
                
                if 'min_quantity' not in column_names:
                    cursor.execute("ALTER TABLE medicines ADD COLUMN min_quantity INTEGER")
                
                if 'supplier' not in column_names:
                    cursor.execute("ALTER TABLE medicines ADD COLUMN supplier TEXT")
                
                if 'expiry_date' not in column_names:
                    cursor.execute("ALTER TABLE medicines ADD COLUMN expiry_date TEXT")
                
                if 'category' not in column_names:
                    cursor.execute("ALTER TABLE medicines ADD COLUMN category TEXT")
                
            else:
                # إنشاء الجدول جديد بالهيكل الصحيح
                cursor.execute('''
                    CREATE TABLE medicines (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        scientific_name TEXT,
                        category TEXT,
                        price REAL,
                        quantity INTEGER,
                        min_quantity INTEGER,
                        supplier TEXT,
                        expiry_date TEXT,
                        created_at TIMESTAMP
                    )
                ''')
            
            conn.commit()
            conn.close()
            
        except Exception as e:
            pass
    
    def fix_broken_data(self, conn, cursor):
        """إصلاح البيانات المكسورة في الجدول"""
        try:
            # التحقق من وجود الأعمدة القديمة
            cursor.execute("PRAGMA table_info(medicines)")
            columns = [col[1] for col in cursor.fetchall()]
            
            # إصلاح البيانات: نقل البيانات من الأعمدة القديمة إلى الجديدة
            if 'medicine' in columns and 'name' in columns:
                cursor.execute('''
                    UPDATE medicines 
                    SET name = medicine 
                    WHERE (name IS NULL OR name = '' OR name = 'None' OR name = 'دواء غير معروف') 
                    AND medicine IS NOT NULL AND medicine != '' AND medicine != 'None'
                ''')
            
            if 'selling_price' in columns and 'price' in columns:
                cursor.execute('''
                    UPDATE medicines 
                    SET price = CAST(selling_price AS REAL) 
                    WHERE (price IS NULL OR price = '' OR price = 'مثال' OR price = 'None' OR price = 0) 
                    AND selling_price IS NOT NULL AND selling_price != '' AND selling_price != 'None'
                ''')
            
            if 'company' in columns and 'supplier' in columns:
                cursor.execute('''
                    UPDATE medicines 
                    SET supplier = company 
                    WHERE (supplier IS NULL OR supplier = '' OR supplier = 'None' OR supplier = 'غير محدد') 
                    AND company IS NOT NULL AND company != '' AND company != 'None'
                ''')
            
            # إصلاح القيم الفارغة في الحقول الأساسية
            cursor.execute('''
                UPDATE medicines 
                SET name = COALESCE(NULLIF(medicine, ''), 'دواء غير معروف') 
                WHERE name IS NULL OR name = '' OR name = 'None'
            ''')
            
            cursor.execute('''
                UPDATE medicines 
                SET category = COALESCE(NULLIF(category, ''), 'أخرى') 
                WHERE category IS NULL OR category = '' OR category = 'None'
            ''')
            
            cursor.execute('''
                UPDATE medicines 
                SET quantity = COALESCE(quantity, 0) 
                WHERE quantity IS NULL
            ''')
            
            cursor.execute('''
                UPDATE medicines 
                SET price = COALESCE(CAST(NULLIF(price, '') AS REAL), 
                                     CAST(NULLIF(selling_price, '') AS REAL), 0.0) 
                WHERE price IS NULL OR price = '' OR price = 'مثال' OR price = 'None'
            ''')
            
            cursor.execute('''
                UPDATE medicines 
                SET supplier = COALESCE(NULLIF(supplier, ''), 
                                       NULLIF(company, ''), 'غير محدد') 
                WHERE supplier IS NULL OR supplier = '' OR supplier = 'None'
            ''')
            
            # تحديث min_quantity للقيم الفارغة
            cursor.execute('''
                UPDATE medicines 
                SET min_quantity = 5 
                WHERE min_quantity IS NULL
            ''')
            
            # تحديث created_at للقيم الفارغة
            cursor.execute('''
                UPDATE medicines 
                SET created_at = datetime('now') 
                WHERE created_at IS NULL
            ''')
            
            conn.commit()
            return True
            
        except Exception as e:
            conn.rollback()
            return False
    
    def get_connection(self):
        """الحصول على اتصال بقاعدة البيانات"""
        return sqlite3.connect(self.db_path)
    
    def get_next_id(self):
        """الحصول على آخر ID مستخدم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT MAX(id) FROM medicines")
            result = cursor.fetchone()
            max_id = result[0] if result[0] is not None else 0
            
            conn.close()
            return max_id + 1
            
        except Exception as e:
            return 1
    
    def get_all_medicines(self):
        """جلب جميع الأدوية مع تنظيف البيانات"""
        try:
            conn = self.get_connection()
            
            # استخدام استعلام مبسط أولاً لمعرفة هيكل الجدول
            query = "SELECT * FROM medicines"
            df = pd.read_sql_query(query, conn)
            conn.close()
            
            # تنظيف البيانات بعد جلبها
            if not df.empty:
                # إعادة تسمية الأعمدة القديمة إذا كانت موجودة
                column_mapping = {
                    'medicine': 'name',
                    'selling_price': 'price', 
                    'company': 'supplier',
                    'purchase_price': 'cost_price'
                }
                
                for old_col, new_col in column_mapping.items():
                    if old_col in df.columns and new_col not in df.columns:
                        df[new_col] = df[old_col]
                
                # التأكد من وجود الأعمدة الأساسية
                if 'name' not in df.columns:
                    if 'medicine' in df.columns:
                        df['name'] = df['medicine']
                    else:
                        df['name'] = 'دواء غير معروف'
                
                if 'price' not in df.columns:
                    if 'selling_price' in df.columns:
                        df['price'] = df['selling_price']
                    else:
                        df['price'] = 0.0
                
                if 'supplier' not in df.columns:
                    if 'company' in df.columns:
                        df['supplier'] = df['company']
                    else:
                        df['supplier'] = 'غير محدد'
                
                # تنظيف البيانات
                df['name'] = df['name'].fillna('دواء غير معروف')
                df['name'] = df['name'].replace('', 'دواء غير معروف')
                df['name'] = df['name'].replace('None', 'دواء غير معروف')
                
                df['category'] = df.get('category', 'أخرى').fillna('أخرى')
                df['category'] = df['category'].replace('', 'أخرى')
                df['category'] = df['category'].replace('None', 'أخرى')
                
                df['supplier'] = df['supplier'].fillna('غير محدد')
                df['supplier'] = df['supplier'].replace('', 'غير محدد')
                df['supplier'] = df['supplier'].replace('None', 'غير محدد')
                
                df['scientific_name'] = df.get('scientific_name', '').fillna('')
                df['expiry_date'] = df.get('expiry_date', '').fillna('')
                
                # معالجة الأعمدة الرقمية
                df['quantity'] = pd.to_numeric(df.get('quantity', 0), errors='coerce').fillna(0).astype(int)
                df['min_quantity'] = pd.to_numeric(df.get('min_quantity', 5), errors='coerce').fillna(5).astype(int)
                df['price'] = pd.to_numeric(df['price'], errors='coerce').fillna(0.0)
                
                # إذا كان السعر 0 ولكن هناك selling_price، نستخدمه
                if 'selling_price' in df.columns:
                    selling_prices = pd.to_numeric(df['selling_price'], errors='coerce').fillna(0.0)
                    df['price'] = df['price'].where(df['price'] > 0, selling_prices)
                
            return df
            
        except Exception as e:
            return pd.DataFrame()
    
    def validate_medicine_data(self, medicine_data):
        """التحقق من صحة بيانات الدواء"""
        errors = []
        
        name = medicine_data.get('name', '').strip()
        if not name:
            errors.append("اسم الدواء مطلوب")
        elif len(name) < 2:
            errors.append("اسم الدواء يجب أن يكون على الأقل حرفين")
        
        try:
            price = float(medicine_data.get('price', 0))
            if price < 0:
                errors.append("السعر لا يمكن أن يكون سالباً")
        except (ValueError, TypeError):
            errors.append("السعر يجب أن يكون رقماً")
        
        try:
            quantity = int(medicine_data.get('quantity', 0))
            if quantity < 0:
                errors.append("الكمية لا يمكن أن تكون سالبة")
        except (ValueError, TypeError):
            errors.append("الكمية يجب أن تكون رقماً صحيحاً")
        
        try:
            min_quantity = int(medicine_data.get('min_quantity', 5))
            if min_quantity < 0:
                errors.append("الحد الأدنى للمخزون لا يمكن أن يكون سالباً")
        except (ValueError, TypeError):
            errors.append("الحد الأدنى للمخزون يجب أن يكون رقماً صحيحاً")
        
        expiry_date = medicine_data.get('expiry_date', '')
        if expiry_date and hasattr(expiry_date, 'isoformat'):
            # تحقق من أن تاريخ الانتهاء ليس في الماضي
            if expiry_date < datetime.now().date():
                errors.append("تاريخ الانتهاء لا يمكن أن يكون في الماضي")
        
        return errors
    
    def add_medicine(self, medicine_data):
        """إضافة دواء جديد مع التحقق من البيانات"""
        # التحقق من صحة البيانات أولاً
        validation_errors = self.validate_medicine_data(medicine_data)
        if validation_errors:
            return False, " • " + " • ".join(validation_errors)
        
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # الحصول على الـ ID التالي
            next_id = self.get_next_id()
            
            # تنظيف البيانات قبل الإدخال
            name = medicine_data.get('name', '').strip()
            scientific_name = medicine_data.get('scientific_name', '').strip()
            category = medicine_data.get('category', 'أخرى').strip()
            supplier = medicine_data.get('supplier', '').strip()
            
            # تحويل الأنواع للتأكد
            price = float(medicine_data.get('price', 0.0))
            quantity = int(medicine_data.get('quantity', 0))
            min_quantity = int(medicine_data.get('min_quantity', 5))
            
            # معالجة تاريخ الانتهاء
            expiry_date = medicine_data.get('expiry_date', '')
            if hasattr(expiry_date, 'isoformat'):
                expiry_date = expiry_date.isoformat()
            elif expiry_date is None:
                expiry_date = ''
            
            # استخدام استعلام آمن مع تحديد ID يدوياً
            cursor.execute('''
                INSERT INTO medicines 
                (id, name, scientific_name, category, price, quantity, min_quantity, supplier, expiry_date, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, datetime('now'))
            ''', (
                next_id,
                name or 'دواء غير معروف',
                scientific_name,
                category or 'أخرى',
                price,
                quantity,
                min_quantity,
                supplier or 'غير محدد',
                expiry_date
            ))
            
            conn.commit()
            conn.close()
            
            return True, f"تم إضافة الدواء '{name}' بنجاح (رقم: {next_id})"
            
        except Exception as e:
            error_msg = f"خطأ في إضافة الدواء: {str(e)}"
            return False, error_msg
    
    def update_medicine_quantity(self, medicine_id, new_quantity):
        """تحديث كمية الدواء"""
        try:
            if new_quantity < 0:
                return False, "الكمية لا يمكن أن تكون سالبة"
            
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                UPDATE medicines SET quantity = ? WHERE id = ?
            ''', (new_quantity, medicine_id))
            
            conn.commit()
            conn.close()
            return True, "تم تحديث الكمية بنجاح"
        except Exception as e:
            return False, f"خطأ في تحديث الكمية: {e}"

    def delete_medicine(self, medicine_id):
        """حذف دواء"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # الحصول على اسم الدواء قبل الحذف لعرض رسالة أفضل
            cursor.execute('SELECT name FROM medicines WHERE id = ?', (medicine_id,))
            result = cursor.fetchone()
            medicine_name = result[0] if result else "دواء غير معروف"
            
            cursor.execute('DELETE FROM medicines WHERE id = ?', (medicine_id,))
            
            conn.commit()
            conn.close()
            return True, f"تم حذف الدواء '{medicine_name}' بنجاح"
        except Exception as e:
            return False, f"خطأ في حذف الدواء: {e}"
    
    def delete_medicine_by_name(self, medicine_name):
        """حذف دواء بالاسم"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('DELETE FROM medicines WHERE name = ?', (medicine_name,))
            rows_affected = cursor.rowcount
            
            conn.commit()
            conn.close()
            
            if rows_affected > 0:
                return True, f"تم حذف الدواء '{medicine_name}' بنجاح"
            else:
                return False, f"لم يتم العثور على دواء بالاسم '{medicine_name}'"
        except Exception as e:
            return False, f"خطأ في حذف الدواء: {e}"
    
    def search_medicines(self, search_term):
        """بحث شامل في جميع الأدوية"""
        try:
            conn = self.get_connection()
            
            # استخدام استعلام أكثر أماناً
            query = '''
                SELECT * FROM medicines 
                WHERE name LIKE ? OR scientific_name LIKE ? OR category LIKE ? 
                   OR supplier LIKE ? OR expiry_date LIKE ?
            '''
            search_pattern = f'%{search_term}%'
            
            df = pd.read_sql_query(query, conn, params=[search_pattern]*5)
            conn.close()
            
            return df
            
        except Exception as e:
            return pd.DataFrame()
    
    def get_low_stock_medicines(self):
        """جلب الأدوية منخفضة المخزون"""
        try:
            medicines_df = self.get_all_medicines()
            if not medicines_df.empty:
                low_stock = medicines_df[medicines_df['quantity'] <= medicines_df['min_quantity']]
                return low_stock
            return pd.DataFrame()
        except Exception as e:
            return pd.DataFrame()
    
    def fix_data_issues(self):
        """إصلاح جميع مشاكل البيانات في الجدول"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # إصلاح البيانات المكسورة
            success = self.fix_broken_data(conn, cursor)
            
            conn.commit()
            conn.close()
            
            if success:
                return True, "تم إصلاح مشاكل البيانات بنجاح"
            else:
                return False, "حدث خطأ أثناء إصلاح البيانات"
                
        except Exception as e:
            return False, f"خطأ في إصلاح البيانات: {e}"

class MedicineApp:
    def __init__(self):
        self.auth = AuthenticationSystem()
        self.db = MedicineDatabase()
        
        # تهيئة حالة الجلسة
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user_role' not in st.session_state:
            st.session_state.user_role = None
        if 'username' not in st.session_state:
            st.session_state.username = None
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "Dashboard"
        if 'medicine_to_delete' not in st.session_state:
            st.session_state.medicine_to_delete = None
        if 'deleting_medicine' not in st.session_state:
            st.session_state.deleting_medicine = None
    
    def login_page(self):
        """صفحة تسجيل الدخول"""
        st.markdown('<div class="main-header"><h1>💊 نظام إدارة الأدوية</h1></div>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            with st.form("login_form"):
                st.subheader("تسجيل الدخول")
                username = st.text_input("اسم المستخدم")
                password = st.text_input("كلمة المرور", type="password")
                submit = st.form_submit_button("دخول")
                
                if submit:
                    if username and password:
                        role = self.auth.login(username, password)
                        if role:
                            st.session_state.authenticated = True
                            st.session_state.user_role = role
                            st.session_state.username = username
                            st.success(f"مرحباً {username}!")
                            st.rerun()
                        else:
                            st.error("اسم المستخدم أو كلمة المرور غير صحيحة")
                    else:
                        st.error("يرجى إدخال جميع البيانات")
    
    def sidebar(self):
        """الشريط الجانبي"""
        with st.sidebar:
            st.markdown('<div class="sidebar-header"><h3>💊 القائمة الرئيسية</h3></div>', unsafe_allow_html=True)
            
            # معلومات المستخدم
            st.info(f"👤 {st.session_state.username} ({st.session_state.user_role})")
            
            # الروابط الرئيسية
            if st.button("📊 لوحة التحكم", use_container_width=True):
                st.session_state.current_page = "Dashboard"
                st.rerun()
            
            if st.button("💊 إضافة دواء جديد", use_container_width=True):
                st.session_state.current_page = "Add Medicine"
                st.rerun()
            
            if st.button("📋 عرض جميع الأدوية", use_container_width=True):
                st.session_state.current_page = "View Medicines"
                st.rerun()
            
            if st.button("🔍 بحث في الأدوية", use_container_width=True):
                st.session_state.current_page = "Search Medicines"
                st.rerun()
            
            if st.button("⚠️ تنبيهات المخزون", use_container_width=True):
                st.session_state.current_page = "Low Stock"
                st.rerun()
            
            # إعدادات المدير فقط
            if st.session_state.user_role == "admin":
                if st.button("👥 إدارة المستخدمين", use_container_width=True):
                    st.session_state.current_page = "User Management"
                    st.rerun()
            
                if st.button("⚙️ إعدادات النظام", use_container_width=True):
                    st.session_state.current_page = "Settings"
                    st.rerun()
            
            if st.button("🚪 تسجيل الخروج", use_container_width=True):
                st.session_state.authenticated = False
                st.session_state.user_role = None
                st.session_state.username = None
                st.session_state.medicine_to_delete = None
                st.session_state.deleting_medicine = None
                st.rerun()
    
    def format_dataframe(self, df):
        """تنسيق DataFrame لعرض أفضل مع إضافة ريال للأسعار"""
        if df.empty:
            return df
        
        display_df = df.copy()
        
        # تنسيق عمود السعر لإضافة "ريال"
        if 'price' in display_df.columns:
            display_df['price'] = display_df['price'].apply(
                lambda x: f"{float(x):,.2f} ريال" if pd.notna(x) and str(x).strip() and float(x) != 0 else "0.00 ريال"
            )
        
        # إعادة ترتيب الأعمدة بشكل منطقي ومترتب
        preferred_order = [
            'id', 
            'name', 
            'scientific_name', 
            'category', 
            'quantity', 
            'price', 
            'min_quantity', 
            'supplier', 
            'expiry_date', 
            'created_at'
        ]
        
        # الحفاظ على الأعمدة الموجودة فقط
        existing_columns = [col for col in preferred_order if col in display_df.columns]
        remaining_columns = [col for col in display_df.columns if col not in existing_columns]
        
        display_df = display_df[existing_columns + remaining_columns]
        
        return display_df
    
    def dashboard_page(self):
        """لوحة التحكم"""
        st.markdown('<div class="main-header"><h1>📊 لوحة التحكم</h1></div>', unsafe_allow_html=True)
        
        # جلب البيانات
        medicines_df = self.db.get_all_medicines()
        low_stock_df = self.db.get_low_stock_medicines()
        
        # زر إصلاح البيانات للمدير
        if st.session_state.user_role == "admin" and not medicines_df.empty:
            with st.expander("🔧 أدوات إصلاح البيانات", expanded=False):
                if st.button("إصلاح مشاكل البيانات التلقائي"):
                    success, message = self.db.fix_data_issues()
                    if success:
                        st.success(message)
                        st.rerun()
                    else:
                        st.error(message)
        
        # عرض تحذير إذا كانت هناك مشاكل في البيانات
        if not medicines_df.empty:
            # التحقق من مشاكل البيانات
            empty_names = medicines_df[medicines_df['name'].isin(['', 'دواء غير معروف', 'None'])]
            invalid_prices = medicines_df[medicines_df['price'] == 0]
            empty_suppliers = medicines_df[medicines_df['supplier'].isin(['', 'غير محدد', 'None'])]
            
            if len(empty_names) > 0 or len(invalid_prices) > 0 or len(empty_suppliers) > 0:
            #     st.markdown('<div class="data-warning">⚠️ هناك بعض المشاكل في البيانات تحتاج إلى المراجعة</div>', unsafe_allow_html=True)
                
                if len(empty_names) > 0:
                    st.warning(f"يوجد {len(empty_names)} دواء بدون اسم صحيح")
                if len(invalid_prices) > 0:
                    st.warning(f"يوجد {len(invalid_prices)} دواء بسعر 0")
                if len(empty_suppliers) > 0:
                    st.warning(f"يوجد {len(empty_suppliers)} دواء بدون مورد")
        
        # الإحصائيات
        total_medicines = len(medicines_df)
        low_stock_count = len(low_stock_df)
        
        total_quantity = medicines_df['quantity'].sum() if 'quantity' in medicines_df.columns and not medicines_df.empty else 0
        total_value = (medicines_df['quantity'] * medicines_df['price']).sum() if 'quantity' in medicines_df.columns and 'price' in medicines_df.columns and not medicines_df.empty else 0
        
        # بطاقات الإحصائيات
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>إجمالي الأدوية</h3>
                <h2>{total_medicines}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>منخفضة المخزون</h3>
                <h2 style="color: #E74C3C;">{low_stock_count}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            st.markdown(f"""
            <div class="metric-card">
                <h3>إجمالي الكمية</h3>
                <h2>{total_quantity}</h2>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            st.markdown(f"""
            <div class="metric-card">
                <h3>القيمة الإجمالية</h3>
                <h2>{total_value:,.2f} ريال</h2>
            </div>
            """, unsafe_allow_html=True)
        
        # عرض عينة من البيانات الحالية
        if not medicines_df.empty:
            st.subheader("آخر الأدوية المضافة")
            
            # عرض الأعمدة المهمة فقط وبشكل مرتب
            display_columns = ['id', 'name', 'quantity', 'price', 'category', 'supplier']
            available_columns = [col for col in display_columns if col in medicines_df.columns]
            
            if available_columns:
                sample_df = medicines_df[available_columns].head(10)
                # تنسيق السعر
                sample_df = self.format_dataframe(sample_df)
                st.dataframe(sample_df, use_container_width=True)
        else:
            st.info("لا توجد أدوية مضافة بعد. استخدم صفحة 'إضافة دواء جديد' لبدء إضافة الأدوية.")
    
    def add_medicine_page(self):
        """صفحة إضافة دواء جديد"""
        st.markdown('<div class="main-header"><h1>💊 إضافة دواء جديد</h1></div>', unsafe_allow_html=True)
        
        with st.form("add_medicine_form", clear_on_submit=True):
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("اسم الدواء *", placeholder="أدخل اسم الدواء التجاري")
                scientific_name = st.text_input("الاسم العلمي", placeholder="الاسم العلمي للدواء")
                category = st.selectbox(
                    "الفئة *",
                    ["مضادات حيوية", "مسكنات", "فيتامينات", "أمراض مزمنة", "أخرى"]
                )
                price = st.number_input("السعر (ريال) *", min_value=0.0, step=0.1, value=0.0)
            
            with col2:
                quantity = st.number_input("الكمية المتاحة *", min_value=0, step=1, value=0)
                min_quantity = st.number_input("الحد الأدنى للمخزون *", min_value=0, step=1, value=5)
                supplier = st.text_input("المورد", placeholder="اسم المورد أو الشركة")
                expiry_date = st.date_input("تاريخ الانتهاء", min_value=datetime.now().date())
            
            submitted = st.form_submit_button("إضافة الدواء")
            
            if submitted:
                if name and price >= 0 and quantity >= 0:
                    medicine_data = {
                        'name': name,
                        'scientific_name': scientific_name,
                        'category': category,
                        'price': price,
                        'quantity': quantity,
                        'min_quantity': min_quantity,
                        'supplier': supplier,
                        'expiry_date': expiry_date
                    }
                    
                    success, message = self.db.add_medicine(medicine_data)
                    if success:
                        st.success(message)
                        # إعادة تحميل الصفحة لعرض البيانات الجديدة
                        st.rerun()
                    else:
                        st.error(message)
                else:
                    st.error("يرجى ملء جميع الحقول الإلزامية (*) بشكل صحيح")
    
    def view_medicines_page(self):
        """صفحة عرض جميع الأدوية"""
        st.markdown('<div class="main-header"><h1>📋 جميع الأدوية</h1></div>', unsafe_allow_html=True)
        
        medicines_df = self.db.get_all_medicines()
        
        if not medicines_df.empty:
            # تنسيق البيانات لعرض أفضل
            display_df = self.format_dataframe(medicines_df)
            
            # عرض جميع الأعمدة المتاحة
            st.dataframe(display_df, use_container_width=True)
            
            # خيارات إدارة الكميات والحذف (للمدير فقط)
            if st.session_state.user_role == "admin":
                st.subheader("🛠️ إدارة الأدوية (للمدير فقط)")
                
                # عرض الأدوية مع أزرار الحذف بشكل بطاقات جميلة
                st.write("### حذف الأدوية")
                
                # استخدام container لعرض البطاقات
                for idx, row in medicines_df.iterrows():
                    # التحقق من وجود id صالح
                    medicine_id = row.get('id')
                    if pd.isna(medicine_id) or medicine_id is None:
                        continue
                    
                    # إنشاء بطاقة لكل دواء
                    with st.container():
                        # إضافة تأثير الحذف إذا كان الدواء قيد الحذف
                        card_class = "medicine-card deleting" if st.session_state.get('deleting_medicine') == medicine_id else "medicine-card"
                        
                        col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                        
                        with col1:
                            st.write(f"**{row['name']}**")
                            if pd.notna(row.get('scientific_name')) and row['scientific_name']:
                                st.caption(f"🏷️ {row['scientific_name']}")
                            st.caption(f"#️⃣ الرقم: {row['id']}")
                        
                        with col2:
                            st.write(f"**📦 الكمية:** {row['quantity']}")
                            st.write(f"**💰 السعر:** {row['price']:,.2f} ريال")
                            st.write(f"**⚠️ الحد الأدنى:** {row.get('min_quantity', 5)}")
                        
                        with col3:
                            st.write(f"**📂 الفئة:** {row.get('category', 'أخرى')}")
                            st.write(f"**🏢 المورد:** {row.get('supplier', 'غير محدد')}")
                            if row.get('expiry_date'):
                                st.write(f"**📅 الانتهاء:** {row['expiry_date']}")
                        
                        with col4:
                            # زر الحذف مع تأكيد
                            if st.button("🗑️ حذف", key=f"delete_{int(medicine_id)}", type="secondary", use_container_width=True):
                                st.session_state.medicine_to_delete = {
                                    'id': int(medicine_id),
                                    'name': row['name'],
                                    'page': 'view_medicines'
                                }
                        
                        st.divider()
                
                # التحقق الآمن لـ medicine_to_delete
                medicine_to_delete = st.session_state.get('medicine_to_delete')
                if medicine_to_delete and isinstance(medicine_to_delete, dict):
                    medicine_info = medicine_to_delete
                    
                    # التحقق من الصفحة الحالية
                    if medicine_info.get('page') == 'view_medicines':
                        st.warning(f"⚠️ أنت على وشك حذف الدواء: **{medicine_info['name']}**")
                        
                        col_confirm, col_cancel = st.columns(2)
                        
                        with col_confirm:
                            if st.button("✅ نعم، احذف الدواء", key="confirm_delete_view_btn", use_container_width=True):
                                # تعيين حالة الحذف لتأثير مرئي
                                st.session_state.deleting_medicine = medicine_info['id']
                                
                                success, message = self.db.delete_medicine(medicine_info['id'])
                                if success:
                                    st.success(f"✅ {message}")
                                    # تنظيف session state وإعادة تحميل الصفحة
                                    st.session_state.medicine_to_delete = None
                                    st.session_state.deleting_medicine = None
                                    st.rerun()
                                else:
                                    st.error(f"❌ {message}")
                                    st.session_state.deleting_medicine = None
                        
                        with col_cancel:
                            if st.button("❌ إلغاء الحذف", key="cancel_delete_view_btn", use_container_width=True):
                                st.session_state.medicine_to_delete = None
                                st.rerun()
                
                # الحفاظ على الخيارات الأخرى الموجودة (تحديث الكمية)
                with st.expander("تحديث كمية الدواء"):
                    with st.form("update_quantity_form"):
                        medicine_id = st.number_input("رقم الدواء", min_value=1, step=1, key="update_qty_id")
                        new_quantity = st.number_input("الكمية الجديدة", min_value=0, step=1, key="new_quantity")
                        
                        submit_update = st.form_submit_button("تحديث الكمية")
                        if submit_update:
                            if medicine_id in medicines_df['id'].values:
                                success, message = self.db.update_medicine_quantity(medicine_id, new_quantity)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                            else:
                                st.error("رقم الدواء غير موجود")
        else:
            st.info("لا توجد أدوية مضافة بعد. استخدم صفحة 'إضافة دواء جديد' لبدء إضافة الأدوية.")
    
    def search_medicines_page(self):
        """صفحة البحث الشامل في الأدوية"""
        st.markdown('<div class="main-header"><h1>🔍 بحث شامل في الأدوية</h1></div>', unsafe_allow_html=True)
        
        search_term = st.text_input("اكتب كلمة للبحث في جميع البيانات", 
                                  placeholder="ابحث في اسم الدواء، الاسم العلمي، الفئة، المورد، السعر، الكمية...")
        
        if search_term:
            results_df = self.db.search_medicines(search_term)
            
            if not results_df.empty:
                st.success(f"تم العثور على {len(results_df)} نتيجة للبحث عن: '{search_term}'")
                # تنسيق النتائج لعرض أفضل
                display_df = self.format_dataframe(results_df)
                st.dataframe(display_df, use_container_width=True)
                
                # إضافة خيارات الحذف للمدير
                if st.session_state.user_role == "admin" and not results_df.empty:
                    st.subheader("خيارات سريعة للحذف")
                    medicine_names = results_df['name'].unique().tolist()
                    selected_name = st.selectbox("اختر دواء للحذف السريع", medicine_names, key="quick_delete")
                    
                    if st.button("🗑️ حذف الدواء المحدد", key="quick_delete_btn"):
                        success, message = self.db.delete_medicine_by_name(selected_name)
                        if success:
                            st.success(message)
                            st.rerun()
                        else:
                            st.error(message)
            else:
                st.warning(f"لا توجد نتائج للبحث عن: '{search_term}'")
        else:
            st.info("اكتب كلمة للبحث في جميع بيانات الأدوية (الأسماء، الأسعار، الكميات، الفئات، الموردين)")
    
    def low_stock_page(self):
        """صفحة تنبيهات المخزون"""
        st.markdown('<div class="main-header"><h1>⚠️ تنبيهات المخزون المنخفض</h1></div>', unsafe_allow_html=True)
        
        low_stock_df = self.db.get_low_stock_medicines()
        
        if not low_stock_df.empty:
            st.warning(f"يوجد {len(low_stock_df)} دواء يحتاج إلى إعادة تخزين")
            
            for idx, medicine in low_stock_df.iterrows():
                # التحقق من وجود id صالح
                medicine_id = medicine.get('id')
                if pd.isna(medicine_id) or medicine_id is None:
                    continue
                
                with st.container():
                    col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 1, 1])
                    
                    with col1:
                        name = medicine.get('name', 'دواء غير معروف')
                        st.write(f"**{name}**")
                        if 'scientific_name' in medicine and medicine['scientific_name']:
                            st.caption(f"الاسم العلمي: {medicine['scientific_name']}")
                    
                    with col2:
                        quantity = medicine.get('quantity', 0)
                        min_quantity = medicine.get('min_quantity', 5)
                        st.write(f"**الكمية:** {quantity}")
                        st.write(f"**الحد الأدنى:** {min_quantity}")
                    
                    with col3:
                        if 'supplier' in medicine:
                            st.write(f"**المورد:** {medicine['supplier']}")
                        if 'price' in medicine:
                            st.write(f"**السعر:** {medicine['price']:,.2f} ريال")
                    
                    with col4:
                        if st.button("🔄 إعادة تخزين", key=f"restock_{int(medicine_id)}"):
                            st.session_state.current_page = "Add Medicine"
                            st.rerun()
                    
                    with col5:
                        if st.session_state.user_role == "admin":
                            # زر الحذف مع تأكيد
                            if st.button("🗑️", key=f"delete_low_{int(medicine_id)}"):
                                st.session_state.medicine_to_delete = {
                                    'id': int(medicine_id),
                                    'name': medicine['name'],
                                    'page': 'low_stock'
                                }
                    
                    st.divider()
            
            # التحقق الآمن لـ medicine_to_delete
            medicine_to_delete = st.session_state.get('medicine_to_delete')
            if medicine_to_delete and isinstance(medicine_to_delete, dict):
                medicine_info = medicine_to_delete
                
                # التحقق من الصفحة الحالية
                if medicine_info.get('page') == 'low_stock':
                    st.warning(f"⚠️ أنت على وشك حذف الدواء: **{medicine_info['name']}**")
                    
                    col_confirm, col_cancel = st.columns(2)
                    
                    with col_confirm:
                        if st.button("✅ نعم، احذف الدواء", key="confirm_delete_low_btn", use_container_width=True):
                            st.session_state.deleting_medicine = medicine_info['id']
                            success, message = self.db.delete_medicine(medicine_info['id'])
                            if success:
                                st.success(f"✅ {message}")
                                st.session_state.medicine_to_delete = None
                                st.session_state.deleting_medicine = None
                                st.rerun()
                            else:
                                st.error(f"❌ {message}")
                                st.session_state.deleting_medicine = None
                    
                    with col_cancel:
                        if st.button("❌ إلغاء الحذف", key="cancel_delete_low_btn", use_container_width=True):
                            st.session_state.medicine_to_delete = None
                            st.rerun()
        else:
            st.success("🎉 جميع الأدوية في مستوى مخزون جيد")
    
    def user_management_page(self):
        """صفحة إدارة المستخدمين"""
        if st.session_state.user_role != "admin":
            st.error("غير مصرح لك بالوصول إلى هذه الصفحة")
            return
        
        st.markdown('<div class="main-header"><h1>👥 إدارة المستخدمين</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2, tab3 = st.tabs(["عرض المستخدمين", "إنشاء مستخدم جديد", "حذف مستخدم"])
        
        with tab1:
            st.subheader("المستخدمون الحاليون")
            users_data = []
            for username, user_info in self.auth.users.items():
                users_data.append({
                    "اسم المستخدم": username,
                    "الدور": user_info["role"],
                    "تاريخ الإنشاء": user_info.get("created_at", "غير معروف"),
                    "آخر تحديث": user_info.get("updated_at", "لم يتم التحديث")
                })
            
            if users_data:
                st.dataframe(users_data, use_container_width=True)
            else:
                st.info("لا توجد مستخدمين في النظام")
        
        with tab2:
            st.subheader("إنشاء مستخدم جديد")
            with st.form("create_user_form"):
                col1, col2 = st.columns(2)
                
                with col1:
                    new_username = st.text_input("اسم المستخدم الجديد")
                    new_role = st.selectbox("الدور", ["user", "admin"])
                
                with col2:
                    new_password = st.text_input("كلمة المرور", type="password")
                    confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
                
                submit_create = st.form_submit_button("إنشاء مستخدم")
                if submit_create:
                    if new_username and new_password:
                        if new_password == confirm_password:
                            success, message = self.auth.create_user(
                                new_username, new_password, new_role, st.session_state.user_role
                            )
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("كلمات المرور غير متطابقة")
                    else:
                        st.error("يرجى ملء جميع الحقول")
        
        with tab3:
            st.subheader("حذف مستخدم")
            if len(self.auth.users) > 1:
                users_list = list(self.auth.users.keys())
                users_list = [user for user in users_list if user != st.session_state.username]
                
                if users_list:
                    selected_user = st.selectbox("اختر المستخدم للحذف", users_list)
                    
                    if selected_user:
                        user_info = self.auth.users[selected_user]
                        st.warning(f"المستخدم المحدد: **{selected_user}** (الدور: {user_info['role']})")
                        
                        if user_info['role'] == 'admin':
                            admin_count = sum(1 for user in self.auth.users.values() if user['role'] == 'admin')
                            if admin_count <= 1:
                                st.error("⚠️ لا يمكن حذف آخر مدير في النظام")
                            else:
                                st.info("⚠️ هذا المستخدم مدير في النظام")
                        
                        confirm_delete = st.checkbox("أؤكد أنني أريد حذف هذا المستخدم")
                        
                        if st.button("🗑️ حذف المستخدم", type="secondary"):
                            if confirm_delete:
                                success, message = self.auth.delete_user(selected_user, st.session_state.user_role)
                                if success:
                                    st.success(message)
                                    st.rerun()
                                else:
                                    st.error(message)
                            else:
                                st.error("يرجى تأكيد الحذف بوضع علامة في خانة التأكيد")
                else:
                    st.info("لا يوجد مستخدمين آخرين يمكن حذفهم")
            else:
                st.error("⚠️ لا يمكن حذف جميع المستخدمين في النظام")
    
    def settings_page(self):
        """صفحة إعدادات النظام"""
        if st.session_state.user_role != "admin":
            st.error("غير مصرح لك بالوصول إلى هذه الصفحة")
            return
        
        st.markdown('<div class="main-header"><h1>⚙️ إعدادات النظام</h1></div>', unsafe_allow_html=True)
        
        tab1, tab2 = st.tabs(["تغيير كلمة المرور", "معلومات النظام"])
        
        with tab1:
            st.subheader("تغيير كلمة المرور")
            
            with st.form("change_password_form"):
                username = st.selectbox(
                    "اختر المستخدم",
                    list(self.auth.users.keys())
                )
                
                new_password = st.text_input("كلمة المرور الجديدة", type="password")
                confirm_password = st.text_input("تأكيد كلمة المرور الجديدة", type="password")
                
                submit_change = st.form_submit_button("تغيير كلمة المرور")
                if submit_change:
                    if new_password and confirm_password:
                        if new_password == confirm_password:
                            success, message = self.auth.update_user(
                                username, username, new_password, st.session_state.user_role
                            )
                            if success:
                                st.success(message)
                                st.rerun()
                            else:
                                st.error(message)
                        else:
                            st.error("كلمات المرور غير متطابقة")
                    else:
                        st.error("يرجى ملء جميع الحقول")
        
        with tab2:
            st.subheader("معلومات النظام")
            
            medicines_df = self.db.get_all_medicines()
            st.write(f"**عدد الأدوية في النظام:** {len(medicines_df)}")
            st.write(f"**عدد المستخدمين:** {len(self.auth.users)}")
            st.write(f"**مسار قاعدة البيانات:** {self.db.db_path}")
            
            if st.button("📥 تصدير البيانات إلى CSV"):
                if not medicines_df.empty:
                    csv = medicines_df.to_csv(index=False, encoding='utf-8-sig')
                    st.download_button(
                        label="تحميل البيانات",
                        data=csv,
                        file_name=f"medicines_export_{datetime.now().strftime('%Y%m%d')}.csv",
                        mime="text/csv"
                    )
                else:
                    st.warning("لا توجد بيانات للتصدير")
    
    def run(self):
        """تشغيل التطبيق"""
        if not st.session_state.authenticated:
            self.login_page()
        else:
            self.sidebar()
            
            if st.session_state.current_page == "Dashboard":
                self.dashboard_page()
            elif st.session_state.current_page == "Add Medicine":
                self.add_medicine_page()
            elif st.session_state.current_page == "View Medicines":
                self.view_medicines_page()
            elif st.session_state.current_page == "Search Medicines":
                self.search_medicines_page()
            elif st.session_state.current_page == "Low Stock":
                self.low_stock_page()
            elif st.session_state.current_page == "User Management":
                self.user_management_page()
            elif st.session_state.current_page == "Settings":
                self.settings_page()

# تشغيل التطبيق
if __name__ == "__main__":
    app = MedicineApp()
    app.run()
