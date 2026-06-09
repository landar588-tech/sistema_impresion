import json
import os

RUTA_CARPETA = "app/data/storage"
RUTA_ARCHIVO = os.path.join(RUTA_CARPETA, "ordenes.json")


def _asegurar_storage():
    os.makedirs(RUTA_CARPETA, exist_ok=True)
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)


def cargar_ordenes():
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def guardar_ordenes(ordenes):
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(ordenes, f, indent=4, ensure_ascii=False)


def generar_id_orden():
    ordenes = cargar_ordenes()
    if not ordenes:
        return 1
    return max(o.get("id_orden", 0) for o in ordenes) + 1


def agregar_orden(orden):
    ordenes = cargar_ordenes()
    ordenes.append(orden)
    guardar_ordenes(ordenes)


def obtener_orden_por_id(id_orden):
    ordenes = cargar_ordenes()
    for o in ordenes:
        if o.get("id_orden") == id_orden:
            return o
    return None


def actualizar_orden(id_orden, datos_actualizados):
    ordenes = cargar_ordenes()
    for o in ordenes:
        if o.get("id_orden") == id_orden:
            o.update(datos_actualizados)
            guardar_ordenes(ordenes)
            return True
    return False


def cancelar_orden_data(id_orden):
    return actualizar_orden(id_orden, {"estado": "Cancelado", "activo": False})