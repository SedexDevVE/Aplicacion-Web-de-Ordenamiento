# Aplicacion Web de Ordenamiento

Aplicación web desacoplada: **backend Flask** (Quicksort, búsqueda binaria, benchmark) y **frontend HTML5 + CSS + JS** que consume la API con `fetch()`.

## Estructura

```
├── app.py               # API Flask + algoritmos
├── templates/index.html # Frontend (fetch API)
├── productos.json       # Catálogo de datos
├── README.md
├── LICENSE              # MIT
└── .gitignore
```

## Ejecución

```bash
python -m venv venv
# Linux: source venv/bin/activate        # Windows: venv\Scripts\activate
pip install flask
python app.py
```

Abrir <http://127.0.0.1:5000>.

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| GET | `/` | Página web |
| GET | `/api/productos?sort_by=precio\|nombre\|id&order=asc\|desc` | Catálogo ordenado con Quicksort |
| GET | `/api/productos/buscar?id=X` | Búsqueda binaria por id (ordena primero por id: precondición) |
| GET | `/api/benchmark?n=1000` | Tiempo en ms de Quicksort vs Burbuja sobre los 1.000 productos del catálogo |

## Algoritmos

- **Quicksort**: recursivo, pivote central, tres particiones (menores / iguales / mayores). Promedio O(n log n). Insensible a mayúsculas al ordenar por texto.
- **Búsqueda binaria**: O(log n). Requiere lista ordenada, por lo que el endpoint ordena por `id` antes de buscar. Devuelve el número de pasos.
- **Burbuja**: O(n²), usada únicamente como referencia en el benchmark.

## Ejemplo de respuestas

`GET /api/productos/buscar?id=15`
```json
{"encontrado": true, "indice": 10, "pasos": 4, "producto": {"id": 15, "nombre": "Laptop 15.6\"", "precio": 749.99}}
```

## Licencia

MIT – ver [LICENSE](LICENSE).
