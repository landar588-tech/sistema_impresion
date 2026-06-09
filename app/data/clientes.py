from app.database.conexion import obtener_conexion


def _fila_a_diccionario(fila):
    return {
        "id_cliente": fila[0],
        "nombre": fila[1],
        "empresa": fila[2],
        "telefono": fila[3],
        "correo": fila[4],
        "direccion": fila[5],
        "fecha_alta": fila[6],
        "observaciones": fila[7],
        "activo": bool(fila[8]),
    }


def cargar_clientes():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_cliente, nombre, empresa, telefono, correo, direccion,
               fecha_alta, observaciones, activo
        FROM clientes
    """)

    clientes = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()
    return clientes


def generar_id_cliente():
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("SELECT MAX(id_cliente) FROM clientes")
    ultimo_id = cursor.fetchone()[0]

    conexion.close()
    return 1 if ultimo_id is None else ultimo_id + 1


def agregar_cliente(cliente):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        INSERT INTO clientes (
            id_cliente, nombre, empresa, telefono, correo,
            direccion, fecha_alta, observaciones, activo
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        cliente["id_cliente"],
        cliente["nombre"],
        cliente.get("empresa", ""),
        cliente["telefono"],
        cliente.get("correo", ""),
        cliente.get("direccion", ""),
        cliente.get("fecha_alta", ""),
        cliente.get("observaciones", ""),
        1 if cliente.get("activo", True) else 0,
    ))

    conexion.commit()
    conexion.close()


def obtener_cliente_por_id(id_cliente):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        SELECT id_cliente, nombre, empresa, telefono, correo, direccion,
               fecha_alta, observaciones, activo
        FROM clientes
        WHERE id_cliente = ?
    """, (id_cliente,))

    fila = cursor.fetchone()
    conexion.close()

    return _fila_a_diccionario(fila) if fila else None


def buscar_clientes(texto):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    texto = f"%{texto.lower()}%"

    cursor.execute("""
        SELECT id_cliente, nombre, empresa, telefono, correo, direccion,
               fecha_alta, observaciones, activo
        FROM clientes
        WHERE activo = 1
        AND (
            LOWER(nombre) LIKE ?
            OR LOWER(empresa) LIKE ?
            OR LOWER(telefono) LIKE ?
        )
    """, (texto, texto, texto))

    clientes = [_fila_a_diccionario(fila) for fila in cursor.fetchall()]
    conexion.close()
    return clientes


def actualizar_cliente(id_cliente, datos_actualizados):
    if not datos_actualizados:
        return False

    campos = []
    valores = []

    for campo, valor in datos_actualizados.items():
        campos.append(f"{campo} = ?")
        valores.append(valor)

    valores.append(id_cliente)

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute(f"""
        UPDATE clientes
        SET {", ".join(campos)}
        WHERE id_cliente = ?
    """, valores)

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado


def desactivar_cliente(id_cliente):
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    cursor.execute("""
        UPDATE clientes
        SET activo = 0
        WHERE id_cliente = ?
    """, (id_cliente,))

    conexion.commit()
    actualizado = cursor.rowcount > 0
    conexion.close()

    return actualizado