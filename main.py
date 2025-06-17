import sys
from PyQt6.QtWidgets import QApplication
from disco.disco import DISCOLBA
from interfaz.visualizador_disco import DiscoInterfaz
from util.helpers import insertar_registro

def main():
    app = QApplication(sys.argv)
    nombres = ["id", "nombre", "edad"]
    disco = DISCOLBA(platos=2, pistas=10, sectores=5, tamano_sector=10, nombres_campos=nombres)

    insertar_registro(disco, "101", ['101', 'Ricardo', 20])
    insertar_registro(disco, "102", ['102', 'Juanito', 30])
    insertar_registro(disco, "103", ['103', 'Alvaro', 21])

    ventana = DiscoInterfaz(disco)
    ventana.resize(1200, 800)
    ventana.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()