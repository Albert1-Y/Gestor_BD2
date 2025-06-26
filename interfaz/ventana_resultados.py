from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView
from PyQt6.QtGui import QColor, QPalette
from PyQt6.QtCore import Qt

class TablaDialog(QDialog):
    def __init__(self, datos, nombres_campos):
        super().__init__()
        self.setWindowTitle("Resultados de cosulta")
        self.setStyleSheet("background-color: #2E2E2E; color: white;")

        if not datos or not isinstance(datos[0], list):
            raise ValueError("no hay nada en al lista")

        self.tabla = QTableWidget()
        self.tabla.setRowCount(len(datos))
        self.tabla.setColumnCount(len(datos[0]))

        #self.tabla.setHorizontalHeaderLabels([f"Columna {i+1}" for i in range(len(datos[0]))])

        self.tabla.setHorizontalHeaderLabels(nombres_campos)

        for i, fila in enumerate(datos):
            for j, valor in enumerate(fila):
                item = QTableWidgetItem(str(valor))
                item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)  
                self.tabla.setItem(i, j, item)

        self.tabla.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.tabla.horizontalHeader().setStyleSheet("QHeaderView::section { background-color: #3E3E3E; border: 1px solid #555; }")

        self.tabla.setStyleSheet("QTableWidget { background-color: #2E2E2E; } QTableWidget::item { border: 1px solid #555; padding: 5px; }")

        self.cerrar_btn = QPushButton("Cerrar")
        self.cerrar_btn.setStyleSheet("background-color: #4CAF50; color: white; border-radius: 5px; padding: 10px; font-size: 14px;")
        self.cerrar_btn.clicked.connect(self.accept)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.cerrar_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.tabla)
        layout.addLayout(botones_layout)

        self.setLayout(layout)
        self.setFixedSize(600, 400)  