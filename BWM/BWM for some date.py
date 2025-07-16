
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


def rank_criteria(weights):
    """
    رتبه‌بندی معیارها بر اساس وزن نهایی.
    :param weights: لیست وزن‌های نهایی معیارها
    :return: لیست رتبه‌بندی معیارها
    """
    ranked_indices = np.argsort(weights)[::-1]  # مرتب‌سازی به ترتیب نزولی
    ranked_weights = weights[ranked_indices]
    return ranked_indices, ranked_weights


# تعداد معیارها و خبرگان
n_criteria = 22
n_experts = 5  # تعداد خبرگان (می‌توانید این مقدار را تغییر دهید)

# داده‌های خبرگان
best_to_criteria_list = [
 [5, 4, 6, 5, 4, 3, 7, 7, 3, 4, 5, 1, 4, 6, 5, 3, 4, 5, 4, 9, 3, 5], # خبره 1
 [4, 3, 1, 6, 2, 7, 8, 8, 4, 4, 2, 3, 8, 7, 8, 3, 4, 5, 5, 9, 7, 6], # خبره 2
 [2, 1, 3, 2, 2, 3, 7, 8, 3, 2, 4, 4, 4, 6, 7, 5, 3, 4, 5, 9, 5, 4],
 [2, 2, 3, 3, 1, 4, 6, 7, 2, 3, 4, 4, 3, 5, 6, 4, 5, 4, 5, 9, 5, 3],
 [3, 2, 2, 3, 1, 4, 5, 6, 4, 2, 3, 4, 3, 5, 6, 4, 3, 4, 5, 9, 5, 3]
]

criteria_to_worst_list = [
 [7, 6, 6, 6, 6, 5, 4, 4, 7, 7, 6, 9, 6, 5, 6, 6, 6, 7, 5, 1, 6, 6], # خبره 1
 [7, 6, 9, 6, 9, 2, 2, 3, 7, 5, 7, 7, 5, 3, 4, 6, 5, 5, 4, 1, 4, 3], # خبره 2
 [8, 9, 7, 8, 9, 7, 3, 3, 8, 9, 6, 6, 7, 4, 4, 6, 8, 7, 6, 1, 6, 7],
 [8, 8, 7, 7, 9, 6, 4, 3, 8, 7, 6, 6, 7, 5, 4, 6, 5, 6, 5, 1, 5, 7],
 [7, 8, 8, 7, 9, 6, 5, 4, 7, 9, 7, 6, 7, 5, 4, 6, 7, 8, 6, 1, 5, 8]
]

# محاسبه وزن‌ها برای هر خبره
weights_list = []
for i in range(n_experts):
    weights = solve_bwm(best_to_criteria_list[i], criteria_to_worst_list[i], n_criteria)
    weights_list.append(weights)

# تجمیع وزن‌های نهایی
final_weights = aggregate_weights(weights_list)

# رتبه‌بندی معیارها
ranked_indices, ranked_weights = rank_criteria(final_weights)

# نمایش وزن‌های نهایی و رتبه‌بندی
print("وزن‌های تجمیع‌شده نهایی:")
print(final_weights)

print("\nرتبه‌بندی معیارها:")
for rank, (index, weight) in enumerate(zip(ranked_indices, ranked_weights), start=1):
    print(f"رتبه {rank}: معیار {index + 1} با وزن {weight:.4f}")