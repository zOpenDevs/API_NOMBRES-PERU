<p align="center">
  <h1 align="center">API DNI Peru</h1>
  <p align="center">REST API for DNI lookup by name — no Playwright or Selenium required</p>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?logo=python">
  <img src="https://img.shields.io/badge/flask-3.1-lightgrey?logo=flask">
  <img src="https://img.shields.io/badge/license-MIT-green">
</p>

---

## Requirements

- Python 3.8+
- pip

## Installation

```bash
pip install requests flask flask-cors
```

## Usage

### Start the server

```bash
py server.py
```

The terminal will display the available endpoint:

```
tu endpoint:
http://192.168.x.x:5000/api/buscar-dni
```

The server runs on `http://0.0.0.0:5000` and is accessible from any device on the same network.

---

## Endpoint

```
GET  /api/buscar-dni
POST /api/buscar-dni
```

### Parameters

| Parameter          | Type   | Required | Description        |
|--------------------|--------|----------|--------------------|
| `nombres`          | string | yes      | Full first name    |
| `apellido_paterno` | string | yes      | Paternal surname   |
| `apellido_materno` | string | yes      | Maternal surname   |

---

## Examples

### cURL

```bash
curl "http://localhost:5000/api/buscar-dni?nombres=pedro&apellido_paterno=castillo&apellido_materno=terrones"
```

### JavaScript (fetch)

```js
fetch("http://localhost:5000/api/buscar-dni?nombres=pedro&apellido_paterno=castillo&apellido_materno=terrones")
  .then(res => res.json())
  .then(data => console.log(data));
```

### Python (requests)

```python
import requests

resp = requests.get("http://localhost:5000/api/buscar-dni", params={
    "nombres": "pedro",
    "apellido_paterno": "castillo",
    "apellido_materno": "terrones",
})
print(resp.json())
```

---

## Successful response (200)

```json
[
  {
    "od_nombres": "PEDRO",
    "od_apaterno": "CASTILLO",
    "od_amaterno": "TERRONES",
    "od_dni": "12345678"
  }
]
```

Each object contains:

| Field           | Description                |
|-----------------|----------------------------|
| `od_nombres`    | Full first name            |
| `od_apaterno`   | Paternal surname           |
| `od_amaterno`   | Maternal surname           |
| `od_dni`        | DNI number                 |

---

## Errors

| Code | Description                    |
|------|--------------------------------|
| 400  | Missing required parameters    |
| 404  | No results found               |
| 500  | Internal server error          |

```json
{
  "error": "Sin resultados"
}
```

---

## Test page

Open `demo.html` in your browser to test the API with a graphical interface.

---

## Project structure

```
api_nombres/
  scraper.py       Scraping logic (token management, DNI search)
  server.py        Flask API server
  demo.html        Web test client
  README.md        This documentation
```

## Credits

Built by [zOpenDevs](https://github.com/zOpenDevs) — OpenSource for everyone.

## License

MIT
