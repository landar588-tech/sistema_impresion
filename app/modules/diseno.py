from datetime import datetime
from app.data.diseno import (
    agregar_diseno,
    generar_id_diseno,
    obtener_diseno_por_orden,
    obtener_diseno_por_id,
    actualizar_diseno,
    listar_disenos_activos_data,
    cancelar_diseno_data,
)
from app.data.ordenes import obtener_orden_por_id, actualizar_orden


ESTADOS_DISENO = [
    "Diseño en proceso",
    "Enviado al cliente",
    "Corrección solicitada",
    "Diseño aprobado",
    "Cancelado",
]


def crear_diseno_desde_orden():
    print("\n--- Crear Diseño desde Orden ---")
    try:
        id_orden = int(input("ID de la orden: "))
    except ValueError:
        print("ID inválido.")
        return

    orden = obtener_orden_por_id(id_orden)
    if not orden or not orden.get("activo", True):
        print("❌ Orden no encontrada o cancelada.")
        return

    if not orden.get("requiere_diseno", False):
        print("❌ Esta orden no requiere diseño.")
        return

    if obtener_diseno_por_orden(id_orden):
        print("❌ Ya existe un diseño activo para esta orden.")
        return

    diseno = {
        "id_diseno": generar_id_diseno(),
        "id_orden": id_orden,
        "fecha_creacion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "nombre_cliente": orden["nombre_cliente"],
        "producto_material": orden["producto_material"],
        "descripcion": orden["descripcion"],
        "estado_diseno": "Diseño en proceso",
        "fecha_envio_cliente": "",
        "fecha_aprobacion": "",
        "numero_correcciones": 0,
        "observaciones": "",
        "activo": True,
    }

    agregar_diseno(diseno)
    actualizar_orden(id_orden, {"estado": "Diseño en proceso"})
    print("✅ Diseño creado correctamente.")


def listar_disenos_activos():
    print("\n--- Diseños Activos ---")
    disenos = listar_disenos_activos_data()

    if not disenos:
        print("No hay diseños activos.")
        return

    for d in disenos:
        print(f"[{d['id_diseno']}] Orden {d['id_orden']} - {d['nombre_cliente']} - {d['estado_diseno']}")


def buscar_diseno_por_orden():
    print("\n--- Buscar Diseño por Orden ---")
    try:
        id_orden = int(input("ID de la orden: "))
    except ValueError:
        print("ID inválido.")
        return

    diseno = obtener_diseno_por_orden(id_orden)
    if not diseno:
        print("No se encontró diseño activo.")
        return

    for k, v in diseno.items():
        print(f"{k}: {v}")


def cambiar_estado_diseno():
    print("\n--- Cambiar Estado de Diseño ---")
    try:
        id_diseno = int(input("ID del diseño: "))
    except ValueError:
        print("ID inválido.")
        return

    diseno = obtener_diseno_por_id(id_diseno)
    if not diseno or not diseno.get("activo", True):
        print("Diseño no encontrado o cancelado.")
        return

    print(f"Estado actual: {diseno['estado_diseno']}")
    for e in ESTADOS_DISENO:
        print(f"- {e}")

    nuevo_estado = input("Nuevo estado: ").strip()
    if nuevo_estado not in ESTADOS_DISENO:
        print("❌ Estado no válido.")
        return

    cambios_diseno = {"estado_diseno": nuevo_estado}
    cambios_orden = {}

    if nuevo_estado == "Enviado al cliente":
        cambios_diseno["fecha_envio_cliente"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cambios_orden["estado"] = "Esperando aprobación del cliente"

    elif nuevo_estado == "Corrección solicitada":
        cambios_diseno["numero_correcciones"] = diseno.get("numero_correcciones", 0) + 1
        cambios_orden["estado"] = "Corrección solicitada"

    elif nuevo_estado == "Diseño aprobado":
        if diseno.get("estado_diseno") not in ["Enviado al cliente", "Corrección solicitada"]:
            print("❌ No se puede aprobar si no fue enviado al cliente.")
            return
        cambios_diseno["fecha_aprobacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cambios_orden["estado"] = "Diseño aprobado"

    elif nuevo_estado == "Cancelado":
        cancelar_diseno_data(id_diseno)
        print("✅ Diseño cancelado correctamente.")
        return

    actualizar_diseno(id_diseno, cambios_diseno)
    if cambios_orden:
        actualizar_orden(diseno["id_orden"], cambios_orden)

    print("✅ Estado de diseño actualizado correctamente.")


def cancelar_diseno():
    print("\n--- Cancelar Diseño ---")
    try:
        id_diseno = int(input("ID del diseño: "))
    except ValueError:
        print("ID inválido.")
        return

    if cancelar_diseno_data(id_diseno):
        print("✅ Diseño cancelado correctamente.")
    else:
        print("Diseño no encontrado.")