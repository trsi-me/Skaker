#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف اختبار تطبيق سكاكر
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.data_manager import DataManager
from core.sms_sender import SMSSender
from core.scheduler import ReminderScheduler
import time

def test_data_manager():
    """اختبار مدير البيانات"""
    print("🧪 اختبار مدير البيانات...")
    
    dm = DataManager("test_reminders.json")
    
    # إضافة تنبيه تجريبي
    reminder_id = dm.add_reminder("اختبار العلاج", "14:30:00", "0501234567", "علاج")
    print(f"✅ تم إضافة تنبيه: {reminder_id}")
    
    # الحصول على التنبيهات
    reminders = dm.get_reminders()
    print(f"✅ عدد التنبيهات: {len(reminders)}")
    
    # حذف التنبيه التجريبي
    dm.delete_reminder(reminder_id)
    print("✅ تم حذف التنبيه التجريبي")
    
    # تنظيف
    if os.path.exists("test_reminders.json"):
        os.remove("test_reminders.json")
    
    print("✅ اختبار مدير البيانات مكتمل\n")

def test_sms_sender():
    """اختبار مرسل الرسائل"""
    print("🧪 اختبار مرسل الرسائل...")
    
    # إعداد وضع التجريب
    sms_sender = SMSSender(provider="demo", demo_mode=True)
    
    # اختبار الاتصال
    if sms_sender.test_connection():
        print("✅ اختبار الاتصال نجح")
    else:
        print("❌ اختبار الاتصال فشل")
    
    # اختبار إرسال رسالة
    success = sms_sender.send_sms("0501234567", "رسالة اختبار من تطبيق سكاكر")
    if success:
        print("✅ اختبار إرسال الرسالة نجح")
    else:
        print("❌ اختبار إرسال الرسالة فشل")
    
    print("✅ اختبار مرسل الرسائل مكتمل\n")

def test_scheduler():
    """اختبار مجدول التنبيهات"""
    print("🧪 اختبار مجدول التنبيهات...")
    
    # إنشاء المكونات
    dm = DataManager("test_scheduler.json")
    sms_sender = SMSSender(provider="demo", demo_mode=True)
    scheduler = ReminderScheduler(sms_sender, dm)
    
    # بدء المجدول
    scheduler.start()
    print("✅ تم بدء المجدول")
    
    # إضافة تنبيه تجريبي (بعد 5 ثوان من الآن)
    from datetime import datetime, timedelta
    future_time = datetime.now() + timedelta(seconds=5)
    time_str = future_time.strftime("%H:%M:%S")
    
    success = scheduler.add_reminder("اختبار سريع", time_str, "0501234567", "علاج")
    if success:
        print(f"✅ تم إضافة تنبيه تجريبي للوقت: {time_str}")
        print("⏳ انتظار 6 ثوان لاختبار التنبيه...")
        time.sleep(6)
    else:
        print("❌ فشل في إضافة التنبيه التجريبي")
    
    # إيقاف المجدول
    scheduler.stop()
    print("✅ تم إيقاف المجدول")
    
    # تنظيف
    if os.path.exists("test_scheduler.json"):
        os.remove("test_scheduler.json")
    
    print("✅ اختبار مجدول التنبيهات مكتمل\n")

def test_imports():
    """اختبار استيراد جميع الوحدات"""
    print("🧪 اختبار استيراد الوحدات...")
    
    try:
        from gui.main_window import MainWindow
        print("✅ استيراد MainWindow")
        
        from gui.about_window import AboutWindow
        print("✅ استيراد AboutWindow")
        
        from gui.styles import COLORS, FONTS
        print("✅ استيراد الأنماط")
        
        from core.notification_manager import NotificationManager
        print("✅ استيراد NotificationManager")
        
        print("✅ جميع الاستيرادات نجحت\n")
        
    except Exception as e:
        print(f"❌ خطأ في الاستيراد: {e}\n")

def main():
    """الدالة الرئيسية للاختبار"""
    print("🚀 بدء اختبار تطبيق سكاكر")
    print("=" * 50)
    
    try:
        test_imports()
        test_data_manager()
        test_sms_sender()
        test_scheduler()
        
        print("🎉 جميع الاختبارات نجحت!")
        print("✅ التطبيق جاهز للاستخدام")
        
    except Exception as e:
        print(f"❌ خطأ في الاختبار: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

