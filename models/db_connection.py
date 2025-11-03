import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            port=3307,
            user='A',            # Tu usuario de MySQL
            password='nara8900', # Tu contraseña
            database='FormularioDB'
        )
        if connection.is_connected():
            print("✅ Conexión a la base de datos exitosa.")
            return connection
    except Error as e:
        print(f"❌ Error al conectar a la base de datos: {e}")
        return None
