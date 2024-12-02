from flask import Flask, request, jsonify
from flask_cors import CORS
from macro_logic import calculate_macros
from tips import get_tips
import logging
import json
import os

# Initialize Flask application and CORS
app = Flask(__name__)
CORS(app)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Load food recommendations from JSON file
food_chart_path = os.path.join(os.path.dirname(__file__), 'food_chart.json')
with open(food_chart_path, 'r') as f:
    food_recommendations = json.load(f)

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

# API endpoint to calculate macros
@app.route('/api/calculate_macros', methods=['POST'])
def calculate_macros_api():
    try:
        # Collect user input from JSON request
        data = request.get_json()
        app.logger.info("Received data for macro calculation.")

        # Extract user input
        goal = data.get('goal')
        weight = data.get('weight')
        height_feet = data.get('height_feet')
        height_inches = data.get('height_inches')
        age = data.get('age')
        gender = data.get('gender')
        activity_level = data.get('activity_level')

        # Ensure all required fields are provided
        if not all([goal, weight, height_feet, height_inches, age, gender, activity_level]):
            return jsonify({"error": "Missing form fields. Please provide all required inputs."}), 400

        # Calculate macros using the logic function
        macros = calculate_macros(
            weight_lbs=weight,
            height_feet=height_feet,
            height_inches=height_inches,
            age=age,
            gender=gender,
            activity_level=activity_level,
            goal=goal
        )

        # Get tips
        tips = get_tips()

        # Return the calculated macros, tips, and food chart as a JSON response
        return jsonify({
            "macros": macros,
            "tips": tips,
            "food_chart": food_recommendations
        }), 200

    except Exception as e:
        app.logger.error(f"Error during macro calculation: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# Run the app (for local development)
if __name__ == '__main__':
    app.run()
