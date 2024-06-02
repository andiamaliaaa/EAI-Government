from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from sqlalchemy.orm import relationship
from typing import Literal

# schema model untuk data pajak objek wisata
class Pajak(Base):
    __tablename__ = 'pajak'

    id_pajak = Column(String(5), primary_key=True, index=True)
    id_wisata = Column(String, unique=True)
    nama_objek = Column(String)
    status_kepemilikan = Column(Literal['Pemerintah', 'Swasta', 'Campuran'])
    jenis_pajak = Column(String)
    tarif_pajak = Column(Float)
    besar_pajak = Column(Integer)

# schema model untuk data setoran pajak objek wisata
class SetoranPajak(Base):
    __tablename__ = 'setoran_pajak'

    id_setoran = Column(String(5), primary_key=True, index=True)
    pajak_id_pajak = Column(String(5), ForeignKey=True, index=True)
    pajak = relationship("Pajak", back_populates='setoranpajak')
    tanggal_jatuh_tempo = Column(DateTime)
    tanggal_setoran = Column(DateTime)
    status_setoran = Column(Literal['Tepat Waktu', 'Terlambat'])
    denda = Column(Float)
    besar_pajak_setelah_denda = Column(Integer)