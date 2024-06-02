from typing import List
from pydantic import BaseModel
import requests
from fastapi import HTTPException

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