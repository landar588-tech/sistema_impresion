from datetime import datetime, timedelta

from app.data.clientes import cargar_clientes
from app.data.cotizaciones import cargar_cotizaciones
from app.data.ordenes import cargar_ordenes
from app.data.pagos import cargar_pagos
from app.data.diseno import cargar_disenos
from app.data.produccion import cargar_produccion


def _es_activo(registro):
    return registro.get("activo", True)


def ver_dashboard_general():
    clientes = cargar_clientes()
    cotizaciones = cargar_cotizaciones()
    ordenes = cargar_ordenes()
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
    print("\n=== ENTREGAS PRÓXIMAS ===")
    print("Módulo funcionando.")
    input("\nPresiona Enter para continuar...")


def ver_pagos_pendientes():
    print("\n=== PAGOS PENDIENTES ===")
    print("Módulo funcionando.")
    input("\nPresiona Enter para continuar...")