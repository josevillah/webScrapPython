import mysql.connector
from mysql.connector import Error

class Connection:
    def __init__(self):
        self.host="localhost"
        self.user="root"
        self.password="leticia1994"
        self.database="isaflorc_web"
        self.connection = None

    def connect(self):
        """
        Establece la conexión con la base de datos.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                print("Conexión exitosa a la base de datos.")
        except Error as e:
            print(f"Error al conectar a la base de datos: {e}")

    def execute_query(self, query):
        """
        Ejecuta una consulta SQL.
        """
        if not self.connection or not self.connection.is_connected():
            print("No hay conexión activa a la base de datos.")
            return None

        try:
            cursor = self.connection.cursor()
            cursor.execute(query)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error al ejecutar la consulta: {e}")
            return None

    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")