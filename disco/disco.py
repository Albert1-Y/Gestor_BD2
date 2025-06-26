from .sector import Sector

class DISCOLBA:
    def __init__(self, platos=2, pistas=10, sectores=100, tamano_sector=10, nombres_campos=None):
        self.platos = platos
        self.superficies_por_plato = 2
        self.pistas = pistas
        self.sectores_por_pista = sectores
        self.tamano_sector = tamano_sector

        self.sectores_por_superficie = self.pistas * self.sectores_por_pista
        self.sectores_por_plato = self.superficies_por_plato * self.sectores_por_superficie
        self.total_sectores = self.platos * self.sectores_por_plato

        self.sectores = [Sector(tamano_sector) for _ in range(self.total_sectores)]
        self.indice_registros = {}  
        self.nombres_campos = nombres_campos or []

    def _lba_a_pps(self, lba_index):
        plato = lba_index // self.sectores_por_plato
        resto_plato = lba_index % self.sectores_por_plato
        superficie = resto_plato // self.sectores_por_superficie
        resto_superficie = resto_plato % self.sectores_por_superficie
        pista = resto_superficie // self.sectores_por_pista
        sector = resto_superficie % self.sectores_por_pista
        return plato, superficie, pista, sector

    def _pps_a_lba(self, plato, superficie, pista, sector):
        return (plato * self.sectores_por_plato
                + superficie * self.sectores_por_superficie
                + pista * self.sectores_por_pista
                + sector)

    def guardar_registro(self, id_registro, campos):
        fragmentos = []
        campos_guardados = []

        for tipo, valor in campos:
            for lba, sector in enumerate(self.sectores):
                resultado = sector.agregar_campo(tipo, valor)
                if resultado:
                    inicio, fin = resultado
                    p, s, pi, se = self._lba_a_pps(lba)
                    fragmentos.append([p, s, pi, se, inicio, fin])
                    campos_guardados.append((tipo, valor))
                    break
            else:
                raise MemoryError("No hay espacio suficiente en disco.")

        self.indice_registros[id_registro] = {
            "campos": campos_guardados,
            "fragmentos": fragmentos
        }

        return True, fragmentos

    def mostrar_sector(self, lba_index):
        if 0 <= lba_index < self.total_sectores:
            p, s, pi, se = self._lba_a_pps(lba_index)
            cabecera = f"Sector {lba_index} → Plato {p}, Superficie {s}, Pista {pi}, Sector {se}"
            contenido = str(self.sectores[lba_index])
            return f"{cabecera}\n{contenido}"
        return "Índice fuera de rango"

    def recuperar_registro(self, id_registro):
        if id_registro not in self.indice_registros:
            return None
        return self.indice_registros[id_registro]["campos"]
