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


    def execute_query(self, query, params=None):
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error ejecutando la consulta: {e}")
            return None


    def close(self):
        """
        Cierra la conexión con la base de datos.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Conexión cerrada.")