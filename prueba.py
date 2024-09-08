import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QFileDialog


class VentanaPrincipal(QWidget):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.setWindowTitle('Exportar Archivo')
        self.setGeometry(100, 100, 300, 200)

        # Botón para abrir el diálogo de guardar archivo
        boton_exportar = QPushButton('Exportar Archivo', self)
        boton_exportar.clicked.connect(self.exportar_archivo)
        boton_exportar.resize(boton_exportar.sizeHint())
        boton_exportar.move(100, 80)

    def exportar_archivo(self):
        # Abre el diálogo para guardar el archivo
        opciones = QFileDialog.Option()
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Archivo", "",
                                                 "Todos los archivos (*);;Archivos de texto (*.txt)", options=opciones)

        if archivo:
            # Aquí puedes manejar la lógica para exportar el archivo
            print(f"Archivo seleccionado para exportar: {archivo}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec())
