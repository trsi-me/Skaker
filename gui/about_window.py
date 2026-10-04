import customtkinter as ctk
from .styles import COLORS, FONTS, BUTTON_STYLES, LABEL_STYLES, FRAME_STYLES
import os

class AboutWindow:
    def __init__(self, parent):
        self.parent = parent
        self.create_widgets()
    
    def create_widgets(self):
        """إنشاء عناصر صفحة نبذة عن التطبيق"""
        # إطار رئيسي
        self.main_frame = ctk.CTkFrame(
            self.parent,
            **FRAME_STYLES["main"]
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # إطار المحتوى
        self.content_frame = ctk.CTkFrame(
            self.main_frame,
            **FRAME_STYLES["card"]
        )
        self.content_frame.pack(fill="both", expand=True, padx=30, pady=30)
        
        # شعار التطبيق
        self.create_logo()
        
        # عنوان التطبيق
        self.app_title = ctk.CTkLabel(
            self.content_frame,
            text="تطبيق سكاكر",
            **LABEL_STYLES["title"]
        )
        self.app_title.pack(pady=(20, 10))
        
        # وصف التطبيق
        self.app_description = ctk.CTkLabel(
            self.content_frame,
            text="تطبيق احترافي لإرسال تنبيهات مواعيد العلاجات وعد الكارب",
            **LABEL_STYLES["heading"]
        )
        self.app_description.pack(pady=(0, 30))
        
        # معلومات التطبيق
        self.create_info_section()
        
        # معلومات المطورة
        self.create_developer_section()
        
        # ميزات التطبيق
        self.create_features_section()
    
    def create_logo(self):
        """إنشاء شعار التطبيق"""
        try:
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sukar_logo.png")
            if os.path.exists(logo_path):
                logo_image = ctk.CTkImage(
                    light_image=ctk.CTkImage.open(logo_path),
                    dark_image=ctk.CTkImage.open(logo_path),
                    size=(100, 100)
                )
                self.logo_label = ctk.CTkLabel(
                    self.content_frame,
                    image=logo_image,
                    text=""
                )
                self.logo_label.pack(pady=(20, 0))
        except Exception as e:
            print(f"خطأ في تحميل الشعار: {e}")
    
    def create_info_section(self):
        """إنشاء قسم معلومات التطبيق"""
        info_frame = ctk.CTkFrame(
            self.content_frame,
            fg_color="transparent"
        )
        info_frame.pack(fill="x", pady=(0, 20))
        
        # الإصدار
        version_label = ctk.CTkLabel(
            info_frame,
            text="الإصدار: 1.0.0",
            **LABEL_STYLES["body"]
        )
        version_label.pack(pady=5)
        
        # تاريخ الإصدار
        date_label = ctk.CTkLabel(
            info_frame,
            text="تاريخ الإصدار: يوليو 2025",
            **LABEL_STYLES["body"]
        )
        date_label.pack(pady=5)
    
    def create_developer_section(self):
        """إنشاء قسم معلومات المطورة"""
        dev_frame = ctk.CTkFrame(
            self.content_frame,
            **FRAME_STYLES["card"]
        )
        dev_frame.pack(fill="x", pady=(0, 20), padx=20)
        
        # عنوان القسم
        dev_title = ctk.CTkLabel(
            dev_frame,
            text="معلومات المطورة",
            **LABEL_STYLES["heading"]
        )
        dev_title.pack(pady=(15, 10))
        
        # اسم المطورة
        dev_name = ctk.CTkLabel(
            dev_frame,
            text="الطالبة: بدور الدوسري",
            **LABEL_STYLES["body"]
        )
        dev_name.pack(pady=5)
        
        # حقوق النشر
        copyright_label = ctk.CTkLabel(
            dev_frame,
            text="© 2025 جميع الحقوق محفوظة",
            **LABEL_STYLES["small"]
        )
        copyright_label.pack(pady=(5, 15))
    
    def create_features_section(self):
        """إنشاء قسم ميزات التطبيق"""
        features_frame = ctk.CTkFrame(
            self.content_frame,
            **FRAME_STYLES["card"]
        )
        features_frame.pack(fill="both", expand=True, padx=20)
        
        # عنوان القسم
        features_title = ctk.CTkLabel(
            features_frame,
            text="ميزات التطبيق",
            **LABEL_STYLES["heading"]
        )
        features_title.pack(pady=(15, 10))
        
        # قائمة الميزات
        features = [
            "📱 واجهة مستخدم عصرية وسهلة الاستخدام",
            "💊 تنبيهات مواعيد العلاجات",
            "🍎 تذكير بعد الكربوهيدرات",
            "📲 إرسال رسائل SMS حقيقية",
            "⏰ جدولة مرنة للتنبيهات",
            "🔔 تنبيهات صوتية ومرئية",
            "💾 حفظ البيانات محلياً",
            "🔒 أمان وخصوصية البيانات"
        ]
        
        # إطار قابل للتمرير للميزات
        scrollable_frame = ctk.CTkScrollableFrame(
            features_frame,
            height=200
        )
        scrollable_frame.pack(fill="both", expand=True, padx=15, pady=(0, 15))
        
        for feature in features:
            feature_label = ctk.CTkLabel(
                scrollable_frame,
                text=feature,
                **LABEL_STYLES["body"],
                anchor="w"
            )
            feature_label.pack(fill="x", pady=3, padx=10)

