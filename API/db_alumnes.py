# Autor: Alba Segura
# Data: 9/10/24

#Importem la funcio db_client de client
from client import db_client
import db_aules

#Funció per a retornar tots els alumnes amb la classe
def read_alumnes(orderby=None, contain=None, skip=0, limit=None):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT NomAlumne, Cicle, Curs, Grup, DescAula FROM Alumne JOIN Aula ON Alumne.IdAula = Aula.IdAula"
        if contain:
            query += f" WHERE NomAlumne LIKE '%{contain}%' OR Cicle LIKE '%{contain}%' OR Curs LIKE '%{contain}%' OR Grup LIKE '%{contain}%' OR DescAula LIKE '%{contain}%'"
        if orderby:
            query += f" ORDER BY NomAlumne {orderby}"
        if limit:
            query += f" LIMIT {limit} OFFSET {skip}"
        cur.execute(query)
        alumnes = cur.fetchall()
        cur.close()
        conn.close()
        return alumnes
    except Exception as e:
        print(f"Error reading from database: {e}")
        return []

#Funció per a retornar tots els alumnes
def read():
    try:
        print("Hola")
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Alumne")
        alumns = cur.fetchall()
        cur.close()
        conn.close()
        return alumns
    except Exception as e:
        print(f"Error reading from database: {e}")
        return []

#Funció per a retornar un alumne per id
def read_id(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Alumne WHERE IdAlumne = %s", (id,))
        alumne = cur.fetchone()
       # print("Fetched alumne:", alumne)
        cur.close()
        conn.close()
        return alumne
    except Exception as e:
        print(f"Error reading from database: {e}")
        return None

#Funció per a retornar una aula per id
def read_class_id(id):
    try:
        classID = None
        conn = db_client()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Aula WHERE IdAula = %s", (id,))
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
        return classID
    
#Funció per a retornar tots els alumnes amb la classe
def read_AlumnClass():
    try:
        conn = db_client()
        cur = conn.cursor()
        cur.execute("""SELECT 
                        Alumne.IdAlumne,
                        Alumne.NomAlumne,
                        Alumne.Cicle,
                        Alumne.Curs,
                        Alumne.Grup,
                        Alumne.CreatedAt as AlumneCreatedAt,
                        Alumne.UpdatedAt as AlumneUpdateAt,
                        Alumne.IdAula,
                        Aula.DescAula, 
                        Aula.Edifici, 
                        Aula.Pis,
                        Aula.CreatedAt as AulaCreatedAt,
                        Aula.UpdatedAt as AulaUpdatedAt
                    FROM 
                        Alumne 
                    JOIN 
                        Aula ON Alumne.IdAula = Aula.IdAula;""")
        alumns = cur.fetchall()
        cur.close()
        conn.close()
        return alumns
    except Exception as e:
        print(f"Error reading from database: {e}")
        return []

#Funció per a crear un alumne i retornarlo
def create(IdAula,NomAlumne,Cicle,Curs,Grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        highest_id = get_highest_id_alumne() + 1
        #print(f"The highest IdAlumne is: {highest_id}")
        query = "insert into Alumne (IdAlumne, IdAula,NomAlumne,Cicle,Curs,Grup) VALUES (%s,%s,%s,%s,%s,%s);"
        values=(highest_id, IdAula,NomAlumne,Cicle,Curs,Grup)
        cur.execute(query,values)
    
        conn.commit()
        alumne_id = cur.lastrowid
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return alumne_id 

#Funció per a actualitzar un alumne i retornarlo
def update_vots(IdAlumne,IdAula,NomAlumne,Cicle,Curs,Grup):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = """UPDATE Alumne 
        SET IdAula = %s, NomAlumne = %s, Cicle = %s, Curs = %s, Grup = %s 
        WHERE IdAlumne = %s;"""
        values=(IdAula,NomAlumne,Cicle,Curs,Grup,IdAlumne)
        cur.execute(query,values)
        updated_recs = cur.rowcount
    
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()

    return updated_recs

#Funció per a eliminar un alumne i retornarlo
def delete_alumn(id):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "DELETE FROM Alumne WHERE IdAlumne = %s;"
        cur.execute(query,(id,))
        deleted_recs = cur.rowcount
        conn.commit()
    
    except Exception as e:
        return {"status": -1, "message": f"Error de connexió:{e}" }
    
    finally:
        conn.close()
        
    return deleted_recs

#Funció per a retornar el IdAlumne més alt
def get_highest_id_alumne():
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT MAX(IdAlumne) FROM Alumne;"
        cur.execute(query)
        result = cur.fetchone()
        highest_id = result[0] if result[0] is not None else 0
    except Exception as e:
        print(f"Error reading from database: {e}")
        highest_id = None
    finally:
        cur.close()
        conn.close()
    
    return highest_id

#Funció per a retornar un alumne
def get_alumne(nom_alumne: str, cicle: str, curs: str, grup: str):
    try:
        conn = db_client()
        cur = conn.cursor()
        query = "SELECT * FROM Alumne WHERE NomAlumne = %s AND Cicle = %s AND Curs = %s AND Grup = %s"
        print ("goasl")
        cur.execute(query, (nom_alumne, cicle, curs, grup,))
        print ("goal")
        return cur.fetchone()
    except Exception as e:
        print(f"Error reading from database: {e}")
        return None
    finally:
        cur.close()
        conn.close()

#Funció per a insertar un alumne
def insert_alumne(nom_alumne: str, cicle: str, curs: str, grup: str, desc_aula: str):
    try:
        conn = db_client()
        cur = conn.cursor()
        aula_id = db_aules.get_aula_id(desc_aula)
        print(aula_id)
        if aula_id is None:
            raise ValueError(f"Aula with DescAula {desc_aula} not found")
        query = "INSERT INTO Alumne (NomAlumne, Cicle, Curs, Grup, IdAula) VALUES (%s, %s, %s, %s, %s)"
        cur.execute(query, (nom_alumne, cicle, curs, grup, aula_id,))
        conn.commit()
    except Exception as e:
        print(f"Error inserting into database: {e}")
        raise e
    finally:
        cur.close()
        conn.close()