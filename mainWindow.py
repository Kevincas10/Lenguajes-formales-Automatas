import sys
import re
from collections import defaultdict
import pandas as pd
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFileDialog, QTextEdit, QTableWidget, QTableWidgetItem
from PyQt6.QtGui import QPixmap, QFont, QIcon

# Lista de palabras clave, operadores y símbolos
keywords = ["entero", "decimal", "booleano", "cadena", "si", "sino", "mientras", "hacer", "verdadero", "falso", "if",
            "else", "while", "int", "print", "main", "return"]
operators = ["+", "-", "*", "/", "%", "=", "==", "<", ">", ">=", "<=", "&&", "||", "!="]
symbols = ["(", ")", "{", "}", ";"]

# Expresiones regulares para diferentes tokens
decimal_regex = r'^\d+\.\d+$'  # Coincide con números decimales
integer_regex = r'^\d+$'  # Coincide con números enteros
identifier_regex = r'^[a-zA-Z_]\w*$'  # Coincide con identificadores
string_regex = r'^".*"$'  # Coincide con cadenas de texto entre comillas dobles

# Diccionarios para almacenar la tabla de símbolos y la frecuencia de tokens
symbol_table = {}
token_count = defaultdict(lambda: {"tipo": "", "cantidad": 0})

def analyze_line(line, line_number):
    global symbol_table
    line = re.sub(r'//.*', '', line)  # Elimina comentarios de línea única
    line = re.sub(r'/\*.*?\*/', '', line)  # Elimina comentarios de bloque
    tokens = re.findall(r'\".*?\"|\d+\.\d+|\w+|<=|>=|==|&&|\|\||!=|[-+*/%=<>();{}]|[^\w\s]', line)

    resultado = []
    for i, token in enumerate(tokens):
        if token in keywords:
            resultado.append(f"Token encontrado: {token} - Palabra Reservada")
            token_count[token]["tipo"] = "Palabra Reservada"
            token_count[token]["cantidad"] += 1
            # Si el siguiente token es un identificador, agrégalo a la tabla de símbolos
            if token in ["int", "decimal", "booleano", "cadena"] and i + 1 < len(tokens):
                symbol_table[tokens[i + 1]] = "variable"
        elif token in operators:
            resultado.append(f"Token encontrado: {token} - Operador")
            token_count[token]["tipo"] = "Operador"
            token_count[token]["cantidad"] += 1
        elif token in symbols:
            resultado.append(f"Token encontrado: {token} - Símbolo")
            token_count[token]["tipo"] = "Símbolo"
            token_count[token]["cantidad"] += 1
        elif re.match(decimal_regex, token):
            resultado.append(f"Token encontrado: {token} - Número (Decimal)")
            token_count[token]["tipo"] = "Número (Decimal)"
            token_count[token]["cantidad"] += 1
        elif re.match(integer_regex, token):
            resultado.append(f"Token encontrado: {token} - Número (Entero)")
            token_count[token]["tipo"] = "Número (Entero)"
            token_count[token]["cantidad"] += 1
        elif re.match(string_regex, token):
            resultado.append(f"Token encontrado: {token} - Cadena de texto")
            token_count[token]["tipo"] = "Cadena de texto"
            token_count[token]["cantidad"] += 1
        elif re.match(identifier_regex, token):
            resultado.append(f"Token encontrado: {token} - Identificador")
            token_count[token]["tipo"] = "Identificador"
            token_count[token]["cantidad"] += 1
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
    lex_result, tokens = [], []
    lines = content.split('\n')

    for line_number, line in enumerate(lines, start=1):
        line_result, line_tokens = analyze_line(line.strip(), line_number)
        lex_result.extend(line_result)
        tokens.extend(line_tokens)

    sintactic_result = parse_tokens(tokens)
    semantic_result = analyze_semantics(tokens)

    return "\n".join(lex_result), sintactic_result, "\n".join(semantic_result)

def create_token_table():
    table_data = []
    for token, info in token_count.items():
        table_data.append([token, info["tipo"], str(info["cantidad"])])
    return table_data

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Analizador Léxico, Sintáctico y Semántico")
        self.setGeometry(480, 90, 570, 690)

        self.contenido_txt = None

        icon = QIcon("analizador_lexico_logo.png")
        self.setWindowIcon(icon)

        layout = QVBoxLayout()
        layout4 = QHBoxLayout()
        layout2 = QVBoxLayout()
        layout3 = QVBoxLayout()
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

        contenido_label = QLabel("Contenido del archivo:")
        contenido_label.setFont(QFont("Arial", 10))
        self.contenitdo_text = QTextEdit(self)
        self.contenitdo_text.setFont(QFont("Arial", 11))
        self.contenitdo_text.setReadOnly(True)

        resultado_label_lexico = QLabel("Análisis Léxico:")
        resultado_label_lexico.setFont(QFont("Arial", 10))
        self.resultado_text_edit_lexico = QTextEdit(self)
        self.resultado_text_edit_lexico.setFont(QFont("Arial", 11))
        self.resultado_text_edit_lexico.setReadOnly(True)

        resultado_label_sintactico = QLabel("Análisis Sintáctico:")
        resultado_label_sintactico.setFont(QFont("Arial", 10))
        self.resultado_text_edit_sintactico = QTextEdit(self)
        self.resultado_text_edit_sintactico.setFont(QFont("Arial", 11))
        self.resultado_text_edit_sintactico.setReadOnly(True)

        resultado_label_semantico = QLabel("Análisis Semántico:")
        resultado_label_semantico.setFont(QFont("Arial", 10))
        self.resultado_text_edit_semantico = QTextEdit(self)
        self.resultado_text_edit_semantico.setFont(QFont("Arial", 11))
        self.resultado_text_edit_semantico.setReadOnly(True)

        self.table_widget = QTableWidget()
        self.table_widget.setColumnCount(3)
        self.table_widget.setHorizontalHeaderLabels(["TOKEN", "TIPO", "CANTIDAD"])

        layout.addLayout(logo_layout)
        layout2.addWidget(contenido_label)
        layout2.addWidget(self.contenitdo_text)
        layout3.addWidget(resultado_label_lexico)
        layout3.addWidget(self.resultado_text_edit_lexico)
        layout3.addWidget(resultado_label_sintactico)
        layout3.addWidget(self.resultado_text_edit_sintactico)
        layout3.addWidget(resultado_label_semantico)
        layout3.addWidget(self.resultado_text_edit_semantico)
        layout2.addWidget(self.table_widget)
        layout4.addLayout(layout2)
        layout4.addLayout(layout3)
        layout.addLayout(layout4)
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
                    lex_result, sintactic_result, semantic_result = analyze_content(contenido)
                    self.resultado_text_edit_lexico.setText(lex_result)
                    self.resultado_text_edit_sintactico.setText(sintactic_result)
                    self.resultado_text_edit_semantico.setText(semantic_result)
                    self.mostrar_tabla_tokens()
            except Exception as e:
                self.resultado_text_edit_lexico.setText(f"Error al abrir el archivo: {e}")

    def mostrar_tabla_tokens(self):
        token_data = create_token_table()
        self.table_widget.setRowCount(len(token_data))
        for row, data in enumerate(token_data):
            for column, item in enumerate(data):
                self.table_widget.setItem(row, column, QTableWidgetItem(item))

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
