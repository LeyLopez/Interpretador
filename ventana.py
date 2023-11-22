import tkinter as tk
from tkinter import *
from tkinter import filedialog
import ts as TS
import gramar as g
from gramar import lexer
from instrucciones import *
from expresiones import *
from principal import *
import gettext
import os
from tkinter import ttk
import ply.lex
import ply.yacc


directorio_actual = os.getcwd()
localedir = os.path.join(directorio_actual, 'locales')

gettext.bindtextdomain('myapp', localedir)
gettext.textdomain('myapp')


class InterpreterApp:
    def __init__(self, master):
        
        self.master = master
        
        self.crear_interfaz()

    def crear_interfaz(self, idioma = 'es'):
        
        translations = gettext.translation('mensajes', localedir, languages=[idioma])
        translations.install()
        _ = translations.gettext
        
        
        self.master.title(_("Interpretador"))
        self.master.geometry("500x600")
        
        
        # Entry para ingresar código
        self.input_code = Text(self.master, width=57, height=20)
        self.input_code.place(x=20, y=50)
        
        
        # Widget de texto para mostrar resultados
        self.result_text = Text(self.master, width=57, height=10, state='disabled')
        self.result_text.place(x=20, y=300)
        
        
        # Menú para seleccionar idiomas
        # Menú para seleccionar idiomas usando Combobox
        languages = [_('Español'), _('Inglés'), _('Francés')]
        self.selected_language = StringVar(self.master)
        self.language_combobox = ttk.Combobox(self.master, textvariable=self.selected_language, values=languages)
        self.language_combobox.place(x=300, y=10)
        self.language_combobox.bind("<<ComboboxSelected>>", lambda event: self.cambiar_idioma())
        

        self.button_open_file = Button(self.master, text=_('Abrir archivo'), bd=5, command=self.abrir_archivo)
        self.button_open_file.place(x=10, y=10)
        
        
        
        self.button_lex = Button(self.master, text=_('Validar léxico'), bd=5, command=self.validar_lexico)
        self.button_lex.place(x=30, y=500)
        
        self.button_gramar = Button(self.master, text=_('Validar gramática'), bd=5, command=self.validar_gramatica)
        self.button_gramar.place(x=130, y=500)

        self.button_execute = Button(self.master, text=_('Ejecutar'), bd=5, command=self.ejecutar_codigo)
        self.button_execute.place(x=250, y=500)
        
        
    def cambiar_idioma(self, event=None):
        selected_language = self.selected_language.get()
        if selected_language == 'Español':
            locale = 'es'
        elif selected_language == 'Inglés':
            locale = 'en'
        elif selected_language == 'Francés':
            locale = 'fr'
        else:
            locale = 'es'
        gettext.install('mensajes', localedir, names=("ngettext",))
        gettext.translation('mensajes', localedir, languages=[locale]).install()
        self.crear_interfaz(locale)
        
        
        
        

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


