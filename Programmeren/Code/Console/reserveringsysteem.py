#modules inladen
import MySQLdb
import csv
import os

#Connecties met database maken
db = MySQLdb.connect(host="localhost",
                     user="root",
                     passwd="",
                     db="reserveringen")

cur = db.cursor()

#functies beschrijven
#functie alle reserveringen ophalen
def alle_reserveringen_opvragen():
        cur.execute("""
                select gereedschap.naam, gereedschap.merk, medewerker.voornaam, medewerker.achternaam, Startdatum, einddatum FROM lening
                JOIN gereedschap ON lening.gereedschap_ID = gereedschap.ID
                JOIN medewerker ON lening.medewerker_ID = medewerker.ID
        """)
        resultaten = cur.fetchall()
        print("gevonden rijen:", len(resultaten))
        return resultaten
#functie reserveringen ophalen op basis van meegegeven gereedschapnaam
def reserveringen_opvragen(gereedschapnaam):
    cur.execute("""
                select gereedschap.naam, medewerker.voornaam, medewerker.achternaam, reservering.startdatum, reservering.einddatum FROM lening
                JOIN gereedschap ON reservering.gereedschap_ID = gereedschap.ID
                JOIN medewerker ON reservering.medewerker_ID = medewerker.ID
                WHERE gereedschap.naam = %s
            """,(gereedschapnaam,))
    resultaat = cur.fetchall()
    return resultaat
#functie voor opvragen van Medewerker_ID en doorgeven naar andere functies
def opvragen_medewerker_ID(voornaam, achternaam):
    cur.execute("""
        Select ID FROM medewerker
        WHERE voornaam = %s AND achternaam = %s
    """, (voornaam, achternaam))
    resultaat = cur.fetchone()
    if resultaat:
        print("Fout: Medewerker niet gevonden.")
        return resultaat[0]
    return None
    
#functie voor opvragen van gereedschap_ID en doorgeven naar andere functies
def opvragen_gereedschap_ID (serienummer):
    cur.execute ("""
    Select ID FROM gereedschap
    WHERE serienummer = %s
    """, (serienummer,))
    resultaat = cur.fetchone()
    return resultaat[0]

#functie voor aanmaken medewerker
def medewerker_aanmaken(voornaam, achternaam, email):
    cur.execute("""
                insert into medewerker (voornaam, achternaam, email)
                values (%s, %s, %s)
            """, (voornaam, achternaam, email))
    db.commit()

#functie voor het aanmaken van nieuw gereedschap
def gereedschap_aanmaken(naam, merk, serienummer):
    cur.execute("""
                insert into gereedschap (naam, merk, serienummer)
                values (%s, %s, %s)
            """, (naam, merk, serienummer))
    db.commit()

#functie voor het aanmaken vaan een nieuwe reservering
def reservering_plaatsen(gereedschap_ID, medewerker_ID, startdatum,einddatum):
    cur.execute("""
        INSERT INTO lening (gereedschap_ID, medewerker_ID, startdatum, einddatum)
        VALUES (%s, %s, %s, %s)
    """, (gereedschap_ID, medewerker_ID, startdatum, einddatum))
    db.commit()

#functie voor het verwijderen van gereedschap met extra controle of er nog een resevering staat met aangegeven gereedschap
def gereedschap_verwijderen(gereedschap_ID):
    cur.execute("""
                SELECT COUNT(*) FROM lening WHERE gereedschap_ID = %s
                """, (gereedschap_ID,))
    aantal = cur.fetchone()[0]
    if aantal > 0:
        print ("Kan niet verwijderen: er zijn nog reserveringen gekoppeld an dit gereedschap.")
        bevestiging = input("Weet je zeker dat je het gereedschap wilt verwijderen? (ja/nee) ")
        if bevestiging == "ja":
            cur.execute("""
                        DELETE FROM lening WHERE gereedschap_ID = %s
                        """, (gereedschap_ID,))
            db.commit()
            cur.execute("""
                        DELETE FROM gereedschap WHERE ID = %s
                        """, (gereedschap_ID,))
            db.commit()
            print("Gereedschap succesvol verwijderd")
            return
        else:
            print("Gereedschap niet verwijderd")
            return
    elif aantal == 0:
            cur.execute("""
                DELETE FROM gereedschap WHERE ID = %s
                """, (gereedschap_ID,))
            db.commit()
            print("Gereedschap succesvol verwijderd")
            return
    else:
        print("gereedschap niet gevonden")
        return
    
#functie voor het verwijderen van medewerker met extra controle of er nog een resevering staat met aangegeven medewerker    
def medewerker_verwijderen(medewerker_ID):
    cur.execute("""
                SELECT COUNT(*) FROM lening WHERE medewerker_ID = %s
                """, (medewerker_ID,))
    aantal = cur.fetchone()[0]
    if aantal > 0:
        print("kan medewerker niet verwijderen: Er zijn nog reserveringen gekoppeld aan de medewerker.")
        bevestiging = input("Weet je zeker dat je de medewerker wilt verwijderen? (ja/nee) ")
        if bevestiging == "ja":
            cur.execute("""
                        DELETE FROM lening WHERE medewerker_ID = %s
                        """, (medewerker_ID,))
            db.commit()
            cur.execute("""
                        DELETE FROM medewerker WHERE ID = %s
                        """, (medewerker_ID,))
            db.commit()
        else:
            print("Medewerker niet verwijderd")
            return
    elif aantal == 0:
        cur.execute("""
                    DELETE FROM medewerker WHERE ID = %s
                    """, (medewerker_ID,))
        db.commit()
        print("Medewerker succesvol verwijderd.")
        return
    else:
        print("Medewerker niet gevonden.")
        return
    
#functie voor exporteren naar CSV van alle reserveringen
def export_naar_csv(resultaten):
    print("Exporteren gestart")
    print("Bestand opgeslagen in: ", os.path.abspath("reserveringen.csv"))
    with open("reserveringen.csv", "w") as bestand:
        schrijver = csv.writer(bestand)
        schrijver.writerows(resultaten)
    print("Exporteren klaar")

#keuze menu voor eindgebruiker
while True:
    print("---reserveringsysteem---\nKies uit onderstaande opties\n1. Reservering Plaatsen\n 2. Reservering opzoeken\n3. Medewerker aanmaken\n4. Gereedschap aanmaken\n 5. Reserveringen exporteren\n 6. gereedschap verwijderen\n 7. medewerker verwijderen\n 8. stoppen")
    keuze = int(input("Kies een optie: "))
    #keuze 1 = reservering aanmaken
    if keuze == 1:
        voornaam = input("Voer je voornaam in: ")
        achternaam = input("Voer je achternaam in: ")

        medewerker_ID = opvragen_medewerker_ID(voornaam, achternaam)
        if medewerker_ID is None:
            print("Fout: medewerker niet gevonden")
            continue

        serienummer = input("Vul het serinummer in: ")

        gereedschap_ID = opvragen_gereedschap_ID(serienummer)
        if gereedschap_ID is None:
            print("Fout: Gereedschap niet gevonden")
            continue

        startdatum = input("voer startdatum in (JJJ-MM-DD): ")
        einddatum = input ("Voer einddatum in (JJJJ-MM-DD): ")

        reservering_plaatsen(gereedschap_ID, medewerker_ID, startdatum, einddatum)
        print("Reservering succesvol geplaatst")
    #keuze 2 is reserveringen opzoeken
    elif keuze == 2:
        gereedschapnaam = input("Welk gereedschap wil je opzoeken: ")
        resultaat = reserveringen_opvragen(gereedschapnaam)
        if not resultaat:
            print("Geen reserveringen gevonden")
        else:
            for rij in resultaat:
                print (rij)
    #keuze 3 = medewerker aanmaken
    elif keuze == 3:
        voornaam = input("Voer voornaam in van medewerker: ")
        achternaam = input("Voer achternaam in van medewerker")
        email = input("Voer email in van medewerker")
        medewerker_aanmaken(voornaam, achternaam, email)
        print("Medewerker succesvol aangemaakt")
    # keuze 4 = gereedschap toevoegen
    elif keuze == 4:
        naam = input("Voer naam van gereedschap in: ")
        merk = input("Voer merk van gereedschap in: ")
        serienummer = input ("Voer serienummer van gereedschap in: ")
        gereedschap_aanmaken(naam, merk, serienummer)
        print("Gereedschap succesvol toegevoegd")

    #export aanvragen
    elif keuze == 5:
        export_naar_csv(alle_reserveringen_opvragen())
    #gereedschap verwijderen
    elif keuze == 6:
        serienummer = input("Vul het serienummer in van het gereedschap dat je wilt verwijderen: ")
        gereedschap_ID = opvragen_gereedschap_ID(serienummer)
        print("gevonden ID:", gereedschap_ID)
        if gereedschap_ID is None:
            print("Geen gereedschap gevonden")
            continue
        else:
            gereedschap_verwijderen(gereedschap_ID)

    elif keuze == 7:
        voornaam = input("Vul voornaam in van medewerker: ")
        achternaam = input("Vul achternaam in van medewerker: ")
        medewerker_ID = opvragen_medewerker_ID(voornaam, achternaam)
        print("Gevonden ID:", medewerker_ID)
        if medewerker_ID is None:
            print("Medewerker niet gevonden.")
            continue
        else:
            medewerker_verwijderen(medewerker_ID)

    elif keuze == 8:
        break

    else:
        print("Optie niet gevonden")