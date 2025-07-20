import matplotlib.pyplot as plt
import numpy as np
from matplotlib import font_manager

# لیست نام‌های رایج فونت‌های فارسی
persian_fonts = ['Vazirmatn', 'IRANSans', 'BNazanin', 'B Nazanin', 'Shabnam', 'Yekan', 'Tahoma']

# جستجوی فونت مناسب در سیستم
font_path = None
for font in font_manager.findSystemFonts():
    for pf in persian_fonts:
        if pf.lower() in font.lower():
            font_path = font
            break
    if font_path:
        break

if font_path:
    font_prop = font_manager.FontProperties(fname=font_path)
    print(f"فونت فارسی پیدا شد و استفاده می‌شود: {font_path}")
else:
    font_prop = None
    print("هیچ فونت فارسی پیدا نشد. از فونت پیش‌فرض استفاده می‌شود.")

labels = [
    "افزایش خطر حملات سایبری", "اتصال و اشتراک‌گذاری داده‌ها", "هزینه‌های سرمایه‌گذاری و پیاده‌سازی",
    "ریسک‌های بالا در پیاده‌سازی فناوری‌های نوظهور", "عدم شناخت از اولویت‌های دیجیتالی‌سازی", "نیروی کار ماهر و آموزش‌دیده",
    "مقاومت کارکنان و مدیران در برابر تغییر", "سیاست‌های دولتی", "عدم تمایل ذینفعان به اشتراک‌گذاری اطلاعات",
    "محدودیت‌های زیرساختی", "پیچیدگی سیستم‌ها", "آموزش کارکنان", "توسعه‌نیافتگی در زمینه تحقیقات صنایع دریایی صنعت ۴",
    "عدم تطابق فناوری‌ها", "عدم وجود مدل‌های کسب‌وکار دیجیتال", "چالش‌های مربوط به مسئولیت اجتماعی",
    "مدیریت تغییر", "چالش‌های نظارتی", "پیچیدگی زنجیره تامین", "عدم قطعیت در عملیات", "عدم درک جامع",
    "از بین رفتن شغل", "عدم دسترسی به تکنولوژی"
]

R_plus_D = [
    10.16, 11.24, 10.94, 11.32, 11.07, 10.14, 10.01, 10.74, 9.33, 10.71, 10.76, 9.73,
    10.93, 11.01, 10.61, 7.94, 10.95, 9.96, 10.23, 10.22, 11.98, 9.25, 12.83
]
R_minus_D = [
    1.56, 0.17, 0.03, -0.41, 0.10, -0.21, -0.25, 0.57, -0.20, 0.36, 0.42, -0.18,
    -0.13, -0.08, -0.20, -0.12, 0.07, 0.02, 0.18, -0.40, -0.17, -0.87, -0.27
]

# --- نمودار پراکندگی ---
plt.figure(figsize=(12,7))
plt.scatter(R_minus_D, R_plus_D, color="royalblue")

for i, label in enumerate(labels):
    plt.text(R_minus_D[i]+0.02, R_plus_D[i], label, fontsize=10, fontproperties=font_prop)

plt.axvline(x=0, color='grey', linestyle='--')
plt.xlabel("R-D (عامل علی / عامل معلول)", fontproperties=font_prop, fontsize=12)
plt.ylabel("R+D (اهمیت کل)", fontproperties=font_prop, fontsize=12)
plt.title("نمودار علی-معلولی چالش‌های انقلاب صنعتی چهارم در صنعت دریایی", fontproperties=font_prop, fontsize=14)
plt.grid(True)
plt.tight_layout()
plt.show()

# --- نمودار ستونی ---
plt.figure(figsize=(13,7))
indices = np.arange(len(labels))
plt.bar(indices, R_plus_D, color="deepskyblue")
plt.xticks(indices, labels, rotation=90, fontproperties=font_prop, fontsize=10)
plt.ylabel("R+D (اهمیت کل)", fontproperties=font_prop, fontsize=12)
plt.title("اهمیت کلی هر چالش بر اساس روش دیمتل", fontproperties=font_prop, fontsize=14)
plt.tight_layout()
plt.show()