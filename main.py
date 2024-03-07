import subprocess
import sys

# install packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

import mysql.connector


class KrautundruebenDatabaseManager:

    def __init__(self):
        self.sql_connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database=""
        )
        self.create_database()
        self.krautundrueben_connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="krautundrueben"
        )
        self.db_cursor = self.krautundrueben_connection.cursor()

    def create_database(self):
        self.sql_connection.cursor().execute("""DROP DATABASE IF EXISTS krautundrueben;
            CREATE DATABASE IF NOT EXISTS krautundrueben;
            USE krautundrueben;""")
        print("created database")

    def execute_sql(self, statement):
        print(statement)
        self.db_cursor.execute(f"""{statement}""")
        result = self.db_cursor.fetchall()
        for item in result:
            item = [str(x) for x in item]
            ", ".join(item)
            print("\n")
        return result

    def execute_sql_commit(self, statement):
        self.db_cursor.execute(f"""{statement}""")
        self.krautundrueben_connection.commit()

    def select(self, statement: str = "*"):
        print()
        print(statement)
        self.db_cursor.execute(f"""{statement}""")
        result = self.db_cursor.fetchall()
        for item in result:
            print("\t" + str(item))
        return result

    # Auswahl aller Rezepte einer bestimmten Ernährungskategorie
    def select_rezept_by_ernährungskategorie(self, ernährungskategorie: str):
        self.select(
            f"SELECT * FROM rezept JOIN ernährungskategorierezept ER ON rezept.RezeptNr = ER.RezeptNr JOIN ernährungskategorie E ON ER.ErnährungskategorieNr = E.ErnährungskategorieNr WHERE E.Bezeichnung = '{ernährungskategorie}';")

    # Auswahl von Rezepten entsprechend vorgegebener Ernährungskategorien
    def select_rezept_by_ernährungskategorien(self, *args: str):
        # Makrobiotisch
        selectors = [f"E.Bezeichnung = '{x}'" for x in args]
        selector = " AND ".join(selectors)
        self.select(
            f"SELECT * FROM `rezept` JOIN ernährungskategorierezept ER ON rezept.RezeptNr = ER.RezeptNr JOIN ernährungskategorie E ON ER.ErnährungskategorieNr = E.ErnährungskategorieNr WHERE {selector};")

    # Zusammenstellung von Zutaten entsprechend einem Rezept
    def select_zutaten_by_rezeptnr(self, rezeptnr: int):
        self.select(
            f"SELECT Zutat.* FROM Zutat JOIN Zutatrezept ON Zutat.ZutatNr = Zutatrezept.ZutatNr JOIN Rezept ON Zutatrezept.RezeptNr = Rezept.RezeptNr WHERE Rezept.RezeptNr = {rezeptnr};")

    # Auswahl aller Zutaten eines Rezeptes nach Rezeptname
    def select_zutaten_by_rezeptname(self, rezeptname: str):
        self.select(
            f"SELECT Zutat.* FROM Zutat JOIN Zutatrezept ON Zutat.ZutatNr = Zutatrezept.ZutatNr JOIN Rezept ON Zutatrezept.RezeptNr = Rezept.RezeptNr WHERE Rezept.Name = '{rezeptname}';")

    # Auswahl aller Rezepte, die eine gewisse Zutat enthalten
    def select_rezept_by_zutat(self, zutat: str):
        self.select(
            f"SELECT R.* FROM zutat AS Z JOIN zutatrezept AS ZR ON Z.ZutatNr = ZR.ZutatNr JOIN rezept AS R ON R.RezeptNr = ZR.RezeptNr WHERE Z.Bezeichnung = '{zutat}';")

    # Auswahl aller Zutaten, die bisher keinem Rezept zugeordnet sind
    def select_unused_zutaten(self):
        self.select(
            "SELECT Z.* FROM zutat AS Z LEFT JOIN zutatrezept ZR ON ZR.ZutatNr = Z.ZutatNr WHERE ZR.ZutatNr IS NULL;")

    # Auswahl aller Rezepte, die eine bestimmte Kalorienmenge nicht überschreiten
    def select_rezepte_kolorien_not_bigger_than(self, max_kalorien: int):
        self.select(
            f"SELECT R.*, SUM(z.Kalorien) AS RezeptKalorien FROM Rezept R LEFT JOIN zutatrezept ZR ON ZR.RezeptNr = R.RezeptNr LEFT JOIN zutat Z ON ZR.ZutatNr = Z.ZutatNr GROUP BY R.RezeptNr HAVING COALESCE(SUM(Z.Kalorien), 0) <= {max_kalorien};")

    # Auswahl aller Rezepte, die weniger als fünf Zutaten enthalten
    def select_rezepte_by_max_zutaten(self, max_zutaten: int):
        self.select(
            f"SELECT R.*, COUNT(ZR.ZutatNr) FROM Rezept R LEFT JOIN zutatrezept ZR ON ZR.RezeptNr = R.RezeptNr GROUP BY R.RezeptNr HAVING COUNT(ZR.ZutatNr) <= {max_zutaten};")

    # Auswahl aller Rezepte, die weniger als fünf Zutaten enthalten und eine bestimmte Ernährungskategorie erfüllen
    def select_rezepte_by_max_zutaten_by_ernährungskategorie(self, max_zutaten: int, ernährungskategorie: str):
        self.select(
            f"SELECT R.*, E.Bezeichnung AS Ernährungskategorie, COUNT(ZR.ZutatNr) AS ZutatenAnzahl FROM Rezept R LEFT JOIN zutatrezept ZR ON ZR.RezeptNr = R.RezeptNr LEFT JOIN ernährungskategorierezept ER ON R.RezeptNr = ER.RezeptNr LEFT JOIN Ernährungskategorie E ON ER.ErnährungskategorieNr = E.ErnährungskategorieNr WHERE E.Bezeichnung = '{ernährungskategorie}' GROUP BY R.RezeptNr HAVING COUNT(ZR.ZutatNr) <= {max_zutaten};")

    # Auswahl von Rezepten auf Basis von Beschränkungen
    def select_rezept_by_allergen(self, allergen: str):
        self.select(
            f"SELECT Rezept.* FROM Rezept WHERE Rezept.RezeptNr IN ( SELECT Zutatrezept.RezeptNr FROM Zutatrezept JOIN Zutatallergen ON Zutatrezept.ZutatNr = Zutatallergen.ZutatNr JOIN Allergen ON Zutatallergen.AllergenNr = Allergen.AllergenNr WHERE Allergen.Bezeichnung IN ('{allergen}') );")

    # Auskunft über Daten nach DSGVO
    def get_dsgvo_kunde(self, kundennr: int):
        self.select(
            f"SELECT Vorname, Nachname, Geburtsdatum, Strasse, HausNr, PLZ, Ort, Email, Telefon FROM kunde WHERE KundenNr = {kundennr};")

    def create_stored_procedured(self):
        self.execute_sql(
            "CREATE PROCEDURE `SelectZutatenByRezeptNr`(IN `RezeptNr` INT) NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER SELECT Zutat.* FROM Zutat JOIN Zutatrezept ON Zutat.ZutatNr = Zutatrezept.ZutatNr JOIN Rezept ON Zutatrezept.RezeptNr = Rezept.RezeptNr WHERE Rezept.RezeptNr = RezeptNr;")
        self.execute_sql(
            "CREATE PROCEDURE `SelectZutatenByRezeptName`(IN `RezeptName` VARCHAR(100)) NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER SELECT Zutat.* FROM Zutat JOIN Zutatrezept ON Zutat.ZutatNr = Zutatrezept.ZutatNr JOIN Rezept ON Zutatrezept.RezeptNr = Rezept.RezeptNr WHERE Rezept.Name = RezeptName; ")
        self.execute_sql(
            "CREATE PROCEDURE `SelectRezeptByZutat`(IN `ZutatName` VARCHAR(100)) NOT DETERMINISTIC CONTAINS SQL SQL SECURITY DEFINER SELECT R.* FROM zutat AS Z JOIN zutatrezept AS ZR ON Z.ZutatNr = ZR.ZutatNr JOIN rezept AS R ON R.RezeptNr = ZR.RezeptNr WHERE Z.Bezeichnung = ZutatName;")

    # Creating the endpoints of the ERM
    def create_tables(self):
        self.execute_sql("""
            CREATE TABLE Kunde (
                KundenNr            INTEGER NOT NULL AUTO_INCREMENT,
                Vorname             VARCHAR(50),
                Nachname            VARCHAR(50),
                Geburtsdatum	    DATE,
                Strasse             VARCHAR(50),
                HausNr			    VARCHAR(6),			
                PLZ                 VARCHAR(5),
                Ort                 VARCHAR(50),
                Email               VARCHAR(50),
                Telefon             VARCHAR(25),
                DatenlöschungDSGVO  BIT DEFAULT 0,
                PRIMARY KEY (KundenNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE Lieferant (
                LieferantNr         INTEGER NOT NULL AUTO_INCREMENT,
                Name                VARCHAR(50),
                Strasse             VARCHAR(50),
                HausNr			    VARCHAR(6),			
                PLZ                 VARCHAR(5),
                Ort                 VARCHAR(50),
                Email               VARCHAR(50),
                Telefon             VARCHAR(25),
                PRIMARY KEY (LieferantNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE Allergen (
                AllergenNr          INTEGER NOT NULL AUTO_INCREMENT,
                Bezeichnung         VARCHAR(50),
                PRIMARY KEY (AllergenNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE Ernährungskategorie (
                ErnährungskategorieNr   INTEGER NOT NULL AUTO_INCREMENT,
                Bezeichnung             VARCHAR(100),
                PRIMARY KEY (ErnährungskategorieNr)
            );
        """)

        # Creating the main tables in order of the ERM
        self.execute_sql("""
            CREATE TABLE Bestellung (
                BestellNr           INTEGER NOT NULL AUTO_INCREMENT,
                KundenNr            INTEGER NOT NULL,
                Rechnungsbetrag     DECIMAL(10,2) NOT NULL,
                Bestelldatum	    DATE,
                PRIMARY KEY (BestellNr),
                FOREIGN KEY (KundenNr) REFERENCES Kunde (KundenNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE Rezept (
                RezeptNr            INTEGER NOT NULL AUTO_INCREMENT,
                Name                VARCHAR(100),
                hinzugefütAm        DATE DEFAULT CURRENT_DATE,
                Arbeitsschritte     TEXT,
                Ersteller           VARCHAR(50),
                Zeitaufwand         TIME,
                Schwierigkeitsgrad  DECIMAL(2,1),
                PRIMARY KEY (RezeptNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE Zutat (
                ZutatNr             INTEGER NOT NULL AUTO_INCREMENT,
                Bezeichnung         VARCHAR(100),
                Bestand             INTEGER,
                Nettopreis          DECIMAL(10,2) NOT NULL,
                Kalorien			INTEGER,
                Kohlenhydrate		DECIMAL (10,2),
                Protein			    DECIMAL(10,2),
                Maßeinheit          VARCHAR(50),
                LieferantNr         INTEGER,
                PRIMARY KEY (ZutatNr),
                FOREIGN KEY (LieferantNr) REFERENCES Lieferant (LieferantNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE Rezeptbox (
                RezeptboxNr         INTEGER NOT NULL AUTO_INCREMENT,
                Verpackung          VARCHAR(100),
                Extra               VARCHAR(100),
                RezeptNr            INTEGER NOT NULL,
                PRIMARY KEY (RezeptboxNr),
                FOREIGN KEY (RezeptNr) REFERENCES Rezept (RezeptNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE ProduktBestellung (
                ProduktArt          VARCHAR(50) NOT NULL,
                ArtNr               INTEGER NOT NULL,
                BestellNr           INTEGER NOT NULL,
                FOREIGN KEY (BestellNr) REFERENCES Bestellung (BestellNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE RezeptboxBestellung (
                BestellNr           INTEGER NOT NULL,
                RezeptboxNr         INTEGER NOT NULL,
                Menge               INTEGER,
                FOREIGN KEY (BestellNr) REFERENCES Bestellung (BestellNr),
                FOREIGN KEY (RezeptboxNr) REFERENCES Rezeptbox (RezeptboxNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE ZutatBestellung (
                BestellNr           INTEGER NOT NULL,
                ZutatNr             INTEGER NOT NULL,
                Menge               INTEGER,
                FOREIGN KEY (BestellNr) REFERENCES Bestellung (BestellNr),
                FOREIGN KEY (ZutatNr) REFERENCES Zutat (ZutatNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE ZutatAllergen (
                AllergenNr          INTEGER NOT NULL,
                ZutatNr             INTEGER NOT NULL,
                FOREIGN KEY (AllergenNr) REFERENCES Allergen (AllergenNr),
                FOREIGN KEY (ZutatNr) REFERENCES Zutat (ZutatNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE ErnährungskategorieRezept (
                ErnährungskategorieNr   INTEGER NOT NULL,
                RezeptNr                INTEGER NOT NULL,
                FOREIGN KEY (ErnährungskategorieNr) REFERENCES Ernährungskategorie (ErnährungskategorieNr),
                FOREIGN KEY (RezeptNr) REFERENCES Rezept (RezeptNr)
            );
        """)

        self.execute_sql("""
            CREATE TABLE ZutatRezept (
                ZutatNr             INTEGER NOT NULL,
                RezeptNr            INTEGER NOT NULL,
                Menge               INTEGER,
                FOREIGN KEY (ZutatNr) REFERENCES Zutat (ZutatNr),
                FOREIGN KEY (RezeptNr) REFERENCES Rezept (RezeptNr)
            );
        """)



def main():
    print("hi")


if __name__ == '__main__':
    main()
