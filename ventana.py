import tkinter as tk
from tkinter import *
from tkinter import filedialog
import ts as TS
import gramar as g
from gramar import lexer
from instrucciones import *
from expresiones import *
from principal import *



class InterpreterApp:
    def __init__(self, master):
        self.master = master
        master.title("Interpretador")
        master.geometry("500x600")

        # Entry para ingresar código
        self.input_code = Text(master, width=57, height=20)
        self.input_code.place(x=20, y=50)
        
        
        # Widget de texto para mostrar resultados
        self.result_text = Text(master, width=57, height=10, state='disabled')
        self.result_text.place(x=20, y=300)
        
        
        # Menú para seleccionar idiomas
        languages = ['Español', 'Inglés', 'Francés']
        self.selected_language = StringVar(self.master)
        self.selected_language.set(languages[1])  # Establecer el idioma predeterminado

        language_menu = OptionMenu(self.master, self.selected_language, *languages)
        language_menu.place(x=400, y=10)
        

        self.button_open_file = Button(master, text='Abrir archivo', bd=5, command=self.abrir_archivo)
        self.button_open_file.place(x=10, y=10)
        
        
        
        self.button_lex = Button(self.master, text='Validar léxico', bd=5, command=self.validar_lexico)
        self.button_lex.place(x=30, y=500)
        
        self.button_gramar = Button(self.master, text='Validar gramática', bd=5, command=self.validar_gramatica)
        self.button_gramar.place(x=130, y=500)

        self.button_execute = Button(self.master, text='Ejecutar', bd=5, command=self.ejecutar_codigo)
        self.button_execute.place(x=250, y=500)
        
        
        

    def abrir_archivo(self):
  
        file_path = filedialog.askopenfilename(filetypes=[("Archivos de texto", "*.txt")])

        if file_path:

            with open(file_path, 'r') as file:
                codigo = file.read()

            # Insertar el contenido en el widget de texto
            self.input_code.delete(1.0, END)
            self.input_code.insert(END, codigo)
            
   

    

    def validar_lexico(self):
        codigo = self.input_code.get("1.0", tk.END)

        self.result_text.config(state='normal')
        self.result_text.delete(1.0, END)

        # Utilizar la instancia de lexer de la gramatica
        g.lexer.input(codigo)
        tokens = []
        while True:
            tok = g.lexer.token()
            if not tok:
                break
            tokens.append(tok)
            print(tok)

        # Mostrar los tokens en el widget de resultados
        self.mostrar_resultado("Tokens", tokens)


    def validar_gramatica(self):
        codigo = self.input_code.get("1.0", tk.END)
        
        self.result_text.config(state='normal')
        self.result_text.delete(1.0, END)
        try:
            instrucciones = g.parse(codigo)
            self.mostrar_resultado("Análisis gramatical exitoso")
            self.mostrar_resultado(str(instrucciones))
        except Exception as e:
            self.mostrar_resultado(f"Error en el análisis gramatical {str(e)}")



    def ejecutar_codigo(self):
        codigo = self.input_code.get("1.0", END)

        
        instrucciones = g.parse(codigo)
        ts_global = TS.TablaDeSimbolos()

        verdad = ExpresionIdentificador("verdad")
        ts_global.agregar(TS.Simbolo("verdad", TS.TIPO_DATO.__bool__, True))
        mentira = ExpresionIdentificador("mentira")
        ts_global.agregar(TS.Simbolo("mentira", TS.TIPO_DATO.__bool__, False))
        
        try:
            procesar_instrucciones(instrucciones, ts_global, self)
            self.mostrar_resultado("Ejecución exitosa")
            self.mostrar_resultado(str(ts_global))
        except Exception as e:
            self.mostrar_resultado(f"Error en la ejecución: {str(e)}")

    def mostrar_resultado(self, resultado, tokens=None):
        self.result_text.config(state='normal')
        self.result_text.insert(tk.END, resultado + "\n")
        
        if tokens is not None:
        # Convertir la lista de tokens a una cadena antes de insertarla
            tokens_str = "\n".join([str(tok) for tok in tokens])
            self.result_text.insert(tk.END, tokens_str + "\n")
        
        self.result_text.config(state='disabled')

   


if __name__ == "__main__":
    root = tk.Tk()
    app = InterpreterApp(root)
    root.mainloop()


