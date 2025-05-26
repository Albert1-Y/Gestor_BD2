class Registro:
    def __init__(self, id, nombre, edad):
        self.id = id
        self.nombre = nombre
        self.edad = edad
        self.ubicaciones = []  # [(plato, superficie, pista, sector)]

    def serializar(self):
        return f"{self.id}|{self.nombre}|{self.edad}"
