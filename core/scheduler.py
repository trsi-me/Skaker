from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from datetime import datetime, time
import logging
from .sms_sender import SMSSender
from .data_manager import DataManager
from .notification_manager import NotificationManager

class ReminderScheduler:
    def __init__(self, sms_sender: SMSSender, data_manager: DataManager):
        self.scheduler = BackgroundScheduler()
        self.sms_sender = sms_sender
        self.data_manager = data_manager
        self.notification_manager = NotificationManager()
        self.setup_logging()
        
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
    
    def start(self):
        """بدء نظام الجدولة"""
        try:
            self.scheduler.start()
            self.logger.info("تم بدء نظام الجدولة")
            # تحميل التنبيهات الموجودة
            self.load_existing_reminders()
        except Exception as e:
            self.logger.error(f"خطأ في بدء نظام الجدولة: {e}")
    
    def stop(self):
        """إيقاف نظام الجدولة"""
        try:
            self.scheduler.shutdown()
            self.logger.info("تم إيقاف نظام الجدولة")
        except Exception as e:
            self.logger.error(f"خطأ في إيقاف نظام الجدولة: {e}")
    
    def load_existing_reminders(self):
        """تحميل التنبيهات الموجودة وجدولتها"""
        reminders = self.data_manager.get_active_reminders()
        for reminder in reminders:
            self.schedule_reminder(reminder)
    
    def parse_time_string(self, time_str: str) -> tuple:
        """تحليل نص الوقت وإرجاع (ساعة، دقيقة، ثانية)"""
        try:
            # تنسيقات مختلفة للوقت
            if ':' in time_str:
                parts = time_str.split(':')
                hour = int(parts[0])
                minute = int(parts[1]) if len(parts) > 1 else 0
                second = int(parts[2]) if len(parts) > 2 else 0
            else:
                # إذا كان الوقت بصيغة أخرى
                hour = int(time_str) if time_str.isdigit() else 12
                minute = 0
                second = 0
            
            return hour, minute, second
        except:
            # قيم افتراضية في حالة الخطأ
            return 12, 0, 0
    
    def schedule_reminder(self, reminder: dict):
        """جدولة تنبيه واحد"""
        try:
            reminder_id = reminder['id']
            time_str = reminder['time']
            
            # تحليل الوقت
            hour, minute, second = self.parse_time_string(time_str)
            
            # إنشاء trigger للتنبيه اليومي
            trigger = CronTrigger(
                hour=hour,
                minute=minute,
                second=second
            )
            
            # إضافة المهمة للجدولة
            self.scheduler.add_job(
                func=self.send_reminder,
                trigger=trigger,
                args=[reminder],
                id=reminder_id,
                replace_existing=True,
                name=f"تنبيه: {reminder['name']}"
            )
            
            self.logger.info(f"تم جدولة التنبيه: {reminder['name']} في {time_str}")
            
        except Exception as e:
            self.logger.error(f"خطأ في جدولة التنبيه {reminder.get('name', 'غير معروف')}: {e}")
    
    def send_reminder(self, reminder: dict):
        """إرسال التنبيه"""
        try:
            name = reminder['name']
            phone = reminder['phone']
            reminder_type = reminder.get('type', 'تنبيه')
            
            # عرض تنبيه محلي
            self.notification_manager.show_reminder_notification(name, reminder_type)
            
            # إنشاء نص الرسالة
            if reminder_type == "علاج":
                message = f"🔔 تذكير من تطبيق سكاكر\n\nحان وقت أخذ العلاج: {name}\n\nلا تنس أخذ دوائك في الوقت المحدد للحفاظ على صحتك.\n\nمع تحيات تطبيق سكاكر 💊"
            elif reminder_type == "كارب":
                message = f"🔔 تذكير من تطبيق سكاكر\n\nحان وقت عد الكارب: {name}\n\nتذكر مراقبة مستوى الكربوهيدرات للحفاظ على صحتك.\n\nمع تحيات تطبيق سكاكر 🍎"
            else:
                message = f"🔔 تذكير من تطبيق سكاكر\n\n{name}\n\nمع تحيات تطبيق سكاكر"
            
            # إرسال الرسالة
            success = self.sms_sender.send_sms(phone, message)
            
            if success:
                # تسجيل أن التنبيه تم إرساله
                self.data_manager.mark_as_sent(reminder['id'])
                self.logger.info(f"تم إرسال التنبيه بنجاح: {name} إلى {phone}")
                
                # عرض تنبيه نجاح الإرسال
                self.notification_manager.show_notification(
                    "تم الإرسال", 
                    f"تم إرسال تنبيه '{name}' بنجاح", 
                    "success"
                )
            else:
                self.logger.error(f"فشل في إرسال التنبيه: {name} إلى {phone}")
                
                # عرض تنبيه فشل الإرسال
                self.notification_manager.show_notification(
                    "فشل الإرسال", 
                    f"فشل في إرسال تنبيه '{name}'", 
                    "error"
                )
                
        except Exception as e:
            self.logger.error(f"خطأ في إرسال التنبيه: {e}")
            self.notification_manager.show_notification(
                "خطأ", 
                f"حدث خطأ في إرسال التنبيه: {e}", 
                "error"
            )
    
    def add_reminder(self, name: str, time_str: str, phone: str, reminder_type: str = "علاج"):
        """إضافة تنبيه جديد وجدولته"""
        try:
            # إضافة التنبيه للبيانات
            reminder_id = self.data_manager.add_reminder(name, time_str, phone, reminder_type)
            
            # الحصول على التنبيه المضاف
            reminders = self.data_manager.get_reminders()
            reminder = next((r for r in reminders if r['id'] == reminder_id), None)
            
            if reminder:
                # جدولة التنبيه
                self.schedule_reminder(reminder)
                return True
            
        except Exception as e:
            self.logger.error(f"خطأ في إضافة التنبيه: {e}")
            return False
    
    def remove_reminder(self, reminder_id: str):
        """إزالة تنبيه من الجدولة والبيانات"""
        try:
            # إزالة من الجدولة
            if self.scheduler.get_job(reminder_id):
                self.scheduler.remove_job(reminder_id)
            
            # إزالة من البيانات
            self.data_manager.delete_reminder(reminder_id)
            
            self.logger.info(f"تم حذف التنبيه: {reminder_id}")
            return True
            
        except Exception as e:
            self.logger.error(f"خطأ في حذف التنبيه: {e}")
            return False
    
    def get_scheduled_jobs(self):
        """الحصول على قائمة المهام المجدولة"""
        return self.scheduler.get_jobs()

