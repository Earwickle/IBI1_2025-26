# Pseudocode:
# 1. Set total_students = 91, initial_infected = 5, growth_rate = 0.4
# 2. Initialize current_infected, days
# 3. While current_infected < total_students:
#    a. Print current day and infected count
#    b. Update current_infected = current_infected * (1 + growth_rate)
#    c. Increment days
# 4. Print final results

# Define core parameters
TOTAL_STUDENTS = 91
initial_infected = 5
daily_growth_rate = 0.4  

# Initialize loop variables
current_infected = initial_infected
days = 0  

# Print title for readability
print("=== IBI1 Class Infection Spread Simulation ===")
print(f"Initial infected: {initial_infected} students")
print(f"Daily growth rate: {daily_growth_rate * 100}%\n")

# While loop to calculate infection spread
while current_infected < TOTAL_STUDENTS:
    # Print daily infected number (1 decimal place, meets practical requirement)
    print(f"Day {days}: {current_infected:.1f} students infected")
    current_infected = current_infected * (1 + daily_growth_rate)
    days += 1

# Print final results
print(f"Day {days}: {current_infected:.1f} students infected (Whole class infected)")
print(f"\nTotal days to infect all 91 students: {days} days")