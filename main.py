import sys
import os
import csv
from PyQt6.QtWidgets import QApplication, QDialog
from disco.disco import DISCOLBA
from interfaz.visualizador_disco import DiscoInterfaz
from util.helpers import insertar_registro
from util.configuracion import ConfigDialog

def extraer_nombres_campos(ruta_archivo):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    campos = []
    for linea in lineas:
        linea = linea.strip().rstrip(",")
        if "(" in linea or ")" in linea or linea.upper().startswith("CREATE TABLE"):
            continue
        nombre_campo = linea.split()[0]
        campos.append(nombre_campo)
    return campos

class DISCOLBA_Mod(DISCOLBA):
    def __init__(self, *args, nombres_campos=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombres_campos = nombres_campos or []

def cargar_registros_desde_csv(ruta_archivo):
    dialogo = ConfigDialog()

    if dialogo.exec() == QDialog.DialogCode.Accepted:
        config = dialogo.get_valores()

        platos = config["platos"]
        pistas = config["pistas"]
        sectores = config["sectores"]
        tamano_sector = config["tamano"]

        with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            filas = list(lector)

        if not filas:
            raise ValueError("El archivo CSV está vacío.")

        nombres_campos = [campo.strip() for campo in filas[0]]

        disco = DISCOLBA_Mod(
            platos=platos,
            pistas=pistas,
            sectores=sectores,
            tamano_sector=tamano_sector,
            nombres_campos=nombres_campos
        )

        for fila in filas[1:]:
            valores = [valor.strip() for valor in fila]
            if len(valores) != len(nombres_campos):
                print(f"Saltando registro inválido: {fila}")
                continue
            id_registro = valores[0]
            insertar_registro(disco, id_registro, valores)

        return disco
    else:
        print("Configuración no confirmada por el usuario.")
        return None

class DISCOLBA_Mod(DISCOLBA):
    def __init__(self, *args, nombres_campos=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombres_campos = nombres_campos or []


def cargar_registros_desde_archivo(ruta_archivo, platos=2, pistas=2, sectores=5, tamano_sector=18):
    with open(ruta_archivo, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    if not lineas:
        raise ValueError("El archivo está vacío.")

    nombres_campos = [campo.strip() for campo in lineas[0].strip().split(",")]

    disco = DISCOLBA_Mod(platos=platos, pistas=pistas, sectores=sectores,
                         tamano_sector=tamano_sector, nombres_campos=nombres_campos)

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
    ruta = "producto.csv"

    disco = cargar_registros_desde_csv(ruta)

    if disco:
        ventana = DiscoInterfaz(disco)
        ventana.resize(1200, 800)
        ventana.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()
