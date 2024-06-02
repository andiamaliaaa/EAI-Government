from typing import List
from decimal import Decimal
import pandas as pd
from typing import Literal
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

app = FastAPI(
    title="Government",
    description="API untuk mengelola data pemerintahan",
    docs_url="/",  # Ubah docs_url menjadi "/"
)

# chema model untuk data pajak objek wisata
class Pajak(BaseModel):
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
    return {'example': 'this is an example', "Data":"Successful"}

# Endpoint untuk menabahkan data pajak objek wisata
@app.post('/pajak')
async def add_pajakwisata(pajak: Pajak):
    data_pajakwisata.append(pajak.model_dump())
    return {"message": "Data Pajak Objek Wisata Berhasil Ditambahkan."}

#Endpoint untuk mendapatkan data pajak objek wisata
@app.get("/pajak", response_model=List[Pajak])
async def get_pajakwisata():
    return data_pajakwisata

#Fungsi untuk mengambil data objek wisata dari website objek wisata
async def get_objek_wisata_from_web():
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

# Endpoint untuk mendapatkan data objek wisata
@app.get('/wisata', response_model=List[ObjekWisata])
async def get_objekwisata():
    data_objekwisata = get_objek_wisata_from_web()
    return data_objekwisata