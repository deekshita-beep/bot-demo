import pandas as pd
from flask import Flask, request, jsonify
from langdetect import detect
from googletrans import Translator

# Load student data
students = pd.read_csv("students.csv")
translator = Translator()

app = Flask(__name__)

def get_student(roll_no):
    row = students[students["Roll No"] == roll_no]
    return row.iloc[0] if not row.empty else None

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    roll_no = data.get("roll_no")
    user_query = data.get("query", "")

    student = get_student(roll_no)
    if student is None:
        return jsonify({"error": "Student not found"}), 404

    # 1. Detect language
    lang = detect(user_query)

    # 2. Translate to English
    translated = translator.translate(user_query, src=lang, dest="en").text.lower()

    # 3. Simple intent matching
    response = "Sorry, I couldn’t understand."
    intent = "unknown"

    if "fee" in translated and "due" in translated:
        response = f"Your fee due is {student['Fee Due (INR)']} INR."
        intent = "fee_due"
    elif "total fee" in translated:
        response = f"Your total fee is {student['Total Fee (INR)']} INR."
        intent = "total_fee"
    elif "paid" in translated or "already paid" in translated:
        response = f"You have already paid {student['Fee Paid (INR)']} INR."
        intent = "fee_paid"
    elif "attendance" in translated:
        response = f"Your attendance is {student['Attendance %']}%."
        intent = "attendance"
    elif "faculty" in translated:
        response = f"Your faculty is {student['Faculty Name']}."
        intent = "faculty"
    elif "holiday" in translated:
        response = f"Upcoming holidays: {student['Holidays List']}."
        intent = "holidays"
    elif "timetable" in translated or "time table" in translated:
        response = f"Your timetable: {student['Timetable']}."
        intent = "timetable"

    # 4. Translate response back
    final_response = translator.translate(response, src="en", dest=lang).text

    return jsonify({
        "original_query": user_query,
        "detected_language": lang,
        "translated_query": translated,
        "intent": intent,
        "response": final_response
    })

if __name__ == "__main__":
    app.run(debug=True)
