
class Sector:
    def __init__(self, capacidad_util=512):
        self.capacidad_util = capacidad_util
        # self.gap_inicio = gap_bytes // 2
        # self.gap_fin = gap_bytes // 2
        self.ocupado = False
        self.id_registro = None
        self.contenido = ""

    def espacio_total(self):
        return self.capacidad_util + self.gap_inicio + self.gap_fin
