from app.database.conexion import obtener_conexion


def obtener_cotizaciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT *
        FROM cotizaciones
        WHERE activo = 1
    """)

    cotizaciones = [dict(fila) for fila in cursor.fetchall()]

    conexion.close()

    return cotizaciones