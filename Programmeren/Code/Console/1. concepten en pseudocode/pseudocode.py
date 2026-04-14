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
                    Groepeer Gereedschap op Reservering.gereedschap_id = gereedschap.gereedschap_id
                    Groepeer Medewerkers op Reserveringen.medewerker_id = Medewerkers.medewerker_ID
                    """

Medewerker_opzoeken = """"
                        selecteer Medewerker_ID
                        van Medewerkers
                        Waar voornaam = ? en achternaam = ?
                    """"

Reservering_plaatsen = """
                        plaats in Reserveringen (Medewerker_voornaam, Medewerker_achternaam Gereedschap_ID, start_datum, eind_datum)
                        waardes (?,?,?,?,?)
                       """"

Opties_weergeven=input("kies onderstaande opties
                        1. Reservering plaatsen
                        2. Reservering opzoeken
                        3. Reserveringen exporteren")

While True
    Als Opties_weergeven = "1.":
        print("Reservering plaatsen")
        Medewerker_voornaam = input("voer je voornaam in: ")
        Medewerker_achternaam = input("Voer je achternaam in: ")
        Serienummer_gereedschap = input("vul het serienummer in van het gereedschap dat je wilt reseveren: ")
        start_datum_reservering = input("Vul de startdatum in dat je het gereedschap wilt reserveren: ")
        Eind_datum_reservering = input("Vul de einddatum van je reservering in: ")
        Reservering_plaatsen(Medewerker_voornaam, Medewerker_achternaam, Serienummer_gereedschap, start_datum_reservering,Eind_datum_reservering)

    Als Opties_weergeven = "2.":
            Gereedschap = input("Welk gereedschap wil je opzoeken: ")
            opvragen_gereedschap(Gereedschap)

    Als Opties_weergeven = "3.":
        Opvragen_gereedschap exporteren

    Anders:
        Print("Optie niet gevonden")