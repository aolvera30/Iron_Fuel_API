from flask import Flask, request, jsonify
from flask_cors import CORS
from macro_logic import calculate_macros
import logging

app = Flask(__name__)
CORS(app)  # Enable CORS for cross-origin requests

# Configure logging to see debug information in the console
logging.basicConfig(level=logging.INFO)

# API endpoint to calculate macros
@app.route('/api/calculate_macros', methods=['POST'])
def calculate_macros_api():
    try:
        # Collect user input from JSON request
        data = request.get_json()
        app.logger.info(f"Received data: {data}")

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

        # Calculate macros using your macro logic function
        macros = calculate_macros(
            weight_lbs=weight,
            height_feet=height_feet,
            height_inches=height_inches,
            age=age,
            gender=gender,
            activity_level=activity_level,
            goal=goal
        )

        # Log calculated macros
        app.logger.info(f"Calculated Macros: {macros}")

        # Return the calculated macros as a JSON response
        return jsonify({"macros": macros}), 200

    except Exception as e:
        app.logger.error(f"Error during macro calculation: {str(e)}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True)