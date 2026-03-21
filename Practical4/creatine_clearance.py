# Using the Cockcroft-Gault formula to calculate creatine clearance
# input variables: age, weight, concentration, gender
# check the validity of age, weight, concentration, gender
# calculated variable: clearance = (140 - age) * weight / (concentration * 72) * (0.85 if female)
# output: creatine clearance in mL/min

def calculate_creatine_clearance():
    errors = []

    # Age input and validation
    try:
        age = int(input("Enter age (years): "))
        if age <= 0 or age >= 100:
            errors.append("Age must be between 0 and 100")
    except ValueError:
        errors.append("Age must be an integer")

    # Weight input and validation
    try:
        weight = float(input("Enter weight (kg): "))
        if weight <= 20 or weight >= 80:
            errors.append("Weight must be between 20 and 80 kg")
    except ValueError:
        errors.append("Weight must be a number")

    # Gender input and validation
    gender = input("Enter gender (male/female): ").strip().lower()
    if gender not in ["male", "female"]:
        errors.append("Gender must be 'male' or 'female'")

    # Creatinine input and validation
    try:
        cr = float(input("Enter creatinine level (µmol/L): "))
        if cr <= 0 or cr >= 100:
            errors.append("Creatinine level must be >0 and <100")
    except ValueError:
        errors.append("Creatinine level must be a number")

    # If any errors, exit
    if errors:
        print("Input errors detected, please fix the following:")
        for e in errors:
            print("-", e)
        return

    # Calculate CrCl
    factor = 0.85 if gender == "female" else 1.0
    crcl = ((140 - age) * weight) / (72 * cr) * factor

    # Show result
    print(f"\nResult: CrCl = {crcl:.2f} mL/min")


if __name__ == "__main__":
    print("Creatinine Clearance Calculator")
    calculate_creatine_clearance()