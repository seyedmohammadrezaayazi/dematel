import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# خواندن نظرات خبرگان از فایل‌های اکسل
def read_expert_opinions(file_paths):
    expert_matrices = []
    for file_path in file_paths:
        # خواندن فایل اکسل به صورت DataFrame
        df = pd.read_excel(file_path, header=None)
        # تبدیل DataFrame به آرایه numpy
        expert_matrix = df.values
        expert_matrices.append(expert_matrix)
    return expert_matrices

# ترکیب نظرات خبرگان (میانگین‌گیری)
def combine_expert_opinions(expert_matrices):
    # تبدیل لیست ماتریس‌ها به یک آرایه سه‌بعدی
    stacked_matrices = np.array(expert_matrices)
    # محاسبه میانگین در بعد اول (میانگین نظرات خبرگان)
    combined_matrix = np.mean(stacked_matrices, axis=0)
    return combined_matrix

# فایل‌های اکسل نظرات خبرگان
file_paths = [
    'expert1.xlsx',  # مسیر فایل اول
    'expert2.xlsx'
]

# مرحله 1: خواندن و ترکیب نظرات خبرگان
expert_matrices = read_expert_opinions(file_paths)
array_23x23 = combine_expert_opinions(expert_matrices)

# چاپ ماتریس ترکیبی نظرات خبرگان
print("Combined Expert Opinions Matrix:\n", array_23x23)

# مرحله 2: نرمال‌سازی ماتریس تأثیرات اولیه
def normalize_matrix(direct_matrix):
    max_row_sum = np.max(direct_matrix.sum(axis=1))  # مجموع بزرگ‌ترین سطر
    normalized_matrix = direct_matrix / max_row_sum
    print("Normalized Direct-Relation Matrix:\n", normalized_matrix)
    return normalized_matrix

normalized_matrix = normalize_matrix(array_23x23)

# مرحله 3: محاسبه ماتریس تأثیرات کلی (Total-Relation Matrix)
def calculate_total_relation_matrix(normalized_matrix):
    n = len(normalized_matrix)
    I = np.eye(n)  # ماتریس همانی
    epsilon = 1e-10  # مقدار کوچک برای جلوگیری از مشکلات عددی
    # محاسبه ماتریس معکوس
    inverse_matrix = np.linalg.inv(I - normalized_matrix + epsilon)
    print("Inverse Matrix (I - N)^-1:\n", inverse_matrix)
    # ضرب ماتریس معکوس در ماتریس اولیه
    total_relation_matrix = inverse_matrix @ normalized_matrix
    print("Total-Relation Matrix:\n", total_relation_matrix)
    return total_relation_matrix

total_relation_matrix = calculate_total_relation_matrix(normalized_matrix)

# مرحله 4: محاسبه درجه تأثیر (R) و وابستگی (D)
degree_influence = total_relation_matrix.sum(axis=1)  # تأثیر کل هر چالش (جمع ردیف‌ها)
degree_dependency = total_relation_matrix.sum(axis=0)  # وابستگی کل هر چالش (جمع ستون‌ها)

print("Degree of Influence (R):\n", degree_influence)
print("Degree of Dependency (D):\n", degree_dependency)

# محاسبه وابستگی (R + D) و عدم وابستگی (R - D)
dependency = degree_influence + degree_dependency  # R + D
independency = degree_influence - degree_dependency  # R - D

print("Dependency (R + D):\n", dependency)
print("Independency (R - D):\n", independency)

# میانگین مقادیر ماتریس تأثیرات کلی
mean_total_relation = np.mean(total_relation_matrix)
print("Mean of Total-Relation Matrix:\n", mean_total_relation)

# مرحله 5: رسم نمودار وابستگی و عدم وابستگی در یک نمودار با فلش‌های جهت‌دار
plt.figure(figsize=(15, 15))

# رسم نقاط وابستگی و تأثیر با اندازه بزرگ‌تر
point_size = 1000  # اندازه نقاط
circle_radius = np.sqrt(point_size / np.pi) / 100  # شعاع دایره (براساس اندازه نقاط)

plt.scatter(dependency, independency, color='blue', s=point_size, label='Challenges')  # s=1000 برای بزرگ‌تر کردن نقاط

# نام‌گذاری چالش‌ها داخل نقاط
for i, txt in enumerate(range(1, len(dependency) + 1)):
    plt.text(dependency[i], independency[i], f"C{txt}", fontsize=12, color='white', ha='center', va='center')

# رسم خطوط جهت‌دار بین چالش‌ها برای مقادیر بالاتر از میانگین
for i in range(len(degree_influence)):
    for j in range(len(degree_dependency)):
        if total_relation_matrix[i, j] > mean_total_relation:  # فقط مقادیر بالاتر از میانگین
            # محاسبه جهت فلش‌ها با تنظیم برخورد به لبه دایره‌ها
            dx = dependency[j] - dependency[i]
            dy = independency[j] - independency[i]
            distance = np.sqrt(dx**2 + dy**2)
            if distance > circle_radius:  # بررسی فاصله کافی برای رسم فلش
                reduction_factor = circle_radius / distance  # تنظیم فاصله فلش‌ها از لبه دایره
                start_x = dependency[i] + dx * reduction_factor
                start_y = independency[i] + dy * reduction_factor
                end_x = dependency[j] - dx * reduction_factor
                end_y = independency[j] - dy * reduction_factor
                plt.arrow(
                    start_x, start_y,  # نقطه شروع فلش
                    end_x - start_x,  # اختلاف x برای جهت فلش
                    end_y - start_y,  # اختلاف y برای جهت فلش
                    head_width=0.05, head_length=0.05, fc='black', ec='black', alpha=0.7
                )

plt.title('Dependency and Independency Analysis with Directed Arrows')
plt.xlabel('Dependency (R + D)')
plt.ylabel('Independency (R - D)')
plt.grid()
plt.axhline(0, color='black', lw=1)
plt.axvline(0, color='black', lw=1)
plt.legend()
plt.show()