import threading
import time
import os
import sys

try:
    import tkinter as tk
    from tkinter import messagebox
    TKINTER_AVAILABLE = True
except ImportError:
    TKINTER_AVAILABLE = False

class NotificationManager:
    def __init__(self):
        self.notification_sound = True
        self.notification_popup = True
    
    def show_notification(self, title: str, message: str, notification_type: str = "info"):
        """عرض تنبيه للمستخدم"""
        try:
            # تشغيل الصوت
            if self.notification_sound:
                self.play_notification_sound(notification_type)
            
            # عرض النافذة المنبثقة
            if self.notification_popup:
                self.show_popup_notification(title, message, notification_type)
                
        except Exception as e:
            print(f"خطأ في عرض التنبيه: {e}")
    
    def play_notification_sound(self, notification_type: str):
        """تشغيل صوت التنبيه"""
        try:
            if sys.platform == "win32":
                import winsound
                if notification_type == "success":
                    winsound.MessageBeep(winsound.MB_OK)
                elif notification_type == "error":
                    winsound.MessageBeep(winsound.MB_ICONHAND)
                else:
                    winsound.MessageBeep(winsound.MB_ICONASTERISK)
            elif sys.platform == "darwin":  # macOS
                os.system("afplay /System/Library/Sounds/Glass.aiff")
            else:  # Linux
                os.system("paplay /usr/share/sounds/alsa/Front_Left.wav 2>/dev/null || echo -e '\\a'")
        except Exception as e:
            print(f"خطأ في تشغيل الصوت: {e}")
    
    def show_popup_notification(self, title: str, message: str, notification_type: str):
        """عرض نافذة منبثقة"""
        def show_popup():
            try:
                if not TKINTER_AVAILABLE:
                    # عرض في وحدة التحكم إذا لم يكن tkinter متوفر
                    print(f"\n🔔 {title}")
                    print(f"📝 {message}")
                    print("=" * 50)
                    return
                
                root = tk.Tk()
                root.withdraw()  # إخفاء النافذة الرئيسية
                
                if notification_type == "success":
                    messagebox.showinfo(title, message)
                elif notification_type == "error":
                    messagebox.showerror(title, message)
                elif notification_type == "warning":
                    messagebox.showwarning(title, message)
                else:
                    messagebox.showinfo(title, message)
                
                root.destroy()
            except Exception as e:
                print(f"خطأ في عرض النافذة المنبثقة: {e}")
                # عرض في وحدة التحكم كبديل
                print(f"\n🔔 {title}")
                print(f"📝 {message}")
                print("=" * 50)
        
        # تشغيل النافذة في thread منفصل
        thread = threading.Thread(target=show_popup, daemon=True)
        thread.start()
    
    def show_reminder_notification(self, reminder_name: str, reminder_type: str):
        """عرض تنبيه خاص بالتذكير"""
        if reminder_type == "علاج":
            title = "🔔 تذكير دواء"
            message = f"حان وقت أخذ العلاج:\n{reminder_name}\n\nلا تنس أخذ دوائك في الوقت المحدد!"
        elif reminder_type == "كارب":
            title = "🔔 تذكير كارب"
            message = f"حان وقت عد الكارب:\n{reminder_name}\n\nتذكر مراقبة مستوى الكربوهيدرات!"
        else:
            title = "🔔 تذكير"
            message = f"تذكير: {reminder_name}"
        
        self.show_notification(title, message, "info")
    
    def set_sound_enabled(self, enabled: bool):
        """تفعيل أو إلغاء تفعيل الصوت"""
        self.notification_sound = enabled
    
    def set_popup_enabled(self, enabled: bool):
        """تفعيل أو إلغاء تفعيل النوافذ المنبثقة"""
        self.notification_popup = enabled

