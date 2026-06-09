import json
import os

RUTA_CARPETA = "app/data/storage"
RUTA_ARCHIVO = os.path.join(RUTA_CARPETA, "produccion.json")


def _asegurar_storage():
    os.makedirs(RUTA_CARPETA, exist_ok=True)
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)


def cargar_produccion():
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def guardar_produccion(registros):
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(registros, f, indent=4, ensure_ascii=False)


def generar_id_produccion():
    registros = cargar_produccion()
    if not registros:
        return 1
    return max(r.get("id_produccion", 0) for r in registros) + 1


def agregar_registro_produccion(registro):
    registros = cargar_produccion()
    registros.append(registro)
    guardar_produccion(registros)


def obtener_produccion_por_orden(id_orden):
    for r in cargar_produccion():
        if r.get("id_orden") == id_orden and r.get("activo", True):
            return r
    return None


def obtener_produccion_por_id(id_produccion):
    for r in cargar_produccion():
        if r.get("id_produccion") == id_produccion:
            return r
    return None


def actualizar_produccion(id_produccion, datos_actualizados):
    registros = cargar_produccion()
    for r in registros:
        if r.get("id_produccion") == id_produccion:
            r.update(datos_actualizados)
            guardar_produccion(registros)
            return True
    return False


def listar_produccion_activa_data():
    return [r for r in cargar_produccion() if r.get("activo", True)]


def cancelar_produccion_data(id_produccion):
    return actualizar_produccion(
        id_produccion,
        {"estado_produccion": "Cancelado", "activo": False}
    )