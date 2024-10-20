# Autor: Alba Segura
# Data: 9/10/24

# Importem la llibreria datetime
from datetime import datetime

#def alumne_schema(alumne):
#    return {
#        "IdAlumne": alumne[0],
#        "IdAula": alumne[1],
#        "NomAlumne": alumne[2], 
#        "Cicle": alumne[3],
#        "Curs": alumne[4],
#        "Grup": alumne[5],
#        "CreatedAt": alumne[6].strftime("%Y-%m-%d %H:%M:%S") if isinstance(alumne[6], datetime) else alumne[6],
#        "UpdatedAt": alumne[7].strftime("%Y-%m-%d %H:%M:%S") if isinstance(alumne[7], datetime) else alumne[7]
#    }

def alumnes_schema(alumnes):
    return [alumne_schema(alumne) for alumne in alumnes]

# Funció per a retornar un alumne
def alumne_schema(fetchAlumnes):
    return {
        "NomAlumne": fetchAlumnes[0],
        "Cicle": fetchAlumnes[1],
        "Curs": fetchAlumnes[2],
        "Grup": fetchAlumnes[3],
        "DescAula": fetchAlumnes[4]
    }

# Funció per a retornar un alumne amb la classe
def alumneAll_schema(alumne):
    return {
        "IdAlumne": alumne[0],
        "NomAlumne": alumne[1], 
        "Cicle": alumne[2],
        "Curs": alumne[3],
        "Grup": alumne[4],
        "AlumneCreatedAt": alumne[5].strftime("%Y-%m-%d %H:%M:%S") if isinstance(alumne[5], datetime) else alumne[5],
        "AlumneUpdatedAt": alumne[6].strftime("%Y-%m-%d %H:%M:%S") if isinstance(alumne[6], datetime) else alumne[6],
        "IdAula": alumne[7],
        "DescAula": alumne[8], 
        "Edifici": alumne[9],
        "Pis": alumne[10], 
        "AulaCreatedAt": alumne[11].strftime("%Y-%m-%d %H:%M:%S") if isinstance(alumne[11], datetime) else alumne[11] if alumne[11] is not None else None,
        "AulaUpdatedAt": alumne[12].strftime("%Y-%m-%d %H:%M:%S") if isinstance(alumne[12], datetime) else alumne[12] if alumne[12] is not None else None
    }

# Funció per a retornar tots els alumnes amb la classe
def alumnesAll_schema(alumnes):
    return [alumneAll_schema(alumne) for alumne in alumnes]