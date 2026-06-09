from app.data.clientes import cargar_clientes
from app.data.cotizaciones import cargar_cotizaciones
from app.data.ordenes import cargar_ordenes
from app.database.conexion import obtener_conexion

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
                id_cotizacion, id_cliente, fecha_creacion, total, estado, activo
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            cotizacion.get("id_cotizacion"),
            cotizacion.get("id_cliente"),
            cotizacion.get("fecha_creacion"),
            cotizacion.get("total", 0),
            cotizacion.get("estado"),
            1 if cotizacion.get("activo", True) else 0
        ))


def migrar_ordenes(cursor):
    for orden in cargar_ordenes():
        cursor.execute("""
            INSERT OR REPLACE INTO ordenes (
                id_orden,
                id_cotizacion,
                id_cliente,
                nombre_cliente,
                producto_material,
                cantidad,
                descripcion,
                total,
                saldo_pendiente,
                fecha_estimada_entrega,
                estado,
                activo
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            orden.get("id_orden"),
            orden.get("id_cotizacion"),
            orden.get("id_cliente"),
            orden.get("nombre_cliente"),
            orden.get("producto_material"),
            orden.get("cantidad"),
            orden.get("descripcion"),
            orden.get("total", 0),
            orden.get("saldo_pendiente", 0),
            orden.get("fecha_estimada_entrega"),
            orden.get("estado"),
            1 if orden.get("activo", True) else 0
        ))


def migrar_json_a_sqlite():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    migrar_clientes(cursor)
    migrar_cotizaciones(cursor)
    migrar_ordenes(cursor)

    conexion.commit()
    conexion.close()

    print("Migración JSON a SQLite completada correctamente.")


if __name__ == "__main__":
    migrar_json_a_sqlite()
