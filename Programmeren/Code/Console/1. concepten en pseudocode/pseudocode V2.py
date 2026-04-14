start

#connectie met database maken
database = database.inloggegevens(locatie="lokaal",
                                  gebruiker="gebruikersnaam",
                                  wachtwoord="wachtwoord",
                                  database="Naam-database")

#voorbereiden query's
Zoekterm = {ingetypt gereedschap}

opvragen_gereedschap = """
                    Selecteer gereedschap.naam, Medewerker.voornaam, Medewerker.achternaam, reservering.start_datum, reservering.eind_datum
                    van reserveringen
                    Koppel Gereedschap op Reservering.gereedschap_id = gereedschap.gereedschap_id
                    Koppel Medewerkers op Reserveringen.medewerker_id = Medewerkers.medewerker_ID
                    waar gereedschap.naam = ?
                    """

Medewerker_opzoeken = """"
                        selecteer Medewerker_ID
                        van Medewerkers
                        Waar voornaam = ? en achternaam = ?
                    """"

Reservering_plaatsen = """
                        plaats in Reserveringen (Medewerker_ID, Gereedschap_ID, start_datum, eind_datum)
                        waardes (?,?,?,?)
                       """"



While True

    Opties_weergeven=input("kies onderstaande opties
                        1. Reservering plaatsen
                        2. Reservering opzoeken
                        3. Reserveringen exporteren")

    Als Opties_weergeven == "1.":
        print("Reservering plaatsen")
        Medewerker_voornaam = input("voer je voornaam in: ")
        Medewerker_achternaam = input("Voer je achternaam in: ")
        Gevonden_Medewerker_ID = Medewerker_opzoeken(Medewerker_voornaam, Medewerker_achternaam)
        Als gevonden_medewerker_ID leeg is:
            print("Fout: Medewerker niet gevonden")
            Stop en terug naar Opties_weergeven
        Serienummer_gereedschap = input("vul het serienummer in van het gereedschap dat je wilt reseveren: ")
        Gevonden_Gereedschap_ID = Gereedschap_opzoeken(Serienummer_gereedschap)
        Als Gevonden_gereedschap_ID leeg is:
            Print("Fout: Gereedschap niet gevonden.")
            stop en terug naar Opties_weergeven
        start_datum_reservering = input("Vul de startdatum in dat je het gereedschap wilt reserveren: ")
        Eind_datum_reservering = input("Vul de einddatum van je reservering in: ")
        Reservering_plaatsen(Gevonden_Medewerker_ID Gevonden_Gereedschap_ID, start_datum_reservering,Eind_datum_reservering)

    Als Opties_weergeven == "2.":
            Gereedschap = input("Welk gereedschap wil je opzoeken: ")
            opvragen_gereedschap(Gereedschap)

    Als Opties_weergeven == "3.":
        Opvragen_gereedschap exporteren

    Als Opties_weergeven == "4.":
    stop while True (break)

    Anders:
        Print("Optie niet gevonden")