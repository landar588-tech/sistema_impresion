import json
import os

RUTA_CARPETA = "app/data/storage"
RUTA_ARCHIVO = os.path.join(RUTA_CARPETA, "cotizaciones.json")


def _asegurar_storage():
    os.makedirs(RUTA_CARPETA, exist_ok=True)
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)


def cargar_cotizaciones():
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
def guardar_cotizaciones(cotizaciones):
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(cotizaciones, f, indent=4, ensure_ascii=False)


def generar_id_cotizacion():
    cotizaciones = cargar_cotizaciones()
    if not cotizaciones:
        return 1
    return max(c.get("id_cotizacion", 0) for c in cotizaciones) + 1


def agregar_cotizacion(cotizacion):
    cotizaciones = cargar_cotizaciones()
    cotizaciones.append(cotizacion)
    guardar_cotizaciones(cotizaciones)


def obtener_cotizacion_por_id(id_cotizacion):
    cotizaciones = cargar_cotizaciones()
    for c in cotizaciones:
        if c.get("id_cotizacion") == id_cotizacion:
            return c
    return None


def buscar_cotizaciones(texto):
    texto = texto.lower()
    cotizaciones = cargar_cotizaciones()
    return [
        c for c in cotizaciones
        if c.get("activo", True)
        and (
            texto in str(c.get("id_cotizacion", "")).lower()
            or texto in c.get("nombre_cliente", "").lower()
            or texto in c.get("producto_material", "").lower()
        )
    ]


def cancelar_cotizacion(id_cotizacion):
    cotizaciones = cargar_cotizaciones()
    for c in cotizaciones:
        if c.get("id_cotizacion") == id_cotizacion:
            c["estado"] = "Cancelada"
            c["activo"] = False
            guardar_cotizaciones(cotizaciones)
            return True
    return False