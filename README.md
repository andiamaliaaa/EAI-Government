# Alur EAI-Government

1. Setelah clone repository, kalian ikutin langkah di bawah:
- pip install fastapi
- pip install uvicorn
- pip intsall requests
- pip install Literal
- pip install sqlalchemy mysql-connector-python

2. Setelah itu baru kalian bikin schema model masing-masing database
class nama_model(BaseModel):
    atribut: tipe data
    atribut: tipe data
    dll

3. Setelah itu bikin data dummy dari masing-masing model database
nama_variabel =[
    {'atribut': 'isi (kalau string)', 'atribut': isi (kalo int), dll},
    {'atribut': 'isi (kalau string)', 'atribut': isi (kalo int), dll},
    {'atribut': 'isi (kalau string)', 'atribut': isi (kalo int), dll},
    {'atribut': 'isi (kalau string)', 'atribut': isi (kalo int), dll},
    {'atribut': 'isi (kalau st
    ring)', 'atribut': isi (kalo int), dll}
]

4. Setelah itu bikin endpoint untuk post data (sebagai provider) ke kelompok yang menjadi tanggung jawabnya
