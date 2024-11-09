import os
from flask import Flask, render_template, request, jsonify
import openai

# Initialize Flask App
app = Flask(__name__)

# Set Azure OpenAI API credentials
openai.api_key = "F4t6ZhKWbThgotYQuaNURBVcJsDcqL4xkebqwPiVrVHw3s8d7dTjJQQJ99AKACfhMk5XJ3w3AAABACOGoNkI"
openai.api_base = "https://educationhackathon.openai.azure.com/"  # Replace with your Azure endpoint
openai.api_version = "2024-08-01-preview"

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_questions", methods=["POST"])
def get_questions():
    user_data = request.json  # Get user data from frontend
    
    subject = user_data.get("subject")
    interests = user_data.get("interests")
    characteristics = user_data.get("characteristics")
    
    # Generate personalized revision question
    prompt = f"Generate a revision question for a {subject} student who is interested in {interests} and has the following characteristics: {characteristics}. Make the question challenging and related to their interests."
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",  # Or the model you prefer
            messages=[
                {"role": "system", "content": "You are a helpful assistant who creates personalized revision questions."},
                {"role": "user", "content": prompt}
            ]
        )

        question = response['choices'][0]['message']['content']
        return jsonify({"question": question})

    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == "__main__":
    app.run(debug=True)
