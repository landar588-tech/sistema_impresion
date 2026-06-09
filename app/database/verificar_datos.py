from app.database.conexion import obtener_conexion


def verificar_datos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    tablas = ["clientes", "cotizaciones", "ordenes"]

    for tabla in tablas:
        cursor.execute(f"SELECT COUNT(*) FROM {tabla}")
        cantidad = cursor.fetchone()[0]

        print(f"{tabla}: {cantidad} registros")

    conexion.close()


if __name__ == "__main__":
    verificar_datos()