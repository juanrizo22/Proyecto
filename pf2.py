import mysql.connector
import csv


# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'informatica1',
    'password': 'bio123',
    'database': 'informatica1'
}

# Conexión a la base de datos
db = mysql.connector.connect(**db_config)
cursor = db.cursor()

# Funciones de validación
def validar_entero(mensaje):
    """
    Solicita al usuario ingresar un valor entero a través de la consola.

    Parámetros:
    - mensaje: str. El mensaje que se muestra al usuario para solicitar el valor.

    Retorna:
    - int. El valor entero ingresado por el usuario.

    """
    while True:
        try:
            valor = int(input(mensaje))
            return valor
        except ValueError:
            print('Error: Debes ingresar un valor entero.')
def validar_numero(mensaje):
    """
    Solicita al usuario ingresar un valor numérico (número decimal) a través de la consola.

    Parámetros:
    - mensaje: str. El mensaje que se muestra al usuario para solicitar el valor.

    Retorna:
    - float. El valor numérico ingresado por el usuario.

    """
    while True:
        try:
            valor = float(input(mensaje))
            return valor
        except ValueError:
            print('Error: Debes ingresar un valor numérico.')

# Funciones CRUD para equipos
def ingresar_equipo():
    """
    Permite al usuario ingresar los datos de un equipo y los inserta en una base de datos.

    Esta función solicita al usuario que ingrese el serial, número de activo, nombre, marca,
    código de ubicación y código de responsable del equipo. Los datos ingresados se validan
    según los tipos esperados y se insertan en una tabla de la base de datos.

    """
    print('== Ingresar Equipo ==')
    serial = input('Serial: ')
    numero_activo = validar_entero('Número de activo: ')
    nombre = input('Nombre del equipo: ')
    marca = input('Marca: ')
    codigo_ubicacion = validar_entero('Código de ubicación: ')
    codigo_responsable = validar_entero('Código de responsable: ')

    # Insertar datos en la base de datos
    query = "INSERT INTO equipos (serial, numero_activo, nombre, marca, codigo_ubicacion, codigo_responsable) VALUES (%s, %s, %s, %s, %s, %s)"
    values = (serial, numero_activo, nombre, marca, codigo_ubicacion, codigo_responsable)
    cursor.execute(query, values)
    db.commit()
    print('Equipo ingresado exitosamente.')

def ingresar_equipo_automatico():
    """
    Permite ingresar automáticamente los datos de equipos desde un archivo CSV a una base de datos.

    Esta función solicita al usuario la ruta del archivo CSV que contiene los datos de los equipos.
    Luego, lee el archivo CSV y obtiene los datos de los equipos. Cada fila del archivo se interpreta
    como un equipo con los siguientes campos: serial, número de activo, nombre, marca, código de ubicación
    y código de responsable. Los datos se validan y se insertan en la base de datos.

    """
    print('== Ingresar Equipo Automático ==')
    archivo = input('Ruta del archivo CSV: ')

    # Leer archivo CSV y obtener los datos de los equipos
    equipos = []
    try:
        with open(archivo, 'r') as file:
            reader = csv.reader(file)
            next(reader)  # Saltar la primera línea (encabezados)
            for row in reader:
                serial = row[0]
                numero_activo = int(row[1])
                nombre = row[2]
                marca = row[3]
                codigo_ubicacion = int(row[4])
                codigo_responsable = int(row[5])
                equipos.append((serial, numero_activo, nombre, marca, codigo_ubicacion, codigo_responsable))
        # Insertar los datos en la base de datos
        query = "INSERT INTO equipos (serial, numero_activo, nombre, marca, codigo_ubicacion, codigo_responsable) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.executemany(query, equipos)
        db.commit()
        print('Equipos ingresados exitosamente.')
    except FileNotFoundError:
        print('Error: Archivo no encontrado.')
    except csv.Error:
        print('Error: Error al leer el archivo CSV.')
    except ValueError:
        print('Error: El archivo CSV debe contener valores enteros válidos en las columnas correspondientes.')
    print('Equipos ingresados exitosamente.')

def actualizar_equipo():
    """
    Permite actualizar la información de un equipo existente en la base de datos.

    Esta función solicita al usuario el número de activo del equipo que desea actualizar.
    Luego, consulta la base de datos para obtener la información actual del equipo.
    Si el equipo existe, se muestra su información y se solicitan los nuevos datos.
    Después de validar los nuevos datos, se actualiza la entrada correspondiente en la base de datos.

    """
    print('== Actualizar Equipo ==')
    numero_activo = validar_entero('Número de activo del equipo a actualizar: ')

    # Consultar el equipo en la base de datos
    query = "SELECT * FROM equipos WHERE numero_activo = %s"
    cursor.execute(query, (numero_activo,))
    equipo = cursor.fetchone()

    if equipo:
        print('Información del equipo:')
        print(f'Serial: {equipo[0]}')
        print(f'Número de activo: {equipo[1]}')
        print(f'Nombre del equipo: {equipo[2]}')
        print(f'Marca: {equipo[3]}')
        print(f'Código de ubicación: {equipo[4]}')
        print(f'Código de responsable: {equipo[5]}')

        # Solicitar los nuevos datos del equipo
        serial = input('Nuevo serial (dejar en blanco para mantener el valor actual): ')
        numero_activo = validar_entero('Nuevo número de activo: ')
        nombre = input('Nuevo nombre del equipo: ')
        marca = input('Nueva marca: ')
        codigo_ubicacion = validar_entero('Nuevo código de ubicación: ')
        codigo_responsable = validar_entero('Nuevo código de responsable: ')

        # Actualizar los datos en la base de datos
        query = "UPDATE equipos SET serial = %s, numero_activo = %s, nombre = %s, marca = %s, codigo_ubicacion = %s, codigo_responsable = %s WHERE numero_activo = %s"
        values = (serial or equipo[0], numero_activo, nombre, marca, codigo_ubicacion, codigo_responsable, numero_activo)
        cursor.execute(query, values)
        db.commit()
        print('Equipo actualizado exitosamente.')
    else:
        print('No se encontró ningún equipo con ese número de activo.')

def buscar_equipo():
    """
    Busca un equipo en la base de datos utilizando su número de activo.

    Esta función solicita al usuario el número de activo del equipo que desea buscar.
    Luego, consulta la base de datos para obtener la información del equipo correspondiente.
    Si se encuentra un equipo con el número de activo proporcionado, se muestra su información.

    """
    print('== Buscar Equipo ==')
    numero_activo = validar_entero('Número de activo del equipo a buscar: ')

    # Consultar el equipo en la base de datos
    query = "SELECT * FROM equipos WHERE numero_activo = %s"
    cursor.execute(query, (numero_activo,))
    equipo = cursor.fetchone()

    if equipo:
        print('Información del equipo:')
        print(f'Serial: {equipo[0]}')
        print(f'Número de activo: {equipo[1]}')
        print(f'Nombre del equipo: {equipo[2]}')
        print(f'Marca: {equipo[3]}')
        print(f'Código de ubicación: {equipo[4]}')
        print(f'Código de responsable: {equipo[5]}')
    else:
        print('No se encontró ningún equipo con ese número de activo.')

def ver_equipos():
    """
    Muestra la información de todos los equipos registrados en la base de datos.

    Esta función consulta la base de datos para obtener la información de todos los equipos registrados.
    Luego, muestra la información de cada equipo en el siguiente formato: Serial, Número de activo, Nombre.

    """
    print('== Equipos Registrados ==')
    # Consultar todos los equipos en la base de datos
    query = "SELECT * FROM equipos"
    cursor.execute(query)
    equipos = cursor.fetchall()

    if equipos:
        print('Información de los equipos:')
        for equipo in equipos:
            print(f'Serial: {equipo[0]}, Número de activo: {equipo[1]}, Nombre: {equipo[2]}')
    else:
        print('No hay equipos registrados.')

def eliminar_equipo():
    """
    Elimina un equipo de la base de datos según su número de activo.

    Esta función solicita al usuario el número de activo del equipo que desea eliminar.
    Luego, consulta la base de datos para verificar si existe un equipo con ese número de activo.
    Si se encuentra un equipo, se solicita una confirmación al usuario antes de proceder con la eliminación.
    Si se confirma la eliminación, se elimina el equipo de la base de datos.

    """
    print('== Eliminar Equipo ==')
    numero_activo = validar_entero('Número de activo del equipo a eliminar: ')

    # Consultar el equipo en la base de datos
    query = "SELECT * FROM equipos WHERE numero_activo = %s"
    cursor.execute(query, (numero_activo,))
    equipo = cursor.fetchone()

    if equipo:
        confirmacion = input(f'Seguro que desea eliminar el equipo con número de activo {numero_activo}? (S/N): ')
        if confirmacion.upper() == 'S':
            # Eliminar el equipo de la base de datos
            query = "DELETE FROM equipos WHERE numero_activo = %s"
            cursor.execute(query, (numero_activo,))
            db.commit()
            print('Equipo eliminado exitosamente.')
    else:
        print('No se encontró ningún equipo con ese número de activo.')

# Funciones para la gestión de responsables
def ingresar_responsable():
    """
    Ingresa un responsable en la base de datos.

    Esta función solicita al usuario los datos del responsable, como el código responsable, nombre, apellido,
    número de documento de identidad y cargo. Luego, inserta los datos del responsable en la base de datos.

    """
    print('== Ingresar Responsable ==')
    codigo_responsable = validar_entero('Código responsable: ')
    nombre = input('Nombre: ')
    apellido = input('Apellido: ')
    numero_documento = validar_entero('Número de documento de identidad: ')
    cargo = input('Cargo: ')

    # Insertar el responsable en la base de datos
    query = "INSERT INTO responsables (codigo_responsable, nombre, apellido, numero_documento, cargo) VALUES (%s, %s, %s, %s, %s)"
    values = (codigo_responsable, nombre, apellido, numero_documento, cargo)
    cursor.execute(query, values)
    db.commit()
    print('Responsable ingresado exitosamente.')

def ver_responsables():
    """
    Muestra la lista de responsables registrados en la base de datos.

    Esta función consulta todos los responsables almacenados en la base de datos y los muestra por pantalla.
    Si hay responsables registrados, muestra información como el código responsable, nombre y apellido.
    En caso contrario, muestra un mensaje indicando que no hay responsables registrados.

    """
    print('== Responsables Registrados ==')
    # Consultar todos los responsables en la base de datos
    query = "SELECT * FROM responsables"
    cursor.execute(query)
    responsables = cursor.fetchall()

    if responsables:
        print('Información de los responsables:')
        for responsable in responsables:
            print(f'Código responsable: {responsable[0]}, Nombre: {responsable[1]}, Apellido: {responsable[2]}')
    else:
        print('No hay responsables registrados.')

def actualizar_responsable():
    """
    Permite actualizar la información de un responsable existente en la base de datos.

    Esta función solicita al usuario el código responsable del responsable que se desea actualizar.
    Luego, consulta la base de datos para obtener la información actual del responsable.
    Si se encuentra un responsable con el código responsable especificado, se muestra su información
    por pantalla y se solicitan los nuevos datos del responsable.
    Después de recopilar los nuevos datos, actualiza la información del responsable en la base de datos.

    """
    print('== Actualizar Responsable ==')
    codigo_responsable = validar_entero('Código responsable del responsable a actualizar: ')

    # Consultar el responsable en la base de datos
    query = "SELECT * FROM responsables WHERE codigo_responsable = %s"
    cursor.execute(query, (codigo_responsable,))
    responsable = cursor.fetchone()

    if responsable:
        print('Información del responsable:')
        print(f'Código responsable: {responsable[0]}')
        print(f'Nombre: {responsable[1]}')
        print(f'Apellido: {responsable[2]}')
        print(f'Número de documento: {responsable[3]}')
        print(f'Cargo: {responsable[4]}')

        # Solicitar los nuevos datos del responsable
        codigo_responsable = validar_entero('Nuevo código responsable: ')
        nombre = input('Nuevo nombre: ')
        apellido = input('Nuevo apellido: ')
        numero_documento = validar_entero('Nuevo número de documento de identidad: ')
        cargo = input('Nuevo cargo: ')

        # Actualizar los datos en la base de datos
        query = "UPDATE responsables SET codigo_responsable = %s, nombre = %s, apellido = %s, numero_documento = %s, cargo = %s WHERE codigo_responsable = %s"
        values = (codigo_responsable, nombre, apellido, numero_documento, cargo, codigo_responsable)
        cursor.execute(query, values)
        db.commit()
        print('Responsable actualizado exitosamente.')
    else:
        print('No se encontró ningún responsable con ese código responsable.')

def eliminar_responsable():
    """
    Permite eliminar un responsable de la base de datos.

    Esta función solicita al usuario el código responsable del responsable que se desea eliminar.
    Luego, consulta la base de datos para verificar la existencia del responsable.
    Si se encuentra un responsable con el código responsable especificado, se solicita una confirmación
    para proceder con la eliminación. Si la confirmación es positiva, se elimina el responsable de la base de datos.

    """
    print('== Eliminar Responsable ==')
    codigo_responsable = validar_entero('Código responsable del responsable a eliminar: ')

    # Consultar el responsable en la base de datos
    query = "SELECT * FROM responsables WHERE codigo_responsable = %s"
    cursor.execute(query, (codigo_responsable,))
    responsable = cursor.fetchone()

    if responsable:
        confirmacion = input(f'Seguro que desea eliminar el responsable con código responsable {codigo_responsable}? (S/N): ')
        if confirmacion.upper() == 'S':
            # Eliminar el responsable de la base de datos
            query = "DELETE FROM responsables WHERE codigo_responsable = %s"
            cursor.execute(query, (codigo_responsable,))
            db.commit()
            print('Responsable eliminado exitosamente.')
    else:
        print('No se encontró ningún responsable con ese código responsable.')

# Menú principal
def menu():
    """
    Muestra un menú de opciones para el sistema de gestión de equipos.

    Esta función presenta al usuario un menú con diferentes opciones relacionadas con el sistema de gestión de equipos.
    El usuario puede seleccionar una opción ingresando el número correspondiente.
    Según la opción seleccionada, se llamará a la función correspondiente para llevar a cabo la operación deseada.
    Las opciones disponibles incluyen: ingreso de equipo, búsqueda de equipo, visualización de equipos, eliminación de equipo,
    ingreso de responsable, visualización de responsables, actualización de responsable y eliminación de responsable.

    """
    while True:
        print('=== Sistema de Gestión de Equipos ===')
        print('1. Ingresar Equipo')
        print('2. Buscar Equipo')
        print('3. Ver Equipos')
        print('4. Eliminar Equipo')
        print('5. Ingresar Responsable')
        print('6. Ver Responsables')
        print('7. Actualizar Responsable')
        print('8. Eliminar Responsable')
        print('0. Salir')

        opcion = validar_entero('Ingrese una opción: ')

        if opcion == 1:
            ingresar_equipo()
        elif opcion == 2:
            buscar_equipo()
        elif opcion == 3:
            ver_equipos()
        elif opcion == 4:
            eliminar_equipo()
        elif opcion == 5:
            ingresar_responsable()
        elif opcion == 6:
            ver_responsables()
        elif opcion == 7:
            actualizar_responsable()
        elif opcion == 8:
            eliminar_responsable()
        elif opcion == 0:
            print('Hasta luego.')
            break
        else:
            print('Opción inválida. Intente nuevamente.')


# Ejecutar el programa
menu()
