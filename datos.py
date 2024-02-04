# registro.py
# Importar los módulos necesarios
import mysql.connector
from PyQt6 import QtWidgets, uic
import smtplib
import os
from dotenv import load_dotenv
from email.mime.multipart import MIMEMultipart
from email import encoders 
from email.mime.base import MIMEBase
import fitz  # PyMuPDF

# Importar la clase de conexión a la base de datos
from conexionBD import ConexionBD

# Crear una aplicación de PyQt6
app = QtWidgets.QApplication([])

# Crear una instancia única de ConexionBD
conexion_bd = ConexionBD()

# Cargar la interfaz de usuario desde el archivo .ui
datos = uic.loadUi("datos.ui")

# Función para realizar una consulta en la base de datos
def consulta():
    cedula = datos.lineEdit.text()

    # Consultar por cédula
    consulta_nombre = "SELECT nombre FROM usuarios WHERE cedula = %s"
    parametros_nombre = (cedula,)

    # Consultar por apellido
    consulta_apellido = "SELECT apellido FROM usuarios WHERE cedula = %s"
    parametros_apellido = (cedula,)

    # Consultar por correo
    consulta_correo = "SELECT correo FROM usuarios WHERE cedula = %s"
    parametros_correo = (cedula,)

    cursor = conexion_bd.obtener_cursor()

    try:
        # Ejecutar la consulta por cédula
        cursor.execute(consulta_nombre, parametros_nombre)
        resultados_nombre = cursor.fetchall()

        # Ejecutar la consulta por apellido
        cursor.execute(consulta_apellido, parametros_apellido)
        resultados_apellido = cursor.fetchall()

        # Ejecutar la consulta por correo
        cursor.execute(consulta_correo, parametros_correo)
        resultados_correo = cursor.fetchall()

        # Mostrar los resultados en los lineEdit correspondientes
        datos.lineEdit_2.setText(resultados_nombre[0][0] if resultados_nombre else "")
        datos.lineEdit_3.setText(resultados_apellido[0][0] if resultados_apellido else "")
        datos.lineEdit_4.setText(resultados_correo[0][0] if resultados_correo else "")

        # Mostrar el mensaje en el QLabel si no se encuentran resultados
        mensaje = "No encontrado" if not any(resultados_nombre + resultados_apellido + resultados_correo) else ""
        datos.label_5.setText(mensaje)

    except mysql.connector.Error as error:
        print(f"Error al ejecutar la consulta: {error}")

    finally:
        # No cerrar el cursor aquí, ya que podrías necesitarlo más adelante
        pass

# Función para actualizar los datos en la base de datos
def actualizar_datos():
    cedula = datos.lineEdit.text()
    nuevo_nombre = datos.lineEdit_2.text()
    nuevo_apellido = datos.lineEdit_3.text()
    nuevo_correo = datos.lineEdit_4.text()

    # Verificar si al menos un campo tiene datos
    if not nuevo_nombre and not nuevo_apellido and not nuevo_correo:
        datos.label_5.setText("Debe llenar por lo menos un campo con datos válidos")
        return

    consulta_actualizacion = "UPDATE usuarios SET nombre = %s, apellido = %s, correo = %s WHERE cedula = %s"
    parametros_actualizacion = (nuevo_nombre, nuevo_apellido, nuevo_correo, cedula)

    cursor = conexion_bd.obtener_cursor()

    try:
        cursor.execute(consulta_actualizacion, parametros_actualizacion)
        conexion_bd.conexion.commit()  # Confirmar la actualización en la base de datos
        datos.label_5.setText("Datos Actualizados Correctamente")

    except mysql.connector.Error as error:
        datos.label_5.setText(f"Error al actualizar los datos: {error}")
    finally:
        cursor.close()

# Función para enviar un correo electrónico con un archivo adjunto
def enviar_correo():
    load_dotenv()
    remitente = os.getenv('USER')
    destinatario = datos.lineEdit_4.text()

    # Verificar si el campo de correo está vacío
    if not destinatario:
        datos.label_5.setText("Correo No valido")
        return

    asunto = 'Test'
    
    msg = MIMEMultipart()
    msg['Subject'] = asunto
    msg['From'] = remitente
    msg['To'] = destinatario
    
    # Adjuntar el archivo PDF
    archivo_pdf = 'Hoja de vida alvaro (3).pdf'
    adjunto = open(archivo_pdf, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((adjunto).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(archivo_pdf))
    
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(remitente, os.getenv('PASS'))
    
    server.sendmail(remitente, destinatario, msg.as_string())
    server.quit()

# Función para limpiar los campos en la interfaz de usuario
def limpiar_campos():
    datos.lineEdit.clear()
    datos.lineEdit_2.clear()
    datos.lineEdit_3.clear()
    datos.lineEdit_4.clear()
    datos.label_5.clear()

# Conectar las funciones a los eventos de los botones
datos.pushButton_1.clicked.connect(consulta)
datos.pushButton_5.clicked.connect(actualizar_datos)
datos.pushButton_6.clicked.connect(limpiar_campos)
datos.pushButton_7.clicked.connect(enviar_correo)

# Mostrar la interfaz de usuario y ejecutar la aplicación
datos.show()
app.exec()

