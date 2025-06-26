from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QLabel, QHBoxLayout, QPushButton
from PyQt6.QtGui import QIcon
import os
from PyQt6.QtCore import Qt

class VentanaResultados(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Resultados de Búsqueda")
        self.setWindowIcon(QIcon(os.path.join(os.path.dirname(__file__), "plato_cd.png")))
        self.resize(800, 400)
        
        # Layout principal
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)
        
        # Etiqueta de título
        self.titulo_label = QLabel("Resultados de la búsqueda")
        self.titulo_label.setStyleSheet("font-weight: bold; font-size: 14px; color: #4a9ae9;")
        layout.addWidget(self.titulo_label)
        
        # Tabla de resultados
        self.tabla_resultados = QTableWidget()
        self.tabla_resultados.setAlternatingRowColors(True)
        self.tabla_resultados.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.tabla_resultados.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.tabla_resultados.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        # Configurar el header para que se ajuste
        header = self.tabla_resultados.horizontalHeader()
        header.setStretchLastSection(True)
        header.setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        
        layout.addWidget(self.tabla_resultados)
        
        # Botones de control
        botones_layout = QHBoxLayout()
        botones_layout.addStretch()
        
        self.btn_cerrar = QPushButton("Cerrar")
        self.btn_cerrar.clicked.connect(self.close)
        botones_layout.addWidget(self.btn_cerrar)
        
        layout.addLayout(botones_layout)
        
        # Estilos visuales
        self.setStyleSheet("""
            QDialog {
                background-color: #2b2b2b;
                color: #e0e0e0;
            }
            QLabel {
                color: #4a9ae9;
            }
            QTableWidget {
                background-color: #3c3f41;
                gridline-color: #4a6ea9;
                alternate-background-color: #454547;
            }
            QHeaderView::section {
                background-color: #4a6ea9;
                color: white;
                padding: 6px;
                border: 1px solid #4a6ea9;
                font-weight: bold;
            }
            QTableWidget::item {
                padding: 5px;
                border: none;
            }
            QTableWidget::item:selected {
                background-color: #5c80b9;
            }
            QPushButton {
                background-color: #4a6ea9;
                color: white;
                font-weight: bold;
                border: 1px solid #2e4e74;
                border-radius: 4px;
                padding: 8px 16px;
            }
            QPushButton:hover {
                background-color: #5c80b9;
            }
        """)

    def mostrar_resultados(self, registros, columnas, titulo_busqueda=""):
        """Mostrar los resultados en la tabla"""
        if titulo_busqueda:
            self.titulo_label.setText(f"Resultados de búsqueda: {titulo_busqueda}")
        
        print("Estructura de los resultados:", registros)  # Imprime la estructura de los resultados
        
        self.tabla_resultados.setRowCount(0)
        self.tabla_resultados.setColumnCount(len(columnas))
        self.tabla_resultados.setHorizontalHeaderLabels(columnas)
        
        for item in registros:
            # Verificar si las claves necesarias están presentes
            if 'registro_id' not in item or 'item' not in item or 'cost' not in item or 'tax' not in item:
                print(f"Advertencia: Las claves necesarias no están presentes en el item: {item}")
                continue  # Si no están, saltamos este item

            # Acceder a los datos dentro del registro
            registro_id = item['registro_id']
            item_name = item['item']
            cost = item['cost']
            tax = item['tax']
            total = cost + tax  # Calcular el total como la suma de 'cost' y 'tax'
            
            # Crear una fila para la tabla
            fila = self.tabla_resultados.rowCount()
            self.tabla_resultados.insertRow(fila)
            
            # Llenar los datos en la tabla
            self.tabla_resultados.setItem(fila, 0, QTableWidgetItem(str(registro_id)))  # Columna para 'registro_id'
            self.tabla_resultados.setItem(fila, 1, QTableWidgetItem(item_name))  # Columna para 'item'
            self.tabla_resultados.setItem(fila, 2, QTableWidgetItem(str(cost)))  # Columna para 'cost'
            self.tabla_resultados.setItem(fila, 3, QTableWidgetItem(str(tax)))  # Columna para 'tax'
            self.tabla_resultados.setItem(fila, 4, QTableWidgetItem(str(total)))  # Columna para 'total'
        
        # Ajustar el tamaño de las columnas al contenido
        self.tabla_resultados.resizeColumnsToContents()
        
        # Mostrar la ventana
        self.show()
        self.raise_()
        self.activateWindow()
