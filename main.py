# Menú principal.

# Pruebas y control de flujo (insertar, leer, mostrar estado).

from disco.disco import Disco
from registros.manejador_registros import ManejadorRegistros
from memoria.arbol_avl import BinaryTree

def main():
    # Crear disco
    disco = Disco(num_platos=2, num_superficies=2, num_pistas=3, num_sectores=4)

    # Crear AVL para memoria interna
    memoria = BinaryTree()

    # Manejador de registros
    manejador = ManejadorRegistros(disco, memoria)

    # Aquí podrías construir un menú o pruebas simples
    print("Simulador de Base de Datos iniciado.")

if __name__ == "__main__":
    main()
