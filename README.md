# Chat

### Usage

Run
```bash
docker-compose up --build -d
```

Entrypoints:

- Signin

POST `api/users/signin`

```bash
curl -d '{"email":"test@test.com","password":"qwerty12"}' -H 'Content-Type: application/json' -H 'Accept: application/json' http://localhost:8100/api/users/signin
```

Response

```json
{
  "data": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzcsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9.EEMaDY2wJg3KksTRQTOl1chI4bWALsJTLM6iuRgFD8A",
  "meta": {
    "code": 200,
    "message": "OK"
  }
}
```

- Users list

GET `api/users`

```bash
curl -H 'Content-Type: application/json' -H 'Accept: application/json' http://localhost:8100/api/users
```

Response

```json
{
  "data": [
    {
      "created": "2018-12-25T17:42:46.501001",
      "email": "test@test.com",
      "id": 37
    },
    {
      "created": "2018-12-26T09:58:06.355573",
      "email": "test2@test.com",
      "id": 70
    }
  ],
  "meta": {
    "code": 200,
    "message": "OK"
  }
}
```

- Messages list

GET `api/messages`

```bash
curl -H 'Content-Type: application/json' -H 'Accept: application/json' http://localhost:8100/api/messages
```

Response

```json
{
  "data": [
    {
      "created": "2018-12-25T19:43:58.027719",
      "id": 2,
      "text": "Hello world!",
      "user": {
        "created": "2018-12-25T17:42:46.501001",
        "email": "test@test.com",
        "id": 37
      }
    },
    {
      "created": "2018-12-25T19:52:43.753067",
      "id": 3,
      "text": "Hello world1!",
      "user": {
        "created": "2018-12-25T17:42:46.501001",
        "email": "test@test.com",
        "id": 37
      }
    },
    {
      "created": "2018-12-25T19:52:48.320707",
      "id": 4,
      "text": "Hello world2!",
      "user": {
        "created": "2018-12-25T17:42:46.501001",
        "email": "test@test.com",
        "id": 37
      }
    },
    {
      "created": "2018-12-25T19:52:52.629876",
      "id": 5,
      "text": "Hello world3!",
      "user": {
        "created": "2018-12-25T17:42:46.501001",
        "email": "test@test.com",
        "id": 37
      }
    }
  ],
  "meta": {
    "code": 200,
    "message": "OK"
  }
}
```

- Post message (need auth)

POST `api/message`

```bash
curl -d '{"text":"Happy New Year!"}' -H 'Content-Type: application/json' -H 'Accept: application/json' -H 'Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpZCI6MzcsImVtYWlsIjoidGVzdEB0ZXN0LmNvbSJ9.EEMaDY2wJg3KksTRQTOl1chI4bWALsJTLM6iuRgFD8A' http://localhost:8100/api/messages
```

Response

```json
{
  "data": null,
  "meta": {
    "code": 200,
    "message": "OK"
  }
}
```