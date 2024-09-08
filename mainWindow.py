import sys
import re
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
from PyQt6.QtGui import QPixmap, QFont, QIcon


keywords = ["entero", "decimal", "booleano", "cadena", "si", "sino", "mientras", "hacer", "verdadero", "falso"]
operators = ["+", "-", "*", "/", "%", "=", "==", "<", ">", ">=", "<="]
symbols = ["(", ")", "{", "}", ";"]

# Expresiones regulares para diferentes tokens
decimal_regex = r'^\d+(\.\d+)?$'  # Coincide con números enteros y decimales
identifier_regex = r'^[a-zA-Z_]\w*$'  # Coincide con identificadores
string_regex = r'^".*"$'  # Coincide con cadenas de texto entre comillas dobles



decimal_regex = r'^\d+\.\d+$'  # Coincide con números decimales
integer_regex = r'^\d+$'  # Coincide con números enteros
identifier_regex = r'^[a-zA-Z_]\w*$'  # Coincide con identificadores
string_regex = r'^".*"$'  # Coincide con cadenas de texto entre comillas dobles


def analyze_line(line, line_number):
    line = re.sub(r'//.*', '', line)  # Elimina comentarios de línea única
    line = re.sub(r'/\*.*?\*/', '', line)  # Elimina comentarios de bloque
    tokens = re.findall(r'\".*?\"|\d+\.\d+|\w+|<=|>=|==|[-+*/%=<>();{}]|[^\w\s]', line)

    resultado = []
    for token in tokens:
        if token in keywords:
            resultado.append(f"Token encontrado: {token} - Palabra Reservada")
        elif token in operators:
            resultado.append(f"Token encontrado: {token} - Operador")
        elif token in symbols:
            resultado.append(f"Token encontrado: {token} - Símbolo")
        elif re.match(decimal_regex, token):
            resultado.append(f"Token encontrado: {token} - Número (Decimal)")
        elif re.match(integer_regex, token):
            resultado.append(f"Token encontrado: {token} - Número (Entero)")
        elif re.match(string_regex, token):
            resultado.append(f"Token encontrado: {token} - Cadena de texto")
        elif re.match(identifier_regex, token):
            resultado.append(f"Token encontrado: {token} - Identificador")
        else:
            resultado.append(f"Error léxico en la línea {line_number}: Token no reconocido \"{token}\"")

    return "\n".join(resultado)


def analyze_content(content):
    resultado = []
    lines = content.split('\n')
    for line_number, line in enumerate(lines, start=1):
        resultado.append(analyze_line(line.strip(), line_number))

    return "\n".join(resultado)

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador Léxico")
        self.setGeometry(480, 90, 570, 690)

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

        contenido_label = QLabel("Contenido txt: ")
        contenido_label.setFont(QFont("Arial", 10))
        self.contenitdo_text = QTextEdit(self)
        self.contenitdo_text.setFont(QFont("Arial", 11))
        self.contenitdo_text.setReadOnly(True)


        # TextEdit para mostrar resultados del análisis
        resultado_label = QLabel("Resultado:")
        resultado_label.setFont(QFont("Arial", 10))
        self.resultado_text_edit = QTextEdit(self)
        self.resultado_text_edit.setFont(QFont("Arial", 11))
        self.resultado_text_edit.setReadOnly(True)




        # Asignar el layout al widget
        layout.addLayout(logo_layout)
        layout.addWidget(contenido_label)
        layout.addWidget(self.contenitdo_text)
        layout.addWidget(resultado_label)
        layout.addWidget(self.resultado_text_edit)
        layout.addWidget(txt_button)
        self.setLayout(layout)

    def txt_button(self):
        image_button = QPixmap("logo_txt.png")
        image_button = image_button.scaledToWidth(700)
        button = QPushButton(self)
        button.setText("Cargar Archivo txt")
        button.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        button.setIcon(QIcon(image_button))
        button.setIconSize(QSize(65, 65))
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
                    self.contenitdo_text.setText(f"Contenido del archivo:\n\n{contenido}\n")
                    resultado = analyze_content(contenido)
                    self.resultado_text_edit.setText(f"Resultado del análisis:\n\n{resultado}")
            except Exception as e:
                self.resultado_text_edit.setText(f"Error al abrir el archivo: {e}")


app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())