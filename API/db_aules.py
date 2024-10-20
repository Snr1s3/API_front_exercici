# Autor: Alba Segura
# Data: 16/10/24

#Importem la funcio db_client de client
from client import db_client

#Funció per a retornar una aula per id
def get_aula_by_desc(desc):
    try:
        classID = None
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Aula WHERE DescAula = %s", (desc,))
        result = cur.fetchone()
        print("Fetched aula:", result)
        #print("Fetched alumne:", classID)
        cur.close()
        conn.close()
        return result
    except Exception as e:
        print(f"Error reading from database: {e}")
        return classID
    
def get_aula_id(desc):
    try:
        classID = None
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Aula WHERE DescAula = %s", (desc,))
        result = cur.fetchone()
        print("Fetched aula:", result)
        if result:
            classID = result[0]
        #print("Fetched alumne:", classID)
        cur.close()
        conn.close()
        return classID
    except Exception as e:
        print(f"Error reading from database: {e}")

#Funció per a crear una aula i retornarla
def insert_aula(desc_aula: str, edifici: str, pis: str):
    try:
        conn = db_client()
        cur = conn.cursor()
        #print(f"The highest IdAlumne is: {highest_id}")
        query = "insert into Aula (DescAula, Edifici, Pis) VALUES (%s,%s,%s);"
        values=(desc_aula, edifici, pis)
        cur.execute(query,values)
    
        conn.commit()
        alumne_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return alumne_id 