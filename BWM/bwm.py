import numpy as np
from scipy.optimize import linprog


def solve_bwm(best_to_criteria, criteria_to_worst, n_criteria):
    """
    حل BWM برای یک خبره.
    :param best_to_criteria: لیست مقایسه‌های بهترین-به-معیارها
    :param criteria_to_worst: لیست مقایسه‌های معیارها-به-بدترین
    :param n_criteria: تعداد معیارها
    :return: وزن نهایی معیارها
    """
    # تعریف متغیرهای تصمیم
    c = np.zeros(n_criteria + 1)
    c[-1] = 1  # متغیر ایپسیلون (ε)

    # محدودیت‌ها
    A = []
    b = []

    # محدودیت‌های بهترین به معیارها
    for i in range(n_criteria):
        constraint = np.zeros(n_criteria + 1)
        constraint[i] = -best_to_criteria[i]
        constraint[-1] = -1
        A.append(constraint)
        b.append(0)

        constraint = np.zeros(n_criteria + 1)
        constraint[i] = best_to_criteria[i]
        constraint[-1] = -1
        A.append(constraint)
        b.append(0)

    # محدودیت‌های معیارها به بدترین
    for i in range(n_criteria):
        constraint = np.zeros(n_criteria + 1)
        constraint[i] = -1 / criteria_to_worst[i]
        constraint[-1] = -1
        A.append(constraint)
        b.append(0)

        constraint = np.zeros(n_criteria + 1)
        constraint[i] = 1 / criteria_to_worst[i]
        constraint[-1] = -1
        A.append(constraint)
        b.append(0)

    # محدودیت‌های نرمال‌سازی (جمع وزن‌ها = 1)
    A_eq = [np.ones(n_criteria + 1)]
    A_eq[0][-1] = 0
    b_eq = [1]

    # حل مسئله بهینه‌سازی خطی
    result = linprog(c, A_ub=np.array(A), b_ub=np.array(b), A_eq=np.array(A_eq), b_eq=np.array(b_eq), bounds=(0, 1))

    if result.success:
        return result.x[:-1]  # وزن‌های نهایی
    else:
        raise ValueError("بهینه‌سازی خطی موفقیت‌آمیز نبود!")


def aggregate_weights(weights_list):
    """
    تجمیع وزن‌ها با میانگین هندسی.
    :param weights_list: لیست وزن‌های خبرگان
    :return: وزن‌های تجمیع‌شده
    """
    weights_array = np.array(weights_list)
    aggregated_weights = np.prod(weights_array, axis=0) ** (1 / len(weights_list))
    return aggregated_weights


# مثال داده‌ها برای دو خبره
n_criteria = 22

# داده‌های خبره اول
best_to_criteria_1 =  [5, 4, 6, 5, 4, 3, 7, 7, 3, 4, 5, 1, 4, 6, 5, 3, 4, 5, 4, 9, 3, 5]
criteria_to_worst_1 = [7, 6, 6, 6, 6, 5, 4, 4, 7, 7, 6, 9, 6, 5, 6, 6, 6, 7, 5, 1, 6, 6]

# داده‌های خبره دوم
best_to_criteria_2 =  [4, 3, 1, 6, 2, 7, 8, 8, 4, 4, 2, 3, 8, 7, 8, 3, 4, 5, 5, 9, 7, 6]
criteria_to_worst_2 = [7, 6, 9, 6, 9, 2, 2, 3, 7, 5, 7, 7, 5, 3, 4, 6, 5, 5, 4, 1, 4, 3]

# محاسبه وزن‌ها برای هر خبره
weights_1 = solve_bwm(best_to_criteria_1, criteria_to_worst_1, n_criteria)
weights_2 = solve_bwm(best_to_criteria_2, criteria_to_worst_2, n_criteria)

# تجمیع وزن‌های نهایی
final_weights = aggregate_weights([weights_1, weights_2])

# نمایش وزن‌های نهایی
#print("وزن‌های خبره اول:", weights_1)
#print("وزن‌های خبره دوم:", weights_2)
print("وزن‌های تجمیع‌شده نهایی:", final_weights)