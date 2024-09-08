import sys
from PyQt6.QtCore import Qt, QSize, QRect, QPropertyAnimation
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog
from PyQt6.QtGui import QPixmap, QFont, QIcon

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador Léxico")
        self.setGeometry(610, 290, 320, 250)

        self.contenido_txt = None

        # Establecer el ícono de la ventana
        icon = QIcon("analizador_lexico_logo.png")
        self.setWindowIcon(icon)

        # Configuración del layout principal
        layout = QVBoxLayout()

        # Layout que contiene el encabezado
        logo_layout = QHBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap("analizador_lexico_logo.png").scaled(130, 130)
        aux_label = QLabel()
        logo_label.setPixmap(pixmap)
        logo_layout.addWidget(logo_label)

        title_label = QLabel("Analizador Léxico")
        title_label.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        logo_layout.addWidget(aux_label)
        logo_layout.addWidget(title_label)
        logo_layout.addWidget(aux_label)

        txt_button = self.txt_button()
        txt_button.clicked.connect(self.cargar_archivo_txt)

        # Asignar el layout al widget
        layout.addLayout(logo_layout)
        layout.addWidget(txt_button)
        self.setLayout(layout)

    def txt_button(self):
        image_button = QPixmap("logo_txt.png")
        image_button = image_button.scaledToWidth(700)
        button = QPushButton(self)
        button.setText("Cargar Archivo txt")
        button.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        button.setIcon(QIcon(image_button))
        button.setIconSize(QSize(105, 105))
        button.setGeometry(10, 150, 250, 150)

        # Aplicar estilo para la sombra en hover
        button.setStyleSheet("""
            QPushButton:hover {
                border: 10px  #5e5e5e;
                border-radius: 6px;
                background-color: #757575;
                box-shadow: 5px 5px 5px gray;
            }
        """)

        return button

    def cargar_archivo_txt(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo", "", "Archivos de texto (*.txt)")

        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as file:
                    contenido = file.read()
                    self.contenido_txt = contenido
                    print(self.contenido_txt)
            except Exception as e:
                print(f"Error al abrir el archivo: {e}")


# Inicializar la aplicación
app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
