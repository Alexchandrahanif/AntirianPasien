from sqlalchemy import Column, ForeignKey, Integer, String, Date
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


Pasien.antrian = relationship("Antrian", back_populates="pasien")


class Layanan(Base):
    __tablename__ = "layanan"

    id = Column(Integer, primary_key=True, index=True)
    tanggal = Column(Date)
    keterangan = Column(String)
    kuota = Column(Integer)
    dokter_id = Column(Integer, ForeignKey("dokter.id"))

    dokter = relationship("Dokter", back_populates="layanan")
    antrian = relationship("Antrian", back_populates="layanan")


Dokter.layanan = relationship("Layanan", back_populates="dokter")


class Antrian(Base):
    __tablename__ = "antrian"

    id = Column(Integer, primary_key=True, index=True)
    nomor_antrian = Column(Integer, autoincrement=True)
    keluhan = Column(String)
    layanan_id = Column(Integer, ForeignKey("layanan.id"))
    pasien_id = Column(Integer, ForeignKey("pasien.id"))

    pasien = relationship("Pasien", back_populates="antrian")
    layanan = relationship("Layanan", back_populates="antrian")
