import re

# Definir las listas de palabras reservadas, operadores y símbolos
keywords = ["entero", "decimal", "booleano", "cadena", "si", "sino", "mientras", "hacer", "verdadero", "falso"]
operators = ["+", "-", "*", "/", "%", "=", "==", "<", ">", ">=", "<="]
symbols = ["(", ")", "{", "}", ";"]

# Expresiones regulares para diferentes tokens
decimal_regex = r'^\d+(\.\d+)?$'  # Coincide con números enteros y decimales
identifier_regex = r'^[a-zA-Z_]\w*$'  # Coincide con identificadores
string_regex = r'^".*"$'  # Coincide con cadenas de texto entre comillas dobles

# Función para analizar una línea y encontrar los tokens
def analyze_line(line, line_number):
    # Eliminar comentarios de una línea
    line = re.sub(r'//.*', '', line)  # Elimina comentarios de línea única
    line = re.sub(r'/\*.*?\*/', '', line)  # Elimina comentarios de bloque

    # Utilizar una expresión regular para dividir la línea en tokens, respetando los operadores y símbolos
    tokens = re.findall(r'\".*?\"|\w+|<=|>=|==|[-+*/%=<>();{}]', line)

    for token in tokens:
        if token in keywords:
            print(f"Token encontrado: {token} - Palabra Reservada")
        elif token in operators:
            print(f"Token encontrado: {token} - Operador")
        elif token in symbols:
            print(f"Token encontrado: {token} - Símbolo")
        elif re.match(decimal_regex, token):  # Coincide con números enteros y decimales
            print(f"Token encontrado: {token} - Número")
        elif re.match(string_regex, token):  # Coincide con cadenas de texto
            print(f"Token encontrado: {token} - Cadena de texto")
        elif re.match(identifier_regex, token):  # Coincide con identificadores
            print(f"Token encontrado: {token} - Identificador")
        else:
            print(f"Error léxico en la línea {line_number}: Token no reconocido \"{token}\"")

# Función para analizar el archivo línea por línea
def analyze_file(file_path):
    with open(file_path, 'r') as file:
        for line_number, line in enumerate(file, start=1):
            analyze_line(line.strip(), line_number)

# Función principal para iniciar el análisis
def main():
    file_path = input("Ingresa la ruta del archivo: ")
    try:
        analyze_file(file_path)
    except FileNotFoundError:
        print(f"Archivo no encontrado: {file_path}")

# Ejecutar la función principal
if __name__ == "__main__":
    main()
