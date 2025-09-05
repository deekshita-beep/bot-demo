from flask import Flask, request, jsonify
import pandas as pd
from deep_translator import GoogleTranslator

app = Flask(__name__)

# Load your student database CSV
df = pd.read_csv("students.csv")  # Make sure this CSV is in the same folder

# Detect language and translate to English if needed
def translate_to_english(text):
    try:
        return GoogleTranslator(source='auto', target='en').translate(text)
    except:
        return text

# Basic query handler
@app.route("/query", methods=["POST"])
def handle_query():
    data = request.json
    user_query = data.get("query", "")
    
    # Translate query to English
    query_en = translate_to_english(user_query).lower()
    
    response = "Sorry, I couldn't understand your query."

    # Example checks
    if "due" in query_en or "fee" in query_en:
        student_name = data.get("student", "")
        student_row = df[df["Name"].str.lower() == student_name.lower()]
        if not student_row.empty:
            due = student_row.iloc[0]["Fee Due"]
            response = f"{student_name}'s fee due is {due}."
    elif "timetable" in query_en or "time table" in query_en:
        student_name = data.get("student", "")
        student_row = df[df["Name"].str.lower() == student_name.lower()]
        if not student_row.empty:
            timetable = student_row.iloc[0]["Time Table"]
            response = f"{student_name}'s timetable: {timetable}."
    elif "attendance" in query_en:
        student_name = data.get("student", "")
        student_row = df[df["Name"].str.lower() == student_name.lower()]
        if not student_row.empty:
            attendance = student_row.iloc[0]["Attendance %"]
            response = f"{student_name}'s attendance is {attendance}%."

    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

