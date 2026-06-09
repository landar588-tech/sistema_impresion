from datetime import datetime
from app.data.clientes import cargar_clientes, obtener_cliente_por_id
from app.data.cotizaciones import (
    cargar_cotizaciones,
    agregar_cotizacion,
    generar_id_cotizacion,
    buscar_cotizaciones,
    obtener_cotizacion_por_id,
    cancelar_cotizacion,
)


def crear_cotizacion():
    print("\n--- Crear Cotización ---")

    clientes = [c for c in cargar_clientes() if c.get("activo", True)]

    if not clientes:
        print("❌ No hay clientes activos registrados.")
        return

    print("\nClientes activos:")
    for c in clientes:
        print(f"[{c['id_cliente']}] {c['nombre']} - {c['telefono']}")

    try:
        id_cliente = int(input("\nID del cliente: "))
    except ValueError:
        print("ID inválido.")
        return

    cliente = obtener_cliente_por_id(id_cliente)
    if not cliente or not cliente.get("activo", True):
        print("❌ Cliente no válido o inactivo.")
        return

    producto = input("Producto o material solicitado: ").strip()
    if not producto:
        print("❌ El producto/material es obligatorio.")
        return

    cantidad = input("Cantidad: ").strip()
    if not cantidad:
        print("❌ La cantidad es obligatoria.")
        return

    descripcion = input("Descripción del trabajo: ").strip()

    trae_diseno = input("¿Cliente trae diseño? (s/n): ").strip().lower()
    cliente_trae_diseno = trae_diseno == "s"

    try:
        costo_diseno = 0 if cliente_trae_diseno else float(input("Costo de diseño: "))
        costo_produccion = float(input("Costo de producción: "))
    except ValueError:
        print("❌ Costos inválidos.")
        return

    if costo_diseno < 0 or costo_produccion < 0:
        print("❌ Los costos no pueden ser negativos.")
        return

    total = costo_diseno + costo_produccion
    if total <= 0:
        print("❌ El total debe ser mayor a 0.")
        return

    anticipo = round(total * 0.50, 2)
    saldo = round(total - anticipo, 2)

    try:
        dias_entrega = int(input("Días estimados de entrega: "))
    except ValueError:
        dias_entrega = 3

    observaciones = input("Observaciones (opcional): ").strip()

    cotizacion = {
        "id_cotizacion": generar_id_cotizacion(),
        "fecha": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "id_cliente": cliente["id_cliente"],
        "nombre_cliente": cliente["nombre"],
        "producto_material": producto,
        "cantidad": cantidad,
        "descripcion": descripcion,
        "cliente_trae_diseno": cliente_trae_diseno,
        "costo_diseno": costo_diseno,
        "costo_produccion": costo_produccion,
        "total": total,
        "anticipo_50": anticipo,
        "saldo_pendiente": saldo,
        "dias_entrega_estimados": dias_entrega,
        "estado": "Cotizada",
        "observaciones": observaciones,
        "activo": True,
    }

    agregar_cotizacion(cotizacion)
    print("✅ Cotización creada correctamente.")


def listar_cotizaciones():
    print("\n--- Lista de Cotizaciones Activas ---")
    cotizaciones = [c for c in cargar_cotizaciones() if c.get("activo", True)]

    if not cotizaciones:
        print("No hay cotizaciones activas.")
        return

    for c in cotizaciones:
        print(f"[{c['id_cotizacion']}] {c['nombre_cliente']} - {c['producto_material']} - ${c['total']}")


def buscar_cotizacion():
    print("\n--- Buscar Cotización ---")
    texto = input("Buscar por cliente, producto o ID: ").strip()
    resultados = buscar_cotizaciones(texto)

    if not resultados:
        print("No se encontraron coincidencias.")
        return

    for c in resultados:
        print(f"[{c['id_cotizacion']}] {c['nombre_cliente']} - {c['producto_material']} - ${c['total']}")


def ver_cotizacion():
    print("\n--- Ver Cotización ---")
    try:
        id_cot = int(input("ID de la cotización: "))
    except ValueError:
        print("ID inválido.")
        return

    cot = obtener_cotizacion_por_id(id_cot)
    if not cot or not cot.get("activo", True):
        print("Cotización no encontrada o cancelada.")
        return

    print("\n--- Detalle ---")
    for k, v in cot.items():
        print(f"{k}: {v}")


def cancelar_cotizacion_ui():
    print("\n--- Cancelar Cotización ---")
    try:
        id_cot = int(input("ID de la cotización: "))
    except ValueError:
        print("ID inválido.")
        return

    if cancelar_cotizacion(id_cot):
        print("✅ Cotización cancelada correctamente.")
    else:
        print("No se encontró la cotización.")