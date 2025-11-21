@echo off
chcp 65001
title تثبيت المتطلبات
echo.
echo 🛠️ جاري تثبيت المتطلبات...
echo 📥 قد يستغرق 5-10 دقائق...
echo.
pip install streamlit pandas pdfplumber pillow
echo.
echo ✅ تم التثبيت بنجاح!
echo.
pause