"""Catálogo de productos - LPII
Backend Flask con Quicksort, Búsqueda Binaria y Benchmark.
"""
import json
import os
import random
import time

from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

RUTA_JSON = os.path.join(os.path.dirname(os.path.abspath(__file__)), "productos.json")
CAMPOS_VALIDOS = {"id", "nombre", "precio"}


def cargar_productos():
    with open(RUTA_JSON, encoding="utf-8") as f:
        return json.load(f)


def valor(item, clave):
    """Valor comparable: los textos se comparan sin distinguir mayúsculas."""
    v = item[clave]
    return v.lower() if isinstance(v, str) else v


# ---------------------------------------------------------------- Algoritmos
def quicksort(items, clave, reverse=False):
    """Quicksort recursivo (pivote central, 3 particiones: menores/iguales/mayores)."""
    if len(items) <= 1:
        return items
    pivote = valor(items[len(items) // 2], clave)
    if reverse:
        izq = [x for x in items if valor(x, clave) > pivote]
        der = [x for x in items if valor(x, clave) < pivote]
    else:
        izq = [x for x in items if valor(x, clave) < pivote]
        der = [x for x in items if valor(x, clave) > pivote]
    centro = [x for x in items if valor(x, clave) == pivote]
    return quicksort(izq, clave, reverse) + centro + quicksort(der, clave, reverse)


def burbuja(items, clave, reverse=False):
    """Ordenamiento burbuja O(n^2) con corte anticipado (solo para el benchmark)."""
    datos = list(items)
    n = len(datos)
    for i in range(n - 1):
        hubo_cambio = False
        for j in range(n - 1 - i):
            a, b = valor(datos[j], clave), valor(datos[j + 1], clave)
            if (a < b) if reverse else (a > b):
                datos[j], datos[j + 1] = datos[j + 1], datos[j]
                hubo_cambio = True
        if not hubo_cambio:
            break
    return datos


def busqueda_binaria(items, clave, objetivo):
    """Búsqueda binaria. PRECONDICIÓN: `items` debe estar ordenada ascendentemente por `clave`.
    Devuelve (indice, pasos); indice = -1 si no existe."""
    bajo, alto, pasos = 0, len(items) - 1, 0
    while bajo <= alto:
        pasos += 1
        medio = (bajo + alto) // 2
        actual = items[medio][clave]
        if actual == objetivo:
            return medio, pasos
        if actual < objetivo:
            bajo = medio + 1
        else:
            alto = medio - 1
    return -1, pasos


# ---------------------------------------------------------------------- Rutas
@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/productos")
def get_productos():
    sort_by = request.args.get("sort_by", "precio")
    if sort_by not in CAMPOS_VALIDOS:
        return jsonify(error=f"sort_by inválido. Use: {sorted(CAMPOS_VALIDOS)}"), 400
    desc = request.args.get("order", "asc") == "desc"
    return jsonify(quicksort(cargar_productos(), sort_by, reverse=desc))


@app.route("/api/productos/buscar")
def buscar_producto():
    """Búsqueda binaria por id. Primero se ordena por id (precondición)."""
    try:
        objetivo = int(request.args.get("id", ""))
    except ValueError:
        return jsonify(error="Parámetro 'id' obligatorio y numérico."), 400

    ordenados = quicksort(cargar_productos(), "id")  # precondición
    indice, pasos = busqueda_binaria(ordenados, "id", objetivo)
    if indice == -1:
        return jsonify(encontrado=False, id=objetivo, pasos=pasos,
                       mensaje="Producto no encontrado"), 404
    return jsonify(encontrado=True, indice=indice, pasos=pasos,
                   producto=ordenados[indice])


@app.route("/api/benchmark")
def benchmark():
    """Compara Quicksort vs Burbuja con los productos de productos.json (1.000 por defecto).
    Si el catálogo tiene menos de n elementos, se completa con productos aleatorios."""
    try:
        n = min(max(int(request.args.get("n", 1000)), 2), 5000)
    except ValueError:
        n = 1000
    datos = cargar_productos()[:n]
    for i in range(len(datos), n):
        datos.append({"id": i + 1, "nombre": f"Producto {i + 1}",
                      "precio": round(random.uniform(1, 1000), 2)})

    t0 = time.perf_counter()
    r_quick = quicksort(datos, "precio")
    t_quick = (time.perf_counter() - t0) * 1000

    t0 = time.perf_counter()
    r_burb = burbuja(datos, "precio")
    t_burb = (time.perf_counter() - t0) * 1000

    return jsonify(
        elementos=n,
        quicksort_ms=round(t_quick, 3),
        burbuja_ms=round(t_burb, 3),
        veces_mas_rapido=round(t_burb / t_quick, 1) if t_quick else None,
        resultados_iguales=[x["precio"] for x in r_quick] == [x["precio"] for x in r_burb],
    )


if __name__ == "__main__":
    app.run(debug=True)