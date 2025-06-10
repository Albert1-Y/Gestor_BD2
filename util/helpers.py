<<<<<<< Updated upstream
def imprimir_mapa_disco(disco):
    for i, plato in enumerate(disco.platos):
        for j, superficie in enumerate(plato.superficies):
            for k, pista in enumerate(superficie.pistas):
                estados = []
                for l, sector in enumerate(pista.sectores):
                    if sector.ocupado:
                        estados.append(f"[{sector.id_registro}]")
                    else:
                        estados.append("[ ]")
                print(f"P{i} S{j} PI{k}: {' '.join(estados)}")
=======
def inferir_tipo(valor):
    if isinstance(valor, bool):
        return 'bool'
    if isinstance(valor, int):
        return 'int'
    if isinstance(valor, float):
        return 'float'
    if isinstance(valor, str):
        if valor.lower() in ['true', 'false']:
            return 'bool'
        if valor.isdigit():
            return 'int'
        try:
            float(valor)
            return 'float'
        except ValueError:
            if len(valor) == 1:
                return 'char'
            return 'string'
    raise ValueError(f"No se puede inferir tipo para: {valor}")

def insertar_registro(disco, id_registro, valores):
    campos = [(inferir_tipo(v), str(v)) for v in valores]
    return disco.guardar_registro(id_registro, campos)


def construir_avl_por_campo(disco, campo_tipo, campo_orden):
    from memoria.arbol_avl import AVL
    avl = AVL()
    
    for reg_id, datos in disco.indice_registros.items():
        campos = datos["campos"]
        fragmentos = datos["fragmentos"]
        
        if campo_orden < len(campos):
            tipo, valor = campos[campo_orden]
            
            if tipo == campo_tipo:
                if isinstance(valor, str):
                    if valor.isdigit():  # si la cadena es un numero entero
                        valor = int(valor)
                    else:
                        try:
                            # intentamos convertirlo a float
                            valor = float(valor)
                        except ValueError:
                            pass
                
                elif isinstance(valor, (int, float)):  # numerica
                    pass
                elif isinstance(valor, str):
                    pass
                elif isinstance(valor, datetime):  # Si es fecha
                    try:
                        valor = datetime.strptime(valor, "%Y-%m-%d")  # de string a datetime
                    except ValueError:
                        pass
                else:
                    raise ValueError(f"Tipo de valor no soportado para comparación: {tipo}")
                
                # insertar en el AVL
                avl.insertar(valor, {
                    "registro_id": reg_id,
                    "fragmentos": fragmentos
                })
    return avl


def reconstruir_contenido(fragmentos, disco):
    resultado = []
    for p, s, pi, se, ini, fin in fragmentos:
        lba = disco._pps_a_lba(p, s, pi, se)
        sector = disco.sectores[lba]
        for campo in sector.campos:
            if campo["inicio"] >= ini and campo["fin"] <= fin:
                resultado.append(f"{campo['valor']} ({campo['tipo']})")
    return " | ".join(resultado)
>>>>>>> Stashed changes
