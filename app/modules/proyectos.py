from datetime import datetime, timedelta
from app.data.cotizaciones import obtener_cotizacion_por_id
from app.data.ordenes import (
    cargar_ordenes,
    agregar_orden,
    generar_id_orden,
    obtener_orden_por_id,
    actualizar_orden,
    cancelar_orden_data,
)


def crear_orden_desde_cotizacion():
    print("\n--- Crear Orden desde Cotización ---")
    try:
        id_cot = int(input("ID de la cotización: "))
    except ValueError:
        print("ID inválido.")
        return

    cot = obtener_cotizacion_por_id(id_cot)
    if not cot or not cot.get("activo", True):
        print("❌ Cotización no encontrada o cancelada.")
        return

    for o in cargar_ordenes():
        if o.get("id_cotizacion") == id_cot and o.get("activo", True):
            print("❌ Ya existe una orden activa para esta cotización.")
            return

    fecha_creacion = datetime.now()
    dias = cot.get("dias_entrega_estimados", 3)

    orden = {
        "id_orden": generar_id_orden(),
        "id_cotizacion": cot["id_cotizacion"],
        "fecha_creacion": fecha_creacion.strftime("%Y-%m-%d %H:%M:%S"),
        "id_cliente": cot["id_cliente"],
        "nombre_cliente": cot["nombre_cliente"],
        "producto_material": cot["producto_material"],
        "cantidad": cot["cantidad"],
        "descripcion": cot["descripcion"],
        "cliente_trae_diseno": cot["cliente_trae_diseno"],
        "requiere_diseno": not cot["cliente_trae_diseno"],
        "costo_diseno": cot["costo_diseno"],
        "costo_produccion": cot["costo_produccion"],
        "total": cot["total"],
        "anticipo_requerido": cot["anticipo_50"],
        "anticipo_pagado": 0,
        "saldo_pendiente": cot["total"],
        "dias_entrega_estimados": dias,
        "fecha_estimada_entrega": (fecha_creacion + timedelta(days=dias)).strftime("%Y-%m-%d"),
        "estado": "Anticipo pendiente",
        "observaciones": cot.get("observaciones", ""),
        "activo": True,
    }

    agregar_orden(orden)
    print("✅ Orden creada correctamente.")


def listar_ordenes_activas():
    print("\n--- Órdenes Activas ---")
    ordenes = [o for o in cargar_ordenes() if o.get("activo", True)]

    if not ordenes:
        print("No hay órdenes activas.")
        return

    for o in ordenes:
        print(f"[{o['id_orden']}] Cot:{o['id_cotizacion']} - {o['nombre_cliente']} - {o['producto_material']} - {o['estado']}")


def buscar_orden():
    print("\n--- Buscar Orden ---")
    texto = input("Buscar por cliente, producto o ID: ").strip().lower()
    resultados = []

    for o in cargar_ordenes():
        if not o.get("activo", True):
            continue
        if (
            texto in str(o.get("id_orden", "")).lower()
            or texto in o.get("nombre_cliente", "").lower()
            or texto in o.get("producto_material", "").lower()
        ):
            resultados.append(o)

    if not resultados:
        print("No se encontraron coincidencias.")
        return

    for o in resultados:
        print(f"[{o['id_orden']}] {o['nombre_cliente']} - {o['producto_material']} - {o['estado']}")


def ver_detalle_orden():
    print("\n--- Ver Detalle de Orden ---")
    try:
        id_orden = int(input("ID de la orden: "))
    except ValueError:
        print("ID inválido.")
        return

    orden = obtener_orden_por_id(id_orden)
    if not orden or not orden.get("activo", True):
        print("Orden no encontrada o cancelada.")
        return

    for k, v in orden.items():
        print(f"{k}: {v}")


def cambiar_estado_orden():
    print("\n--- Cambiar Estado de Orden ---")
    print("Este cambio lo conectaremos después con Pagos/Diseño/Producción.")


def cancelar_orden():
    print("\n--- Cancelar Orden ---")
    try:
        id_orden = int(input("ID de la orden: "))
    except ValueError:
        print("ID inválido.")
        return

    if cancelar_orden_data(id_orden):
        print("✅ Orden cancelada correctamente.")
    else:
        print("Orden no encontrada.")