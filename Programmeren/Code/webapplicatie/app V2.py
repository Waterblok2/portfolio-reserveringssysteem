from flask import Flask, request, jsonify
import MySQLdb

app = Flask(__name__)


#database connectie maken
db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="reserveringen")
cur = db.cursor()

@app.route("/", methods=["POST"])
def medewerker_aanmaken():
    resultaat = request.form
    voornaam = resultaat["voornaam"]
    achternaam = resultaat["achternaam"]
    email = resultaat["email"]

    cur.execute("""
                INSERT INTO medewerker (voornaam, achternaam, email)
                VALUES (%s, %s, %s)
                """, (voornaam, achternaam, email))
    db.commit()

    return "Medewerker aangemaakt"

@app.route("/reserveren", methods=["POST"])
def reservering_aanmaken(medewerker_ID, gereedschap_ID, startdatum, einddatum):
    resultaat = request.form


if __name__ == "__main__":
    app.run(debug=True)