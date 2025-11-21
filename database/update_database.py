# update_database.py - تحديث قاعدة البيانات لتتناسب مع الشكل الجديد
import sqlite3
import pandas as pd
import random

print("🔄 تحديث قاعدة البيانات لتتناسب مع الشكل الجديد...")

# الاتصال بقاعدة البيانات
conn = sqlite3.connect('medicines.db')

# جلب البيانات الحالية
df = pd.read_sql('SELECT * FROM medicines', conn)

if not df.empty:
    print(f"📊 البيانات الحالية: {len(df)} صف")
    
    # تعديل الأسعار لتكون مشابهة للصورة (أسعار واقعية)
    def adjust_prices(row):
        # جعل الأسعار مشابهة للصورة (بآلاف الريالات)
        if row['purchase_price'] < 50:
            new_public = random.randint(8000, 15000)  # سعر الجمهور
            new_pharmacy = int(new_public * random.uniform(0.7, 0.85))  # سعر الصيدلية
        else:
            new_public = random.randint(15000, 35000)
            new_pharmacy = int(new_public * random.uniform(0.7, 0.85))
        
        return pd.Series([new_pharmacy, new_public])

    # تطبيق تعديل الأسعار
    df[['purchase_price', 'selling_price']] = df.apply(adjust_prices, axis=1)
    
    # حفظ البيانات المحدثة
    df.to_sql('medicines', conn, if_exists='replace', index=False)
    
    print("✅ تم تحديث الأسعار بنجاح!")
    
    # عرض عينة من البيانات المحدثة
    sample = conn.execute("SELECT * FROM medicines LIMIT 5").fetchall()
    print("\n📋 عينة من البيانات المحدثة:")
    for row in sample:
        discount = ((row[4] - row[3]) / row[4]) * 100
        print(f"   {row[1]} - {row[2]}")
        print(f"      سعر الجمهور: {row[4]:,} ريال")
        print(f"      سعر الصيدلية: {row[3]:,} ريال")
        print(f"      الخصم: {discount:.1f}%")
        print()

else:
    print("❌ لا توجد بيانات للتحديث")

conn.close()

print("🎯 الآن شغل التطبيق المحدث: python desktop_app.py")