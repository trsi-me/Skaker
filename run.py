#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف تشغيل مبسط لتطبيق سكاكر
"""

import sys
import os

def check_requirements():
    """التحقق من المتطلبات"""
    try:
        import customtkinter
        import apscheduler
        import requests
        return True
    except ImportError as e:
        print(f"❌ مكتبة مفقودة: {e}")
        print("📦 قم بتثبيت المتطلبات باستخدام:")
        print("pip install -r requirements.txt")
        return False

def main():
    """الدالة الرئيسية"""
    print("🚀 تطبيق سكاكر - تنبيهات العلاجات والكارب")
    print("المطورة: بدور الدوسري")
    print("=" * 50)
    
    # التحقق من المتطلبات
    if not check_requirements():
        return False
    
    # التحقق من ملف الإعدادات
    if not os.path.exists("config/settings.json"):
        print("⚙️ لم يتم العثور على ملف الإعدادات")
        print("🔧 قم بتشغيل: python setup_sms.py")
        return False
    
    try:
        # تشغيل التطبيق
        from main import main as run_app
        run_app()
        return True
        
    except Exception as e:
        print(f"❌ خطأ في تشغيل التطبيق: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

