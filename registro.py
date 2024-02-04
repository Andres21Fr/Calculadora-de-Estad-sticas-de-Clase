import mysql.connector
from PyQt6 import QtWidgets, uic

from conexionBD import ConexionBD

app = QtWidgets.QApplication([])

# Crear una instancia única de ConexionBD
conexion_bd = ConexionBD()

registro = uic.loadUi("registro.ui")

def registrar():
    ced = registro.lineEdit.text()
    nom = registro.lineEdit_2.text()
    ape = registro.lineEdit_3.text()
    cor = registro.lineEdit_4.text()

    # Verificar si algún campo está vacío
    if not ced or not nom or not ape or not cor:
        registro.label_6.setText("Por favor, complete todos los campos.")
        return

    # Validar que ced sea un valor no vacío y sea convertible a entero
    try:
        ced = int(ced)
    except ValueError:
        registro.label_6.setText("Usuario cedula no es valido")
        return

    consulta = "INSERT INTO usuarios(cedula, nombre, apellido, correo) VALUES (%s, %s, %s, %s)"
    parametros = (ced, nom, ape, cor)

    try:
        # Obtener el cursor de la conexión
        cursor = conexion_bd.obtener_cursor()
        
        # Ejecutar la consulta
        cursor.execute(consulta, parametros)

        # Realizar el commit utilizando el cursor
        conexion_bd.conexion.commit()

        registro.label_6.setText("Usuario creado Exitosamente")

    except mysql.connector.Error as error:
        print(f"Error al ejecutar la consulta: {error}")
        registro.label_6.setText("No se pudo completar la operación")

    finally:
        # Cerrar el cursor
        cursor.close()

def limpiar_campos():
    # Limpia todos los QLineEdit en tu interfaz
    registro.lineEdit.clear()
    registro.lineEdit_2.clear()
    registro.lineEdit_3.clear()
    registro.lineEdit_3.clear()
    registro.label_6.clear()

registro.pushButton_6.clicked.connect(limpiar_campos)
registro.pushButton_2.clicked.connect(registrar)

registro.show()
app.exec()
