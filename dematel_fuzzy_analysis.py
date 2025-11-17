# -*- coding: utf-8 -*-
"""
DEMATEL FUZZY Analysis for Industry 4.0 Project Risk Management
محاسبات DEMATEL Fuzzy برای مدیریت ریسک پروژه‌های صنایع هوشمند


نویسنده: تجزیه‌وتحلیل ریسک
تاریخ: نوامبر 2025
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams
import warnings

warnings.filterwarnings('ignore')

# تنظیم فونت برای نمایش درست فارسی
plt.rcParams['font.sans-serif'] = ['DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class DEMATELFuzzyAnalysis:
    """
    کلاس برای تحلیل DEMATEL Fuzzy
    """
    
    def __init__(self, data_dict, threshold_ratio=0.5):
        """
        مقداردهی اولیه
        
        Parameters:
        -----------
        data_dict : dict
            فرهنگ داده‌های DEMATEL (Factor Code: {D, R, C, NetEffect, Cluster})
        threshold_ratio : float
            نسبت آستانه برای Prominence
        """
        self.data_dict = data_dict
        self.threshold_ratio = threshold_ratio
        self.df = pd.DataFrame.from_dict(data_dict, orient='index')
        self._categorize_factors()
        
    def _categorize_factors(self):
        """
        دسته‌بندی عوامل بر اساس Net Effect
        """
        def categorize(net_effect):
            if net_effect > 0.05:
                return "Cause (Driver)"
            elif net_effect < -0.05:
                return "Effect (Consequence)"
            else:
                return "Balanced"
        
        self.df['Category'] = self.df['NetEffect'].apply(categorize)
    
    def print_summary(self):
        """
        چاپ خلاصه تحلیل
        """
        print("=" * 100)
        print("DEMATEL FUZZY Analysis Summary - خلاصه تحلیل DEMATEL Fuzzy")
        print("=" * 100)
        print()
        
        print("1. توزیع عوامل بر اساس دسته‌بندی:")
        print("-" * 100)
        category_counts = self.df['Category'].value_counts()
        for category, count in category_counts.items():
            print(f"  • {category}: {count} عامل")
        print()
        
        print("2. آمار D (Prominence - بروز):")
        print("-" * 100)
        print(f"  • بیشترین D: {self.df['D'].max():.4f}")
        print(f"  • کمترین D: {self.df['D'].min():.4f}")
        print(f"  • میانگین D: {self.df['D'].mean():.4f}")
        print(f"  • انحراف معیار D: {self.df['D'].std():.4f}")
        print()
        
        print("3. آمار Net Effect (تأثیر خالص):")
        print("-" * 100)
        print(f"  • بیشترین Net Effect: {self.df['NetEffect'].max():.4f} (بیشترین رانش‌دهندگی)")
        print(f"  • کمترین Net Effect: {self.df['NetEffect'].min():.4f} (بیشترین پیامدی)")
        print(f"  • میانگین Net Effect: {self.df['NetEffect'].mean():.4f}")
        print()
        
        # محاسبه threshold
        threshold = self.df['D'].abs().mean() * self.threshold_ratio
        important_factors = (self.df['D'].abs() > threshold).sum()
        print(f"4. آستانه معنی‌داری (Threshold):")
        print("-" * 100)
        print(f"  • Threshold برای D: {threshold:.4f}")
        print(f"  • تعداد عوامل معنی‌دار: {important_factors} عامل")
        print()
    
    def print_drivers(self, top_n=None):
        """
        چاپ عوامل Cause (Driver)
        """
        drivers = self.df[self.df['Category'] == 'Cause (Driver)'].sort_values('NetEffect', ascending=False)
        
        print("=" * 100)
        print("CAUSE FACTORS (DRIVERS) - عوامل رانش‌دهنده (درایورها)")
        print("=" * 100)
        print("استراتژی: پیشگیری و کنترل مستقیم")
        print()
        
        if top_n:
            drivers = drivers.head(top_n)
        
        for idx, (code, row) in enumerate(drivers.iterrows(), 1):
            print(f"{idx}. {code}")
            print(f"   Prominence (D): {row['D']:.4f} | Outgoing (R): {row['R']:.4f} | Incoming (C): {row['C']:.4f}")
            print(f"   Net Effect: {row['NetEffect']:.4f} | Cluster: {row['Cluster']}")
            print()
    
    def print_effects(self):
        """
        چاپ عوامل Effect
        """
        effects = self.df[self.df['Category'] == 'Effect (Consequence)'].sort_values('NetEffect')
        
        print("=" * 100)
        print("EFFECT FACTORS (CONSEQUENCES) - عوامل پیامدی (پیامدها)")
        print("=" * 100)
        print("استراتژی: پایش و کنترل غیرمستقیم")
        print()
        
        for idx, (code, row) in enumerate(effects.iterrows(), 1):
            print(f"{idx}. {code}")
            print(f"   Prominence (D): {row['D']:.4f} | Outgoing (R): {row['R']:.4f} | Incoming (C): {row['C']:.4f}")
            print(f"   Net Effect: {row['NetEffect']:.4f} | Cluster: {row['Cluster']}")
            print()
    
    def print_balanced(self):
        """
        چاپ عوامل Balanced
        """
        balanced = self.df[self.df['Category'] == 'Balanced'].sort_values('D', ascending=False)
        
        print("=" * 100)
        print("BALANCED FACTORS - عوامل متوازن")
        print("=" * 100)
        print("استراتژی: مدیریت کامل و یکپارچه")
        print()
        
        for idx, (code, row) in enumerate(balanced.iterrows(), 1):
            print(f"{idx}. {code}")
            print(f"   Prominence (D): {row['D']:.4f} | Outgoing (R): {row['R']:.4f} | Incoming (C): {row['C']:.4f}")
            print(f"   Net Effect: {row['NetEffect']:.4f} | Cluster: {row['Cluster']}")
            print()
    
    def get_top_drivers(self, n=5):
        """
        برگرداندن برتر رانش‌دهندگان
        """
        drivers = self.df[self.df['Category'] == 'Cause (Driver)'].sort_values('NetEffect', ascending=False)
        return drivers.head(n)
    
    def get_top_effects(self, n=5):
        """
        برگرداندن برتر پیامدها
        """
        effects = self.df[self.df['Category'] == 'Effect (Consequence)'].sort_values('NetEffect')
        return effects.head(n)
    
    def cluster_analysis(self):
        """
        تحلیل بر اساس خوشه‌ها
        """
        print("=" * 100)
        print("CLUSTER ANALYSIS - تحلیل بر اساس خوشه‌ها")
        print("=" * 100)
        print()
        
        clusters = self.df.groupby('Cluster')
        
        for cluster_name, cluster_data in clusters:
            print(f"\nخوشه: {cluster_name}")
            print("-" * 100)
            print(f"  تعداد عوامل: {len(cluster_data)}")
            print(f"  میانگین D: {cluster_data['D'].mean():.4f}")
            print(f"  میانگین Net Effect: {cluster_data['NetEffect'].mean():.4f}")
            print(f"  نوع غالب: {cluster_data['Category'].mode()[0]}")
            print()
    
    def export_to_csv(self, filename='dematel_results.csv'):
        """
        صادرات نتایج به CSV
        """
        self.df.to_csv(filename, encoding='utf-8-sig')
        print(f"نتایج به فایل {filename} صادر شدند.")
    
    def print_methodology(self):
        """
        چاپ روش‌شناسی DEMATEL Fuzzy
        """
        print("=" * 100)
        print("DEMATEL FUZZY METHODOLOGY - روش‌شناسی DEMATEL Fuzzy")
        print("=" * 100)
        print()
        
        methodology = """
مراحل اجرای DEMATEL Fuzzy:

مرحله 1: تهیه ماتریس مجاورت Fuzzy (Direct Relation Matrix)
  • هر خبره برای هر جفت (i, j) یک عدد مثلثی Fuzzy وارد کرد
  • اعداد مثلثی: (Lower, Middle, Upper)
  • نشان‌دهنده تأثیر عامل i بر عامل j

مرحله 2: Defuzzification (تبدیل اعداد Fuzzy به اعداد دقیق)
  • فرمول: Defuzzified = (Lower + 4×Middle + Upper) / 6
  • این روش معیار (Center of Gravity) است

مرحله 3: میانگین‌گیری نظرات خبرگان
  • میانگین سه ماتریس defuzzified شده از سه خبره

مرحله 4: نرمال‌سازی (Normalization)
  • تقسیم ماتریس بر ماکزیمم مجموع ردیف‌ها و ستون‌ها
  • نتیجه: ماتریس نرمال‌شده (Normalized Direct Relation Matrix)

مرحله 5: محاسبه T matrix (Total Relation Matrix)
  • T = N × (I - N)^(-1)
  • که N ماتریس نرمال‌شده و I ماتریس یکه است

مرحله 6: محاسبه R و C
  • R = مجموع ردیف‌های T (Outgoing Influence)
  • C = مجموع ستون‌های T (Incoming Influence)

مرحله 7: محاسبه D و Net Effect
  • D = R + C (Prominence)
  • R - C = Net Effect (Causal Effect)

دسته‌بندی نهایی:
  • Cause (Driver): R - C > 0.05
  • Effect (Consequence): R - C < -0.05
  • Balanced: -0.05 ≤ R - C ≤ 0.05

فواید روش DEMATEL Fuzzy:
  ✓ مدیریت عدم‌قطعیت نظرات خبرگان
  ✓ درک عمیق روابط پیچیده بین عوامل
  ✓ شناسایی عوامل حساس و راننده
  ✓ کمک به تصمیم‌گیری استراتژیک
"""
        print(methodology)


# ============================================
# بخش اساسی - داده‌های DEMATEL
# ============================================

# داده‌های مثال (از فایل Excel)
data_dematel = {
    'F28': {'D': -1.7648, 'R': -0.7098, 'C': -1.0550, 'NetEffect': 0.3452, 'Cluster': 'محیطی/قانونی'},
    'F24': {'D': -1.8641, 'R': -0.8120, 'C': -1.0521, 'NetEffect': 0.2401, 'Cluster': 'مالی'},
    'F20': {'D': -1.8953, 'R': -0.8441, 'C': -1.0512, 'NetEffect': 0.2071, 'Cluster': 'مالی'},
    'F06': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'فنی'},
    'F16': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'سازمانی/مدیریتی'},
    'F14': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'سازمانی/مدیریتی'},
    'F35': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'اجتماعی-فرهنگی'},
    'F19': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'مالی'},
    'F10': {'D': -1.9661, 'R': -0.9170, 'C': -1.0491, 'NetEffect': 0.1321, 'Cluster': 'عملیاتی'},
    'F32': {'D': -2.0058, 'R': -0.9579, 'C': -1.0479, 'NetEffect': 0.0900, 'Cluster': 'اجتماعی-فرهنگی'},
    'F13': {'D': -2.0200, 'R': -0.9725, 'C': -1.0475, 'NetEffect': 0.0750, 'Cluster': 'سازمانی/مدیریتی'},
    'F25': {'D': -2.0200, 'R': -0.9725, 'C': -1.0475, 'NetEffect': 0.0750, 'Cluster': 'محیطی/قانونی'},
    'F04': {'D': -2.0693, 'R': -1.0232, 'C': -1.0461, 'NetEffect': 0.0228, 'Cluster': 'فنی'},
    'F36': {'D': -2.3552, 'R': -1.3176, 'C': -1.0376, 'NetEffect': -0.2799, 'Cluster': 'اجتماعی-فرهنگی'},
}


def main():
    """
    تابع اصلی
    """
    # ایجاد شی تحلیل
    analysis = DEMATELFuzzyAnalysis(data_dematel, threshold_ratio=0.5)
    
    # چاپ خلاصه
    analysis.print_summary()
    
    # چاپ روش‌شناسی
    analysis.print_methodology()
    
    # چاپ عوامل Cause
    print("\n")
    analysis.print_drivers(top_n=5)
    
    # چاپ عوامل Effect
    print("\n")
    analysis.print_effects()
    
    # چاپ عوامل Balanced
    print("\n")
    analysis.print_balanced()
    
    # تحلیل خوشه‌ها
    print("\n")
    analysis.cluster_analysis()
    
    # صادرات به CSV
    print("\n")
    analysis.export_to_csv('dematel_fuzzy_results.csv')
    
    # نمایش برتر رانش‌دهندگان
    print("=" * 100)
    print("TOP 5 DRIVERS - برتر 5 رانش‌دهنده")
    print("=" * 100)
    top_drivers = analysis.get_top_drivers(5)
    print(top_drivers[['D', 'R', 'C', 'NetEffect', 'Category', 'Cluster']])
    print()
    
    # توصیه‌های مدیریتی
    print("=" * 100)
    print("MANAGEMENT RECOMMENDATIONS - توصیه‌های مدیریتی")
    print("=" * 100)
    print()
    print("1. برای عوامل Cause (Drivers - بالاترین اولویت):")
    print("   • تمرکز بر پیشگیری و کنترل مستقیم")
    print("   • تخصیص بیشترین منابع و نظارت مکرر")
    print("   • طراحی اقدامات تخفیفی جریان‌بندی")
    print()
    print("2. برای عوامل Effect (Consequences - اولویت ثانوی):")
    print("   • پایش منظم و نظارت مستمر")
    print("   • آماده‌سازی پلان‌های واکنشی")
    print("   • کنترل از طریق کاهش عوامل رانش‌دهنده")
    print()
    print("3. برای عوامل Balanced (متوازن - اولویت سوم):")
    print("   • مدیریت شامل و جامع")
    print("   • نظارت دوطرفه و متعادل")
    print("   • تعادل بین پیشگیری و پاسخ")
    print()


if __name__ == "__main__":
    main()
