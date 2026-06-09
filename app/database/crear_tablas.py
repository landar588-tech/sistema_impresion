from app.database.conexion import obtener_conexion


def crear_tablas():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produccion (
            id_produccion INTEGER PRIMARY KEY,
            id_orden INTEGER,
            fecha_inicio TEXT,
            nombre_cliente TEXT,
            producto_material TEXT,
            cantidad TEXT,
            estado_produccion TEXT,
            fecha_finalizacion TEXT,
            responsable TEXT,
            observaciones TEXT,
            activo INTEGER DEFAULT 1
        )
    """)

    conexion.commit()
    conexion.close()

    print("Tabla produccion creada correctamente.")


if __name__ == "__main__":
    crear_tablas()