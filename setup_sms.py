#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ملف إعداد خدمة SMS لتطبيق سكاكر
"""

import json
import os
from getpass import getpass

def setup_twilio():
    """إعداد خدمة Twilio"""
    print("=== إعداد خدمة Twilio ===")
    print("للحصول على هذه المعلومات:")
    print("1. اذهب إلى https://console.twilio.com/")
    print("2. سجل دخولك أو أنشئ حساب جديد")
    print("3. من لوحة التحكم، احصل على Account SID و Auth Token")
    print("4. اشتر رقم هاتف من Twilio لإرسال الرسائل")
    print()
    
    account_sid = input("أدخل Account SID: ").strip()
    auth_token = getpass("أدخل Auth Token: ").strip()
    from_number = input("أدخل رقم الهاتف المرسل (مثال: +1234567890): ").strip()
    
    return {
        "provider": "twilio",
        "account_sid": account_sid,
        "auth_token": auth_token,
        "from_number": from_number
    }

def setup_local_service():
    """إعداد خدمة محلية"""
    print("=== إعداد خدمة محلية ===")
    print("اختر الخدمة المحلية:")
    print("1. Taqnyat")
    print("2. ConnectSaudi")
    print("3. أخرى")
    
    choice = input("اختر الخدمة (1-3): ").strip()
    
    if choice == "1":
        api_key = getpass("أدخل API Key من Taqnyat: ").strip()
        sender_name = input("أدخل اسم المرسل: ").strip() or "سكاكر"
        return {
            "provider": "local",
            "api_key": api_key,
            "sender_name": sender_name,
            "service_url": "https://api.taqnyat.sa/v1/messages"
        }
    elif choice == "2":
        api_key = getpass("أدخل API Key من ConnectSaudi: ").strip()
        sender_name = input("أدخل اسم المرسل: ").strip() or "سكاكر"
        return {
            "provider": "local",
            "api_key": api_key,
            "sender_name": sender_name,
            "service_url": "https://connectsaudi.com/api/sms"
        }
    else:
        api_key = getpass("أدخل API Key: ").strip()
        sender_name = input("أدخل اسم المرسل: ").strip() or "سكاكر"
        service_url = input("أدخل رابط الخدمة: ").strip()
        return {
            "provider": "local",
            "api_key": api_key,
            "sender_name": sender_name,
            "service_url": service_url
        }

def setup_demo_mode():
    """إعداد وضع التجريب (بدون إرسال حقيقي)"""
    print("=== وضع التجريب ===")
    print("في هذا الوضع، سيتم عرض الرسائل في وحدة التحكم بدلاً من إرسالها")
    
    return {
        "provider": "demo",
        "demo_mode": True
    }

def main():
    """الدالة الرئيسية لإعداد SMS"""
    print("مرحباً بك في إعداد خدمة SMS لتطبيق سكاكر")
    print("=" * 50)
    
    print("اختر نوع الخدمة:")
    print("1. Twilio (خدمة عالمية)")
    print("2. خدمة محلية سعودية")
    print("3. وضع التجريب (بدون إرسال حقيقي)")
    
    choice = input("اختر الخدمة (1-3): ").strip()
    
    if choice == "1":
        sms_config = setup_twilio()
    elif choice == "2":
        sms_config = setup_local_service()
    elif choice == "3":
        sms_config = setup_demo_mode()
    else:
        print("اختيار غير صحيح!")
        return
    
    # تحديث ملف الإعدادات
    config_path = os.path.join("config", "settings.json")
    
    try:
        # قراءة الإعدادات الحالية
        if os.path.exists(config_path):
            with open(config_path, 'r', encoding='utf-8') as f:
                config = json.load(f)
        else:
            config = {}

        # تحديث إعدادات SMS
        config["sms_api"] = sms_config
        
        # حفظ الإعدادات
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)

        print()
        print("✅ تم حفظ إعدادات SMS بنجاح!")
        print(f"📁 الملف: {config_path}")
        
        # اختبار الإعدادات
        test_choice = input("هل تريد اختبار الإعدادات؟ (y/n): ").strip().lower()
        if test_choice == 'y':
            test_sms_config(sms_config)
            
    except Exception as e:
        print(f"❌ خطأ في حفظ الإعدادات: {e}")

def test_sms_config(sms_config):
    """اختبار إعدادات SMS"""
    try:
        from core.sms_sender import SMSSender
        
        # إنشاء مرسل الرسائل
        sms_sender = SMSSender(**sms_config)
        
        # اختبار الاتصال
        if sms_sender.test_connection():
            print("✅ تم الاتصال بخدمة SMS بنجاح!")
            
            # اختبار إرسال رسالة
            test_choice = input("هل تريد إرسال رسالة تجريبية؟ (y/n): ").strip().lower()
            if test_choice == 'y':
                phone = input("أدخل رقم الهاتف للاختبار: ").strip()
                message = "رسالة تجريبية من تطبيق سكاكر 🔔"
                
                if sms_sender.send_sms(phone, message):
                    print("✅ تم إرسال الرسالة التجريبية بنجاح!")
                else:
                    print("❌ فشل في إرسال الرسالة التجريبية")
        else:
            print("❌ فشل في الاتصال بخدمة SMS")
            
    except Exception as e:
        print(f"❌ خطأ في اختبار الإعدادات: {e}")

if __name__ == "__main__":
    main()

