from .pista import Pista

class Superficie:
    def __init__(self, num_pistas, num_sectores):
        self.pistas = [Pista(num_sectores) for _ in range(num_pistas)]
