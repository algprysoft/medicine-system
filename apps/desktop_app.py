# desktop_app.py - التطبيق الرئيسي الكامل مع إصلاح الأسعار
import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import os
from tkinter import font as tkfont

class PharmacyApp:
    def __init__(self, root):
        self.root = root
        self.root.title("نظام إدارة أسعار الأدوية")
        self.root.geometry("1400x800")
        self.root.configure(bg='#f8f9fa')
        
        # إعداد الخطوط
        self.setup_fonts()
        
        # إعداد الألوان
        self.setup_colors()
        
        # إعداد قاعدة البيانات
        self.setup_database()
        
        # إنشاء الواجهة
        self.create_widgets()
        
        # تحميل البيانات
        self.load_data()
        
    def setup_fonts(self):
        """إعداد الخطوط العربية"""
        self.title_font = tkfont.Font(family="Arial", size=16, weight="bold")
        self.header_font = tkfont.Font(family="Arial", size=12, weight="bold")
        self.normal_font = tkfont.Font(family="Arial", size=11)
        self.small_font = tkfont.Font(family="Arial", size=10)
        
    def setup_colors(self):
        """إعداد الألوان"""
        self.colors = {
            'primary': '#2c5f77',
            'secondary': '#4a8bad',
            'accent': '#ff6b35',
            'success': '#28a745',
            'warning': '#ffc107',
            'danger': '#dc3545',
            'light': '#f8f9fa',
            'dark': '#343a40',
            'header_bg': "#34609B",    # 🎨 تم التعديل هنا
            'header_fg': 'blue',
            'row_even': '#ffffff',
            'row_odd': '#f8f9fa'
        }
        
    def setup_database(self):
        """الاتصال بقاعدة البيانات"""
        self.conn = sqlite3.connect('medicines.db')
        self.cursor = self.conn.cursor()
        
    def create_widgets(self):
        """إنشاء عناصر الواجهة"""
        self.create_header()
        self.create_search_section()
        self.create_table()
        self.create_footer()
        
    def create_header(self):
        """إنشاء رأس التطبيق"""
        header_frame = tk.Frame(self.root, bg=self.colors['primary'], height=100)
        header_frame.pack(fill=tk.X, padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        # العنوان الرئيسي
        title_label = tk.Label(
            header_frame,
            text="🏥 نظام إدارة أسعار الأدوية",
            font=self.title_font,
            fg='white',
            bg=self.colors['primary'],
            pady=20
        )
        title_label.pack(expand=True)
        
        # الشعار الجانبي
        subtitle_label = tk.Label(
            header_frame,
            text="لقطاعات الأدوية والصيدليات",
            font=self.small_font,
            fg='#e0e0e0',
            bg=self.colors['primary']
        )
        subtitle_label.pack()
        
    def create_search_section(self):
        """إنشاء قسم البحث"""
        search_frame = tk.Frame(self.root, bg='#e9ecef', padx=20, pady=15)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # عنوان قسم البحث
        search_title = tk.Label(
            search_frame,
            text="🔍 البحث في قائمة الأدوية",
            font=self.header_font,
            bg='#e9ecef',
            fg=self.colors['dark']
        )
        search_title.grid(row=0, column=0, columnspan=4, sticky=tk.W, pady=(0, 10))
        
        # البحث باسم الدواء
        tk.Label(
            search_frame,
            text="البحث باسم الدواء:",
            font=self.normal_font,
            bg='#e9ecef',
            fg=self.colors['dark']
        ).grid(row=1, column=0, sticky=tk.W, padx=(0, 10))
        
        self.medicine_entry = tk.Entry(
            search_frame,
            font=self.normal_font,
            width=25,
            bg='white',
            relief='solid',
            bd=1
        )
        self.medicine_entry.grid(row=1, column=1, padx=(0, 20), pady=5)
        self.medicine_entry.bind('<KeyRelease>', self.search_medicines)
        
        # البحث بالشركة المصنعة
        tk.Label(
            search_frame,
            text="البحث بالشركة المصنعة:",
            font=self.normal_font,
            bg='#e9ecef',
            fg=self.colors['dark']
        ).grid(row=1, column=2, sticky=tk.W, padx=(0, 10))
        
        self.company_entry = tk.Entry(
            search_frame,
            font=self.normal_font,
            width=25,
            bg='white',
            relief='solid',
            bd=1
        )
        self.company_entry.grid(row=1, column=3, padx=(0, 20), pady=5)
        self.company_entry.bind('<KeyRelease>', self.search_medicines)
        
        # أزرار التحكم
        button_frame = tk.Frame(search_frame, bg='#e9ecef')
        button_frame.grid(row=1, column=4, padx=20)
        
        clear_btn = tk.Button(
            button_frame,
            text="🗑️ مسح البحث",
            font=self.normal_font,
            command=self.clear_search,
            bg=self.colors['warning'],
            fg='white',
            width=12,
            relief='raised',
            bd=2
        )
        clear_btn.pack(side=tk.LEFT, padx=5)
        
        refresh_btn = tk.Button(
            button_frame,
            text="🔄 تحديث البيانات",
            font=self.normal_font,
            command=self.load_data,
            bg=self.colors['success'],
            fg='white',
            width=12,
            relief='raised',
            bd=2
        )
        refresh_btn.pack(side=tk.LEFT, padx=5)
        
    def create_table(self):
        """إنشاء الجدول الرئيسي"""
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # إنشاء Treeview مع الأعمدة المطلوبة
        columns = ('company', 'commercial_name', 'public_price', 'pharmacy_price', 'discount')
        
        self.tree = ttk.Treeview(
            table_frame, 
            columns=columns, 
            show='headings',
            height=20,
            style="Custom.Treeview"
        )
        
        # تعريف العناوين حسب الصورة
        self.tree.heading('company', text='اسم المورد')
        self.tree.heading('commercial_name', text='الاسم التجاري')
        self.tree.heading('public_price', text='سعر الجمهور')
        self.tree.heading('pharmacy_price', text='سعر الصيدلية')
        self.tree.heading('discount', text='الخصم/هامش الربح')
        
        # تحديد أبعاد الأعمدة
        self.tree.column('company', width=200, anchor='center')
        self.tree.column('commercial_name', width=300, anchor='center')
        self.tree.column('public_price', width=150, anchor='center')
        self.tree.column('pharmacy_price', width=150, anchor='center')
        self.tree.column('discount', width=150, anchor='center')
        
        # تنسيق الجدول
        self.setup_table_style()
        
        # شريط التمرير
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        
        # وضع العناصر
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # ربط حدث النقر المزدوج
        self.tree.bind('<Double-1>', self.on_item_double_click)
        
    def setup_table_style(self):
        """تنسيق مظهر الجدول"""
        style = ttk.Style()
        
        # تنسيق العناوين
        style.configure(
            "Custom.Treeview.Heading",
            font=self.header_font,
            background=self.colors['header_bg'],
            foreground=self.colors['header_fg'],
            relief='flat'
        )
        
        # تنسيق الصفوف
        style.configure(
            "Custom.Treeview",
            font=self.normal_font,
            rowheight=35,
            background=self.colors['row_even'],
            fieldbackground=self.colors['row_even']
        )
        
        style.map(
            "Custom.Treeview",
            background=[('selected', self.colors['secondary'])],
            foreground=[('selected', 'white')]
        )
        
    def create_footer(self):
        """إنشاء تذييل التطبيق"""
        footer_frame = tk.Frame(self.root, bg=self.colors['dark'], height=40)
        footer_frame.pack(fill=tk.X, padx=0, pady=0)
        footer_frame.pack_propagate(False)
        
        self.info_label = tk.Label(
            footer_frame,
            text="جاهز للبحث في قاعدة الأدوية...",
            font=self.small_font,
            fg='white',
            bg=self.colors['dark']
        )
        self.info_label.pack(expand=True)
        
        # إحصائيات
        self.stats_label = tk.Label(
            footer_frame,
            text="",
            font=self.small_font,
            fg='#e0e0e0',
            bg=self.colors['dark']
        )
        self.stats_label.pack(side=tk.RIGHT, padx=20)
        
    def calculate_discount(self, public_price, pharmacy_price):
        """حساب نسبة الخصم/الربح"""
        if public_price > 0 and pharmacy_price > 0:
            discount_percent = ((public_price - pharmacy_price) / public_price) * 100
            return f"{discount_percent:.1f}%"
        return "0%"
    
    def load_data(self):
        """تحميل جميع البيانات"""
        try:
            self.cursor.execute("SELECT COUNT(*) FROM medicines")
            count = self.cursor.fetchone()[0]
            
            self.cursor.execute("""
                SELECT company, medicine, selling_price, purchase_price 
                FROM medicines 
                ORDER BY company, medicine
                LIMIT 100
            """)
            results = self.cursor.fetchall()
            
            self.update_table(results)
            self.update_stats(len(results), count)
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في تحميل البيانات: {e}")
    
    def search_medicines(self, event=None):
        """البحث في قاعدة البيانات"""
        medicine_query = self.medicine_entry.get().strip()
        company_query = self.company_entry.get().strip()
        
        query = """
            SELECT company, medicine, selling_price, purchase_price 
            FROM medicines 
            WHERE 1=1
        """
        params = []
        
        if medicine_query:
            query += " AND LOWER(medicine) LIKE LOWER(?)"
            params.append(f'%{medicine_query}%')
        
        if company_query:
            query += " AND LOWER(company) LIKE LOWER(?)"
            params.append(f'%{company_query}%')
        
        query += " ORDER BY company, medicine"
        
        try:
            self.cursor.execute(query, params)
            results = self.cursor.fetchall()
            self.update_table(results)
            self.update_stats(len(results))
            
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ في البحث: {e}")
    
    def clear_search(self):
        """مسح حقول البحث"""
        self.medicine_entry.delete(0, tk.END)
        self.company_entry.delete(0, tk.END)
        self.load_data()
    
    def update_table(self, data):
        """تحديث الجدول بالبيانات"""
        # مسح البيانات الحالية
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # تلوين الصفوف مرة واحدة فقط
        self.tree.tag_configure('even', background=self.colors['row_even'])
        self.tree.tag_configure('odd', background=self.colors['row_odd'])
        
        # إضافة البيانات الجديدة
        for i, row in enumerate(data):
            company, medicine, selling_price, purchase_price = row
            
            # حساب الخصم
            discount = self.calculate_discount(selling_price, purchase_price)
            
            # ✅ الإصلاح: الأسعار كاملة بدون تنسيق خاطئ
            formatted_public = f"{int(selling_price)} ريال"
            formatted_pharmacy = f"{int(purchase_price)} ريال"
            
            # إضافة إلى الجدول
            self.tree.insert(
                '', 
                tk.END, 
                values=(
                    company,
                    medicine,
                    formatted_public,
                    formatted_pharmacy,
                    discount
                ),
                tags=('even' if i % 2 == 0 else 'odd',)
            )
    
    def update_stats(self, results_count, total_count=None):
        """تحديث الإحصائيات"""
        if total_count:
            stats_text = f"عرض {results_count} من أصل {total_count} دواء"
        else:
            stats_text = f"عرض {results_count} نتيجة"
        
        self.stats_label.config(text=stats_text)
        self.info_label.config(text=f"تم العثور على {results_count} نتيجة للبحث")
    
    def on_item_double_click(self, event):
        """عند النقر المزدوج على عنصر"""
        item = self.tree.selection()[0]
        values = self.tree.item(item, 'values')
        
        if values:
            messagebox.showinfo(
                "تفاصيل الدواء",
                f"اسم المورد: {values[0]}\n"
                f"الاسم التجاري: {values[1]}\n"
                f"سعر الجمهور: {values[2]}\n"
                f"سعر الصيدلية: {values[3]}\n"
                f"هامش الربح: {values[4]}"
            )
    
    def __del__(self):
        """إغلاق الاتصال عند الخروج"""
        if hasattr(self, 'conn'):
            self.conn.close()

def main():
    # التحقق من وجود قاعدة البيانات
    if not os.path.exists('medicines.db'):
        messagebox.showerror("خطأ", "قاعدة البيانات غير موجودة! قم بتشغيل create_full_database.py أولاً")
        return
    
    root = tk.Tk()
    app = PharmacyApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()