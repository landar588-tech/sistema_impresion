from datetime import datetime, timedelta

from app.data.clientes import cargar_clientes
from app.data.cotizaciones import cargar_cotizaciones
from app.data.ordenes import cargar_ordenes
from app.data.diseno import cargar_disenos
from app.data.produccion import cargar_produccion
from app.data.pagos import cargar_pagos


def _es_activo(registro):
    return registro.get("activo", True)


def ver_dashboard_general():
    clientes = cargar_clientes()
    cotizaciones = cargar_cotizaciones()
    ordenes = cargar_ordenes()
    disenos = cargar_disenos()
    produccion = cargar_produccion()
    pagos = cargar_pagos()

    print("\n=== DASHBOARD GENERAL GM7 ===\n")

    print(f"Clientes activos: {sum(1 for c in clientes if _es_activo(c))}")
    print(f"Cotizaciones activas: {sum(1 for c in cotizaciones if _es_activo(c))}")
    print(f"Órdenes activas: {sum(1 for o in ordenes if _es_activo(o))}")
    print(f"Diseños activos: {sum(1 for d in disenos if _es_activo(d))}")
    print(f"Producción activa: {sum(1 for p in produccion if _es_activo(p))}")
    print(f"Pagos registrados: {sum(1 for p in pagos if _es_activo(p))}")

    total_ingresos = sum(float(p.get("monto", 0)) for p in pagos if _es_activo(p))
    saldo_pendiente = sum(float(o.get("saldo_pendiente", 0)) for o in ordenes if _es_activo(o))

    print("\n--- Resumen financiero ---")
    print(f"Ingresos registrados: ${total_ingresos:,.2f}")
    print(f"Saldos pendientes: ${saldo_pendiente:,.2f}")

    input("\nPresiona Enter para continuar...")


def ver_entregas_proximas():
    ordenes = cargar_ordenes()

    hoy = datetime.now().date()
    limite = hoy + timedelta(days=7)

    print("\n=== ENTREGAS PRÓXIMAS ===")

    hay_entregas = False

    for orden in ordenes:
        if not _es_activo(orden):
            continue

        fecha_str = orden.get("fecha_estimada_entrega")

        if not fecha_str:
            continue

        try:
            fecha_entrega = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            continue

        if hoy <= fecha_entrega <= limite:
            hay_entregas = True
            print(f"\nOrden: {orden.get('id_orden')}")
            print(f"Cliente: {orden.get('nombre_cliente')}")
            print(f"Entrega: {fecha_str}")
            print(f"Estado: {orden.get('estado')}")

    if not hay_entregas:
        print("No hay entregas próximas.")

    input("\nPresiona Enter para continuar...")


def ver_pagos_pendientes():
    ordenes = cargar_ordenes()

    print("\n=== PAGOS PENDIENTES ===")

    hay_pendientes = False

    for orden in ordenes:
        if not _es_activo(orden):
            continue

        saldo = float(orden.get("saldo_pendiente", 0) or 0)

        if saldo > 0:
            hay_pendientes = True
            print(f"\nOrden: {orden.get('id_orden')}")
            print(f"Cliente: {orden.get('nombre_cliente')}")
            print(f"Anticipo requerido: ${float(orden.get('anticipo_requerido', 0) or 0):,.2f}")
            print(f"Anticipo pagado: ${float(orden.get('anticipo_pagado', 0) or 0):,.2f}")
            print(f"Saldo pendiente: ${saldo:,.2f}")

    if not hay_pendientes:
        print("No hay pagos pendientes.")

    input("\nPresiona Enter para continuar...")
