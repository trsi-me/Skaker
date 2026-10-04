"""
ملف الأنماط والألوان لتطبيق سكاكر
"""

# الألوان الرئيسية
COLORS = {
    # الألوان الأساسية
    "primary": "#2E86AB",      # أزرق طبي
    "secondary": "#A23B72",    # وردي داكن
    "accent": "#F18F01",       # برتقالي
    "success": "#C73E1D",      # أحمر للتنبيهات المهمة
    
    # ألوان الخلفية
    "bg_primary": "#F5F5F5",   # خلفية رئيسية فاتحة
    "bg_secondary": "#FFFFFF", # خلفية ثانوية بيضاء
    "bg_dark": "#2B2B2B",      # خلفية داكنة
    
    # ألوان النصوص
    "text_primary": "#2B2B2B", # نص رئيسي داكن
    "text_secondary": "#666666", # نص ثانوي رمادي
    "text_light": "#FFFFFF",   # نص فاتح
    
    # ألوان الحدود
    "border": "#E0E0E0",       # حدود فاتحة
    "border_focus": "#2E86AB", # حدود عند التركيز
    
    # ألوان الحالات
    "hover": "#1E5F7A",        # لون عند التمرير
    "active": "#0F3A4A",       # لون عند النقر
    "disabled": "#CCCCCC",     # لون عند التعطيل
}

# أنماط الخطوط
FONTS = {
    "title": ("Arial", 24, "bold"),
    "heading": ("Arial", 18, "bold"),
    "subheading": ("Arial", 14, "bold"),
    "body": ("Arial", 12, "normal"),
    "small": ("Arial", 10, "normal"),
    "button": ("Arial", 12, "bold"),
}

# أحجام العناصر
SIZES = {
    "button_height": 40,
    "input_height": 35,
    "padding": 20,
    "margin": 10,
    "border_radius": 8,
    "icon_size": 24,
}

# إعدادات النوافذ
WINDOW = {
    "min_width": 800,
    "min_height": 600,
    "default_width": 900,
    "default_height": 700,
}

# أنماط الأزرار
BUTTON_STYLES = {
    "primary": {
        "fg_color": COLORS["primary"],
        "hover_color": COLORS["hover"],
        "text_color": COLORS["text_light"],
        "font": FONTS["button"],
        "height": SIZES["button_height"],
        "corner_radius": SIZES["border_radius"],
    },
    "secondary": {
        "fg_color": COLORS["bg_secondary"],
        "hover_color": COLORS["border"],
        "text_color": COLORS["text_primary"],
        "font": FONTS["button"],
        "height": SIZES["button_height"],
        "corner_radius": SIZES["border_radius"],
    },
    "success": {
        "fg_color": COLORS["success"],
        "hover_color": "#A02F1A",
        "text_color": COLORS["text_light"],
        "font": FONTS["button"],
        "height": SIZES["button_height"],
        "corner_radius": SIZES["border_radius"],
    },
    "accent": {
        "fg_color": COLORS["accent"],
        "hover_color": "#D17A01",
        "text_color": COLORS["text_light"],
        "font": FONTS["button"],
        "height": SIZES["button_height"],
        "corner_radius": SIZES["border_radius"],
    }
}

# أنماط حقول الإدخال
INPUT_STYLES = {
    "default": {
        "height": SIZES["input_height"],
        "corner_radius": SIZES["border_radius"],
        "fg_color": COLORS["bg_secondary"],
        "text_color": COLORS["text_primary"],
        "font": FONTS["body"],
    }
}

# أنماط التسميات
LABEL_STYLES = {
    "title": {
        "font": FONTS["title"],
        "text_color": COLORS["text_primary"],
    },
    "heading": {
        "font": FONTS["heading"],
        "text_color": COLORS["text_primary"],
    },
    "body": {
        "font": FONTS["body"],
        "text_color": COLORS["text_primary"],
    },
    "small": {
        "font": FONTS["small"],
        "text_color": COLORS["text_secondary"],
    }
}

# أنماط الإطارات
FRAME_STYLES = {
    "main": {
        "fg_color": COLORS["bg_primary"],
        "corner_radius": SIZES["border_radius"],
    },
    "card": {
        "fg_color": COLORS["bg_secondary"],
        "corner_radius": SIZES["border_radius"],
    },
    "sidebar": {
        "fg_color": COLORS["bg_dark"],
        "corner_radius": 0,
    }
}

