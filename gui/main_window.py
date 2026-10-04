import customtkinter as ctk
from tkinter import messagebox
from .styles import COLORS, FONTS, BUTTON_STYLES, LABEL_STYLES, FRAME_STYLES, INPUT_STYLES
import os
from datetime import datetime

class MainWindow:
    def __init__(self, parent, scheduler, data_manager):
        self.parent = parent
        self.scheduler = scheduler
        self.data_manager = data_manager
        self.create_widgets()
    
    def create_widgets(self):
        """إنشاء عناصر الصفحة الرئيسية"""
        # إطار رئيسي
        self.main_frame = ctk.CTkFrame(
            self.parent,
            **FRAME_STYLES["main"]
        )
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # إنشاء الأقسام
        self.create_header()
        self.create_add_reminder_section()
        self.create_reminders_list_section()
    
    def create_header(self):
        """إنشاء رأس الصفحة"""
        header_frame = ctk.CTkFrame(
            self.main_frame,
            **FRAME_STYLES["card"]
        )
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        # شعار التطبيق
        self.create_logo(header_frame)
        
        # عنوان التطبيق
        title_label = ctk.CTkLabel(
            header_frame,
            text="تطبيق سكاكر - تنبيهات العلاجات والكارب",
            **LABEL_STYLES["title"]
        )
        title_label.pack(pady=(10, 20))
    
    def create_logo(self, parent):
        """إنشاء شعار التطبيق"""
        try:
            from PIL import Image
            logo_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets", "sukar_logo.png")
            if os.path.exists(logo_path):
                # فتح الصورة باستخدام PIL
                pil_image = Image.open(logo_path)
                logo_image = ctk.CTkImage(
                    light_image=pil_image,
                    dark_image=pil_image,
                    size=(80, 80)
                )
                logo_label = ctk.CTkLabel(
                    parent,
                    image=logo_image,
                    text=""
                )
                logo_label.pack(pady=(20, 0))
        except Exception as e:
            print(f"خطأ في تحميل الشعار: {e}")
            # إنشاء تسمية نصية بدلاً من الصورة
            logo_label = ctk.CTkLabel(
                parent,
                text="🍬 سكاكر",
                font=("Arial", 24, "bold"),
                text_color=COLORS["primary"]
            )
            logo_label.pack(pady=(20, 0))
    
    def create_add_reminder_section(self):
        """إنشاء قسم إضافة التنبيهات"""
        add_frame = ctk.CTkFrame(
            self.main_frame,
            **FRAME_STYLES["card"]
        )
        add_frame.pack(fill="x", padx=20, pady=10)
        
        # عنوان القسم
        section_title = ctk.CTkLabel(
            add_frame,
            text="إضافة تنبيه جديد",
            **LABEL_STYLES["heading"]
        )
        section_title.pack(pady=(20, 15))
        
        # إطار النموذج
        form_frame = ctk.CTkFrame(
            add_frame,
            fg_color="transparent"
        )
        form_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # الصف الأول: اسم التنبيه ونوعه
        row1_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row1_frame.pack(fill="x", pady=(0, 15))
        
        # اسم التنبيه
        name_frame = ctk.CTkFrame(row1_frame, fg_color="transparent")
        name_frame.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        name_label = ctk.CTkLabel(name_frame, text="اسم التنبيه:", **LABEL_STYLES["body"])
        name_label.pack(anchor="w", pady=(0, 5))
        
        self.name_entry = ctk.CTkEntry(
            name_frame,
            placeholder_text="مثال: أخذ علاج الضغط",
            **INPUT_STYLES["default"]
        )
        self.name_entry.pack(fill="x")
        
        # نوع التنبيه
        type_frame = ctk.CTkFrame(row1_frame, fg_color="transparent")
        type_frame.pack(side="right", padx=(10, 0))
        
        type_label = ctk.CTkLabel(type_frame, text="نوع التنبيه:", **LABEL_STYLES["body"])
        type_label.pack(anchor="w", pady=(0, 5))
        
        self.type_var = ctk.StringVar(value="علاج")
        self.type_menu = ctk.CTkOptionMenu(
            type_frame,
            values=["علاج", "كارب"],
            variable=self.type_var,
            **INPUT_STYLES["default"]
        )
        self.type_menu.pack()
        
        # الصف الثاني: الوقت
        row2_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row2_frame.pack(fill="x", pady=(0, 15))
        
        time_label = ctk.CTkLabel(row2_frame, text="وقت التنبيه:", **LABEL_STYLES["body"])
        time_label.pack(anchor="w", pady=(0, 5))
        
        # إطار الوقت
        time_frame = ctk.CTkFrame(row2_frame, fg_color="transparent")
        time_frame.pack(fill="x")
        
        # الساعة
        hour_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        hour_frame.pack(side="left", padx=(0, 10))
        
        hour_label = ctk.CTkLabel(hour_frame, text="الساعة:", **LABEL_STYLES["small"])
        hour_label.pack()
        
        self.hour_var = ctk.StringVar(value="12")
        self.hour_menu = ctk.CTkOptionMenu(
            hour_frame,
            values=[f"{i:02d}" for i in range(24)],
            variable=self.hour_var,
            width=80
        )
        self.hour_menu.pack()
        
        # الدقيقة
        minute_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        minute_frame.pack(side="left", padx=(0, 10))
        
        minute_label = ctk.CTkLabel(minute_frame, text="الدقيقة:", **LABEL_STYLES["small"])
        minute_label.pack()
        
        self.minute_var = ctk.StringVar(value="00")
        self.minute_menu = ctk.CTkOptionMenu(
            minute_frame,
            values=[f"{i:02d}" for i in range(60)],
            variable=self.minute_var,
            width=80
        )
        self.minute_menu.pack()
        
        # الثانية
        second_frame = ctk.CTkFrame(time_frame, fg_color="transparent")
        second_frame.pack(side="left")
        
        second_label = ctk.CTkLabel(second_frame, text="الثانية:", **LABEL_STYLES["small"])
        second_label.pack()
        
        self.second_var = ctk.StringVar(value="00")
        self.second_menu = ctk.CTkOptionMenu(
            second_frame,
            values=[f"{i:02d}" for i in range(60)],
            variable=self.second_var,
            width=80
        )
        self.second_menu.pack()
        
        # الصف الثالث: رقم الجوال
        row3_frame = ctk.CTkFrame(form_frame, fg_color="transparent")
        row3_frame.pack(fill="x", pady=(0, 20))
        
        phone_label = ctk.CTkLabel(row3_frame, text="رقم الجوال:", **LABEL_STYLES["body"])
        phone_label.pack(anchor="w", pady=(0, 5))
        
        self.phone_entry = ctk.CTkEntry(
            row3_frame,
            placeholder_text="مثال: 0501234567 أو +966501234567",
            **INPUT_STYLES["default"]
        )
        self.phone_entry.pack(fill="x")
        
        # زر الإضافة
        add_button = ctk.CTkButton(
            add_frame,
            text="إضافة التنبيه",
            command=self.add_reminder,
            **BUTTON_STYLES["primary"]
        )
        add_button.pack(pady=(0, 20))
    
    def create_reminders_list_section(self):
        """إنشاء قسم قائمة التنبيهات"""
        list_frame = ctk.CTkFrame(
            self.main_frame,
            **FRAME_STYLES["card"]
        )
        list_frame.pack(fill="both", expand=True, padx=20, pady=(10, 20))
        
        # عنوان القسم
        section_title = ctk.CTkLabel(
            list_frame,
            text="التنبيهات المجدولة",
            **LABEL_STYLES["heading"]
        )
        section_title.pack(pady=(20, 15))
        
        # إطار قابل للتمرير
        self.scrollable_frame = ctk.CTkScrollableFrame(
            list_frame,
            height=200
        )
        self.scrollable_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        
        # تحديث قائمة التنبيهات
        self.update_reminders_list()
        
        # زر تحديث
        refresh_button = ctk.CTkButton(
            list_frame,
            text="تحديث القائمة",
            command=self.update_reminders_list,
            **BUTTON_STYLES["secondary"]
        )
        refresh_button.pack(pady=(0, 20))
    
    def add_reminder(self):
        """إضافة تنبيه جديد"""
        try:
            # التحقق من البيانات
            name = self.name_entry.get().strip()
            phone = self.phone_entry.get().strip()
            reminder_type = self.type_var.get()
            
            if not name:
                messagebox.showerror("خطأ", "يرجى إدخال اسم التنبيه")
                return
            
            if not phone:
                messagebox.showerror("خطأ", "يرجى إدخال رقم الجوال")
                return
            
            # تكوين الوقت
            hour = self.hour_var.get()
            minute = self.minute_var.get()
            second = self.second_var.get()
            time_str = f"{hour}:{minute}:{second}"
            
            # إضافة التنبيه
            success = self.scheduler.add_reminder(name, time_str, phone, reminder_type)
            
            if success:
                messagebox.showinfo("نجح", "تم إضافة التنبيه بنجاح!")
                # مسح النموذج
                self.clear_form()
                # تحديث القائمة
                self.update_reminders_list()
            else:
                messagebox.showerror("خطأ", "فشل في إضافة التنبيه")
                
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {e}")
    
    def clear_form(self):
        """مسح النموذج"""
        self.name_entry.delete(0, 'end')
        self.phone_entry.delete(0, 'end')
        self.type_var.set("علاج")
        self.hour_var.set("12")
        self.minute_var.set("00")
        self.second_var.set("00")
    
    def update_reminders_list(self):
        """تحديث قائمة التنبيهات"""
        # مسح القائمة الحالية
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        
        # الحصول على التنبيهات
        reminders = self.data_manager.get_active_reminders()
        
        if not reminders:
            no_reminders_label = ctk.CTkLabel(
                self.scrollable_frame,
                text="لا توجد تنبيهات مجدولة",
                **LABEL_STYLES["body"]
            )
            no_reminders_label.pack(pady=20)
            return
        
        # عرض التنبيهات
        for reminder in reminders:
            self.create_reminder_item(reminder)
    
    def create_reminder_item(self, reminder):
        """إنشاء عنصر تنبيه في القائمة"""
        item_frame = ctk.CTkFrame(
            self.scrollable_frame,
            **FRAME_STYLES["card"]
        )
        item_frame.pack(fill="x", pady=5, padx=10)
        
        # معلومات التنبيه
        info_frame = ctk.CTkFrame(item_frame, fg_color="transparent")
        info_frame.pack(side="left", fill="both", expand=True, padx=15, pady=10)
        
        # اسم التنبيه
        name_label = ctk.CTkLabel(
            info_frame,
            text=f"📋 {reminder['name']}",
            **LABEL_STYLES["body"],
            anchor="w"
        )
        name_label.pack(fill="x")
        
        # تفاصيل التنبيه
        details_text = f"⏰ {reminder['time']} | 📱 {reminder['phone']} | 🏷️ {reminder['type']}"
        details_label = ctk.CTkLabel(
            info_frame,
            text=details_text,
            **LABEL_STYLES["small"],
            anchor="w"
        )
        details_label.pack(fill="x")
        
        # زر الحذف
        delete_button = ctk.CTkButton(
            item_frame,
            text="حذف",
            command=lambda r_id=reminder['id']: self.delete_reminder(r_id),
            **BUTTON_STYLES["success"],
            width=80
        )
        delete_button.pack(side="right", padx=15, pady=10)
    
    def delete_reminder(self, reminder_id):
        """حذف تنبيه"""
        try:
            result = messagebox.askyesno("تأكيد الحذف", "هل أنت متأكد من حذف هذا التنبيه؟")
            if result:
                success = self.scheduler.remove_reminder(reminder_id)
                if success:
                    messagebox.showinfo("نجح", "تم حذف التنبيه بنجاح!")
                    self.update_reminders_list()
                else:
                    messagebox.showerror("خطأ", "فشل في حذف التنبيه")
        except Exception as e:
            messagebox.showerror("خطأ", f"حدث خطأ: {e}")

