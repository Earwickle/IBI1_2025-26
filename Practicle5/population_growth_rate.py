import matplotlib.pyplot as plt

countries = ['UK', 'China', 'Italy', 'Brazil', 'USA']
pop2020 = [66.7, 1426, 59.4, 208.6, 331.6]
pop2024 = [69.2, 1410, 58.9, 212.0, 340.1]

percent_changes = []
for c, p20, p24 in zip(countries, pop2020, pop2024):
    change = (p24 - p20) / p20 * 100
    percent_changes.append((c, change))

print('Population percentage change for each country (2020->2024):')
for c, ch in percent_changes:
    print(f'  {c}: {ch:+.2f}%')

sorted_changes = sorted(percent_changes, key=lambda x: x[1], reverse=True)
print('\nSorted population changes (descending: largest increase to largest decrease):')
for c, ch in sorted_changes:
    print(f'  {c}: {ch:+.2f}%')

largest_increase = sorted_changes[0]
largest_decrease = sorted_changes[-1]
print(f'\nLargest increase: {largest_increase[0]} ({largest_increase[1]:+.2f}%)')
print(f'Largest decrease: {largest_decrease[0]} ({largest_decrease[1]:+.2f}%)')

labels = [c for c, _ in sorted_changes]
values = [v for _, v in sorted_changes]

plt.figure(figsize=(9, 6))
bar_colors = ['#4caf50' if v >= 0 else '#f44336' for v in values]
plt.bar(labels, values, color=bar_colors, edgecolor='black')
for i, v in enumerate(values):
    plt.text(i, v + (0.06 if v >= 0 else -0.06), f'{v:+.2f}%', ha='center', va='bottom' if v >= 0 else 'top')

plt.title('Population Percentage Change (2020-2024)')
plt.xlabel('Country')
plt.ylabel('Percentage change (%)')
plt.grid(axis='y', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.show()