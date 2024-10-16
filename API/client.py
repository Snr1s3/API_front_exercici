# Autor: Alba Segura
# Data: 9/10/24

#Importem la llibreria mysql.connector
import mysql.connector

#Funció per a connectar amb la base de dades
def db_client():
    try:
        dbname = "Practica"
        user = "root"
        password = "root"
        host = "localhost"
        port = "8888"
        collation = "utf8mb4_general_ci"
        
        connection = mysql.connector.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            database=dbname,
            collation=collation
        )
        
        #print("Connexió a la base de dades correcta")
        return connection
    except Exception as e:
        print(f"Error de connexió: {e}")
        return {"status": -1, "message": f"Error de connexió: {e}"}