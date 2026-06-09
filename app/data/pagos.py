import json
import os

RUTA_PAGOS = "app/data/storage/pagos.json"


def cargar_pagos():
    if not os.path.exists(RUTA_PAGOS):
        return []

    with open(RUTA_PAGOS, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


def guardar_pagos(pagos):
    with open(RUTA_PAGOS, "w", encoding="utf-8") as archivo:
        json.dump(pagos, archivo, indent=4, ensure_ascii=False)


def generar_id_pago():
    pagos = cargar_pagos()

    if not pagos:
        return 1

    return max(p["id_pago"] for p in pagos) + 1


def crear_pago(id_orden, monto, metodo_pago, fecha_pago, estado_pago="Pagado"):
    pagos = cargar_pagos()

    nuevo_pago = {
        "id_pago": generar_id_pago(),
        "id_orden": id_orden,
        "monto": monto,
        "metodo_pago": metodo_pago,
        "fecha_pago": fecha_pago,
        "estado_pago": estado_pago,
        "activo": True
    }

    pagos.append(nuevo_pago)
    guardar_pagos(pagos)

    return nuevo_pago


def listar_pagos():
    return cargar_pagos()


def listar_pagos_activos():
    return [p for p in cargar_pagos() if p.get("activo")]


def obtener_pago_por_id(id_pago):
    for p in cargar_pagos():
        if p.get("id_pago") == id_pago:
            return p

    return None


def obtener_pagos_por_orden(id_orden):
    return [p for p in cargar_pagos() if p.get("id_orden") == id_orden]


def actualizar_pago(id_pago, datos_actualizados):
    pagos = cargar_pagos()

    for p in pagos:
        if p.get("id_pago") == id_pago:
            p.update(datos_actualizados)
            guardar_pagos(pagos)
            return True

    return False


def cancelar_pago(id_pago):
    return actualizar_pago(
        id_pago,
        {"estado_pago": "Cancelado", "activo": False}
    )