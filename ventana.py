import tkinter as tk
from tkinter import *
from tkinter import filedialog
import ply.lex as lex
import ply.yacc as yacc
import ts as TS
import gramar as g
from instrucciones import *
from expresiones import *
from principal import *

class InterpreterApp:
    def __init__(self, master):
        self.master = master
        master.title("Intérpretador")
        master.geometry("500x500")

        # Entry para ingresar código
        self.input_code = Text(master, width=57, height=20)
        self.input_code.place(x=20, y=50)

        self.button_open_file = Button(master, text='Abrir Archivo', bd=5, command=self.abrir_archivo)
        self.button_open_file.place(x=300, y=400)
        
        # Menú para seleccionar idiomas
        languages = ['Español', 'Inglés', 'Portugués']
        self.selected_language = StringVar(self.master)
        self.selected_language.set(languages[0])  # Establecer el idioma predeterminado

        language_menu = OptionMenu(self.master, self.selected_language, *languages)
        language_menu.place(x=400, y=10)

        # Botón para ejecutar debajo de la entrada de texto
        self.button_execute = Button(self.master, text='Ejecutar', bd=5, command=self.ejecutar_codigo)
        self.button_execute.place(x=200, y=400)

    def abrir_archivo(self):
        # Diálogo para abrir archivo
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])

        if file_path:
            # Leer el contenido del archivo
            with open(file_path, 'r') as file:
                codigo = file.read()

            # Insertar el contenido en el widget de texto
            self.input_code.delete(1.0, END)
            self.input_code.insert(END, codigo)
            
            
    
    def ejecutar_codigo(self):
        # Obtener el código ingresado en el widget de texto
        codigo = self.input_code.get("1.0", END)

        # Procesar el código con tu intérprete
        instrucciones = g.parse(codigo)
        ts_global = TS.TablaDeSimbolos()

        # Agregar símbolos de prueba (turu y forusu)
        turu = ExpresionIdentificador("turu")
        ts_global.agregar(TS.Simbolo("turu", TS.TIPO_DATO.__bool__, True))
        forusu = ExpresionIdentificador("forusu")
        ts_global.agregar(TS.Simbolo("forusu", TS.TIPO_DATO.__bool__, False))

        procesar_instrucciones(instrucciones, ts_global)
        
        print("Tabla de símbolos:")
        for simbolo in ts_global.simbolos.values():
            print(f"{simbolo.id}: {simbolo.valor}")



if __name__ == "__main__":
    root = tk.Tk()
    app = InterpreterApp(root)
    root.mainloop()


