import logging

logging.basicConfig(level=logging.INFO)

def calculate_macros(
    weight_lbs: float, height_feet: int, height_inches: int, age: int, 
    gender: str, activity_level: str, goal: str
) -> dict:
    try:
        # Convert inputs to the correct types
        weight_lbs = float(weight_lbs)
        height_feet = int(height_feet)
        height_inches = int(height_inches)
        age = int(age)

        # Log for debugging
        logging.info("============================ Input Validation")
        logging.info(f"weight_lbs: {weight_lbs}, height_feet: {height_feet}, height_inches: {height_inches}, age: {age}")
        
        # Convert weight from lbs to kg, height from feet+inches to cm
        weight_kg = weight_lbs * 0.453592
        height_cm = (height_feet * 12 + height_inches) * 2.54

        # Step 1: Calculate BMR using Mifflin-St Jeor Equation
        if gender == 'male':
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age + 5
        else:
            bmr = 10 * weight_kg + 6.25 * height_cm - 5 * age - 161

        # Step 2: Calculate TDEE (adjusting activity factor)
        activity_factors = {
            'lightly_active': 1.375,
            'moderately_active': 1.55,
            'very_active': 1.725
        }

        if activity_level not in activity_factors:
            raise ValueError(f"Invalid activity level: {activity_level}. Must be one of: 'lightly_active', 'moderately_active', or 'very_active'.")

        tdee = bmr * activity_factors[activity_level]

        # Step 3: Adjust calories based on goal
        if goal == 'lose_fat':
            daily_calories = max(tdee - 500, 1200)
        elif goal == 'build_muscle':
            daily_calories = tdee + 250
        else:
            daily_calories = tdee  # maintain weight

        # Step 4: Calculate Macros
        protein_grams = weight_kg * 2.0
        protein_calories = protein_grams * 4  # 1g protein = 4 kcal

        fat_calories = daily_calories * 0.25
        fat_grams = fat_calories / 9  # 1g fat = 9 kcal

        remaining_calories = max(daily_calories - (protein_calories + fat_calories), 0)
        carbs_grams = remaining_calories / 4  # 1g carbohydrate = 4 kcal

        return {
            'calories': round(daily_calories),
            'protein': round(protein_grams),
            'fats': round(fat_grams),
            'carbs': round(carbs_grams)
        }
    except Exception as e:
        logging.error(f"Error in calculate_macros: {e}")
        raise
