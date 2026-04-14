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

if __name__ == "__main__":
    app.run(debug=True)