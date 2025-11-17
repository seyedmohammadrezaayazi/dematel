import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# --------------------------------
# 1. Load data from Excel file
# --------------------------------
file_path = 'HFL_DEMATEL_Fuzzy_Results.xlsx'
df_complete = pd.read_excel(file_path, sheet_name='Complete_Ranking')

# تنظیم فونت برای نمایش انگلیسی
plt.rcParams['font.family'] = ['DejaVu Sans']
sns.set_style("whitegrid")

# --------------------------------
# 2. Impact-Relation Map (Scatter Plot)
# --------------------------------
plt.figure(figsize=(12, 8))
scatter = sns.scatterplot(
    data=df_complete,
    x='D (Total Importance)',
    y='Net Effect (R-C)',
    hue='Category',
    style='Category',
    s=150,
    palette='Set1'
)

plt.title('Impact-Relation Map in DEMATEL Analysis (HFL Fuzzy)', fontsize=14, fontweight='bold')
plt.xlabel('Total Importance (D = R + C)', fontsize=12)
plt.ylabel('Net Effect (R - C)', fontsize=12)
plt.legend(title='Factor Categories', title_fontsize=12, fontsize=10)

# برچسب نقاط
for i, row in df_complete.iterrows():
    plt.annotate(
        row['Code'],
        (row['D (Total Importance)'], row['Net Effect (R-C)']),
        xytext=(3, 3),
        textcoords='offset points',
        fontsize=9,
        ha='left'
    )

plt.tight_layout()
plt.show()

# --------------------------------
# 3. Horizontal Bar Chart (Safe Version)
# --------------------------------
df_sorted = df_complete.sort_values('D (Total Importance)', ascending=True)
y_pos = np.arange(len(df_sorted))

# گزارش داده‌های اشتباه قبل از رسم
invalid_rows = df_sorted[
    (df_sorted['D_Lower'] > df_sorted['D (Total Importance)']) |
    (df_sorted['D_Upper'] < df_sorted['D (Total Importance)'])
]
if not invalid_rows.empty:
    print("\n⚠ داده‌های دارای مشکل محدوده D (حد پایین یا بالا اشتباه):")
    print(invalid_rows[['Code', 'D_Lower', 'D (Total Importance)', 'D_Upper']])

# محاسبه خطای پایین و بالا، جلوگیری از منفی شدن
error_lower = (df_sorted['D (Total Importance)'] - df_sorted['D_Lower']).clip(lower=0)
error_upper = (df_sorted['D_Upper'] - df_sorted['D (Total Importance)']).clip(lower=0)

# مطمئن‌تر: گرفتن قدر مطلق برای حذف منفی‌ها
error_lower = np.abs(error_lower)
error_upper = np.abs(error_upper)

errors = [error_lower.values, error_upper.values]

# رسم نمودار
plt.figure(figsize=(12, 16))
bars = plt.barh(
    y_pos,
    df_sorted['D (Total Importance)'],
    xerr=errors,
    capsize=5,
    color='skyblue',
    alpha=0.7,
    edgecolor='navy'
)

plt.title('Total Importance of Factors (D) with Fuzzy Bounds in DEMATEL Analysis', fontsize=14, fontweight='bold')
plt.xlabel('D Value (Defuzzified)', fontsize=12)
plt.ylabel('Factor Code', fontsize=12)
plt.yticks(y_pos, df_sorted['Code'])
plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.7)

# اضافه کردن مقادیر عددی کنار هر ستون
for bar, val in zip(bars, df_sorted['D (Total Importance)']):
    plt.text(val + 0.01, bar.get_y() + bar.get_height()/2, f'{val:.3f}',
             va='center', fontsize=8)

plt.tight_layout()
plt.show()

# --------------------------------
# 4. Cause Factors
# --------------------------------
df_cause = df_complete[df_complete['Category'].str.contains('Cause')]
plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_cause.sort_values('D (Total Importance)', ascending=True),
    x='D (Total Importance)',
    y='Code',
    palette='Blues_d'
)

plt.title('D Importance for Cause Factors (Drivers)', fontsize=12)
plt.xlabel('D (Total Importance)')
plt.ylabel('Factor Code')
plt.tight_layout()
plt.show()

# --------------------------------
# 5. Effect Factors
# --------------------------------
df_effect = df_complete[df_complete['Category'].str.contains('Effect')]
plt.figure(figsize=(10, 6))
sns.barplot(
    data=df_effect.sort_values('D (Total Importance)', ascending=True),
    x='D (Total Importance)',
    y='Code',
    palette='Reds_d'
)

plt.title('D Importance for Effect Factors (Consequences)', fontsize=12)
plt.xlabel('D (Total Importance)')
plt.ylabel('Factor Code')
plt.tight_layout()
plt.show()

# --------------------------------
# 6. R و C مقایسه‌ای
# --------------------------------
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

sns.barplot(
    data=df_complete.sort_values('R (Outgoing Influence)', ascending=True),
    x='R (Outgoing Influence)',
    y='Code',
    ax=ax1,
    palette='Greens_d'
)
ax1.set_title('Outgoing Influence (R)')
ax1.set_xlabel('R')
ax1.set_ylabel('Factor Code')

sns.barplot(
    data=df_complete.sort_values('C (Incoming Influence)', ascending=True),
    x='C (Incoming Influence)',
    y='Code',
    ax=ax2,
    palette='Oranges_d'
)
ax2.set_title('Incoming Influence (C)')
ax2.set_xlabel('C')
ax2.set_ylabel('Factor Code')

plt.tight_layout()
plt.show()

print("\n✅ Charts created successfully. Place the Excel file in the same directory to run the code.")