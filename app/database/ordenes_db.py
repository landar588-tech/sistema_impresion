from app.database.conexion import obtener_conexion


def obtener_ordenes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM ordenes
        WHERE activo = 1
    """)

    ordenes = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()

    return ordenes