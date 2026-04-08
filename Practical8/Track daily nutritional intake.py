#Track daily nutritional intake

class FoodItem:
    #Class to represent a food item with nutritional information.
    
    def __init__(self, name, calories, protein, carbs, fat):
        """
        Initialize a FoodItem instance.
        :param name: Name of the food (string)
        :param calories: Calorie content (kcal, float/int)
        :param protein: Protein content (grams, float/int)
        :param carbs: Carbohydrate content (grams, float/int)
        :param fat: Fat content (grams, float/int)
        """
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat


def calculate_daily_nutrition(food_list):
    """
    Calculate and display total daily nutritional intake.
    Show warnings if calories exceed 2500 kcal or fat exceeds 90 grams.
    :param food_list: List of FoodItem objects
    """
    # Initialize total values
    total_calories = 0
    total_protein = 0
    total_carbs = 0
    total_fat = 0

    # Sum nutrition from all food items
    for food in food_list:
        total_calories += food.calories
        total_protein += food.protein
        total_carbs += food.carbs
        total_fat += food.fat

    # Display total nutrition results
    print("=== 24-Hour Nutritional Intake Summary ===")
    print(f"Total Calories: {total_calories:.2f} kcal")
    print(f"Total Protein: {total_protein:.2f} g")
    print(f"Total Carbohydrates: {total_carbs:.2f} g")
    print(f"Total Fat: {total_fat:.2f} g")

    # Warning conditions
    print("\n=== Warnings ===")
    if total_calories > 2500:
        print("WARNING: Calorie intake exceeds 2500 kcal!")
    if total_fat > 90:
        print("WARNING: Fat intake exceeds 90 grams!")
    if total_calories <= 2500 and total_fat <= 90:
        print("No warnings - Nutrition intake is within recommended limits.")


# Example usage (required by the assignment)
if __name__ == "__main__":
    # Create food items
    apple = FoodItem("Apple", 60, 0.3, 15, 0.5)
    chicken = FoodItem("Grilled Chicken", 250, 30, 0, 5)
    rice = FoodItem("Cooked Rice", 130, 2.7, 28, 0.3)
    avocado = FoodItem("Avocado", 160, 2, 9, 15)

    # 24-hour food intake list
    daily_food = [apple, chicken, rice, avocado]

    # Calculate and show results
    calculate_daily_nutrition(daily_food)