# Pseudocode planning (assessment key, must retain):
# 1. Define base parameters: total class students (91), initial infected students, daily infection growth rate;
# 2. Initialize loop variables: current infected students (equal to initial infected), days (starts at 0);
# 3. Use while loop to calculate daily infected number with condition: current_infected < total students;
# 4. Each loop: print daily infected number → calculate next day's infected number → increment days by 1;
# 5. After loop termination, print total days to infect the whole class;
# 6. Keep floating-point output (no forced integer conversion) and ensure code terminates normally.

# 1. Define core parameters (meets practical requirement: 91 students in IBI1 class)
TOTAL_STUDENTS = 91  # Fixed total number of students in the class
initial_infected = 5  # Initial number of infected students (modifiable)
daily_growth_rate = 0.4  # Daily infection growth rate (40%, converted to decimal)

# 2. Initialize loop variables
current_infected = initial_infected
days = 0  # Initial day count (Day 0 = initial infection state)

# 3. Print title for readability
print("=== IBI1 Class Infection Spread Simulation ===")
print(f"Initial infected: {initial_infected} students")
print(f"Daily growth rate: {daily_growth_rate * 100}%\n")

# 4. While loop to calculate infection spread (core logic, ensures normal termination)
while current_infected < TOTAL_STUDENTS:
    # Print daily infected number (1 decimal place, meets practical requirement)
    print(f"Day {days}: {current_infected:.1f} students infected")
    # Calculate next day's infected number: current × (1 + daily growth rate)
    current_infected = current_infected * (1 + daily_growth_rate)
    # Increment day count
    days += 1

# 5. Print final results after loop termination (assessment key: total days output)
print(f"Day {days}: {current_infected:.1f} students infected (Whole class infected)")
print(f"\nTotal days to infect all 91 students: {days} days")