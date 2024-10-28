import sys
import re
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit
from PyQt6.QtGui import QPixmap, QFont, QIcon

keywords = ["entero", "decimal", "booleano", "cadena", "si", "sino", "mientras", "hacer", "verdadero", "falso", "if",
            "else", "while", "int", "print", "main", "return"]
operators = ["+", "-", "*", "/", "%", "=", "==", "<", ">", ">=", "<=", "&&", "||", "!="]
symbols = ["(", ")", "{", "}", ";"]

# Expresiones regulares para diferentes tokens
decimal_regex = r'^\d+\.\d+$'  # Coincide con números decimales
integer_regex = r'^\d+$'  # Coincide con números enteros
identifier_regex = r'^[a-zA-Z_]\w*$'  # Coincide con identificadores
string_regex = r'^".*"$'  # Coincide con cadenas de texto entre comillas dobles

# Tabla de símbolos para análisis semántico
symbol_table = {}


def analyze_line(line, line_number):
    global symbol_table  # Asegúrate de usar una tabla de símbolos global o del ámbito de la función principal
    line = re.sub(r'//.*', '', line)  # Elimina comentarios de línea única
    line = re.sub(r'/\*.*?\*/', '', line)  # Elimina comentarios de bloque
    tokens = re.findall(r'\".*?\"|\d+\.\d+|\w+|<=|>=|==|&&|\|\||!=|[-+*/%=<>();{}]|[^\w\s]', line)

    resultado = []
    for i, token in enumerate(tokens):
        if token in keywords:
            resultado.append(f"Token encontrado: {token} - Palabra Reservada")
            # Si el siguiente token es un identificador, agrégalo a la tabla de símbolos
            if token in ["int", "decimal", "booleano", "cadena"] and i + 1 < len(tokens):
                symbol_table[tokens[i + 1]] = "variable"  # Registra el identificador como declarado
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
            # Aquí no se agrega automáticamente a symbol_table; solo se agrega si es declarado
        else:
            resultado.append(f"Error léxico en la línea {line_number}: Token no reconocido \"{token}\"")

    return resultado, tokens

def analyze_semantics(tokens):
    errors = []
    for token in tokens:
        if re.match(identifier_regex, token) and token not in keywords and token not in symbol_table:
            errors.append(f"Error semántico: '{token}' no declarado")
    # Si no hay errores, agrega el mensaje final
    return errors if errors else ["Análisis semántico completado sin errores"]



def parse_tokens(tokens):
    stack = []
    last_if_index = -1  # Índice para almacenar la posición del último 'if'

    for i, token in enumerate(tokens):
        if token == "if":
            stack.append("if")
            last_if_index = i
        elif token == "else":
            # Solo permite 'else' si el último 'if' está en la pila
            if stack and stack[-1] == "if" and last_if_index < i:
                stack.pop()  # Empareja el 'else' con el 'if' correspondiente
            else:
                return "Error sintáctico: 'else' sin 'if'"
        elif token == "{":
            stack.append("{")
        elif token == "}":
            # Asegura que haya un bloque o apertura de llave que cerrar
            if "{" in stack:
                while stack and stack[-1] != "{":
                    stack.pop()
                stack.pop()  # Elimina la llave de apertura
            else:
                return "Error sintáctico: Llave de cierre sin apertura"

    # Validar si todos los bloques y llaves fueron cerrados
    if stack:
        return "Error sintáctico: estructura incompleta (llave o bloque no cerrado)"

    return "Sintaxis válida"

def analyze_content(content):
    resultado = []
    lines = content.split('\n')
    tokens = []

    for line_number, line in enumerate(lines, start=1):
        lex_result, line_tokens = analyze_line(line.strip(), line_number)
        resultado.extend(lex_result)
        tokens += line_tokens

    sintactic_result = parse_tokens(tokens)
    semantic_result = analyze_semantics(tokens)

    resultado.append("\nAnálisis Sintáctico:\n" + sintactic_result)
    resultado.append("\nAnálisis Semántico:\n" + "\n".join(semantic_result))

    return "\n".join(resultado)


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador Léxico, Sintáctico y Semántico")
        self.setGeometry(480, 90, 570, 690)

        self.contenido_txt = None

        icon = QIcon("analizador_lexico_logo.png")
        self.setWindowIcon(icon)

        layout = QVBoxLayout()
        logo_layout = QHBoxLayout()

        logo_label = QLabel()
        pixmap = QPixmap("analizador_lexico_logo.png").scaled(130, 130)
        aux_label = QLabel()
        logo_label.setPixmap(pixmap)
        logo_layout.addWidget(logo_label)

        title_label = QLabel("Analizador Léxico, Sintáctico y Semántico")
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

        resultado_label = QLabel("Resultado:")
        resultado_label.setFont(QFont("Arial", 10))
        self.resultado_text_edit = QTextEdit(self)
        self.resultado_text_edit.setFont(QFont("Arial", 11))
        self.resultado_text_edit.setReadOnly(True)

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
