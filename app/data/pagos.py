from app.database.conexion import obtener_conexion


def _fila_a_diccionario(fila):
    return {
        "id_pago": fila[0],
        "id_orden": fila[1],
        "monto": fila[2],
        "metodo_pago": fila[3],
        "fecha_pago": fila[4],
        "estado_pago": fila[5],
        "activo": bool(fila[6]),
    }


def cargar_pagos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_pago, id_orden, monto, metodo_pago,
               fecha_pago, estado_pago, activo
        FROM pagos
    """)

    pagos = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()

    return pagos


def generar_id_pago():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT MAX(id_pago) FROM pagos")
    ultimo_id = cursor.fetchone()[0]

    conexion.close()

    return 1 if ultimo_id is None else ultimo_id + 1


def crear_pago(id_orden, monto, metodo_pago, fecha_pago, estado_pago="Pagado"):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    id_pago = generar_id_pago()

    cursor.execute("""
        INSERT INTO pagos (
            id_pago, id_orden, monto, metodo_pago,
            fecha_pago, estado_pago, activo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        id_pago,
        id_orden,
        monto,
        metodo_pago,
        fecha_pago,
        estado_pago,
        1
    ))

    conexion.commit()
    conexion.close()

    return {
        "id_pago": id_pago,
        "id_orden": id_orden,
        "monto": monto,
        "metodo_pago": metodo_pago,
        "fecha_pago": fecha_pago,
        "estado_pago": estado_pago,
        "activo": True,
    }


def listar_pagos():
    return cargar_pagos()


def listar_pagos_activos():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_pago, id_orden, monto, metodo_pago,
               fecha_pago, estado_pago, activo
        FROM pagos
        WHERE activo = 1
    """)

    pagos = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()

    return pagos


def obtener_pago_por_id(id_pago):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_pago, id_orden, monto, metodo_pago,
               fecha_pago, estado_pago, activo
        FROM pagos
        WHERE id_pago = ?
    """, (id_pago,))

    fila = cursor.fetchone()
    conexion.close()

    return _fila_a_diccionario(fila) if fila else None


def obtener_pagos_por_orden(id_orden):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_pago, id_orden, monto, metodo_pago,
               fecha_pago, estado_pago, activo
        FROM pagos
        WHERE id_orden = ?
    """, (id_orden,))

    pagos = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()

    return pagos


def actualizar_pago(id_pago, datos_actualizados):
    if not datos_actualizados:
        return False

    campos = []
    valores = []

    for campo, valor in datos_actualizados.items():
        campos.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(id_pago)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(f"""
        UPDATE pagos
        SET {", ".join(campos)}
        WHERE id_pago = ?
    """, valores)

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado


def cancelar_pago(id_pago):
    return actualizar_pago(
        id_pago,
        {
            "estado_pago": "Cancelado",
            "activo": 0
        }
    )