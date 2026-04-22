import os
import pandas as pd
import matplotlib.pyplot as plt

CSV_PATH = r"C:\Users\Joyce\Desktop\学习资料\ICMB\week 10\dalys-rate-from-all-causes.csv"

if not os.path.exists(CSV_PATH):
    raise FileNotFoundError(f"CSV file not found: {CSV_PATH}")

df = pd.read_csv(CSV_PATH)

# 1) Show the third and fourth columns (Year and DALYs) for the first 10 rows.
first_10_year_dalys = df.iloc[:10, [2, 3]]
print("First 10 rows - Year and DALYs:")
print(first_10_year_dalys)
print()

# Afghanistan: first 10 years where DALYs were recorded, then find max DALYs year.
afghanistan_first_10_years = (
    df.loc[df["Entity"] == "Afghanistan", ["Year", "DALYs"]]
    .sort_values("Year")
    .head(10)
)
afghanistan_max_year = afghanistan_first_10_years.loc[
    afghanistan_first_10_years["DALYs"].idxmax(), "Year"
]
# Maximum DALYs across the first 10 recorded years in Afghanistan occurred in 1998.
print("Afghanistan first 10 recorded years (Year, DALYs):")
print(afghanistan_first_10_years)
print(f"Year with max DALYs in those 10 years: {afghanistan_max_year}")
print()

# 2) Use a Boolean to show all years recorded for Zimbabwe.
zimbabwe_mask = df["Entity"] == "Zimbabwe"
zimbabwe_years = df.loc[zimbabwe_mask, "Year"].sort_values().reset_index(drop=True)
# Zimbabwe DALYs data were first recorded in 1990 and last recorded in 2019.
print("All years recorded for Zimbabwe:")
print(zimbabwe_years.to_string(index=False))
print(
    f"Zimbabwe first year: {zimbabwe_years.min()}, "
    f"last year: {zimbabwe_years.max()}"
)
print()

# 3) Compute countries with maximum and minimum DALYs in 2019.
df_2019 = df.loc[df["Year"] == 2019, ["Entity", "DALYs"]]
max_row_2019 = df_2019.loc[df_2019["DALYs"].idxmax()]
min_row_2019 = df_2019.loc[df_2019["DALYs"].idxmin()]
# In 2019, the country with maximum DALYs is Lesotho, and minimum is Singapore.
print("2019 max DALYs country:")
print(max_row_2019.to_string())
print()
print("2019 min DALYs country:")
print(min_row_2019.to_string())
print()

# 4) Plot DALYs over time for one identified country (Lesotho: max in 2019).
country_for_plot = str(max_row_2019["Entity"])
country_series = (
    df.loc[df["Entity"] == country_for_plot, ["Year", "DALYs"]]
    .sort_values("Year")
)

plt.figure(figsize=(10, 6))
plt.plot(country_series["Year"], country_series["DALYs"], marker="o", linewidth=1.6)
plt.title(f"DALYs Over Time in {country_for_plot}")
plt.xlabel("Year")
plt.ylabel("DALYs")
plt.grid(alpha=0.3)
plt.tight_layout()
plot_path = os.path.join(os.path.dirname(__file__), "dalys_lesotho_trend.png")
plt.savefig(plot_path, dpi=300)
plt.close()
print(f"Plot saved to: {plot_path}")
print()

# 5) Code answering question.txt:
# Question: Plot a DALYs boxplot for China, and calculate the range between max and min values.
china_dalys = df.loc[df["Entity"] == "China", "DALYs"].dropna()

plt.figure(figsize=(8, 6))
plt.boxplot(china_dalys.tolist(), tick_labels=["China"])
plt.title("China DALYs Distribution (Boxplot)")
plt.ylabel("DALYs")
plt.grid(axis="y", alpha=0.3)
plt.tight_layout()
china_boxplot_path = os.path.join(os.path.dirname(__file__), "dalys_china_boxplot.png")
plt.savefig(china_boxplot_path, dpi=300)
plt.close()

china_max = float(china_dalys.max())
china_min = float(china_dalys.min())
china_range = china_max - china_min

print("Question from question.txt:")
print("Plot a DALYs boxplot for China, and calculate the range between max and min values.")
print(f"China max DALYs: {china_max:.2f}")
print(f"China min DALYs: {china_min:.2f}")
print(f"China DALYs range (max-min): {china_range:.2f}")
print(f"China boxplot saved to: {china_boxplot_path}")
