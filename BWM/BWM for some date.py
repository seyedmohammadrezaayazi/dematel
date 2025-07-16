import numpy as np
from scipy.optimize import linprog

# تعداد معیارها و خبرگان
num_criteria = 22
num_experts = 2

# داده‌های خبرگان
# ماتریس مقایسه بهترین به معیارها برای هر خبره (هر خبره یک لیست جداگانه دارد)
best_to_criteria = [
    [5, 4, 6, 5, 4, 3, 7, 7, 3, 4, 5, 1, 4, 6, 5, 3, 4, 5, 4, 9, 3, 5],  # خبره 1
    [4, 3, 1, 6, 2, 7, 8, 8, 4, 4, 2, 3, 8, 7, 8, 3, 4, 5, 5, 9, 7, 6]   # خبره 2
]

# ماتریس مقایسه معیارها به بدترین برای هر خبره
criteria_to_worst = [
    [7, 6, 6, 6, 6, 5, 4, 4, 7, 7, 6, 9, 6, 5, 6, 6, 6, 7, 5, 1, 6, 6],  # خبره 1
    [9, 6, 4, 2, 1, 7, 5, 3, 8, 6, 4, 2, 7, 5, 3, 7, 5, 3, 2, 1, 6, 8]   # خبره 2
]

# بهترین و بدترین معیار برای هر خبره
best_criteria = [11, 2]  # شماره معیار منهای یک می شود
worst_criteria = [19, 19]  # شماره معیار منهای یک می شود

# تابع محاسبه وزن‌ها با روش BWM
def calculate_weights(best_to_criteria, criteria_to_worst, best_idx, worst_idx, num_criteria):
    # تعداد متغیرها: وزن هر معیار (w) و مقدار تابع هدف (ξ)
    num_variables = num_criteria + 1

    # قیود
    A = []
    b = []

    # قیود مربوط به بهترین معیار
    for i in range(num_criteria):
        if i != best_idx:
            row = [0] * num_variables
            row[i] = 1
            row[best_idx] = -best_to_criteria[i]
            row[-1] = -1
            A.append(row)
            b.append(0)

    # قیود مربوط به بدترین معیار
    for i in range(num_criteria):
        if i != worst_idx:
            row = [0] * num_variables
            row[i] = -1
            row[worst_idx] = criteria_to_worst[i]
            row[-1] = -1
            A.append(row)
            b.append(0)

    # قیود مجموع وزن‌ها برابر با 1
    row = [1] * num_criteria + [0]
    A.append(row)
    b.append(1)

    # حل مدل با linprog
    A = np.array(A)
    b = np.array(b)
    c = [0] * num_criteria + [1]  # تابع هدف (کمینه کردن ξ)
    bounds = [(0, None)] * num_variables

    result = linprog(c, A_ub=A, b_ub=b, bounds=bounds, method='highs')
    weights = result.x[:-1]  # وزن‌ها
    return weights

# محاسبه وزن‌ها برای هر خبره
weights_experts = []
for i in range(num_experts):
    weights = calculate_weights(
        best_to_criteria[i],
        criteria_to_worst[i],
        best_criteria[i],
        worst_criteria[i],
        num_criteria
    )
    weights_experts.append(weights)

# تجمیع وزن‌های خبرگان با میانگین هندسی
weights_final = np.mean(weights_experts, axis=0)

# نمایش وزن‌های نهایی
print("وزن‌های نهایی معیارها:")
print(weights_final)