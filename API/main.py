# Autor: Alba Segura
# Data: 9/10/24

#Importem les llibreries FastAPI, HTTPException, BaseModel, List, alumnes i db_alumnes
from fastapi import FastAPI, HTTPException, UploadFile, File, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List , Optional
import alumnes
import csv
import io
import db_alumnes
import db_aules

#Inicialitzem la nostra aplicació FastAPI
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




###########
# CLASSES #
###########
class Alumn(BaseModel):    
    IdAlumne: int
    IdAula: int                      
    NomAlumne: str
    Cicle: str     
    Curs: str       
    Grup: str      
    CreatedAt: str
    UpdatedAt: str

class AlumnC(BaseModel):
    IdAula: int
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str

class Alumn2(BaseModel):
    NomAlumne: str
    Cicle: str
    Curs: str
    Grup: str
    DescAula: str

class AlumnClass(BaseModel):
    IdAlumne: int
    NomAlumne: str
    Cicle: str     
    Curs: str       
    Grup: str 
    AlumneCreatedAt: str
    AlumneUpdatedAt: str
    IdAula: int
    DescAula: str
    Edifici: str
    Pis: int
    AulaCreatedAt: str
    AulaUpdatedAt: str

#############
# Endpoints #
#############

#Endpoint per a la pàgina principal
@app.get("/")
def read_root():
    return {"message": "Alumnes API Alba Segura"}

#Endpoint per a la documentació
@app.get("/docs")

#Endpoint per a la llista d'alumnes
#@app.get("/alumne", response_model=List[Alumn])
#def read_alumnes():
#    return alumnes.alumnes_schema(db_alumnes.read())

#Endpoint per a mostrar un alumne per id
#@app.get("/alumne/show/{id}", response_model=Alumn)
#def read_alumnes_id(id: int):
#    alumne = db_alumnes.read_id(id)
#    if alumne is not None:
#        return alumnes.alumne_schema(alumne)
#    else:
#        raise HTTPException(status_code=404, detail="Item not found")

#Endpoint per a la llista d'alumnes amb la seva aula
@app.get("/alumne/listAll", response_model=List[AlumnClass])
def read_all():
    return alumnes.alumnesAll_schema(db_alumnes.read_AlumnClass())

# Endpoint per a la llista d'alumnes amb paràmetres de consulta
@app.get("/alumne/list", response_model=List[Alumn2])
def read_alumnes(
    orderby: Optional[str] = Query(None, regex="^(asc|desc)$"),
    contain: Optional[str] = None,
    skip: int = 0,
    limit: Optional[int] = Query(None, ge=1, le=100)
):
    result = db_alumnes.read_alumnes(orderby, contain, skip, limit)
    return alumnes.alumnes_schema(result)

#Endpoint per afegir un alumne
@app.post("/alumne/add")
async def create(alumne: AlumnC): 
    classID = db_alumnes.read_class_id(alumne.IdAula)
    print (classID)
    if classID is None:
        raise HTTPException(status_code=404, detail="Class ID not found")
    else:   
        db_alumnes.create(alumne.IdAula, alumne.NomAlumne, alumne.Cicle, alumne.Curs, alumne.Grup)
        return {
            "S’ha afegit correctemen"
        }

@app.post("/alumne/loadAlumnes")
async def load_alumnes(file: UploadFile = File(...)):
    try:
        content = await file.read()
        csv_reader = csv.reader(io.StringIO(content.decode("utf-8")))
        next(csv_reader)

        for row in csv_reader:
            desc_aula, edifici, pis, nom_alumne, cicle, curs, grup = row

            aula = db_aules.get_aula_by_desc(desc_aula)
            if not aula:
                db_aules.insert_aula(desc_aula, edifici, pis)
                print("Aula created")
            else:
                print("Aula already exists")
                
            alumne = db_alumnes.get_alumne(nom_alumne, cicle, curs, grup)
            if not alumne:
                db_alumnes.insert_alumne(nom_alumne, cicle, curs, grup, desc_aula)
                print("Alumne created")
            else:
                print("Alumne already exists")

        return {"message": "Alumnes loaded successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
#Endpoint per a modificar un alumne
@app.put("/alumne/update/{id}")
def update_alumn(id: int, alumne: AlumnC):
    classID = db_alumnes.read_class_id(alumne.IdAula)
    alumnID = db_alumnes.read_id(id)
    if(alumnID is not None):
        if(classID is not None):
            updated_records = db_alumnes.update_vots(id, alumne.IdAula, alumne.NomAlumne, alumne.Cicle, alumne.Curs, alumne.Grup)
            if updated_records == 0:
                raise HTTPException(status_code=404, detail="Items to update not found")
            else: 
                return {
                    "S’ha modificat correctemen"
                }
        else:
            raise HTTPException(status_code=404, detail="Items to update not found")
    else:
        raise HTTPException(status_code=404, detail="Items to update not found")

#Endpoint per a eliminar un alumne
@app.delete("/alumne/delete/{id}")
def delete_alumne(id: int):
    deleted_records = db_alumnes.delete_alumn(id)
    if deleted_records == 0:
        raise HTTPException(status_code=404, detail="Items to delete not found")
    else:
        return {
            "message": "S’ha eliminat correctament"
        }     