from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import SessionLocal
import models
from datetime import datetime
from database import engine
from enum import Enum
from typing import List
from datetime import datetime, time, timedelta


app = FastAPI()
models.Base.metadata.create_all(bind=engine)


class JenisKelaminEnum(str, Enum):
    laki_laki = "laki-laki"
    perempuan = "perempuan"


class DokterBase(BaseModel):
    nama: str
    jenis_kelamin: JenisKelaminEnum
    nomor_telepon: str
    jabatan: str


class DokterResponse(BaseModel):
    id: int
    nama: str
    jenis_kelamin: JenisKelaminEnum
    nomor_telepon: str
    jabatan: str


class DokterCreate(DokterBase):
    pass


class PasienBase(BaseModel):
    nik: int
    nama: str
    jenis_kelamin: JenisKelaminEnum
    umur: int
    alamat: str


class PasienCreate(PasienBase):
    pass


class PasienResponse(BaseModel):
    id: int
    nik: int
    nama: str
    jenis_kelamin: JenisKelaminEnum
    umur: int
    alamat: str


class LayananBase(BaseModel):
    tanggal: datetime
    keterangan: str
    kuota: int
    dokter_id: int


class LayananCreate(LayananBase):
    pass


class LayananResponse(BaseModel):
    id: int
    tanggal: datetime
    keterangan: str
    kuota: int
    dokter_id: int


class AntrianBase(BaseModel):
    keluhan: str
    layanan_id: int
    pasien_id: int


class AntrianCreate(AntrianBase):
    pass


class AntrianResponse(BaseModel):
    id: int
    nomor_antrian: int
    keluhan: str
    layanan_id: int
    pasien_id: int
    dokter: DokterResponse
    pasien: PasienResponse


class ResponseModel(BaseModel):
    status_code: int
    message: str


def reset_nomor_antrian_daily():
    now = datetime.now()
    reset_time = time(0, 0)
    if now.time() == reset_time:

        return 1
    return None


def get_next_nomor_antrian(db: Session):
    nomor_antrian_harian = reset_nomor_antrian_daily()
    if nomor_antrian_harian is not None:
        return nomor_antrian_harian

    highest_antrian = db.query(models.Antrian).order_by(
        models.Antrian.nomor_antrian.desc()).first()
    if highest_antrian:
        next_nomor = highest_antrian.nomor_antrian + 1
    else:
        next_nomor = 1

    return next_nomor


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD Dokter


@app.post("/dokter/", response_model=DokterResponse)
def create_dokter(dokter: DokterCreate, db: Session = Depends(get_db)):
    db_dokter = models.Dokter(**dokter.dict())
    db.add(db_dokter)
    db.commit()
    db.refresh(db_dokter)
    return db_dokter


@app.get("/dokter/", response_model=List[DokterResponse])
def read_all_dokter(db: Session = Depends(get_db)):
    dokter = db.query(models.Dokter).all()
    return dokter


@app.get("/dokter/{dokter_id}", response_model=DokterResponse)
def read_dokter(dokter_id: int, db: Session = Depends(get_db)):
    dokter = db.query(models.Dokter).filter(
        models.Dokter.id == dokter_id).first()
    if dokter is None:
        raise HTTPException(
            status_code=404, detail="Id Dokter Tidak Ditemukan")
    return dokter


@app.put("/dokter/{dokter_id}", response_model=DokterResponse)
def update_dokter(dokter_id: int, dokter_data: DokterCreate, db: Session = Depends(get_db)):
    existing_dokter = db.query(models.Dokter).filter(
        models.Dokter.id == dokter_id).first()
    if existing_dokter is None:
        raise HTTPException(
            status_code=404, detail="Id Dokter Tidak Ditemukan")
    for key, value in dokter_data.dict().items():
        setattr(existing_dokter, key, value)
    db.commit()
    db.refresh(existing_dokter)
    return existing_dokter


@app.delete("/dokter/{dokter_id}", response_model=ResponseModel, status_code=200)
def delete_dokter(dokter_id: int, db: Session = Depends(get_db)):
    dokter = db.query(models.Dokter).filter(
        models.Dokter.id == dokter_id).first()
    if dokter is None:
        raise HTTPException(
            status_code=404, detail="Id Dokter Tidak Ditemukan")

    db.delete(dokter)
    db.commit()

    return {"status_code": 200, "message": "Data Dokter Berhasil Dihapus"}

# CRUD Pasien


@app.post("/pasien/", response_model=PasienResponse)
def create_pasien(pasien: PasienCreate, db: Session = Depends(get_db)):
    existing_pasien = db.query(models.Pasien).filter(
        models.Pasien.nik == pasien.nik).first()
    if existing_pasien:
        raise HTTPException(status_code=400, detail="NIK sudah terdaftar")

    db_pasien = models.Pasien(**pasien.dict())
    db.add(db_pasien)
    db.commit()
    db.refresh(db_pasien)
    return db_pasien


@app.get("/pasien/{pasien_id}", response_model=PasienResponse)
def read_pasien(pasien_id: int, db: Session = Depends(get_db)):
    pasien = db.query(models.Pasien).filter(
        models.Pasien.id == pasien_id).first()
    if pasien is None:
        raise HTTPException(
            status_code=404, detail="Id Pasien Tidak Ditemukan")
    return pasien


@app.get("/pasien/", response_model=List[PasienResponse])
def read_all_pasien(db: Session = Depends(get_db)):
    pasien = db.query(models.Pasien).all()
    return pasien


@app.put("/pasien/{pasien_id}", response_model=PasienResponse)
def update_pasien(pasien_id: int, pasien_data: PasienCreate, db: Session = Depends(get_db)):
    existing_pasien = db.query(models.Pasien).filter(
        models.Pasien.id == pasien_id).first()
    if existing_pasien is None:
        raise HTTPException(
            status_code=404, detail="Id Pasien Tidak Ditemukan")
    for key, value in pasien_data.dict().items():
        setattr(existing_pasien, key, value)
    db.commit()
    db.refresh(existing_pasien)
    return existing_pasien


@app.delete("/pasien/{pasien_id}", response_model=ResponseModel, status_code=200)
def delete_pasien(pasien_id: int, db: Session = Depends(get_db)):
    pasien = db.query(models.Pasien).filter(
        models.Pasien.id == pasien_id).first()
    if pasien is None:
        raise HTTPException(
            status_code=404, detail="Id Pasien Tidak Ditemukan")
    db.delete(pasien)
    db.commit()
    return ResponseModel(status_code=200, message="Data Pasien Berhasil Dihapus")

# CRUD Layanan


@app.post("/layanan/", response_model=LayananResponse)
def create_layanan(layanan: LayananCreate, db: Session = Depends(get_db)):
    existing_dokter = db.query(models.Dokter).filter(
        models.Dokter.id == layanan.dokter_id).first()
    if existing_dokter is None:
        raise HTTPException(
            status_code=404, detail="ID Dokter tidak ditemukan")

    db_layanan = models.Layanan(**layanan.dict())
    db.add(db_layanan)
    db.commit()
    db.refresh(db_layanan)
    return db_layanan


@app.get("/layanan/{layanan_id}", response_model=LayananResponse)
def read_layanan(layanan_id: int, db: Session = Depends(get_db)):
    layanan = db.query(models.Layanan).filter(
        models.Layanan.id == layanan_id).first()
    if layanan is None:
        raise HTTPException(
            status_code=404, detail="Id Layanan Tidak Ditemukan")
    return layanan


@app.get("/layanan/", response_model=List[LayananResponse])
def read_all_layanan(db: Session = Depends(get_db)):
    layanan = db.query(models.Layanan).all()
    return layanan


@app.put("/layanan/{layanan_id}", response_model=LayananResponse)
def update_layanan(layanan_id: int, layanan_data: LayananCreate, db: Session = Depends(get_db)):
    existing_layanan = db.query(models.Layanan).filter(
        models.Layanan.id == layanan_id).first()
    if existing_layanan is None:
        raise HTTPException(
            status_code=404, detail="Id Layanan Tidak Ditemukan")
    for key, value in layanan_data.dict().items():
        setattr(existing_layanan, key, value)
    db.commit()
    db.refresh(existing_layanan)
    return existing_layanan


@app.delete("/layanan/{layanan_id}", response_model=ResponseModel, status_code=200)
def delete_layanan(layanan_id: int, db: Session = Depends(get_db)):
    layanan = db.query(models.Layanan).filter(
        models.Layanan.id == layanan_id).first()
    if layanan is None:
        raise HTTPException(
            status_code=404, detail="Id Layanan Tidak Ditemukan")

    db.delete(layanan)
    db.commit()

    return ResponseModel(status_code=200, message="Data Layanan Berhasil Dihapus")

# CRUD Antrian


@app.post("/antrian/", response_model=AntrianResponse)
def create_antrian(antrian: AntrianBase, db: Session = Depends(get_db)):
    existing_layanan = db.query(models.Layanan).filter(
        models.Layanan.id == antrian.layanan_id).first()
    if existing_layanan is None:
        raise HTTPException(
            status_code=404, detail="ID Layanan tidak ditemukan")

    existing_pasien = db.query(models.Pasien).filter(
        models.Pasien.id == antrian.pasien_id).first()
    if existing_pasien is None:
        raise HTTPException(
            status_code=404, detail="ID Pasien tidak ditemukan")

    # Cek apakah kuota layanan masih tersedia
    if existing_layanan.kuota <= 0:
        raise HTTPException(
            status_code=400, detail="Kuota layanan telah habis")

    next_nomor_antrian = get_next_nomor_antrian(db)

    # Kurangi kuota layanan
    existing_layanan.kuota -= 1

    dokter = existing_layanan.dokter
    db_antrian = models.Antrian(
        **antrian.dict(), nomor_antrian=next_nomor_antrian)

    db_antrian.dokter = dokter

    db.add(db_antrian)
    db.commit()
    db.refresh(db_antrian)

    return db_antrian


@app.get("/antrian/{antrian_id}", response_model=AntrianResponse)
def read_antrian(antrian_id: int, db: Session = Depends(get_db)):
    antrian = db.query(models.Antrian).filter(
        models.Antrian.id == antrian_id).first()
    if antrian is None:
        raise HTTPException(
            status_code=404, detail="Id Antrian Tidak Ditemukan")
    return antrian


@app.get("/antrian/", response_model=List[AntrianResponse])
def read_all_antrian(db: Session = Depends(get_db)):
    antrian = db.query(models.Antrian).all()
    return antrian


@app.put("/antrian/{antrian_id}", response_model=ResponseModel)
def update_antrian(antrian_id: int, antrian_data: AntrianCreate, db: Session = Depends(get_db)):
    existing_antrian = db.query(models.Antrian).filter(
        models.Antrian.id == antrian_id).first()
    if existing_antrian is None:
        raise HTTPException(
            status_code=404, detail="Id Antrian Tidak Ditemukan")
    for key, value in antrian_data.dict().items():
        setattr(existing_antrian, key, value)
    db.commit()
    db.refresh(existing_antrian)

    return ResponseModel(status_code=200, message="Data Antrian Berhasil Diperbaharui")


@app.delete("/antrian/{antrian_id}", response_model=ResponseModel, status_code=200)
def delete_antrian(antrian_id: int, db: Session = Depends(get_db)):
    antrian = db.query(models.Antrian).filter(
        models.Antrian.id == antrian_id).first()
    if antrian is None:
        raise HTTPException(
            status_code=404, detail="Id Antrian Tidak Ditemukan")
    db.delete(antrian)
    db.commit()
    return ResponseModel(status_code=200, message="Data Antrian Berhasil Dihapus")
