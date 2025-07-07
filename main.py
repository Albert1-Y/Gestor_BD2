import sys
import csv
import os
from PyQt6.QtWidgets import QApplication, QDialog, QLabel, QVBoxLayout
from PyQt6.QtCore import Qt, QUrl
from disco.disco import DISCOLBA
from interfaz.visualizador_disco import DiscoInterfaz
from util.helpers import insertar_registro
from util.configuracion import ConfigDialog

class DISCOLBA_Mod(DISCOLBA):
    def __init__(self, *args, nombres_campos=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.nombres_campos = nombres_campos or []

def extraer_nombres_campos_desde_txt(ruta_txt):
    with open(ruta_txt, "r", encoding="utf-8") as archivo:
        lineas = archivo.readlines()

    campos = []
    for linea in lineas:
        linea = linea.strip().rstrip(",")
        if "(" in linea or ")" in linea or linea.upper().startswith("CREATE TABLE"):
            continue
        if not linea:
            continue
        nombre_campo = linea.split()[0]
        campos.append(nombre_campo)
    return campos

def cargar_disco_desde_archivo(config, ruta_archivo, nombres_campos):
    with open(ruta_archivo, mode="r", encoding="utf-8") as archivo:
        lector = csv.reader(archivo, quotechar='"', skipinitialspace=True)
        filas = [fila for fila in lector if any(campo.strip() for campo in fila)]

    if not filas:
        raise ValueError("El archivo está vacío.")

    if not nombres_campos:
        nombres_campos = [campo.strip() for campo in filas[0]]
        registros = filas[1:]
    else:
        registros = filas

    disco = DISCOLBA_Mod(
        platos=config["platos"],
        pistas=config["pistas"],
        sectores=config["sectores"],
        tamano_sector=config["tamano"],
        nombres_campos=nombres_campos
    )

    for fila in registros:
        valores = [valor.strip() for valor in fila]
        if len(valores) != len(nombres_campos):
            print(f"Saltando registro inválido: {fila}")
            continue
        id_registro = valores[0]
        insertar_registro(disco, id_registro, valores)

    return disco

class VentanaArrastrable(QDialog):
    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)
        self.setWindowTitle("Arrastra aquí tu archivo CSV o TXT")
        layout = QVBoxLayout()
        self.label = QLabel("📂 Arrastra un archivo CSV o TXT aquí")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.label)
        self.setLayout(layout)
        
        self.nombres_campos_temp = None
        self.config_temp = None
        self.interfaz_disco = None

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        urls = event.mimeData().urls()
        if not urls:
            return

        archivo_path = urls[0].toLocalFile()
        extension = os.path.splitext(archivo_path)[1].lower()

        if not self.config_temp:
            dialogo = ConfigDialog()
            if dialogo.exec() != QDialog.DialogCode.Accepted:
                self.label.setText("Configuración cancelada.")
                return
            self.config_temp = dialogo.get_valores()

        if extension == ".txt":
            self.nombres_campos_temp = extraer_nombres_campos_desde_txt(archivo_path)
            self.label.setText(f"Estructura leída.\nAhora arrastra el archivo CSV con registros.")
            return

        elif extension == ".csv":
            if self.nombres_campos_temp:
                disco = cargar_disco_desde_archivo(self.config_temp, archivo_path, self.nombres_campos_temp)
            else:
                disco = cargar_disco_desde_archivo(self.config_temp, archivo_path, nombres_campos=[])
        else:
            self.label.setText("Formato de archivo no soportado.")
            return

        self.hide()
        self.interfaz_disco = DiscoInterfaz(disco)
        self.interfaz_disco.resize(1200, 800)
        self.interfaz_disco.show()


def main():
    app = QApplication(sys.argv)
    ventana = VentanaArrastrable()
    ventana.resize(500, 300)
    ventana.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
