# -*- coding: utf-8 -*-
"""
DEMATEL Fuzzy Visualization
تصویرسازی نتایج DEMATEL Fuzzy برای مدیریت ریسک
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# تنظیم فونت
rcParams['font.sans-serif'] = ['Arial']
rcParams['axes.unicode_minus'] = False

# داده‌های DEMATEL
data_dematel = {
    'F28': {'D': -1.7648, 'R': -0.7098, 'C': -1.0550, 'NetEffect': 0.3452, 'Cluster': 'Environmental', 'Desc': 'Data Privacy Ambiguity'},
    'F24': {'D': -1.8641, 'R': -0.8120, 'C': -1.0521, 'NetEffect': 0.2401, 'Cluster': 'Financial', 'Desc': 'Budget Cuts'},
    'F20': {'D': -1.8953, 'R': -0.8441, 'C': -1.0512, 'NetEffect': 0.2071, 'Cluster': 'Financial', 'Desc': 'ROI Uncertainty'},
    'F06': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'Technical', 'Desc': 'Supply Chain Failure'},
    'F16': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'Org/Mgmt', 'Desc': 'Change Control Weakness'},
    'F14': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'Org/Mgmt', 'Desc': 'Data Governance Weakness'},
    'F35': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'Social', 'Desc': 'Social Anxiety Increase'},
    'F19': {'D': -1.9531, 'R': -0.9036, 'C': -1.0495, 'NetEffect': 0.1459, 'Cluster': 'Financial', 'Desc': 'High Initial Cost'},
    'F10': {'D': -1.9661, 'R': -0.9170, 'C': -1.0491, 'NetEffect': 0.1321, 'Cluster': 'Operational', 'Desc': 'Benefit Realization Disruption'},
    'F32': {'D': -2.0058, 'R': -0.9579, 'C': -1.0479, 'NetEffect': 0.0900, 'Cluster': 'Social', 'Desc': 'Change Resistance'},
    'F13': {'D': -2.0200, 'R': -0.9725, 'C': -1.0475, 'NetEffect': 0.0750, 'Cluster': 'Org/Mgmt', 'Desc': 'Role Ambiguity'},
    'F25': {'D': -2.0200, 'R': -0.9725, 'C': -1.0475, 'NetEffect': 0.0750, 'Cluster': 'Environmental', 'Desc': 'Compliance Requirements'},
    'F04': {'D': -2.0693, 'R': -1.0232, 'C': -1.0461, 'NetEffect': 0.0228, 'Cluster': 'Technical', 'Desc': 'Data Quality Issues'},
    'F36': {'D': -2.3552, 'R': -1.3176, 'C': -1.0376, 'NetEffect': -0.2799, 'Cluster': 'Social', 'Desc': 'Digital Divide Inequality'},
}

df = pd.DataFrame.from_dict(data_dematel, orient='index')

# دسته‌بندی عوامل
def categorize(net_effect):
    if net_effect > 0.05:
        return "Cause"
    elif net_effect < -0.05:
        return "Effect"
    else:
        return "Balanced"

df['Category'] = df['NetEffect'].apply(categorize)

# رنگ‌ها
color_map = {
    'Cause': '#e74c3c',      # قرمز
    'Effect': '#3498db',     # آبی
    'Balanced': '#f39c12'    # نارنجی
}

# ==========================================
# نمودار 1: Cause-Effect Diagram
# ==========================================
fig, ax = plt.subplots(figsize=(14, 10))

scatter = ax.scatter(df['R'], df['C'], s=np.abs(df['D'])*500, 
                     c=df['Category'].map(color_map), 
                     alpha=0.6, edgecolors='black', linewidth=2)

# خطوط مرجع
ax.axvline(x=df['R'].mean(), color='gray', linestyle='--', alpha=0.5, label='Mean R')
ax.axhline(y=df['C'].mean(), color='gray', linestyle='--', alpha=0.5, label='Mean C')

# نام‌گذاری نقاط
for idx, row in df.iterrows():
    ax.annotate(idx, (row['R'], row['C']), fontsize=9, 
                ha='center', va='center', fontweight='bold')

# برچسب‌ها و ظاهر
ax.set_xlabel('R (Outgoing Influence)', fontsize=12, fontweight='bold')
ax.set_ylabel('C (Incoming Influence)', fontsize=12, fontweight='bold')
ax.set_title('DEMATEL Cause-Effect Diagram\nCausal and Effect Risk Factors', 
             fontsize=14, fontweight='bold', pad=20)

# legend
legend_labels = [
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#e74c3c', 
               markersize=10, label='Cause (Driver)', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#3498db', 
               markersize=10, label='Effect', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#f39c12', 
               markersize=10, label='Balanced', markeredgecolor='black'),
]
ax.legend(handles=legend_labels, loc='upper right', fontsize=11)

ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dematel_cause_effect_diagram.png', dpi=300, bbox_inches='tight')
print("✓ Saved: dematel_cause_effect_diagram.png")
plt.close()

# ==========================================
# نمودار 2: D (Prominence) و Net Effect
# ==========================================
fig, ax = plt.subplots(figsize=(14, 8))

# مرتب کردن بر اساس D
df_sorted = df.sort_values('D', ascending=True)

y_pos = np.arange(len(df_sorted))
colors = [color_map[cat] for cat in df_sorted['Category']]

ax.barh(y_pos, df_sorted['D'], color=colors, alpha=0.7, edgecolor='black', linewidth=1.5)

# نام‌گذاری
ax.set_yticks(y_pos)
ax.set_yticklabels(df_sorted.index, fontsize=10)

ax.set_xlabel('D (Prominence - Importance)', fontsize=12, fontweight='bold')
ax.set_title('Risk Factors Ranked by Prominence (D)\nIndustry 4.0 Project Risk Management', 
             fontsize=14, fontweight='bold', pad=20)

ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('dematel_prominence_ranking.png', dpi=300, bbox_inches='tight')
print("✓ Saved: dematel_prominence_ranking.png")
plt.close()

# ==========================================
# نمودار 3: Net Effect Distribution
# ==========================================
fig, ax = plt.subplots(figsize=(12, 7))

df_sorted_net = df.sort_values('NetEffect', ascending=False)
colors_net = [color_map[cat] for cat in df_sorted_net['Category']]

y_pos = np.arange(len(df_sorted_net))

bars = ax.barh(y_pos, df_sorted_net['NetEffect'], color=colors_net, 
               alpha=0.7, edgecolor='black', linewidth=1.5)

# خط reference
ax.axvline(x=0, color='black', linestyle='-', linewidth=2)
ax.axvline(x=0.05, color='gray', linestyle='--', linewidth=1, alpha=0.5, label='Threshold')
ax.axvline(x=-0.05, color='gray', linestyle='--', linewidth=1, alpha=0.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(df_sorted_net.index, fontsize=10)

ax.set_xlabel('Net Effect (R - C)', fontsize=12, fontweight='bold')
ax.set_title('Risk Factors by Net Effect (Causal Strength)\nPositive: Driver | Negative: Consequence', 
             fontsize=14, fontweight='bold', pad=20)

# Legend
legend_elements = [
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#e74c3c', 
               markersize=10, label='Cause (Driver)', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#3498db', 
               markersize=10, label='Effect', markeredgecolor='black'),
    plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#f39c12', 
               markersize=10, label='Balanced', markeredgecolor='black'),
]
ax.legend(handles=legend_elements, loc='lower right', fontsize=10)

ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('dematel_net_effect_ranking.png', dpi=300, bbox_inches='tight')
print("✓ Saved: dematel_net_effect_ranking.png")
plt.close()

# ==========================================
# نمودار 4: Cluster Analysis
# ==========================================
fig, ax = plt.subplots(figsize=(12, 7))

cluster_summary = df.groupby('Cluster').agg({
    'D': 'mean',
    'NetEffect': 'mean',
    'R': 'mean',
    'C': 'mean'
}).sort_values('D', ascending=True)

y_pos = np.arange(len(cluster_summary))
colors_cluster = plt.cm.Set3(np.linspace(0, 1, len(cluster_summary)))

bars = ax.barh(y_pos, cluster_summary['D'], color=colors_cluster, 
               alpha=0.7, edgecolor='black', linewidth=1.5)

ax.set_yticks(y_pos)
ax.set_yticklabels(cluster_summary.index, fontsize=11, fontweight='bold')

ax.set_xlabel('Average D (Prominence)', fontsize=12, fontweight='bold')
ax.set_title('Risk Clusters by Average Prominence\nIndustry 4.0 Project Risk Categories', 
             fontsize=14, fontweight='bold', pad=20)

# Add value labels
for i, (idx, row) in enumerate(cluster_summary.iterrows()):
    ax.text(row['D']-0.05, i, f"{row['D']:.3f}", va='center', ha='right', 
            fontsize=10, fontweight='bold', color='white')

ax.grid(axis='x', alpha=0.3)
plt.tight_layout()
plt.savefig('dematel_cluster_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: dematel_cluster_analysis.png")
plt.close()

# ==========================================
# نمودار 5: R vs C (Influence Map)
# ==========================================
fig, ax = plt.subplots(figsize=(12, 8))

# Scatter plot
scatter = ax.scatter(df['R'], df['C'], s=500, c=df['NetEffect'], 
                     cmap='RdYlBu_r', alpha=0.6, edgecolors='black', linewidth=2)

# Reference lines
ax.axvline(x=df['R'].mean(), color='red', linestyle='--', alpha=0.5, linewidth=2)
ax.axhline(y=df['C'].mean(), color='blue', linestyle='--', alpha=0.5, linewidth=2)

# Annotations
for idx, row in df.iterrows():
    ax.annotate(idx, (row['R'], row['C']), fontsize=9, 
                ha='center', va='center', fontweight='bold')

# Colorbar
cbar = plt.colorbar(scatter, ax=ax)
cbar.set_label('Net Effect (R-C)', fontsize=11, fontweight='bold')

ax.set_xlabel('R (Outgoing Influence) →', fontsize=12, fontweight='bold')
ax.set_ylabel('← C (Incoming Influence)', fontsize=12, fontweight='bold')
ax.set_title('Influence Map: Outgoing vs Incoming\nRisk Factor Position Analysis', 
             fontsize=14, fontweight='bold', pad=20)

# Add quadrant labels
ax.text(df['R'].max()*0.8, df['C'].max()*0.8, 'DRIVER-RECEIVER\n(High influence both directions)', 
        fontsize=10, alpha=0.3, ha='center', bbox=dict(boxstyle='round', facecolor='gray', alpha=0.1))
ax.text(df['R'].min()*0.8, df['C'].max()*0.8, 'DEPENDENT\n(Low output, High input)', 
        fontsize=10, alpha=0.3, ha='center', bbox=dict(boxstyle='round', facecolor='gray', alpha=0.1))

ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('dematel_influence_map.png', dpi=300, bbox_inches='tight')
print("✓ Saved: dematel_influence_map.png")
plt.close()

# ==========================================
# نمودار 6: Category Distribution
# ==========================================
fig, axes = plt.subplots(1, 2, figsize=(14, 6))

# نمودار 1: تعداد عوامل
category_counts = df['Category'].value_counts()
colors_pie = [color_map[cat] for cat in category_counts.index]

axes[0].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%',
            colors=colors_pie, startangle=90, textprops={'fontsize': 11, 'fontweight': 'bold'})
axes[0].set_title('Distribution of Risk Factors\nby Category', fontsize=12, fontweight='bold')

# نمودار 2: میانگین D
category_d_mean = df.groupby('Category')['D'].mean().sort_values()
colors_bar = [color_map[cat] for cat in category_d_mean.index]

axes[1].bar(range(len(category_d_mean)), category_d_mean.values, 
            color=colors_bar, alpha=0.7, edgecolor='black', linewidth=1.5)
axes[1].set_xticks(range(len(category_d_mean)))
axes[1].set_xticklabels(category_d_mean.index, fontsize=11, fontweight='bold')
axes[1].set_ylabel('Average D (Prominence)', fontsize=11, fontweight='bold')
axes[1].set_title('Average Prominence by Category', fontsize=12, fontweight='bold')
axes[1].grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.savefig('dematel_category_distribution.png', dpi=300, bbox_inches='tight')
print("✓ Saved: dematel_category_distribution.png")
plt.close()

print("\n" + "="*60)
print("DEMATEL Fuzzy Visualization Complete!")
print("="*60)
print("\nGenerated Charts:")
print("  1. dematel_cause_effect_diagram.png - Cause-Effect Position")
print("  2. dematel_prominence_ranking.png - D Value Ranking")
print("  3. dematel_net_effect_ranking.png - Net Effect Distribution")
print("  4. dematel_cluster_analysis.png - Risk Cluster Analysis")
print("  5. dematel_influence_map.png - R vs C Influence Map")
print("  6. dematel_category_distribution.png - Category Distribution")
print("\n" + "="*60)
