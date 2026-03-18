import matplotlib.pyplot as plt

heart_rates = [72, 60, 126, 85, 90, 59, 76, 131, 88, 121, 64]
num_patients = len(heart_rates)
mean_hr = sum(heart_rates) / num_patients

low_count = sum(1 for hr in heart_rates if hr < 60)
normal_count = sum(1 for hr in heart_rates if 60 <= hr <= 120)
high_count = sum(1 for hr in heart_rates if hr > 120)

print(f"Number of patients: {num_patients}")
print(f"Mean heart rate: {mean_hr:.2f} bpm")

categories = {'Low (<60 bpm)': low_count,'Normal (60-120 bpm)': normal_count,'High (>120 bpm)': high_count}

largest_category = max(categories, key=categories.get)

print("\nHeart rate category counts:")
for x, y in categories.items():
    print(f"  {x}: {y}")
print(f"Category with the largest number of patients: {largest_category} ({categories[largest_category]} patients)")

plt.figure(figsize=(7, 7))
plt.pie(
    categories.values(),
    labels=categories.keys(),
    autopct='%1.1f%%',
    startangle=90,
    colors=['#66b3ff', '#99ff99', '#ff9999'],
    wedgeprops={'edgecolor': 'black'}
)
plt.title('Heart Rate Category Distribution')
plt.axis('equal')
plt.tight_layout()
plt.show()