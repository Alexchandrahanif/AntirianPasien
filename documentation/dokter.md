## Endpoints

List of Available Endpoints:

- `GET http://127.0.0.1:8000/dokter/`
- `GET http://127.0.0.1:8000/dokter/:dokter_id`
- `POST http://127.0.0.1:8000/dokter`
- `PATCH http://127.0.0.1:8000/dokter/:dokter_id`
- `DELETE http://127.0.0.1:8000/dokter/:dokter_id`

## 1. GET http://127.0.0.1:8000/dokter

#### Description

- Get All Data dokter

#### Response

_200 - OK_

- Body
  ```json
  {
    "id": Integer,
    "nama": "string",
    "jenis_kelamin": "string",
    "nomor_telepon": "string",
    "jabatan": "string"
  }
  .....
  ```

## 2. GET http://127.0.0.1:8000/dokter/:dokter_id

#### Description

- Get One Data dokter

#### Request

- Params

  ```json
  {
    "dokter_id": Integer
  }
  ```

#### Response

_200 - OK_

- Body
  ```json
  {
    "id": Integer,
    "nama": "string",
    "jenis_kelamin": "string",
    "nomor_telepon": "string",
    "jabatan": "string"
  }
  ```

## 3. POST http://127.0.0.1:8000/dokter

#### Description

- Create dokter

#### Request

- Body

  ```json
  {
    "nama": "string",
    "jenis_kelamin": "string",
    "nomor_telepon": "string",
    "jabatan": "string"
  }
  ```

#### Response

_200 - OK_

- Body

  ```json
    {
    "id": Integer,
    "nama": "string",
    "jenis_kelamin": "string",
    "nomor_telepon": "string",
    "jabatan": "string"
  }
  ```

  _404 - Not Found_

  ```json
  {
    "detail": "string"
  }
  ```

## 4. PATCH http://127.0.0.1:8000/dokter/:dokter_id

#### Description

- Update Data dokter by Req Params dokter_id

#### Request

- Params

  ```json
  {
    "dokter_id": Integer
  }
  ```

- Body

  ```json
  {
    "nama": "string",
    "jenis_kelamin": "string",
    "nomor_telepon": "string",
    "jabatan": "string"
  }
  ```

#### Response

_200 - Success_

- Body

  ```json
  {
    "status_code": 200,
    "message": "Data dokter Berhasil Diperbaharui"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```

## 5. DELETE http://127.0.0.1:8000/dokter/:dokter_id

#### Description

- Delete Data dokter By dokter_id

#### Request

- Params

  ```json
  {
    "dokter_id": Integer
  }
  ```

#### Response

_200 - Success_

- Body

  ```json
  {
    "status_code": 200,
    "message": "Data dokter Berhasil Dihapus"
  }
  ```

_404 - Not Found_

```json
{
  "detail": "string"
}
```
