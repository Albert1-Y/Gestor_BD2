from .plato import Plato

class Disco:
    def __init__(self, num_platos, num_superficies, num_pistas, num_sectores):
        self.platos = [
            Plato(num_superficies, num_pistas, num_sectores)
            for _ in range(num_platos)
        ]

    def buscar_sectores_libres(self, cantidad_necesaria):
        # Buscar sectores libres en todo el disco (sin importar contiguidad)
        ubicaciones = []
        for i, plato in enumerate(self.platos):
            for j, superficie in enumerate(plato.superficies):
                for k, pista in enumerate(superficie.pistas):
                    for l, sector in enumerate(pista.sectores):
                        if not sector.ocupado:
                            ubicaciones.append((i, j, k, l))
                            if len(ubicaciones) == cantidad_necesaria:
                                return ubicaciones
        return None  # No hay suficientes

    def asignar_registro(self, ubicaciones, id_registro, partes):
        for (i, j, k, l), parte in zip(ubicaciones, partes):
            sector = self.platos[i].superficies[j].pistas[k].sectores[l]
            sector.ocupado = True
            sector.id_registro = id_registro
            sector.contenido = parte
