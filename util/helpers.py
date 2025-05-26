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
