from datetime import datetime
from app.data.clientes import (
    cargar_clientes,
    agregar_cliente,
    generar_id_cliente,
    buscar_clientes,
    obtener_cliente_por_id,
    actualizar_cliente,
    desactivar_cliente,
)


def crear_cliente():
    print("\n--- Registrar Cliente ---")
    nombre = input("Nombre del cliente: ").strip()
    if not nombre:
        print("❌ Error: El nombre es obligatorio.")
        return

    telefono = input("Teléfono: ").strip()
    if not telefono:
        print("❌ Error: El teléfono es obligatorio.")
        return

    empresa = input("Empresa (opcional): ").strip()
    correo = input("Correo (opcional): ").strip()
    direccion = input("Dirección (opcional): ").strip()
    observaciones = input("Observaciones (opcional): ").strip()

    cliente = {
        "id_cliente": generar_id_cliente(),
        "nombre": nombre,
        "empresa": empresa,
        "telefono": telefono,
        "correo": correo,
        "direccion": direccion,
        "fecha_alta": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "observaciones": observaciones,
        "activo": True,
    }

    agregar_cliente(cliente)
    print("✅ Cliente registrado correctamente.")


def listar_clientes():
    print("\n--- Lista de Clientes Activos ---")
    clientes = cargar_clientes()
    activos = [c for c in clientes if c.get("activo", True)]

    if not activos:
        print("No hay clientes activos registrados.")
        return

    for c in activos:
        print(f"[{c['id_cliente']}] {c['nombre']} - {c['telefono']} - {c['empresa']}")


def buscar_cliente():
    print("\n--- Buscar Cliente ---")
    texto = input("Buscar por nombre, empresa o teléfono: ").strip()
    resultados = buscar_clientes(texto)

    if not resultados:
        print("No se encontraron coincidencias.")
        return

    for c in resultados:
        print(f"[{c['id_cliente']}] {c['nombre']} - {c['telefono']} - Activo")


def editar_cliente():
    print("\n--- Editar Cliente ---")
    try:
        id_cliente = int(input("ID del cliente: "))
    except ValueError:
        print("ID inválido.")
        return

    cliente = obtener_cliente_por_id(id_cliente)
    if not cliente or not cliente.get("activo", True):
        print("Cliente no encontrado o inactivo.")
        return

    print("Dejar vacío para mantener el valor actual.")

    nombre = input(f"Nombre ({cliente['nombre']}): ").strip()
    telefono = input(f"Teléfono ({cliente['telefono']}): ").strip()
    empresa = input(f"Empresa ({cliente['empresa']}): ").strip()
    correo = input(f"Correo ({cliente['correo']}): ").strip()
    direccion = input(f"Dirección ({cliente['direccion']}): ").strip()
    observaciones = input(f"Observaciones ({cliente['observaciones']}): ").strip()

    datos = {}
    if nombre:
        datos["nombre"] = nombre
    if telefono:
        datos["telefono"] = telefono
    if empresa:
        datos["empresa"] = empresa
    if correo:
        datos["correo"] = correo
    if direccion:
        datos["direccion"] = direccion
    if observaciones:
        datos["observaciones"] = observaciones

    if actualizar_cliente(id_cliente, datos):
        print("✅ Cliente actualizado correctamente.")
    else:
        print("No se pudo actualizar.")


def eliminar_cliente_logico():
    print("\n--- Desactivar Cliente ---")
    try:
        id_cliente = int(input("ID del cliente: "))
    except ValueError:
        print("ID inválido.")
        return

    if desactivar_cliente(id_cliente):
        print("✅ Cliente desactivado correctamente.")
    else:
        print("Cliente no encontrado.")