from flask import Flask, request, jsonify
from flask_cors import CORS
import MySQLdb

app = Flask(__name__)
CORS(app)

# Connectie maken met database
db = MySQLdb.connect(
    host="localhost",
    user="root",
    passwd="",
    db="reserveringen"
)
cur = db.cursor()  # Haakjes toegevoegd!

# Route aanmaken
@app.route("/medewerker", methods=["GET"])
def medewerkers_ophalen():
    
    cur.execute("""
        SELECT id, voornaam, achternaam, email FROM medewerker
    """)
    resultaten = cur.fetchall()

    # Resultaten plaatsen in Python dictionary
    medewerker_lijst = []
    for rij in resultaten:
        medewerker = {
            "id": rij[0],
            "voornaam": rij[1],
            "achternaam": rij[2],
            "email": rij[3]
        }
        medewerker_lijst.append(medewerker)

    # Dictionary terugsturen als JSON
    return jsonify({"status": "succes", "data": medewerker_lijst})

# flask applicatie starten
if __name__ == '__main__':
    app.run(debug=True)