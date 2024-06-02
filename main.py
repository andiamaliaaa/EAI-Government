from typing import List
from decimal import Decimal
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from database import engine, SessionLocal
from sqlalchemy.orm import Session
from typing import Literal
from typing import Annotated
import requests
import models


app = FastAPI(
    title="Government",
    description="API untuk mengelola data pemerintahan",
    docs_url="/",  # Ubah docs_url menjadi "/"
)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# mengatur 
db_dependency = Annotated[Session, Depends(get_db)]

# schema model untuk data pajak objek wisata
class PajakBase(BaseModel):
    id_pajak: str
    id_wisata: str
    nama_objek:  str
    status_kepemilikan: Literal['Pemerintah', 'Swasta', 'Campuran']
    jenis_pajak: str
    tarif_pajak: float
    besar_pajak: int

# Data dummy untuk tabel pajak_objek_wisata
data_pajakwisata =[
    {'id_pajak': 'PJ001', 'status_kepemilikan': 'Swasta', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0.11), 'besar_pajak': 50000000},
    {'id_pajak': 'PJ002', 'status_kepemilikan': 'Swasta', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0.11), 'besar_pajak': 100000000},
    {'id_pajak': 'PJ003', 'status_kepemilikan': 'Pemerintah', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0), 'besar_pajak': 0},
    {'id_pajak': 'PJ004', 'status_kepemilikan': 'Pemerintah', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0.11), 'besar_pajak': 75000000},
    {'id_pajak': 'PJ005', 'status_kepemilikan': 'Campuran', 'jenis_pajak': 'Pajak Pertahanan Nilai (PPN)', 'tarif_pajak': Decimal(0.11), 'besar_pajak': 65000000}
]

# Endpoint untuk mengakses path root "/"
@app.get("/")
async def read_root():
    return {'example': 'Contoh untuk Mengakses API Government', "Data":"Successful"}

# Endpoint untuk menabahkan data pajak objek wisata
@app.post('/pajak', status_code=status.HTTP_201_CREATED)
async def add_pajakwisata(pajak: PajakBase):
    data_pajakwisata.append(pajak.dict())
    return {"message": "Data Pajak Objek Wisata Berhasil Ditambahkan."}

# @app.post('/pajak', status_code=status.HTTP_201_CREATED)
# async def add_pajak(pajak: PajakBase, db: db_dependency):
#     db_pajak = models.Pajak(**pajak.dict())
#     db.add(db_pajak) 
#     db.commit() 
#     return {"message": "Data Pajak Objek Wisata Berhasil Ditambahkan."}

#Endpoint untuk mendapatkan data pajak objek wisata
# @app.get("/pajak", response_model=List[PajakBase])
# async def get_pajakwisata():
#     return data_pajakwisata

@app.get("/pajak", status_code=status.HTTP_201_OK)
async def read_pajak(db = db_dependency):
    pajak = db.query(models.Pajak).filter(models.Pajak).first()
    if pajak is None:
        raise HTTPException(status_code=404, detail='ID Pajak Tidak Ditemukan')
    return pajak

# Fungsi untuk menghapus data pada tabel pajak objek wisata
@app.delete('/pajak{is_pajak}', status_code=status.HTTP_200_OK)
async def delete_pajak(id_pajak: str, db: db_dependency):
    db_pajak = db.query(models.Pajak).filter(models.Pajak.id_pajak == id_pajak).first()
    if db_pajak is None:
        raise HTTPException(status_code=404, detail='Data Pajak Objek Wisata Tidak Ditemukan.')
    db.delete(db_pajak)
    db.commit()
    return {"message": "Data Pajak Objek Wisata Berhasil Dihapus."}

# Fungsi untuk mengambil data objek wisata dari website objek wisata
async def get_objek_wisata_from_web(db = db_dependency):
    url = "https://pajakobjekwisata.onrender.com/wisata" # URL Endpoint API dari Objek Wisata
    response = requests.get(url)
    if response.status.code == 200:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail = "Gagal mengambil data Objek Wisata")
    
# Schema Model untuk data Objek Wisata
class ObjekWisata(BaseModel):
    id_wisata: str
    nama_wisata: str

# Endpoint untuk mendapatkan/memasukkan data objek wisata
@app.get('/wisata', response_model=List[ObjekWisata])
async def get_objekwisata():
    data_objekwisata = get_objek_wisata_from_web()
    return data_objekwisata
