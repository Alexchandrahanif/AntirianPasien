## Tahap Tahap Menjalankan

- Install Python (https://www.python.org/downloads/)

- Install PostgreSQL (https://www.postgresql.org/download/)

- Ubah Konfigurasi URL_DATABASE di file database.py sesuai konfigurasi dari postgreSQL anda (user, password, dan nama Database)

- Buat Database sesuai nama yang anda buat, saat ini nama database nya (AntrianPasien)

- pip install fastapi sqlalchemy uvicorn

- jalankan diterminal "uvicorn main:app --reload"

## Kekurangan

- Untuk Fungsi API nya masih menumpuk di main.py, seharusnya dipisahkan router, controller, dan modelnya
- masih kurang/lengkap pas dalam menampilkan respon dari API
- belum terlalu clean code kasih baru belajar python sejak 20 Oktober 2023
