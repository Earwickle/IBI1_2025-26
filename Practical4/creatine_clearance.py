# Pseudocode planning (key for assessment, must be retained):
# 1. Define input validation rules:
#    - Age: integer, and < 100 years old
#    - Weight: float, and 20 < weight < 80 kg
#    - Gender: string, only "male" or "female" (case-insensitive)
#    - Creatinine level (Cr): float, and 0 < Cr < 100 µmol/l
# 2. Get user input and handle type conversion exceptions (e.g., non-numeric input)
# 3. Validate each input against rules, record invalid items and give prompts
# 4. If all inputs are valid, calculate CrCl using Cockcroft-Gault formula:
#    CrCl = [(140 - age) × weight] / (72 × creatinine_level) × coefficient (0.85 for female, 1 for male)
# 5. Output CrCl result (rounded to 2 decimal places for readability)
# 6. If there are invalid inputs, only prompt specific error variables without calculating CrCl

# Core function: Creatinine Clearance (CrCl) Calculator (strictly follows Cockcroft-Gault formula)
def calculate_creatine_clearance():
    # Initialize input validation status and error messages
    input_errors = []
    age = None
    weight = None
    gender = None
    cr_level = None

    # 1. Get and validate age input
    try:
        age = int(input("Please enter patient's age (years): "))
        if age >= 100:
            input_errors.append("Age must be less than 100 years")
    except ValueError:
        input_errors.append("Age must be an integer")

    # 2. Get and validate weight input
    try:
        weight = float(input("Please enter patient's weight (kg): "))
        if not (20 < weight < 80):
            input_errors.append("Weight must be greater than 20kg and less than 80kg")
    except ValueError:
        input_errors.append("Weight must be a number")

    # 3. Get and validate gender input
    gender_input = input("Please enter patient's gender (male/female): ").strip().lower()
    if gender_input not in ["male", "female"]:
        input_errors.append("Gender only supports 'male' or 'female'")
    else:
        gender = gender_input

    # 4. Get and validate creatinine level input
    try:
        cr_level = float(input("Please enter patient's creatinine level (µmol/l): "))
        if not (0 < cr_level < 100):
            input_errors.append("Creatinine level must be greater than 0µmol/l and less than 100µmol/l")
    except ValueError:
        input_errors.append("Creatinine level must be a number")

    # 5. Judge input validation result
    if input_errors:
        # Output specific error messages (assessment requirement: prompt variables to correct)
        print("❌ Invalid input, please correct the following issues:")
        for error in input_errors:
            print(f"   - {error}")
        return  # Terminate calculation if there are invalid inputs

    # 6. Calculate CrCl (execute only when all inputs are valid)
    # Basic formula calculation
    crcl_base = (140 - age) * weight / (72 * cr_level)
    # Gender coefficient correction
    gender_coefficient = 0.85 if gender == "female" else 1.0
    crcl = crcl_base * gender_coefficient

    # 7. Output result (rounded to 2 decimal places, in line with clinical data display habits)
    print(f"\n✅ Calculation Result:")
    print(f"Patient Age: {age} years, Weight: {weight}kg, Gender: {gender}, Creatinine Level: {cr_level}µmol/l")
    print(f"Creatinine Clearance (CrCl): {crcl:.2f}")

# Execute the calculator function
if __name__ == "__main__":
    print("===== Creatinine Clearance (CrCl) Calculator =====\n")
    calculate_creatine_clearance()