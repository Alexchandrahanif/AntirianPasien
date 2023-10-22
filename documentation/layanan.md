## Endpoints

List of Available Endpoints:

- `GET http://127.0.0.1:8000/layanan/`
- `GET http://127.0.0.1:8000/layanan/:layanan_id`
- `POST http://127.0.0.1:8000/layanan`
- `PATCH http://127.0.0.1:8000/layanan/:layanan_id`
- `DELETE http://127.0.0.1:8000/layanan/:layanan_id`

## 1. GET http://127.0.0.1:8000/layanan

#### Description

- Get All Data layanan

#### Response

_200 - OK_

- Body
  ```json
  {
    "id": Integer,
    "tanggal": "Date",
    "keterangan": "String",
    "kuota": Integer,
    "dokter_id": Integer
  }
  ....
  ```

## 2. GET http://127.0.0.1:8000/layanan/:layanan_id

#### Description

- Get One Data layanan

#### Request

- Params

  ```json
  {
    "layanan_id": Integer
  }
  ```

#### Response

_200 - OK_

- Body

  ```json
   {
    "id": Integer,
    "tanggal": "Date",
    "keterangan": "String",
    "kuota": Integer,
    "dokter_id": Integer
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 3. POST http://127.0.0.1:8000/layanan

#### Description

- Create layanan

#### Request

- Body

  ```json
  {
    "tanggal": "Date",
    "keterangan": "String",
    "kuota": Integer,
    "dokter_id": Integer
  }
  ```

#### Response

_200 - OK_

- Body

  ```json
   {
    "id": Integer,
    "tanggal": "Date",
    "keterangan": "String",
    "kuota": Integer,
    "dokter_id": Integer
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 4. PATCH http://127.0.0.1:8000/layanan/:layanan_id

#### Description

- Update Data layanan by Req Params layanan_id

#### Request

- Params

  ```json
  {
    "layanan_id": Integer
  }
  ```

- Body

  ```json
   {
    "tanggal": "Date",
    "keterangan": "String",
    "kuota": Integer,
    "dokter_id": Integer
  }
  ```

#### Response

_200 - Success_

- Body

  ```json
  {
    "status_code": 200,
    "message": "Data layanan Berhasil Diperbaharui"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 5. DELETE http://127.0.0.1:8000/layanan/:layanan_id

#### Description

- Delete Data layanan By layanan_id

#### Request

- Params

  ```json
  {
    "layanan_id": Integer
  }
  ```

#### Response

_200 - Success_

- Body

  ```json
  {
    "status_code": 200,
    "message": "Data layanan Berhasil Dihapus"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```
