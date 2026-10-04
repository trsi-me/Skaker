import json
import os
from datetime import datetime
from typing import List, Dict, Any

class DataManager:
    def __init__(self, data_file: str = "reminders.json"):
        self.data_file = data_file
        self.reminders = []
        self.load_reminders()
    
    def load_reminders(self):
        """تحميل التنبيهات من الملف"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.reminders = json.load(f)
            except Exception as e:
                print(f"خطأ في تحميل البيانات: {e}")
                self.reminders = []
        else:
            self.reminders = []
    
    def save_reminders(self):
        """حفظ التنبيهات في الملف"""
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(self.reminders, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"خطأ في حفظ البيانات: {e}")
    
    def add_reminder(self, name: str, time_str: str, phone: str, reminder_type: str = "علاج") -> str:
        """إضافة تنبيه جديد"""
        reminder_id = f"reminder_{len(self.reminders) + 1}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        reminder = {
            "id": reminder_id,
            "name": name,
            "time": time_str,
            "phone": phone,
            "type": reminder_type,
            "active": True,
            "created_at": datetime.now().isoformat(),
            "last_sent": None
        }
        
        self.reminders.append(reminder)
        self.save_reminders()
        return reminder_id
    
    def get_reminders(self) -> List[Dict[str, Any]]:
        """الحصول على جميع التنبيهات"""
        return self.reminders
    
    def get_active_reminders(self) -> List[Dict[str, Any]]:
        """الحصول على التنبيهات النشطة فقط"""
        return [r for r in self.reminders if r.get("active", True)]
    
    def update_reminder(self, reminder_id: str, **kwargs):
        """تحديث تنبيه موجود"""
        for reminder in self.reminders:
            if reminder["id"] == reminder_id:
                reminder.update(kwargs)
                self.save_reminders()
                return True
        return False
    
    def delete_reminder(self, reminder_id: str):
        """حذف تنبيه"""
        self.reminders = [r for r in self.reminders if r["id"] != reminder_id]
        self.save_reminders()
    
    def mark_as_sent(self, reminder_id: str):
        """تسجيل أن التنبيه تم إرساله"""
        self.update_reminder(reminder_id, last_sent=datetime.now().isoformat())

