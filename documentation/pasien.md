## Endpoints

List of Available Endpoints:

- `GET http://127.0.0.1:8000/pasien/`
- `GET http://127.0.0.1:8000/pasien/:pasien_id`
- `POST http://127.0.0.1:8000/pasien`
- `PATCH http://127.0.0.1:8000/pasien/:pasien_id`
- `DELETE http://127.0.0.1:8000/pasien/:pasien_id`

## 1. GET http://127.0.0.1:8000/pasien

#### Description

- Get All Data pasien

#### Response

_200 - OK_

- Body
  ```json
  {
    "id": Integer,
    "nik": Integer,
    "nama": "String",
    "jenis_kelamin": "String",
    "umur": Integer,
    "alamat": "String"
  }
  ....
  ```

## 2. GET http://127.0.0.1:8000/pasien/:pasien_id

#### Description

- Get One Data pasien

#### Request

- Params

  ```json
  {
    "pasien_id": Integer
  }
  ```

#### Response

_200 - OK_

- Body

  ```json
  {
    "id": Integer,
    "nik": Integer,
    "nama": "String",
    "jenis_kelamin": "String",
    "umur": Integer,
    "alamat": "String"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 3. POST http://127.0.0.1:8000/pasien

#### Description

- Create pasien

#### Request

- Body

  ```json
  {
    "nik": Integer,
    "nama": "String",
    "jenis_kelamin": "String",
    "umur": Integer,
    "alamat": "String"
  }
  ```

#### Response

_200 - OK_

- Body

  ```json
  {
    "id": Integer,
    "nik": Integer,
    "nama": "String",
    "jenis_kelamin": "String",
    "umur": Integer,
    "alamat": "String"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 4. PATCH http://127.0.0.1:8000/pasien/:pasien_id

#### Description

- Update Data pasien by Req Params pasien_id

#### Request

- Params

  ```json
  {
    "pasien_id": Integer
  }
  ```

- Body

  ```json
  {
    "nik": Integer,
    "nama": "String",
    "jenis_kelamin": "String",
    "umur": Integer,
    "alamat": "String"
  }
  ```

#### Response

_200 - Success_

- Body

  ```json
  {
    "status_code": 200,
    "message": "Data pasien Berhasil Diperbaharui"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 5. DELETE http://127.0.0.1:8000/pasien/:pasien_id

#### Description

- Delete Data pasien By pasien_id

#### Request

- Params

  ```json
  {
    "pasien_id": Integer
  }
  ```

#### Response

_200 - Success_

- Body

  ```json
  {
    "status_code": 200,
    "message": "Data pasien Berhasil Dihapus"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```
