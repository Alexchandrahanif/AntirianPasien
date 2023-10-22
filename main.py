from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
import models
from enum import Enum
from typing import List
from sqlalchemy.orm import joinedload
from datetime import datetime, time

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

class AntrianBase(BaseModel):
    keluhan: str
    dokter_id: int
    pasien_id: int

class AntrianCreate(AntrianBase):
    pass

class AntrianResponse(BaseModel):
    id: int
    nomor_antrian: int
    keluhan: str
    dokter_id: int  
    pasien_id: int  
    dokter: DokterResponse 
    pasien: PasienResponse  



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


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

    highest_antrian = db.query(models.Antrian).order_by(models.Antrian.nomor_antrian.desc()).first()
    if highest_antrian:
        next_nomor = highest_antrian.nomor_antrian + 1
    else:
        next_nomor = 1

    return next_nomor


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
    dokter = db.query(models.Dokter).filter(models.Dokter.id == dokter_id).first()
    if dokter is None:
        raise HTTPException(status_code=404, detail="Id Dokter Tidak Ditemukan")
    return dokter

@app.put("/dokter/{dokter_id}", response_model=DokterResponse)
def update_dokter(dokter_id: int, dokter_data: DokterCreate, db: Session = Depends(get_db)):
    existing_dokter = db.query(models.Dokter).filter(models.Dokter.id == dokter_id).first()
    if existing_dokter is None:
        raise HTTPException(status_code=404, detail="Id Dokter Tidak Ditemukan")
    for key, value in dokter_data.dict().items():
        setattr(existing_dokter, key, value)
    db.commit()
    db.refresh(existing_dokter)
    return existing_dokter

@app.delete("/dokter/{dokter_id}", response_model=str, status_code=200)
def delete_dokter(dokter_id: int, db: Session = Depends(get_db)):
    dokter = db.query(models.Dokter).filter(models.Dokter.id == dokter_id).first()
    if dokter is None:
        raise HTTPException(status_code=404, detail="Id Dokter Tidak Ditemukan")
    db.delete(dokter)
    db.commit()
    return "Data Dokter Berhasil Dihapus"


# CRUD Pasien
@app.post("/pasien/", response_model=PasienResponse)
def create_pasien(pasien: PasienCreate, db: Session = Depends(get_db)):
    existing_pasien = db.query(models.Pasien).filter(models.Pasien.nik == pasien.nik).first()
    if existing_pasien:
        raise HTTPException(status_code=400, detail="NIK sudah terdaftar")

    db_pasien = models.Pasien(**pasien.dict())
    db.add(db_pasien)
    db.commit()
    db.refresh(db_pasien)
    return db_pasien


@app.get("/pasien/{pasien_id}", response_model=PasienResponse)
def read_pasien(pasien_id: int, db: Session = Depends(get_db)):
    pasien = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
    if pasien is None:
        raise HTTPException(status_code=404, detail="Id Pasien Tidak Ditemukan")
    return pasien

@app.get("/pasien/", response_model=List[PasienResponse])
def read_all_pasien(db: Session = Depends(get_db)):
    pasien = db.query(models.Pasien).all()
    return pasien

@app.put("/pasien/{pasien_id}", response_model=PasienResponse)
def update_pasien(pasien_id: int, pasien_data: PasienCreate, db: Session = Depends(get_db)):
    existing_pasien = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
    if existing_pasien is None:
        raise HTTPException(status_code=404, detail="Id Pasien Tidak Ditemukan")
    for key, value in pasien_data.dict().items():
        setattr(existing_pasien, key, value)
    db.commit()
    db.refresh(existing_pasien)
    return existing_pasien

@app.delete("/pasien/{pasien_id}", response_model=str, status_code=200)
def delete_pasien(pasien_id: int, db: Session = Depends(get_db)):
    pasien = db.query(models.Pasien).filter(models.Pasien.id == pasien_id).first()
    if pasien is None:
        raise HTTPException(status_code=404, detail="Id Pasien Tidak Ditemukan")
    db.delete(pasien)
    db.commit()
    return "Data Pasien Berhasil Dihapus"



# Endpoint untuk membuat antrian
@app.post("/antrian/", response_model=AntrianResponse)
def create_antrian(antrian: AntrianCreate, db: Session = Depends(get_db)):
    existing_dokter = db.query(models.Dokter).filter(models.Dokter.id == antrian.dokter_id).first()
    if existing_dokter is None:
        raise HTTPException(status_code=404, detail="ID Dokter tidak ditemukan")

    existing_pasien = db.query(models.Pasien).filter(models.Pasien.id == antrian.pasien_id).first()
    if existing_pasien is None:
        raise HTTPException(status_code=404, detail="ID Pasien tidak ditemukan")

    next_nomor_antrian = get_next_nomor_antrian(db)
    db_antrian = models.Antrian(**antrian.dict(), nomor_antrian=next_nomor_antrian)
    db.add(db_antrian)
    db.commit()
    db.refresh(db_antrian)
    return db_antrian

@app.get("/antrian/{antrian_id}", response_model=AntrianResponse)
def read_antrian(antrian_id: int, db: Session = Depends(get_db)):
    antrian = db.query(models.Antrian).filter(models.Antrian.id == antrian_id).first()
    if antrian is None:
        raise HTTPException(status_code=404, detail="Id Antrian Tidak Ditemukan")
    return antrian

@app.get("/antrian/", response_model=List[AntrianResponse])
def read_all_antrian(db: Session = Depends(get_db)):
    antrian = (
        db.query(models.Antrian)
        .options(joinedload(models.Antrian.pasien), joinedload(models.Antrian.dokter))
        .all()
    )
    return antrian

@app.put("/antrian/{antrian_id}", response_model=AntrianResponse)
def update_antrian(antrian_id: int, antrian_data: AntrianCreate, db: Session = Depends(get_db)):
    existing_antrian = db.query(models.Antrian).filter(models.Antrian.id == antrian_id).first()
    if existing_antrian is None:
        raise HTTPException(status_code=404, detail="Id Antrian Tidak Ditemukan")
    for key, value in antrian_data.dict().items():
        setattr(existing_antrian, key, value)
    db.commit()
    db.refresh(existing_antrian)
    return existing_antrian

@app.delete("/antrian/{antrian_id}", response_model=str, status_code=200)
def delete_antrian(antrian_id: int, db: Session = Depends(get_db)):
    antrian = db.query(models.Antrian).filter(models.Antrian.id == antrian_id).first()
    if antrian is None:
        raise HTTPException(status_code=404, detail="Id Antrian Tidak Ditemukan")
    db.delete(antrian)
    db.commit()
    return "Data Antrian Berhasil Dihapus"
