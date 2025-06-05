import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QLineEdit,
    QPushButton, QLabel, QMessageBox, QGraphicsScene, QGraphicsView,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPixmapItem
)
from PyQt6.QtGui import QColor, QBrush, QPen, QPixmap
from PyQt6.QtCore import Qt

class DiscoInterfaz(QWidget):
    def __init__(self, disco):
        super().__init__()
        self.disco = disco

        self.setWindowTitle("Visualizador Disco BD con Búsqueda")

        # Tomar dinámicamente parámetros desde disco
        self.num_platos = self.disco.platos
        self.superficies_por_plato = self.disco.superficies_por_plato
        self.max_pistas_por_sup = self.disco.pistas
        self.sectores_por_pista = self.disco.sectores_por_pista

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

        # Selectores basados en disco
        self.plato_combo = QComboBox()
        self.plato_combo.addItems([f"Plato {i}" for i in range(self.num_platos)])
        self.superficie_combo = QComboBox()
        self.superficie_combo.addItems([f"Sup {i}" for i in range(self.superficies_por_plato)])
        self.pista_selector = QSpinBox()
        self.pista_selector.setRange(0, self.max_pistas_por_sup - 1)
        self.pistas_a_mostrar = QSpinBox()
        self.pistas_a_mostrar.setRange(1, self.max_pistas_por_sup)
        self.pistas_a_mostrar.setValue(min(3, self.max_pistas_por_sup))

        self.boton_mostrar = QPushButton("Mostrar Diagrama")
        self.boton_mostrar.clicked.connect(self.mostrar_diagrama)

        self.input_busqueda = QLineEdit()
        self.input_busqueda.setPlaceholderText("ID del registro")
        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_registro)

        top_layout.addWidget(QLabel("Plato:"))
        top_layout.addWidget(self.plato_combo)
        top_layout.addWidget(QLabel("Superficie:"))
        top_layout.addWidget(self.superficie_combo)
        top_layout.addWidget(QLabel("Desde pista:"))
        top_layout.addWidget(self.pista_selector)
        top_layout.addWidget(QLabel("Cantidad:"))
        top_layout.addWidget(self.pistas_a_mostrar)
        top_layout.addWidget(self.boton_mostrar)
        top_layout.addWidget(QLabel("Buscar ID:"))
        top_layout.addWidget(self.input_busqueda)
        top_layout.addWidget(self.boton_buscar)

        layout.addLayout(top_layout)
        layout.addWidget(self.view)
        self.setLayout(layout)

        self.registro_encontrado = None

        self.mostrar_diagrama()

    def mostrar_diagrama(self):
        self.scene.clear()
        plato = self.plato_combo.currentIndex()
        superficie = self.superficie_combo.currentIndex()
        pista_ini = self.pista_selector.value()
        num_pistas = self.pistas_a_mostrar.value()
        pista_fin = min(pista_ini + num_pistas, self.max_pistas_por_sup)

        cx, cy = 100, 200
        spacing_y = 100

        # Ruta absoluta a la imagen plato_cd.png en la carpeta actual del archivo
        ruta_imagen = os.path.join(os.path.dirname(__file__), "plato_cd.png")
        pixmap = QPixmap(ruta_imagen)
        if not pixmap.isNull():
            img_item = QGraphicsPixmapItem(pixmap)
            img_item.setOffset(cx - pixmap.width() / 2, cy - pixmap.height() / 2)
            self.scene.addItem(img_item)

        etiqueta = QGraphicsTextItem(f"Plato {plato}, Sup {superficie}")
        etiqueta.setDefaultTextColor(Qt.GlobalColor.white)
        etiqueta.setPos(cx - 40, cy - pixmap.height() / 2 - 25 if not pixmap.isNull() else cy - 130)
        self.scene.addItem(etiqueta)

        base_x = cx + (pixmap.width() if not pixmap.isNull() else 200) / 2 + 30
        base_y = cy - (num_pistas * spacing_y) / 2

        for i, p in enumerate(range(pista_ini, pista_fin)):
            y = base_y + i * spacing_y
            pista_label = QGraphicsTextItem(f"Pista {p}")
            pista_label.setDefaultTextColor(Qt.GlobalColor.white)
            pista_label.setPos(base_x, y)
            self.scene.addItem(pista_label)

            sectores_por_plato = self.disco.pistas * self.disco.sectores_por_pista * self.disco.superficies_por_plato

            for sec in range(self.sectores_por_pista):
                x_sec = base_x + 80 + sec * 30

                ocupado = False
                color = QColor("lightgreen")

                lba = plato * sectores_por_plato + superficie * (self.disco.pistas * self.disco.sectores_por_pista) + p * self.disco.sectores_por_pista + sec
                sector_obj = self.disco.sectores[lba]

                if sector_obj.ocupado:
                    ocupado = True
                    color = QColor("orange")

                if self.registro_encontrado:
                    for (ubi_lba, _, _) in self.registro_encontrado.get("ubicaciones", []):
                        if ubi_lba == lba:
                            color = QColor("blue")

                rect = QGraphicsRectItem(x_sec, y, 20, 20)
                rect.setBrush(QBrush(color))
                rect.setPen(QPen(Qt.GlobalColor.black))
                rect.setToolTip(f"P:{plato} S:{superficie} Pi:{p} Sec:{sec}")
                self.scene.addItem(rect)

            if i == 0:
                flecha = QGraphicsLineItem(cx + (pixmap.width() if not pixmap.isNull() else 200) / 2, cy, base_x, y)
                flecha.setPen(QPen(Qt.GlobalColor.white, 2))
                self.scene.addItem(flecha)

    def buscar_registro(self):
        reg_id = self.input_busqueda.text().strip()
        if not reg_id:
            QMessageBox.warning(self, "No ID", "Ingrese un ID para buscar.")
            return

        registro = self.disco.obtener_registro_formateado(reg_id)
        if registro is None:
            QMessageBox.warning(self, "No encontrado", f"Registro con ID {reg_id} no existe.")
            self.registro_encontrado = None
        else:
            self.registro_encontrado = registro[reg_id]
            info = f"Registro {reg_id}:\nContenido:\n{self.registro_encontrado['contenido']}\n\nUbicaciones:\n"
            for (lba, ini, fin) in self.registro_encontrado["ubicaciones"]:
                plato, sup, pista, sector = self.disco._lba_a_pps(lba)
                info += f"  Plato {plato}, Superficie {sup}, Pista {pista}, Sector {sector} (bytes {ini}-{fin})\n"

            QMessageBox.information(self, f"Registro {reg_id}", info)

        self.mostrar_diagrama()
