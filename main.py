#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
تطبيق سكاكر - تنبيهات العلاجات والكارب
المطورة: بدور الدوسري
الإصدار: 1.0.0
"""

import customtkinter as ctk # type: ignore
import json
import os
import sys
from tkinter import messagebox
import threading
import signal

# إضافة مسار المشروع
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.data_manager import DataManager
from core.sms_sender import SMSSender
from core.scheduler import ReminderScheduler
from gui.main_window import MainWindow
from gui.about_window import AboutWindow
from gui.styles import COLORS, WINDOW

class SukarApp:
    def __init__(self):
        self.setup_app()
        self.load_config()
        self.init_components()
        self.create_main_window()
        self.setup_signal_handlers()
    
    def setup_app(self):
        """إعداد التطبيق الأساسي"""
        # إعداد CustomTkinter
        ctk.set_appearance_mode("light")  # أو "dark" أو "system"
        ctk.set_default_color_theme("blue")
        
        # إنشاء النافذة الرئيسية
        self.root = ctk.CTk()
        self.root.title("تطبيق سكاكر - تنبيهات العلاجات والكارب")
        self.root.geometry(f"{WINDOW['default_width']}x{WINDOW['default_height']}")
        self.root.minsize(WINDOW['min_width'], WINDOW['min_height'])
        
        # تعيين أيقونة التطبيق
        self.set_app_icon()
        
        # متغير لتتبع الصفحة الحالية
        self.current_page = "main"
    
    def set_app_icon(self):
        """تعيين أيقونة التطبيق"""
        try:
            icon_path = os.path.join("assets", "sukar_logo.png")
            if os.path.exists(icon_path):
                self.root.iconbitmap(icon_path)
        except Exception as e:
            print(f"تعذر تحميل أيقونة التطبيق: {e}")
    
    def load_config(self):
        """تحميل إعدادات التطبيق"""
        config_path = os.path.join("config", "settings.json")
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
        except Exception as e:
            print(f"خطأ في تحميل الإعدادات: {e}")
            # إعدادات افتراضية
            self.config = {
                "app_name": "سكاكر",
                "version": "1.0.0",
                "author": "بدور الدوسري",
                "sms_api": {
                    "provider": "twilio",
                    "account_sid": "",
                    "auth_token": "",
                    "from_number": ""
                }
            }
    
    def init_components(self):
        """تهيئة مكونات التطبيق"""
        try:
            # إنشاء مدير البيانات
            self.data_manager = DataManager()
            
            # إنشاء مرسل الرسائل
            sms_config = self.config.get("sms_api", {})
            # التأكد من وجود provider في الإعدادات
            if "provider" not in sms_config:
                sms_config["provider"] = "twilio"
            self.sms_sender = SMSSender(**sms_config)
            
            # إنشاء مجدول التنبيهات
            self.scheduler = ReminderScheduler(self.sms_sender, self.data_manager)
            
            # بدء المجدول
            self.scheduler.start()
            
        except Exception as e:
            messagebox.showerror("خطأ", f"فشل في تهيئة التطبيق: {e}")
            sys.exit(1)
    
    def create_main_window(self):
        """إنشاء النافذة الرئيسية"""
        # إطار التنقل
        self.create_navigation()
        
        # إطار المحتوى
        self.content_frame = ctk.CTkFrame(self.root)
        self.content_frame.pack(fill="both", expand=True)
        
        # عرض الصفحة الرئيسية
        self.show_main_page()
    
    def create_navigation(self):
        """إنشاء شريط التنقل"""
        nav_frame = ctk.CTkFrame(self.root, height=60)
        nav_frame.pack(fill="x", padx=10, pady=(10, 0))
        nav_frame.pack_propagate(False)
        
        # أزرار التنقل
        main_button = ctk.CTkButton(
            nav_frame,
            text="الصفحة الرئيسية",
            command=self.show_main_page,
            fg_color=COLORS["primary"] if self.current_page == "main" else COLORS["bg_secondary"],
            text_color=COLORS["text_light"] if self.current_page == "main" else COLORS["text_primary"],
            hover_color=COLORS["hover"]
        )
        main_button.pack(side="left", padx=10, pady=10)
        
        about_button = ctk.CTkButton(
            nav_frame,
            text="نبذة عن التطبيق",
            command=self.show_about_page,
            fg_color=COLORS["primary"] if self.current_page == "about" else COLORS["bg_secondary"],
            text_color=COLORS["text_light"] if self.current_page == "about" else COLORS["text_primary"],
            hover_color=COLORS["hover"]
        )
        about_button.pack(side="left", padx=10, pady=10)
        
        # معلومات التطبيق في الجانب الأيمن
        info_label = ctk.CTkLabel(
            nav_frame,
            text=f"{self.config['app_name']} v{self.config['version']} - {self.config['author']}",
            text_color=COLORS["text_secondary"]
        )
        info_label.pack(side="right", padx=20, pady=10)
    
    def show_main_page(self):
        """عرض الصفحة الرئيسية"""
        self.current_page = "main"
        self.clear_content()
        self.main_window = MainWindow(self.content_frame, self.scheduler, self.data_manager)
        self.update_navigation()
    
    def show_about_page(self):
        """عرض صفحة نبذة عن التطبيق"""
        self.current_page = "about"
        self.clear_content()
        self.about_window = AboutWindow(self.content_frame)
        self.update_navigation()
    
    def clear_content(self):
        """مسح محتوى الإطار"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()
    
    def update_navigation(self):
        """تحديث شريط التنقل"""
        # إعادة إنشاء شريط التنقل لتحديث الألوان
        for widget in self.root.winfo_children():
            if isinstance(widget, ctk.CTkFrame) and widget != self.content_frame:
                widget.destroy()
                break
        self.create_navigation()
    
    def setup_signal_handlers(self):
        """إعداد معالجات الإشارات"""
        def signal_handler(signum, frame):
            self.on_closing()
        
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
    
    def on_closing(self):
        """معالج إغلاق التطبيق"""
        try:
            # إيقاف المجدول
            if hasattr(self, 'scheduler'):
                self.scheduler.stop()
            
            # حفظ البيانات
            if hasattr(self, 'data_manager'):
                self.data_manager.save_reminders()
            
            print("تم إغلاق التطبيق بنجاح")
            
        except Exception as e:
            print(f"خطأ أثناء إغلاق التطبيق: {e}")
        
        finally:
            self.root.quit()
            self.root.destroy()
    
    def run(self):
        """تشغيل التطبيق"""
        try:
            # ربط حدث الإغلاق
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
            
            # تشغيل الحلقة الرئيسية
            self.root.mainloop()
            
        except KeyboardInterrupt:
            self.on_closing()
        except Exception as e:
            messagebox.showerror("خطأ", f"خطأ في تشغيل التطبيق: {e}")
            self.on_closing()

def main():
    """الدالة الرئيسية"""
    try:
        # التأكد من وجود المجلدات المطلوبة
        os.makedirs("assets", exist_ok=True)
        os.makedirs("config", exist_ok=True)
        
        # إنشاء وتشغيل التطبيق
        app = SukarApp()
        app.run()
        
    except Exception as e:
        print(f"خطأ في بدء التطبيق: {e}")
        messagebox.showerror("خطأ", f"فشل في بدء التطبيق: {e}")

if __name__ == "__main__":
    main()

