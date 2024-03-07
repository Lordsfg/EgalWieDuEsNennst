class SchuhladenDatabaseManager:

    def __init__(self):
        #self.schuhladen_pi_connection = mysql.connector.connect(
        #    host="172.16.5.15",
        #    port=3306,
        #    user="root",
        #    password="itechdb",
        #    database="Schuhladen"
        #)
        self.schuhladen_local_connection = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",
            password="",
            database="Schuhladen"
        )
        self.cursor = self.schuhladen_local_connection.cursor()

    def execute_sql(self, statement):
        self.cursor.execute(f"""{statement}""")
        result = self.cursor.fetchall()
        for item in result:
            print(item)
        print("")
        return result

    def select(self, table: str, selection: str = "*"):
        self.cursor.execute(f"""SELECT {selection} FROM {table};""")
        result = self.cursor.fetchall()
        for item in result:
            print(item)
        return result



def main():
    print("hi")


if __name__ == '__main__':
    main()
