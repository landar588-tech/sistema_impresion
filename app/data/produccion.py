from app.database.conexion import obtener_conexion


def _fila_a_diccionario(fila):
    return {
        "id_produccion": fila[0],
        "id_orden": fila[1],
        "fecha_inicio": fila[2],
        "nombre_cliente": fila[3],
        "producto_material": fila[4],
        "cantidad": fila[5],
        "estado_produccion": fila[6],
        "fecha_finalizacion": fila[7],
        "responsable": fila[8],
        "observaciones": fila[9],
        "activo": bool(fila[10]),
    }


def cargar_produccion():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_produccion, id_orden, fecha_inicio,
               nombre_cliente, producto_material, cantidad,
               estado_produccion, fecha_finalizacion,
               responsable, observaciones, activo
        FROM produccion
    """)

    registros = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()

    return registros


def generar_id_produccion():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT MAX(id_produccion) FROM produccion")
    ultimo_id = cursor.fetchone()[0]

    conexion.close()

    return 1 if ultimo_id is None else ultimo_id + 1


def agregar_registro_produccion(registro):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO produccion (
            id_produccion, id_orden, fecha_inicio,
            nombre_cliente, producto_material, cantidad,
            estado_produccion, fecha_finalizacion,
            responsable, observaciones, activo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        registro.get("id_produccion"),
        registro.get("id_orden"),
        registro.get("fecha_inicio"),
        registro.get("nombre_cliente"),
        registro.get("producto_material"),
        registro.get("cantidad"),
        registro.get("estado_produccion", "En proceso"),
        registro.get("fecha_finalizacion"),
        registro.get("responsable"),
        registro.get("observaciones", ""),
        1 if registro.get("activo", True) else 0,
    ))

    conexion.commit()
    conexion.close()


def obtener_produccion_por_orden(id_orden):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_produccion, id_orden, fecha_inicio,
               nombre_cliente, producto_material, cantidad,
               estado_produccion, fecha_finalizacion,
               responsable, observaciones, activo
        FROM produccion
        WHERE id_orden = ?
        AND activo = 1
    """, (id_orden,))

    fila = cursor.fetchone()
    conexion.close()

    return _fila_a_diccionario(fila) if fila else None


def obtener_produccion_por_id(id_produccion):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_produccion, id_orden, fecha_inicio,
               nombre_cliente, producto_material, cantidad,
               estado_produccion, fecha_finalizacion,
               responsable, observaciones, activo
        FROM produccion
        WHERE id_produccion = ?
    """, (id_produccion,))

    fila = cursor.fetchone()
    conexion.close()

    return _fila_a_diccionario(fila) if fila else None


def actualizar_produccion(id_produccion, datos_actualizados):
    if not datos_actualizados:
        return False

    campos = []
    valores = []

    for campo, valor in datos_actualizados.items():
        campos.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(id_produccion)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(f"""
        UPDATE produccion
        SET {", ".join(campos)}
        WHERE id_produccion = ?
    """, valores)

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado


def listar_produccion_activa_data():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_produccion, id_orden, fecha_inicio,
               nombre_cliente, producto_material, cantidad,
               estado_produccion, fecha_finalizacion,
               responsable, observaciones, activo
        FROM produccion
        WHERE activo = 1
    """)

    registros = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()

    return registros


def cancelar_produccion_data(id_produccion):
    return actualizar_produccion(
        id_produccion,
        {
            "estado_produccion": "Cancelado",
            "activo": 0
        }
    )