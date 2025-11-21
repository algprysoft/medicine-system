# mobile_app.py - تطبيق الجوال
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
import sqlite3

class MedicineApp(App):
    def build(self):
        self.conn = sqlite3.connect('medicines.db')
        self.cursor = self.conn.cursor()
        
        # الواجهة الرئيسية
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # عنوان التطبيق
        title = Label(text='بحث أسعار الأدوية', size_hint_y=0.1, font_size='20sp')
        main_layout.add_widget(title)
        
        # حقل البحث
        search_layout = BoxLayout(orientation='vertical', size_hint_y=0.15, spacing=5)
        
        self.medicine_input = TextInput(hint_text='ابحث باسم الصنف', size_hint_y=0.5)
        self.medicine_input.bind(text=self.on_search)
        
        self.company_input = TextInput(hint_text='ابحث بالشركة المصنعة', size_hint_y=0.5)
        self.company_input.bind(text=self.on_search)
        
        search_layout.add_widget(self.medicine_input)
        search_layout.add_widget(self.company_input)
        main_layout.add_widget(search_layout)
        
        # منطقة النتائج
        self.results_layout = GridLayout(cols=4, size_hint_y=None, spacing=5)
        self.results_layout.bind(minimum_height=self.results_layout.setter('height'))
        
        scroll_view = ScrollView(size_hint=(1, 0.75))
        scroll_view.add_widget(self.results_layout)
        main_layout.add_widget(scroll_view)
        
        return main_layout
    
    def on_search(self, instance, value):
        """دالة البحث"""
        # مسح النتائج السابقة
        self.results_layout.clear_widgets()
        
        # إضافة العناوين
        titles = ['الشركة', 'الصنف', 'سعر الشراء', 'سعر البيع']
        for title in titles:
            self.results_layout.add_widget(Label(text=title, size_hint_y=None, height=40))
        
        # البحث في قاعدة البيانات
        medicine_query = self.medicine_input.text
        company_query = self.company_input.text
        
        query = "SELECT * FROM medicines WHERE 1=1"
        params = []
        
        if medicine_query:
            query += " AND medicine LIKE ?"
            params.append(f'%{medicine_query}%')
        
        if company_query:
            query += " AND company LIKE ?"
            params.append(f'%{company_query}%')
        
        self.cursor.execute(query, params)
        results = self.cursor.fetchall()
        
        # عرض النتائج
        for row in results:
            company, medicine, purchase, selling = row[1], row[2], row[3], row[4]
            
            self.results_layout.add_widget(Label(text=company, size_hint_y=None, height=40))
            self.results_layout.add_widget(Label(text=medicine, size_hint_y=None, height=40))
            self.results_layout.add_widget(Label(text=str(purchase), size_hint_y=None, height=40))
            self.results_layout.add_widget(Label(text=str(selling), size_hint_y=None, height=40))

if __name__ == '__main__':
    MedicineApp().run()