from app.database.conexion import obtener_conexion


def _fila_a_diccionario(fila):
    return {
        "id_cotizacion": fila[0],
        "fecha": fila[1],
        "id_cliente": fila[2],
        "nombre_cliente": fila[3],
        "producto_material": fila[4],
        "cantidad": fila[5],
        "descripcion": fila[6],
        "cliente_trae_diseno": bool(fila[7]),
        "costo_diseno": fila[8],
        "costo_produccion": fila[9],
        "total": fila[10],
        "anticipo_50": fila[11],
        "saldo_pendiente": fila[12],
        "dias_entrega_estimados": fila[13],
        "estado": fila[14],
        "observaciones": fila[15],
        "activo": bool(fila[16]),
    }


def cargar_cotizaciones():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_cotizacion, fecha, id_cliente, nombre_cliente,
               producto_material, cantidad, descripcion,
               cliente_trae_diseno, costo_diseno, costo_produccion,
               total, anticipo_50, saldo_pendiente,
               dias_entrega_estimados, estado, observaciones, activo
        FROM cotizaciones
    """)

    cotizaciones = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()
    return cotizaciones


def generar_id_cotizacion():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT MAX(id_cotizacion) FROM cotizaciones")
    ultimo_id = cursor.fetchone()[0]

    conexion.close()
    return 1 if ultimo_id is None else ultimo_id + 1


def agregar_cotizacion(cotizacion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO cotizaciones (
            id_cotizacion, fecha, id_cliente, nombre_cliente,
            producto_material, cantidad, descripcion,
            cliente_trae_diseno, costo_diseno, costo_produccion,
            total, anticipo_50, saldo_pendiente,
            dias_entrega_estimados, estado, observaciones, activo
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
        cotizacion.get("estado", "Pendiente"),
        cotizacion.get("observaciones", ""),
        1 if cotizacion.get("activo", True) else 0,
    ))

    conexion.commit()
    conexion.close()


def obtener_cotizacion_por_id(id_cotizacion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_cotizacion, fecha, id_cliente, nombre_cliente,
               producto_material, cantidad, descripcion,
               cliente_trae_diseno, costo_diseno, costo_produccion,
               total, anticipo_50, saldo_pendiente,
               dias_entrega_estimados, estado, observaciones, activo
        FROM cotizaciones
        WHERE id_cotizacion = ?
    """, (id_cotizacion,))

    fila = cursor.fetchone()
    conexion.close()

    return _fila_a_diccionario(fila) if fila else None


def buscar_cotizaciones(texto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    texto = f"%{texto.lower()}%"

    cursor.execute("""
        SELECT id_cotizacion, fecha, id_cliente, nombre_cliente,
               producto_material, cantidad, descripcion,
               cliente_trae_diseno, costo_diseno, costo_produccion,
               total, anticipo_50, saldo_pendiente,
               dias_entrega_estimados, estado, observaciones, activo
        FROM cotizaciones
        WHERE activo = 1
        AND (
            CAST(id_cotizacion AS TEXT) LIKE ?
            OR LOWER(nombre_cliente) LIKE ?
            OR LOWER(producto_material) LIKE ?
        )
    """, (texto, texto, texto))

    cotizaciones = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()
    return cotizaciones


def cancelar_cotizacion(id_cotizacion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE cotizaciones
        SET estado = 'Cancelada',
            activo = 0
        WHERE id_cotizacion = ?
    """, (id_cotizacion,))

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado