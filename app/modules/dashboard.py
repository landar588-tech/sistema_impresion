from datetime import datetime, timedelta

from app.database.clientes_db import obtener_clientes
from app.database.cotizaciones_db import obtener_cotizaciones
from app.database.ordenes_db import obtener_ordenes
from app.data.diseno import cargar_disenos
from app.data.produccion import cargar_produccion
from app.data.pagos import cargar_pagos


def _es_activo(registro):
    return registro.get("activo", True)


def ver_dashboard_general():
    clientes = obtener_clientes()
    cotizaciones = obtener_cotizaciones()
    ordenes = obtener_ordenes()
    disenos = cargar_disenos()
    produccion = cargar_produccion()
    pagos = cargar_pagos()

    print("\n=== DASHBOARD GENERAL ===")

    print(f"Clientes activos: {sum(1 for c in clientes if _es_activo(c))}")
    print(f"Cotizaciones activas: {sum(1 for c in cotizaciones if _es_activo(c))}")
    print(f"Órdenes activas: {sum(1 for o in ordenes if _es_activo(o))}")
    print(f"Diseños activos: {sum(1 for d in disenos if _es_activo(d))}")
    print(f"Producción activa: {sum(1 for p in produccion if _es_activo(p))}")
    print(f"Pagos registrados: {sum(1 for p in pagos if _es_activo(p))}")

    input("\nPresiona Enter para continuar...")
    
def ver_entregas_proximas():
    ordenes = obtener_ordenes()

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

        fecha_entrega = datetime.strptime(
            fecha_str,
            "%Y-%m-%d"
        ).date()

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
    ordenes = obtener_ordenes()

    print("\n=== PAGOS PENDIENTES ===")

    hay_pendientes = False

    for orden in ordenes:
        if not _es_activo(orden):
            continue

        saldo = orden.get("saldo_pendiente", 0)

        if saldo > 0:
            hay_pendientes = True

            print(f"\nOrden: {orden.get('id_orden')}")
            print(f"Cliente: {orden.get('nombre_cliente')}")
            print(
                f"Anticipo requerido: "
                f"${orden.get('anticipo_requerido', 0):,.2f}"
            )
            print(
                f"Anticipo pagado: "
                f"${orden.get('anticipo_pagado', 0):,.2f}"
            )
            print(f"Saldo pendiente: ${saldo:,.2f}")

    if not hay_pendientes:
        print("No hay pagos pendientes.")

    input("\nPresiona Enter para continuar...")