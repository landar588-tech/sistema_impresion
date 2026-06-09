from app.database.conexion import obtener_conexion


def _fila_a_diccionario(fila):
    return {
        "id_orden": fila[0],
        "id_cotizacion": fila[1],
        "fecha_creacion": fila[2],
        "id_cliente": fila[3],
        "nombre_cliente": fila[4],
        "producto_material": fila[5],
        "cantidad": fila[6],
        "descripcion": fila[7],
        "cliente_trae_diseno": bool(fila[8]),
        "requiere_diseno": bool(fila[9]),
        "costo_diseno": fila[10],
        "costo_produccion": fila[11],
        "total": fila[12],
        "anticipo_requerido": fila[13],
        "anticipo_pagado": fila[14],
        "saldo_pendiente": fila[15],
        "dias_entrega_estimados": fila[16],
        "fecha_estimada_entrega": fila[17],
        "estado": fila[18],
        "observaciones": fila[19],
        "activo": bool(fila[20]),
    }


def cargar_ordenes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_orden, id_cotizacion, fecha_creacion,
               id_cliente, nombre_cliente, producto_material,
               cantidad, descripcion, cliente_trae_diseno,
               requiere_diseno, costo_diseno, costo_produccion,
               total, anticipo_requerido, anticipo_pagado,
               saldo_pendiente, dias_entrega_estimados,
               fecha_estimada_entrega, estado, observaciones,
               activo
        FROM ordenes
    """)

    ordenes = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()

    return ordenes


def generar_id_orden():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT MAX(id_orden) FROM ordenes")
    ultimo_id = cursor.fetchone()[0]

    conexion.close()

    return 1 if ultimo_id is None else ultimo_id + 1


def agregar_orden(orden):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO ordenes (
            id_orden, id_cotizacion, fecha_creacion,
            id_cliente, nombre_cliente, producto_material,
            cantidad, descripcion, cliente_trae_diseno,
            requiere_diseno, costo_diseno, costo_produccion,
            total, anticipo_requerido, anticipo_pagado,
            saldo_pendiente, dias_entrega_estimados,
            fecha_estimada_entrega, estado, observaciones,
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
        orden.get("estado", "Pendiente"),
        orden.get("observaciones", ""),
        1 if orden.get("activo", True) else 0,
    ))

    conexion.commit()
    conexion.close()


def obtener_orden_por_id(id_orden):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_orden, id_cotizacion, fecha_creacion,
               id_cliente, nombre_cliente, producto_material,
               cantidad, descripcion, cliente_trae_diseno,
               requiere_diseno, costo_diseno, costo_produccion,
               total, anticipo_requerido, anticipo_pagado,
               saldo_pendiente, dias_entrega_estimados,
               fecha_estimada_entrega, estado, observaciones,
               activo
        FROM ordenes
        WHERE id_orden = ?
    """, (id_orden,))

    fila = cursor.fetchone()
    conexion.close()

    return _fila_a_diccionario(fila) if fila else None


def actualizar_orden(id_orden, datos_actualizados):
    if not datos_actualizados:
        return False

    campos = []
    valores = []

    for campo, valor in datos_actualizados.items():
        campos.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(id_orden)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(f"""
        UPDATE ordenes
        SET {", ".join(campos)}
        WHERE id_orden = ?
    """, valores)

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado


def cancelar_orden_data(id_orden):
    return actualizar_orden(
        id_orden,
        {
            "estado": "Cancelado",
            "activo": 0
        }
    )