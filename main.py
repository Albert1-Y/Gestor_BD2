import sys
from PyQt6.QtWidgets import QApplication

from disco.disco import DISCOLBA
from interfaz.visualizador_disco import DiscoInterfaz

def main():
    app = QApplication(sys.argv)

    # Crear disco con parámetros: 3 platos, 10 pistas, 8 sectores por pista, tamaño sector 64 bytes
    disco = DISCOLBA(platos=3, pistas=10, sectores=8, tamano_sector=64)

    # Insertar registros de prueba
    disco.guardar_dato("Este es el registro número 101 almacenado en múltiples sectores.", "101")
    disco.guardar_dato("Otro registro para probar fragmentación y visualización.", "202")
    disco.guardar_dato("Registro corto.", "303")

    # Crear ventana pasando el disco
    ventana = DiscoInterfaz(disco)
    ventana.resize(1200, 800)
    ventana.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
