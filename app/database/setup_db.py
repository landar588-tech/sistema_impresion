from app.database.conexion import obtener_conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id_cliente INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL,
            empresa TEXT,
            telefono TEXT,
            correo TEXT,
            direccion TEXT,
            fecha_alta TEXT,
            observaciones TEXT,
            activo INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS cotizaciones (
            id_cotizacion INTEGER PRIMARY KEY,
            fecha TEXT,
            id_cliente INTEGER,
            nombre_cliente TEXT,
            producto_material TEXT,
            cantidad TEXT,
            descripcion TEXT,
            cliente_trae_diseno INTEGER,
            costo_diseno REAL DEFAULT 0,
            costo_produccion REAL DEFAULT 0,
            total REAL DEFAULT 0,
            anticipo_50 REAL DEFAULT 0,
            saldo_pendiente REAL DEFAULT 0,
            dias_entrega_estimados INTEGER,
            estado TEXT,
            observaciones TEXT,
            activo INTEGER DEFAULT 1
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ordenes (
        id_orden INTEGER PRIMARY KEY,
        id_cotizacion INTEGER,
        fecha_creacion TEXT,
        id_cliente INTEGER,
        nombre_cliente TEXT,
        producto_material TEXT,
        cantidad TEXT,
        descripcion TEXT,
        cliente_trae_diseno INTEGER,
        requiere_diseno INTEGER,
        costo_diseno REAL DEFAULT 0,
        costo_produccion REAL DEFAULT 0,
        total REAL DEFAULT 0,
        anticipo_requerido REAL DEFAULT 0,
        anticipo_pagado REAL DEFAULT 0,
        saldo_pendiente REAL DEFAULT 0,
        dias_entrega_estimados INTEGER,
        fecha_estimada_entrega TEXT,
        estado TEXT,
        observaciones TEXT,
        activo INTEGER DEFAULT 1
    )
""")

    conexion.commit()
    conexion.close()

    print("Base de datos y tablas creadas correctamente.")


if __name__ == "__main__":
    crear_tablas()