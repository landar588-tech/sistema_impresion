import json
import os

RUTA_CARPETA = "app/data/storage"
RUTA_ARCHIVO = os.path.join(RUTA_CARPETA, "disenos.json")


def _asegurar_storage():
    os.makedirs(RUTA_CARPETA, exist_ok=True)
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)


def cargar_disenos():
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []


def guardar_disenos(disenos):
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(disenos, f, indent=4, ensure_ascii=False)


def generar_id_diseno():
    disenos = cargar_disenos()
    if not disenos:
        return 1
    return max(d.get("id_diseno", 0) for d in disenos) + 1


def agregar_diseno(diseno):
    disenos = cargar_disenos()
    disenos.append(diseno)
    guardar_disenos(disenos)


def obtener_diseno_por_orden(id_orden):
    for d in cargar_disenos():
        if d.get("id_orden") == id_orden and d.get("activo", True):
            return d
    return None


def obtener_diseno_por_id(id_diseno):
    for d in cargar_disenos():
        if d.get("id_diseno") == id_diseno:
            return d
    return None


def actualizar_diseno(id_diseno, datos_actualizados):
    disenos = cargar_disenos()
    for d in disenos:
        if d.get("id_diseno") == id_diseno:
            d.update(datos_actualizados)
            guardar_disenos(disenos)
            return True
    return False


def listar_disenos_activos_data():
    return [d for d in cargar_disenos() if d.get("activo", True)]


def cancelar_diseno_data(id_diseno):
    return actualizar_diseno(id_diseno, {"estado_diseno": "Cancelado", "activo": False})