from app.database.conexion import obtener_conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            activo INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id_cotizacion INTEGER PRIMARY KEY,
            id_cliente INTEGER,
            fecha_creacion TEXT,
            total REAL DEFAULT 0,
            estado TEXT,
            activo INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordenes (
            id_orden INTEGER PRIMARY KEY,
            id_cotizacion INTEGER,
            id_cliente INTEGER,
            nombre_cliente TEXT,
            producto_material TEXT,
            cantidad TEXT,
            descripcion TEXT,
            total REAL DEFAULT 0,
            saldo_pendiente REAL DEFAULT 0,
            fecha_estimada_entrega TEXT,
            estado TEXT,
            activo INTEGER DEFAULT 1
        )
    """)

    conexion.commit()
    conexion.close()

    print("Base de datos y tablas creadas correctamente.")


if __name__ == "__main__":
    crear_tablas()