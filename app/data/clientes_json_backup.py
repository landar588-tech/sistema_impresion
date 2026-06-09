import json
import os

RUTA_CARPETA = "app/data/storage"
RUTA_ARCHIVO = os.path.join(RUTA_CARPETA, "clientes.json")


def _asegurar_storage():
    os.makedirs(RUTA_CARPETA, exist_ok=True)
    if not os.path.exists(RUTA_ARCHIVO):
        with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
            json.dump([], f, indent=4, ensure_ascii=False)


def cargar_clientes():
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "r", encoding="utf-8") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []
def guardar_clientes(clientes):
    _asegurar_storage()
    with open(RUTA_ARCHIVO, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)


def generar_id_cliente():
    clientes = cargar_clientes()
    if not clientes:
        return 1
    return max(c.get("id_cliente", 0) for c in clientes) + 1


def agregar_cliente(cliente):
    clientes = cargar_clientes()
    clientes.append(cliente)
    guardar_clientes(clientes)


def obtener_cliente_por_id(id_cliente):
    clientes = cargar_clientes()
    for c in clientes:
        if c.get("id_cliente") == id_cliente:
            return c
    return None


def buscar_clientes(texto):
    texto = texto.lower()
    clientes = cargar_clientes()
    return [
        c for c in clientes
        if c.get("activo", True)
        and (
            texto in c.get("nombre", "").lower()
            or texto in c.get("empresa", "").lower()
            or texto in c.get("telefono", "").lower()
        )
    ]


def actualizar_cliente(id_cliente, datos_actualizados):
    clientes = cargar_clientes()
    for c in clientes:
        if c.get("id_cliente") == id_cliente:
            c.update(datos_actualizados)
            guardar_clientes(clientes)
            return True
    return False


def desactivar_cliente(id_cliente):
    clientes = cargar_clientes()
    for c in clientes:
        if c.get("id_cliente") == id_cliente:
            c["activo"] = False
            guardar_clientes(clientes)
            return True
    return False