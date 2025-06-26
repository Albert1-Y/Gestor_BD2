
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QSpinBox, QPushButton, QHBoxLayout

class ConfigDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Configuración de Disco")

        self.platos_input = QSpinBox()
        self.platos_input.setRange(1, 10)
        self.platos_input.setValue(2)

        self.pistas_input = QSpinBox()
        self.pistas_input.setRange(1, 100)
        self.pistas_input.setValue(5)

        self.sectores_input = QSpinBox()
        self.sectores_input.setRange(1, 100)
        self.sectores_input.setValue(10)

        self.tamano_sector_input = QSpinBox()
        self.tamano_sector_input.setRange(1, 1024)
        self.tamano_sector_input.setValue(64)

        form_layout = QFormLayout()
        form_layout.addRow("Número de platos:", self.platos_input)
        form_layout.addRow("Número de pistas:", self.pistas_input)
        form_layout.addRow("Sectores por pista:", self.sectores_input)
        form_layout.addRow("Tamaño de sector:", self.tamano_sector_input)

        self.confirmar_btn = QPushButton("Confirmar")
        self.confirmar_btn.clicked.connect(self.accept)

        self.usar_default_btn = QPushButton("Usar valores por defecto")
        self.usar_default_btn.clicked.connect(self.accept)

        botones_layout = QHBoxLayout()
        botones_layout.addWidget(self.confirmar_btn)
        botones_layout.addWidget(self.usar_default_btn)

        layout = QVBoxLayout()
        layout.addLayout(form_layout)
        layout.addLayout(botones_layout)

        self.setLayout(layout)

    def get_valores(self):
        return {
            "platos": self.platos_input.value(),
            "pistas": self.pistas_input.value(),
            "sectores": self.sectores_input.value(),
            "tamano": self.tamano_sector_input.value()
        }
    
    def valores(self):
        return [self.platos_input.value(),
                self.pistas_input.value(),
                self.sectores_input.value(),
                self.tamano_sector_input.value()]


