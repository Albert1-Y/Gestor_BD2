import sys
from PyQt6.QtWidgets import QApplication
from disco.disco import DISCOLBA
from interfaz.visualizador_disco import DiscoInterfaz
from util.helpers import insertar_registro

class DISCOLBA_Mod(DISCOLBA):
    def __init__(self, *args, nombres_campos=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombres_campos = nombres_campos or []


def cargar_registros_desde_archivo(ruta_archivo, platos=2, pistas=2, sectores=5, tamano_sector=18):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    if not lineas:
        raise ValueError("El archivo está vacío.")

    # nombres de campos de la primera linea
    nombres_campos = [campo.strip() for campo in lineas[0].strip().split(",")]

    # Crear el disco con los nombres
    disco = DISCOLBA_Mod(platos=platos, pistas=pistas, sectores=sectores,
                         tamano_sector=tamano_sector, nombres_campos=nombres_campos)

    # Insertar registros a partir de las siguientes líneas
    for linea in lineas[1:]:
        valores = [valor.strip() for valor in linea.strip().split(",")]
        if len(valores) != len(nombres_campos):
            print(f"Saltando registro inválido: {linea}")
            continue
        id_registro = valores[0]
        insertar_registro(disco, id_registro, valores)

    return disco

def main():
    app = QApplication(sys.argv)
    ruta = "registros.txt"

    disco = cargar_registros_desde_archivo(ruta)

    ventana = DiscoInterfaz(disco)
    ventana.resize(1200, 800)
    ventana.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()