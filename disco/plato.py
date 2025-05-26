from .superficie import Superficie

class Plato:
    def __init__(self, num_superficies, num_pistas, num_sectores):
        self.superficies = [Superficie(num_pistas, num_sectores) for _ in range(num_superficies)]
