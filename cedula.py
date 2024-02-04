import mysql.connector
from PyQt6 import QtWidgets, uic
from conexionBD import ConexionBD
app = QtWidgets.QApplication([])



conexion_bd = ConexionBD()

cedula = uic.loadUi("cedula.ui")
datos = uic.loadUi("datos.ui")

def buscar_c():
    ced = cedula.lineEdit.text()

    consulta = "SELECT * FROM usuarios WHERE cedula = %s"
    
    parametros = (ced,)

    cursor = conexion_bd.obtener_cursor()

    try:
        # Ejecutar la consulta con los parámetros
        cursor.execute(consulta, parametros)

        # Obtener los resultados de la consulta
        resultados = cursor.fetchall()

        # Mostrar el resultado en el QLabel
        if resultados:
            cedula.label_4.setText(f"Cedula encontrada: {ced}")
        else:
            cedula.label_4.setText("Cedula no encontrada")

    except mysql.connector.Error as error:
        print(f"Error al ejecutar la consulta: {error}")

    finally:
        # Cerrar el cursor
        cursor.close()

def datosbuton():
    cedula.hide()
    datos.show()
# Conectar la función buscar_c al botón
cedula.pushButton.clicked.connect(buscar_c)
cedula.pushButton_2.clicked.connect(datosbuton)

cedula.show()
app.exec()
