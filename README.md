# Book Search API

API REST en FastAPI que busca libros por título usando Google Books API.

## Endpoint

```
GET /books/search?q={titulo}
```

### Respuesta
```json
[
  {
    "title": "Harry Potter and the Sorcerer's Stone",
    "description": "Harry Potter has no idea how famous he is...",
    "authors": ["J.K. Rowling"],
    "cover": "http://books.google.com/books/content?id=...&zoom=1&edge=curl"
  }
]
```

### Errores
| Código | Causa |
|--------|-------|
| 422 | Falta el parámetro `q` o es vacío |
| 502 | Google Books API no disponible |

## Correr localmente

```bash
pip install -r requirements.txt
python main.py
# Docs en http://localhost:8000/docs
```

## Tests

```bash
python -m pytest
```

## Deploy en Railway

1. Sube el proyecto a GitHub
2. En [railway.app](https://railway.app) → New Project → Deploy from GitHub
3. Selecciona el repo → Railway detecta el `Procfile` automáticamente
4. Tu API queda en `https://{tu-proyecto}.up.railway.app/books/search?q=dune`
