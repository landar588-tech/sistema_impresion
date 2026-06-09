from app.data.clientes import cargar_clientes
from app.data.cotizaciones import cargar_cotizaciones
from app.data.ordenes import cargar_ordenes
from app.database.conexion import obtener_conexion
from app.data.diseno import cargar_disenos

def migrar_clientes(cursor):
    for cliente in cargar_clientes():
        cursor.execute("""
            INSERT OR REPLACE INTO clientes (
                id_cliente,
                nombre,
                empresa,
                telefono,
                correo,
                direccion,
                fecha_alta,
                observaciones,
                activo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cliente.get("id_cliente"),
            cliente.get("nombre"),
            cliente.get("empresa"),
            cliente.get("telefono"),
            cliente.get("correo"),
            cliente.get("direccion"),
            cliente.get("fecha_alta"),
            cliente.get("observaciones"),
            1 if cliente.get("activo", True) else 0
        ))

def migrar_cotizaciones(cursor):
    for cotizacion in cargar_cotizaciones():
        cursor.execute("""
            INSERT OR REPLACE INTO cotizaciones (
                id_cotizacion,
                fecha,
                id_cliente,
                nombre_cliente,
                producto_material,
                cantidad,
                descripcion,
                cliente_trae_diseno,
                costo_diseno,
                costo_produccion,
                total,
                anticipo_50,
                saldo_pendiente,
                dias_entrega_estimados,
                estado,
                observaciones,
                activo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            cotizacion.get("id_cotizacion"),
            cotizacion.get("fecha"),
            cotizacion.get("id_cliente"),
            cotizacion.get("nombre_cliente"),
            cotizacion.get("producto_material"),
            cotizacion.get("cantidad"),
            cotizacion.get("descripcion"),
            1 if cotizacion.get("cliente_trae_diseno", False) else 0,
            cotizacion.get("costo_diseno", 0),
            cotizacion.get("costo_produccion", 0),
            cotizacion.get("total", 0),
            cotizacion.get("anticipo_50", 0),
            cotizacion.get("saldo_pendiente", 0),
            cotizacion.get("dias_entrega_estimados"),
            cotizacion.get("estado"),
            cotizacion.get("observaciones"),
            1 if cotizacion.get("activo", True) else 0
        ))


def migrar_ordenes(cursor):
    for orden in cargar_ordenes():
        cursor.execute("""
            INSERT OR REPLACE INTO ordenes (
                id_orden,
                id_cotizacion,
                fecha_creacion,
                id_cliente,
                nombre_cliente,
                producto_material,
                cantidad,
                descripcion,
                cliente_trae_diseno,
                requiere_diseno,
                costo_diseno,
                costo_produccion,
                total,
                anticipo_requerido,
                anticipo_pagado,
                saldo_pendiente,
                dias_entrega_estimados,
                fecha_estimada_entrega,
                estado,
                observaciones,
                activo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            orden.get("id_orden"),
            orden.get("id_cotizacion"),
            orden.get("fecha_creacion"),
            orden.get("id_cliente"),
            orden.get("nombre_cliente"),
            orden.get("producto_material"),
            orden.get("cantidad"),
            orden.get("descripcion"),
            1 if orden.get("cliente_trae_diseno", False) else 0,
            1 if orden.get("requiere_diseno", False) else 0,
            orden.get("costo_diseno", 0),
            orden.get("costo_produccion", 0),
            orden.get("total", 0),
            orden.get("anticipo_requerido", 0),
            orden.get("anticipo_pagado", 0),
            orden.get("saldo_pendiente", 0),
            orden.get("dias_entrega_estimados"),
            orden.get("fecha_estimada_entrega"),
            orden.get("estado"),
            orden.get("observaciones"),
            1 if orden.get("activo", True) else 0
        ))

def migrar_disenos(cursor):
    for diseno in cargar_disenos():
        cursor.execute("""
            INSERT OR REPLACE INTO disenos (
                id_diseno,
                id_orden,
                fecha_creacion,
                nombre_cliente,
                producto_material,
                descripcion,
                estado_diseno,
                fecha_envio_cliente,
                fecha_aprobacion,
                numero_correcciones,
                observaciones,
                activo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            diseno.get("id_diseno"),
            diseno.get("id_orden"),
            diseno.get("fecha_creacion"),
            diseno.get("nombre_cliente"),
            diseno.get("producto_material"),
            diseno.get("descripcion"),
            diseno.get("estado_diseno"),
            diseno.get("fecha_envio_cliente"),
            diseno.get("fecha_aprobacion"),
            diseno.get("numero_correcciones", 0),
            diseno.get("observaciones"),
            1 if diseno.get("activo", True) else 0
        ))

def migrar_json_a_sqlite():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    migrar_clientes(cursor)
    migrar_cotizaciones(cursor)
    migrar_ordenes(cursor)
    migrar_disenos(cursor)

    conexion.commit()
    conexion.close()

    print("Migración JSON a SQLite completada correctamente.")


if __name__ == "__main__":
    migrar_json_a_sqlite()
