import os
import sqlite3
import sys

def read_file_content(file_path):
    """قراءة محتوى الملف مع معالجة الأخطاء"""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"

def display_python_files():
    """عرض محتويات ملفات Python"""
    python_files = [
        'desktop_app.py',
        'mobile_app.py', 
        'database/create_full_database.py',
        'database/fix_prtcs.py',
        'database/update_database.py',
        'utilities/pdf_extractor.py'
    ]
    
    for file_path in python_files:
        if os.path.exists(file_path):
            print(f"\n{'='*60}")
            print(f"ملف: {file_path}")
            print(f"{'='*60}")
            content = read_file_content(file_path)
            print(content[:1000] + "..." if len(content) > 1000 else content)
        else:
            print(f"\nملف غير موجود: {file_path}")

def display_database_structure():
    """عرض هيكل قاعدة البيانات"""
    db_path = 'database/medicines.db'
    if os.path.exists(db_path):
        print(f"\n{'='*60}")
        print(f"هيكل قاعدة البيانات: {db_path}")
        print(f"{'='*60}")
        
        try:
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            
            # الحصول على قائمة الجداول
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
            tables = cursor.fetchall()
            
            print("الجداول في قاعدة البيانات:")
            for table in tables:
                table_name = table[0]
                print(f"\nجدول: {table_name}")
                print("-" * 40)
                
                # الحصول على هيكل الجدول
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                for column in columns:
                    print(f"  عمود: {column[1]} | نوع: {column[2]} | NULL: {column[3]}")
                
                # عرض بعض البيانات كمثال
                cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                sample_data = cursor.fetchall()
                
                if sample_data:
                    print(f"\n  عينة من البيانات (أول 3 صفوف):")
                    for row in sample_data:
                        print(f"    {row}")
            
            conn.close()
        except Exception as e:
            print(f"خطأ في قراءة قاعدة البيانات: {str(e)}")
    else:
        print(f"\nقاعدة البيانات غير موجودة: {db_path}")

def display_directory_structure():
    """عرض هيكل المجلدات"""
    print(f"\n{'='*60}")
    print("هيكل المجلدات والملفات")
    print(f"{'='*60}")
    
    for root, dirs, files in os.walk("."):
        # تجاهل المجلدات المخفية
        dirs[:] = [d for d in dirs if not d.startswith('.')]
        
        level = root.replace(".", "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        
        sub_indent = " " * 2 * (level + 1)
        for file in files:
            if not file.startswith('.'):
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path) if os.path.exists(file_path) else 0
                print(f"{sub_indent}{file} ({file_size} bytes)")

def main():
    """الدالة الرئيسية"""
    print("تحليل نظام إدارة الأدوية")
    print("=" * 60)
    
    # عرض هيكل المجلدات
    display_directory_structure()
    
    # عرض محتويات ملفات Python
    display_python_files()
    
    # عرض هيكل قاعدة البيانات
    display_database_structure()

if __name__ == "__main__":
    main()