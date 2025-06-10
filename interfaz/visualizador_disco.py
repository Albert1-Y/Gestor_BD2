# Versión extendida de DiscoInterfaz con búsqueda por campo usando AVL dinámico

import os
from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QSpinBox, QLineEdit,
    QPushButton, QLabel, QMessageBox, QGraphicsScene, QGraphicsView,
    QGraphicsRectItem, QGraphicsTextItem, QGraphicsLineItem, QGraphicsPixmapItem
)
from PyQt6.QtGui import QColor, QBrush, QPen, QPixmap
from PyQt6.QtCore import Qt
from memoria.arbol_avl import AVL
from util.helpers import reconstruir_contenido, construir_avl_por_campo

class DiscoInterfaz(QWidget):
    def __init__(self, disco):
        super().__init__()
        self.disco = disco
        self.setWindowTitle("Visualizador Disco BD con Búsqueda")

        self.num_platos = disco.platos
        self.superficies_por_plato = disco.superficies_por_plato
        self.max_pistas_por_sup = disco.pistas
        self.sectores_por_pista = disco.sectores_por_pista

        layout = QVBoxLayout()
        top_layout = QHBoxLayout()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)

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
        self.input_busqueda.setPlaceholderText("Valor a buscar")

        self.boton_buscar = QPushButton("Buscar")
        self.boton_buscar.clicked.connect(self.buscar_registro)

        self.combo_campo = QComboBox()
        self.combo_campo = QComboBox()
        if disco.indice_registros:
            ejemplo_id = next(iter(disco.indice_registros))
            campos = disco.indice_registros[ejemplo_id]["campos"]
            campos_nombres = disco.nombres_campos
            opciones = [
                f"{campos_nombres[i]} ({tipo})" if i < len(campos_nombres) else f"Campo {i} ({tipo})"
                for i, (tipo, _) in enumerate(campos)
            ]
            self.combo_campo.addItems(opciones)
        else:
            self.combo_campo.addItem("Ningún campo disponible")

        top_layout.addWidget(QLabel("Plato:"))
        top_layout.addWidget(self.plato_combo)
        top_layout.addWidget(QLabel("Superficie:"))
        top_layout.addWidget(self.superficie_combo)
        top_layout.addWidget(QLabel("Desde pista:"))
        top_layout.addWidget(self.pista_selector)
        top_layout.addWidget(QLabel("Cantidad:"))
        top_layout.addWidget(self.pistas_a_mostrar)
        top_layout.addWidget(self.boton_mostrar)
        top_layout.addWidget(QLabel("Buscar por:"))
        top_layout.addWidget(self.combo_campo)
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
                lba = plato * sectores_por_plato + superficie * self.disco.pistas * self.disco.sectores_por_pista + p * self.disco.sectores_por_pista + sec
                sector_obj = self.disco.sectores[lba]

                color = QColor("lightgreen")
                if sector_obj.campos:
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
        valor = self.input_busqueda.text().strip()
        if not valor:
            QMessageBox.warning(self, "Entrada vacía", "Ingrese un valor a buscar.")
            return

        campo_idx = self.combo_campo.currentIndex()
        tipos = ['int', 'string', 'int']
        campo_tipo = tipos[campo_idx]

        avl = construir_avl_por_campo(self.disco, campo_tipo, campo_idx)
        resultado = avl.buscar(valor)

        if not resultado:
            QMessageBox.information(self, "No encontrado", f"No se encontró ningún registro con valor '{valor}'.")
            self.registro_encontrado = None
        else:
            contenido = reconstruir_contenido(sorted(resultado["fragmentos"], key=lambda f: (f[0], f[1], f[2], f[3], f[4])), self.disco)
            ubicaciones = []
            for frag in sorted(resultado["fragmentos"], key=lambda f: (f[0], f[1], f[2], f[3], f[4])):
                lba = self.disco._pps_a_lba(*frag[:4])
                ubicaciones.append((lba, frag[4], frag[5]))

            self.registro_encontrado = {
                "contenido": contenido,
                "ubicaciones": ubicaciones
            }

            info = f"Registro {resultado['registro_id']}:\nContenido:\n{contenido}\n\nUbicaciones:\n"
            for (lba, ini, fin) in ubicaciones:
                plato, sup, pista, sector = self.disco._lba_a_pps(lba)
                info += f"  Plato {plato}, Sup {sup}, Pista {pista}, Sector {sector} (bytes {ini}-{fin})\n"

            QMessageBox.information(self, f"Registro {resultado['registro_id']}", info)

        self.mostrar_diagrama()
