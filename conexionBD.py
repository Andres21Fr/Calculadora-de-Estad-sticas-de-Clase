import mysql.connector

class ConexionBD:
    def __init__(self):
        try:
            self.conexion = mysql.connector.connect(
                user='root',
                password='Andres',
                host='localhost',
                database='bdejemplo',
                port='3306'
            )
            print("Conexion exitosa")
        except mysql.connector.Error as error:
            print("Error al conectarse a la base de datos: {}".format(error))

    def obtener_cursor(self):
        return self.conexion.cursor()