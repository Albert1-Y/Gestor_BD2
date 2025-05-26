from .registro import Registro

class ManejadorRegistros:
    def __init__(self, disco, memoria):
        self.disco = disco
        self.memoria = memoria

    def insertar(self, id, nombre, edad):
        reg = Registro(id, nombre, edad)
        data = reg.serializar()

        # Dividir contenido por tamaño del sector
        sector_size = self.disco.platos[0].superficies[0].pistas[0].sectores[0].capacidad_util
        partes = [data[i:i+sector_size] for i in range(0, len(data), sector_size)]

        ubicaciones = self.disco.buscar_sectores_libres(len(partes))
        if not ubicaciones:
            print("No hay espacio suficiente en el disco.")
            return

        reg.ubicaciones = ubicaciones
        self.disco.asignar_registro(ubicaciones, id, partes)
        self.memoria.insertar(reg)
