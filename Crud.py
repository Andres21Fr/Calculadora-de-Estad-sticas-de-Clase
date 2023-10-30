import tkinter as tk
from tkinter import ttk
import mysql.connector
from tkinter import messagebox
from tkinter import PhotoImage

try:
    # Conexión a la base de datos
    conexion = mysql.connector.connect(user='root',
                                        password='Andres',
                                        host='127.0.0.1',
                                        database='clientes2',
                                        port='3306')
    print("Conexion exitosa")

except mysql.connector.Error as error:
            print("Error al conectarse a la base de datos{}".format(error))

# Función para crear la "Ventana de Inicio"
def ventanaInicio():
    
    ventana = tk.Tk()
    
    ventana.geometry("400x400")
    ventana.title("Inicio de sesión")


    # Etiquetas y campos de entrada
    nombreLabel = ttk.Label(text="Nombre de usuario:")
    nombreLabel.place(x=50, y=100)

    password = ttk.Label(text="Ingresa la contraseña:")
    password.place(x=50, y=150)

    cajaUser = ttk.Entry()
    cajaUser.place(x=200, y=100)

    cajaPassword = ttk.Entry(show="*")
    cajaPassword.place(x=200, y=150)

    # Función para obtener datos y verificar el inicio de sesión
    def obtenerDatos():
        usuario = cajaUser.get()
        contrasena = cajaPassword.get()



        cursor = conexion.cursor()

        consulta = "SELECT id FROM usuarios_p WHERE nombre = %s AND contrasena = %s"
        valores = (usuario, contrasena)

        cursor.execute(consulta, valores)
        resultado = cursor.fetchone()

        if resultado:
            messagebox.showinfo("Inicio de Sesión", "Inicio de sesión exitoso.")
            # Ocultar la "Ventana de Inicio"
            ventana.withdraw()
            # Mostrar la "Ventana 2"
            ventana2()

        else:
            messagebox.showerror("Error", "Nombre de usuario o contraseña incorrectos.")
            return resultado

        cursor.close()
        conexion.close()


    # Botón para iniciar sesión
    boton_iniciar_sesion = ttk.Button(ventana, text="Iniciar Sesión", command=obtenerDatos)
    boton_iniciar_sesion.place(x=150, y=250)

    ventana.mainloop()


# Función para crear la "Ventana 2"
def ventana2():
    ventana2 = tk.Tk()
    ventana2.geometry("1350x300")
    ventana2.title("Ventana 2")


    def Guardardatos():
    # Obtener los valores de los campos de entrada
        id = texBoxid.get()
        Nombre = texBoxNombre.get()
        Apellido = texBoxApellido.get()
        Numero = texBoxNumero.get()
        Direccion = texBoxDireccion.get()

        if not id or not Nombre or not Apellido or not Numero or not Direccion:
            messagebox.showerror("Error", "Por favor, complete todos los campos.")
            return  # Salir de la función si hay campos vacíos

    # Crear un cursor para interactuar con la base de datos
        cursor = conexion.cursor()

    # Definir la consulta SQL para insertar un nuevo registro
        sql = "INSERT INTO contactos (id, Nombre, Apellido, Numero, Direccion) VALUES (%s, %s, %s, %s, %s)"
        valores = (id, Nombre, Apellido, Numero, Direccion)

    # Ejecutar la consulta SQL
        cursor.execute(sql, valores)

    # Confirmar los cambios en la base de datos
        conexion.commit()

    # Mostrar un mensaje de registro exitoso
        messagebox.showinfo("Registro", "Registro Exitoso")

    # Limpiar los campos de entrada después de un registro exitoso
        texBoxid.delete(0, 'end') 
        texBoxNombre.delete(0, 'end')
        texBoxApellido.delete(0, 'end')
        texBoxNumero.delete(0, 'end') 
        texBoxDireccion.delete(0, 'end')


    def Leerdatos():
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM contactos")
        registros = cursor.fetchall()

        tree.delete(*tree.get_children())
    
        for registro in registros:
            tree.insert("", "end", values=registro)

    def eliminar_contacto_por_id():
    # Obtener el ID del contacto a eliminar
        id = texBoxid.get()
        
        cursor = conexion.cursor()

        

    # Verificar si el ID existe antes de eliminar el contacto
        cursor.execute("SELECT id FROM contactos WHERE id = %s", (id,))
        contacto = cursor.fetchone()
        
        if contacto:
        # Eliminar el contacto por su ID 
            cursor.execute("DELETE FROM contactos WHERE id = %s", (id,))
            conexion.commit()
            messagebox.showinfo("Eliminación", "Contacto eliminado con éxito")
            texBoxid.delete(0, 'end')
        else:
            messagebox.showerror("Error", "ID de contacto no encontrado")
    
    def actualizar_datos():
    # Obtener el ID de la persona cuyos datos se van a actualizar
        id_a_actualizar = texBoxid.get()

    # Obtener los nuevos valores de los campos de entrada
        Nombre = texBoxNombre.get()
        Apellido = texBoxApellido.get()
        Numero = texBoxNumero.get()
        Direccion = texBoxDireccion.get()

    # Crear un cursor para interactuar con la base de datos
        cursor = conexion.cursor()

    # Verificar si el ID existe antes de realizar la actualización
        cursor.execute("SELECT id FROM contactos WHERE id = %s", (id_a_actualizar,))
        persona = cursor.fetchone()

        if persona:
        # Construir la consulta SQL de actualización de manera dinámica
            sql = "UPDATE contactos SET"

        # Crear una lista de valores para la consulta SQL
            valores = []

        # Verificar si se deben actualizar los campos Nombre, Apellido, Numero y Direccion
        # y agregarlos a la consulta SQL según corresponda
            if Nombre:
                sql += " Nombre = %s,"
                valores.append(Nombre)  # Agregar el valor a la lista
            if Apellido:
                sql += " Apellido = %s,"
                valores.append(Apellido)  # Agregar el valor a la lista
            if Numero:
                sql += " Numero = %s,"
                valores.append(Numero)  # Agregar el valor a la lista
            if Direccion:
                sql += " Direccion = %s,"
                valores.append(Direccion)  # Agregar el valor a la lista

        # Eliminar la última coma de la consulta SQL
            sql = sql.rstrip(',')

        # Agregar la cláusula WHERE para la actualización basada en el ID
            sql += " WHERE id = %s"

        # Agregar el ID a la lista de valores
            valores.append(id_a_actualizar)

        # Ejecutar la consulta SQL de actualización
            cursor.execute(sql, valores)
            conexion.commit()
            messagebox.showinfo("Actualización", "Datos actualizados con éxito")
        else:
            messagebox.showerror("Error", "ID de persona no encontrado")


    # Limpiar los campos de entrada después de una actualización exitosa
        texBoxNombre.delete(0, 'end')
        texBoxApellido.delete(0, 'end')
        texBoxNumero.delete(0, 'end')
        texBoxDireccion.delete(0, 'end')
        



    groupBox = tk.LabelFrame(ventana2,text="Datos del personal",padx=5,pady=5)
    groupBox.grid(row=0,column=0,padx=10,pady=10)

    labelid = tk.Label(groupBox,text="ID",width=13,font=("arial",12)).grid(row=0,column=0)
    texBoxid = tk.Entry(groupBox, validate="key")
    texBoxid.grid(column=1,row=0)

    LabelNombres =tk.Label(groupBox,text="Nombre:",width=13,font=("arial",12)).grid(row=1,column=0)
    texBoxNombre = tk.Entry(groupBox)
    texBoxNombre.grid(column=1,row=1)

    LabelApellido = tk.Label(groupBox,text="Apellido:",width=13,font=("arial",12)).grid(row=2,column=0)
    texBoxApellido = tk.Entry(groupBox)
    texBoxApellido.grid(column=1,row=2)

    LabelNumero = tk.Label(groupBox,text="Numero:",width=13,font=("arial",12)).grid(row=3,column=0)
    texBoxNumero = tk.Entry(groupBox)
    texBoxNumero.grid(column=1,row=3)

    LabelDirecccion = tk.Label(groupBox,text="Direccion:",width=13,font=("arial",12)).grid(row=4,column=0)
    texBoxDireccion = tk.Entry(groupBox)
    texBoxDireccion.grid(column=1,row=4)

    botonGuardar = tk.Button(groupBox,text="Guardar",width=10, command=Guardardatos ).grid(row=5,column=0)
    botonLeer = tk.Button(groupBox,text="Leer registros",width=10, command=Leerdatos ).grid(row=5,column=1)
    botonModificar = tk.Button(groupBox,text="Modificar",width=10, command=actualizar_datos).grid(row=6,column=0)
    botonEliminar = tk.Button(groupBox,text="Eliminar",width=10, command=eliminar_contacto_por_id).grid(row=6,column=1)

    groupBox = tk.LabelFrame(ventana2, text="Lista de Contactos",padx=5,pady=5,)
    groupBox.grid(row=0,column=1,padx=5,pady=5)

    tree = ttk.Treeview(groupBox, columns=("ID", "Nombre", "Apellido", "Numero", "Direccion"), show='headings', height=5)
    tree.pack()
    # Definir las columnas y sus anclas
    tree.column("ID", anchor="center")
    tree.column("Nombre", anchor="center")
    tree.column("Apellido", anchor="center")
    tree.column("Numero", anchor="center")
    tree.column("Direccion", anchor="center")

    # Encabezados de columnas
    tree.heading("ID", text="ID")
    tree.heading("Nombre", text="Nombre")
    tree.heading("Apellido", text="Apellido")
    tree.heading("Numero", text="Numero")
    tree.heading("Direccion", text="Direccion")

    


    ventana2.mainloop()

# Llamar a la función para mostrar la "Ventana de Inicio"
ventanaInicio()

