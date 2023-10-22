## Endpoints

List of Available Endpoints:

- `GET http://127.0.0.1:8000/antrian/`
- `GET http://127.0.0.1:8000/antrian/:antrian_id`
- `POST http://127.0.0.1:8000/antrian`
- `PATCH http://127.0.0.1:8000/antrian/:antrian_id`
- `DELETE http://127.0.0.1:8000/antrian/:antrian_id`

## 1. GET http://127.0.0.1:8000/antrian

#### Description

- Get All Data Antrian

#### Response

_200 - OK_

- Body
  ```json
  {
    "id": Integer,
    "nomor_antrian": Integer,
    "keluhan": "string",
    "layanan_id" : Integer,
    "pasien_id" : Integer
  }
  ....
  ```

## 2. GET http://127.0.0.1:8000/antrian/:antrian_id

#### Description

- Get One Data Antrian

#### Request

- Params

  ```json
  {
    "antrian_id": Integer
  }
  ```

#### Response

_200 - OK_

- Body

  ```json
  {
    "id": Integer,
    "nomor_antrian": Integer,
    "keluhan": "string",
    "layanan_id" : Integer,
    "pasien_id" : Integer
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 3. POST http://127.0.0.1:8000/antrian

#### Description

- Create Antrian

#### Request

- Body

  ```json
  {
    "keluhan": "string",
    "layanan_id": Integer,
    "pasien_id": Integer
  }
  ```

#### Response

_200 - OK_

- Body

  ```json
  {
    "id": Integer,
    "nomor_antrian": Integer,
    "keluhan": "string",
    "layanan_id": Integer,
    "pasien_id": Integer
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

_400 - Bad Request_

```json
{
  "detail": "Kuota layanan telah habis"
}
```

## 4. PATCH http://127.0.0.1:8000/antrian/:antrian_id

#### Description

- Update Data Antrian by Req Params antrian_id

#### Request

- Params

  ```json
  {
    "antrian_id": Integer
  }
  ```

- Body

  ```json
  {
    "keluhan": "Oke",
    "layanan_id": 2,
    "pasien_id": 2
  }
  ```

#### Response

_200 - Success_

- Body

  ```json
  {
    "status_code": 200,
    "message": "Data Antrian Berhasil Diperbaharui"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 5. DELETE http://127.0.0.1:8000/antrian/:antrian_id

#### Description

- Delete Data Antrian By antrian_id

#### Request

- Params

  ```json
  {
    "antrian_id": Integer
  }
  ```

#### Response

_200 - Success_

- Body

  ```json
  {
    "status_code": 200,
    "message": "Data Antrian Berhasil Dihapus"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```
