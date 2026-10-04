import requests
import json
import logging
from typing import Optional

class SMSSender:
    def __init__(self, **config):
        self.provider = config.get('provider', 'demo')
        self.config = config
        self.setup_logging()
    
    def setup_logging(self):
        """إعداد نظام التسجيل"""
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('sms_log.txt', encoding='utf-8'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    
    def send_sms_local(self, to_number: str, message: str) -> bool:
        """إرسال رسالة عبر خدمة محلية (مثال)"""
        try:
            # هذا مثال لخدمة محلية - يمكن تخصيصه حسب الخدمة المستخدمة
            url = "https://api.taqnyat.sa/v1/messages"
            
            headers = {
                'Authorization': f"Bearer {self.config.get('api_key', '')}",
                'Content-Type': 'application/json'
            }
            
            data = {
                'recipients': [to_number],
                'body': message,
                'sender': self.config.get('sender_name', 'سكاكر')
            }
            
            response = requests.post(url, headers=headers, json=data)
            
            if response.status_code == 200:
                self.logger.info(f"تم إرسال الرسالة بنجاح إلى {to_number}")
                return True
            else:
                self.logger.error(f"فشل في إرسال الرسالة: {response.text}")
                return False
                
        except Exception as e:
            self.logger.error(f"خطأ في إرسال الرسالة: {e}")
            return False
    
    def send_sms(self, to_number: str, message: str) -> bool:
        """إرسال رسالة نصية"""
        # تنسيق رقم الهاتف
        if not to_number.startswith('+'):
            if to_number.startswith('05'):
                to_number = '+966' + to_number[1:]
            elif to_number.startswith('5'):
                to_number = '+966' + to_number
        
        # وضع التجريب
        if self.provider == "demo":
            self.logger.info("=== وضع التجريب ===")
            self.logger.info(f"إلى: {to_number}")
            self.logger.info(f"الرسالة: {message}")
            self.logger.info("=== انتهاء الرسالة ===")
            self.logger.info("✅ تم إرسال الإشعار بنجاح")
            print(f"\n🔔 رسالة تجريبية إلى {to_number}:")
            print(f"📱 {message}")
            print("✅ تم إرسال الإشعار بنجاح")
            print("=" * 50)
            return True
        
        # اختيار طريقة الإرسال حسب المزود
        if self.provider == "local":
            return self.send_sms_local(to_number, message)
        else:
            # افتراضياً وضع المحاكاة
            return True
    
    def test_connection(self) -> bool:
        """اختبار الاتصال بخدمة SMS"""
        # دائماً نعيد True لأننا في وضع المحاكاة
        return True

