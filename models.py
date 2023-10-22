from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Dokter(Base):
    __tablename__ = "dokter"

    id = Column(Integer, primary_key=True, index=True)
    nama = Column(String) 
    jenis_kelamin = Column(String)
    nomor_telepon = Column(String)
    jabatan = Column(String)

class Pasien(Base):
    __tablename__ = "pasien"

    id = Column(Integer, primary_key=True, index=True)
    nik = Column(Integer, unique=True)
    nama = Column(String)
    jenis_kelamin = Column(String)
    umur = Column(Integer)
    alamat = Column(String)

class Antrian(Base):
    __tablename__ = "antrian"

    id = Column(Integer, primary_key=True, index=True)
    nomor_antrian = Column(Integer, autoincrement=True)
    keluhan = Column(String)
    dokter_id = Column(Integer, ForeignKey("dokter.id"))
    pasien_id = Column(Integer, ForeignKey("pasien.id"))

    dokter = relationship("Dokter", back_populates="antrian")
    pasien = relationship("Pasien", back_populates="antrian")

Dokter.antrian = relationship("Antrian", back_populates="dokter")
Pasien.antrian = relationship("Antrian", back_populates="pasien")
