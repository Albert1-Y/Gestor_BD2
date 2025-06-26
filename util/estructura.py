import struct

def crear_formato(estructura):
    return ''.join(tipo for _, tipo in estructura)

def empaquetar(estructura, fila):
    valores = []
    for (_, tipo), val in zip(estructura, fila):
        if tipo.endswith('s'):  # string fijo
            tam = int(tipo[:-1])
            valores.append(val.encode('utf-8')[:tam].ljust(tam, b'\x00'))
        elif tipo == 'c':  # char
            valores.append(val.encode('utf-8')[0:1])
        elif tipo == '?':  # bool
            valores.append(bool(val))
        elif tipo == 'i':
            valores.append(int(val))
        elif tipo == 'd':
            valores.append(float(val))
    return struct.pack(crear_formato(estructura), *valores)

def desempaquetar(estructura, data_bytes):
    unpacked = struct.unpack(crear_formato(estructura), data_bytes)
    resultado = []
    for (_, tipo), val in zip(estructura, unpacked):
        if tipo.endswith('s'):
            val = val.decode('utf-8').rstrip('\x00')
        elif tipo == 'c':
            val = val.decode('utf-8')
        resultado.append(val)
    return resultado



import re

def extraer_schema_de_create_table(path_txt):
    with open(path_txt, encoding='utf-8') as archivo:
        contenido = archivo.read()

    # Extraer nombre de la tabla (ignorando CREATE TABLE)
    match_tabla = re.search(r'CREATE TABLE (\w+)', contenido, re.IGNORECASE)
    if not match_tabla:
        raise ValueError("No se pudo encontrar el nombre de la tabla.")
    nombre_tabla = match_tabla.group(1).lower()

    # Extraer columnas (ignorando palabras reservadas como PRIMARY, KEY, etc.)
    columnas = re.findall(r'\s*(\w+)\s+([A-Z]+(?:\(\d+(?:,\s*\d+)?\))?)', contenido, re.IGNORECASE)

    
    # Palabras reservadas que deben ser ignoradas
    palabras_reservadas = {'CREATE', 'TABLE', 'PRIMARY', 'KEY', 'NOT', 'NULL'}
    
    schema = []
    for nombre, tipo_sql in columnas:
        if nombre.upper() in palabras_reservadas:
            continue  # Saltar palabras reservadas
            
        tipo_sql = tipo_sql.upper()
        if tipo_sql.startswith("INTEGER"):
            schema.append((nombre, 'i'))
        elif tipo_sql.startswith("DECIMAL") or tipo_sql.startswith("NUMERIC"):
            schema.append((nombre, 'd'))
        elif tipo_sql.startswith("VARCHAR"):
            longitud = re.search(r'\((\d+)\)', tipo_sql)
            tam = int(longitud.group(1)) if longitud else 20
            schema.append((nombre, f'{tam}s'))
        elif tipo_sql.startswith("BOOLEAN"):
            schema.append((nombre, '?'))
        else:
            schema.append((nombre, '40s'))  # valor por defecto
            
    return nombre_tabla, schema