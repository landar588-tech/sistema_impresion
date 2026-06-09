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
    print("\n=== DASHBOARD GENERAL ===")
    print("Dashboard funcionando.")


def ver_entregas_proximas():
    print("\n=== ENTREGAS PRÓXIMAS ===")
    print("Módulo funcionando.")


def ver_pagos_pendientes():
    print("\n=== PAGOS PENDIENTES ===")
    print("Módulo funcionando.")