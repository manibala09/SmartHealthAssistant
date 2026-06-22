import database
from flask import Flask, render_template, request, redirect
from health_data import health_data
import sqlite3
from datetime import datetime
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html", found=None)


@app.route("/predict", methods=["POST"])
def predict():

    symptom = request.form["symptom"].lower()
    current_time = datetime.now().strftime("%d-%m-%Y %I:%M %p")

    # Save symptom to database
    conn = sqlite3.connect("health.db")
    cursor = conn.cursor()

    cursor.execute(
    "INSERT INTO history(symptom, date_time) VALUES (?, ?)",
    (symptom, current_time)
)

    conn.commit()
    conn.close()

    causes = []
    foods = []
    care = []

    found = False

    for key in health_data:

        if key in symptom:

            found = True

            causes.extend(health_data[key]["causes"])
            foods.extend(health_data[key]["food"])
            care.extend(health_data[key]["care"])

    if found:

        return render_template(
            "index.html",
            symptom=symptom,
            causes=list(set(causes)),
            foods=list(set(foods)),
            care=list(set(care)),
            found=True
        )

    return render_template(
        "index.html",
        symptom=symptom,
        found=False
    )


@app.route("/bmi")
def bmi():
    return render_template("bmi.html")


@app.route("/calculate_bmi", methods=["POST"])
def calculate_bmi():

    weight = float(request.form["weight"])
    height = float(request.form["height"])

    height = height / 100

    bmi = weight / (height * height)

    if bmi < 18.5:
        status = "Underweight"
    elif bmi < 25:
        status = "Healthy Weight"
    elif bmi < 30:
        status = "Overweight"
    else:
        status = "Obese"

    return render_template(
        "bmi.html",
        bmi=round(bmi, 2),
        status=status,
        weight=weight,
        height=request.form["height"]
    )


@app.route("/water")
def water():
    return render_template("water.html")


@app.route("/calculate_water", methods=["POST"])
def calculate_water():

    weight = float(request.form["weight"])

    water_ml = weight * 35
    water_liters = round(water_ml / 1000, 2)

    return render_template(
        "water.html",
        weight=weight,
        water=water_liters
    )


@app.route("/history")
def history():

    conn = sqlite3.connect("health.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM history ORDER BY id ASC"
    )

    records = cursor.fetchall()

    conn.close()

    return render_template(
        "history.html",
        records=records
    )
@app.route("/delete/<int:id>")
def delete(id):

    conn = sqlite3.connect("health.db")
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM history WHERE id=?",
        (id,)
    )

    cursor.execute("SELECT COUNT(*) FROM history")
    count = cursor.fetchone()[0]

    if count == 0:
        cursor.execute(
            "DELETE FROM sqlite_sequence WHERE name='history'"
        )

    conn.commit()
    conn.close()

    return redirect("/history")
@app.route("/clear_history")
def clear_history():

    conn = sqlite3.connect("health.db")
    cursor = conn.cursor()

    cursor.execute("DELETE FROM history")

    cursor.execute(
        "DELETE FROM sqlite_sequence WHERE name='history'"
    )

    conn.commit()
    conn.close()

    return redirect("/history")

if __name__ == "__main__":
    app.run(debug=True)