from app.database.conexion import obtener_conexion


def obtener_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM clientes
        WHERE activo = 1
    """)

    clientes = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()

    return clientes