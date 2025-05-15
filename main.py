
from flask import Flask, request, jsonify
import openai
import base64

app = Flask(__name__)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT = """
אתה מקבל קובץ Excel של שיבוץ חיילים.
המבנה אינו טבלאי סטנדרטי — מדובר בטבלת שיבוצים ויזואלית.

הוראות ניתוח:
1. בתא כלשהו יופיע שם של חייל.
2. התא שמשמאל לשם יכיל את שעת השיבוץ (למשל "14:00-22:00" או "14:00").
3. עליך לעלות כלפי מעלה באותו הטור עד שתמצא שם של אחת המשימות מהרשימה הבאה:
ש.ג., מערבית, של"ז, כיתת כוננות, תורני רס"פ, סיור 80, חץ דרוך, תורני מטבח, חווה 7, חפק, חמל
4. שם המשימה הראשון שאתה מוצא למעלה — הוא המשימה של החייל.
5. אם עבור חייל מופיעה שעה אחת בלבד (למשל "14:00") — התייחס אליה כאל תחילת המשמרת בלבד.
6. בתא אחר בטבלה מופיעה המילה "תאריך", ולצידה מופיע התאריך הרלוונטי. יש להוציא את התאריך הזה ולהוסיפו לכל שיבוץ.

הפק פלט בפורמט JSON לפי הדוגמה:
[
  { "name": "יוחאי מנדבי", "task": "סיור 80", "time": "06:00-14:00", "date": "15.5.25" }
]
"""

@app.route("/analyze", methods=["POST"])
def analyze():
    file = request.files['file']
    file_content = base64.b64encode(file.read()).decode('utf-8')

    response = openai.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[
            {
                "role": "user",
                "content": [
                    { "type": "text", "text": PROMPT },
                    { "type": "image_url", "image_url": {
                        "url": f"data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{file_content}"
                    }}
                ]
            }
        ],
        max_tokens=2000
    )

    return jsonify({ "result": response.choices[0].message.content })

app.run(host="0.0.0.0", port=8080)
