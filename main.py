import subprocess
import sys

# install packages
subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])

import mysql.connector


class DatabaseManager:

    def __init__(self, database_name: str = "logistics_system"):
        self.sql_connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database=""
        )
        # always deleting the database and creating it new (for testing)
        self.create_database(database_name)
        self.database_connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database=database_name
        )
        self.db_cursor = self.database_connection.cursor()

    def create_database(self, database_name: str):
        self.sql_connection.cursor().execute(f"""DROP DATABASE IF EXISTS {database_name};""")
        self.sql_connection.cursor().execute(f"""CREATE DATABASE IF NOT EXISTS {database_name};""")
        self.sql_connection.cursor().execute(f"""USE {database_name};""")
        print("created database")

    def execute_sql(self, statement):
        print(statement)
        self.db_cursor.execute(f"""{statement}""")
        # result = self.db_cursor.fetchall()
        # for item in result:
        #     item = [str(x) for x in item]
        #     ", ".join(item)
        #     print("\n")
        # return result

    def execute_sql_commit(self, statement):
        self.db_cursor.execute(f"""{statement}""")
        self.database_connection.commit()

    def select(self, statement: str = "*"):
        print()
        print(statement)
        self.db_cursor.execute(f"""{statement}""")
        result = self.db_cursor.fetchall()
        for item in result:
            print("\t" + str(item))
        return result

    def create_tables(self):
        self.execute_sql("""
            CREATE TABLE ProductType (
                ProductID           INTEGER NOT NULL AUTO_INCREMENT,
                Name                VARCHAR(50),
                Description         VARCHAR(512),
                PRIMARY KEY (ProductID)
            );
        """)

        self.execute_sql("""
            CREATE TABLE UserType (
                UserTypeID          INTEGER NOT NULL AUTO_INCREMENT,
                Name                VARCHAR(50),
                PRIMARY KEY (UserTypeID)
            );
        """)

        self.execute_sql("""
            CREATE TABLE Room (
                RoomID              INTEGER NOT NULL AUTO_INCREMENT,
                RoomNumber          VARCHAR(50),
                PRIMARY KEY (RoomID)
            );
        """)

        self.execute_sql("""
            CREATE TABLE ItemHistoryType (
                ItemHistoryTypeID   INTEGER NOT NULL AUTO_INCREMENT,
                Name                VARCHAR(50),
                PRIMARY KEY (ItemHistoryTypeID)
            );
        """)

        self.execute_sql("""
            CREATE TABLE User (
                UserID              INTEGER NOT NULL AUTO_INCREMENT,
                FirstName           VARCHAR(100),
                LastName            VARCHAR(100),
                Email               VARCHAR(100),
                UserTypeID          INTEGER NOT NULL,
                PasswordHash        VARCHAR(255),
                PRIMARY KEY (UserID),
                FOREIGN KEY (UserTypeID) REFERENCES UserType (UserTypeID)
            );
        """)

        # maybe add the other foreign keys
        self.execute_sql("""
            CREATE TABLE Item (
                ItemID              INTEGER NOT NULL AUTO_INCREMENT,
                ProductID           INTEGER NOT NULL,
                CurrentRoomID       INTEGER,
                BorrowedByUserID    INTEGER,
                Annotation          VARCHAR(512),
                QrCode              VARCHAR(512),
                PRIMARY KEY (ItemID),
                FOREIGN KEY (ProductID) REFERENCES ProductType (ProductID)
            );
        """)

        self.execute_sql("""
            CREATE TABLE ItemHistory (
                HistoryID           INTEGER NOT NULL AUTO_INCREMENT,
                ItemID              INTEGER NOT NULL,
                UserID              INTEGER,
                ItemHistoryTypeID   INTEGER,
                Date                VARCHAR(128),
                RoomID              INTEGER,
                PRIMARY KEY (HistoryID),
                FOREIGN KEY (ItemID) REFERENCES Item (ItemID),
                FOREIGN KEY (UserID) REFERENCES User (UserID),
                FOREIGN KEY (ItemHistoryTypeID) REFERENCES ItemHistoryType (ItemHistoryTypeID),
                FOREIGN KEY (RoomID) REFERENCES Room (RoomID)
            );
        """)


def main():
    dbm = DatabaseManager()
    dbm.create_tables()


if __name__ == '__main__':
    main()
