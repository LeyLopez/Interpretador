import gramar as g
import ts as TS
from expresiones import *
from instrucciones import *


def procesar_exhibir(instr, ts, app):
    resultado = resolver_cadena(instr.cad, ts)
    app.mostrar_resultado(f"> {resultado}")


def procesar_definicion(instr, ts):
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.numero, 0)
    ts.agregar(simbolo)

def procesar_call_procedimiento(instr, ts, app):
    if instr.id in ts.simbolos:
        funcion = ts.obtener(instr.id)
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(funcion.valor, ts_local, app)
    
    
def procesar_definicion_procedimiento(instr, ts):
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.function, instr.instrucciones)
    ts.agregar(simbolo)



def procesar_asignacion(instr, ts):
    val = resolver_expresion_aritmetica(instr.expNumerica, ts)
    simbolo = TS.Simbolo(instr.id, TS.TIPO_DATO.numero, val)
    ts.actualizar(simbolo)



def procesar_durante(instr, ts, app):
    while resolver_expresion_logica(instr.expLogica, ts):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local, app)


def procesar_condicion(instr, ts, app):
    val = resolver_expresion_logica(instr.expLogica, ts)
    if val:
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local, app)




def procesar_alternativa(instr, ts, app):
    val = resolver_expresion_logica(instr.expLogica, ts)
    if val:
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfVerdadero, ts_local, app)
    else:
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrIfFalso, ts_local, app)


def procesar_iterar(instr, ts, app):
    inicio = resolver_expresion_aritmetica(instr.inicio, ts)
    fin = resolver_expresion_aritmetica(instr.fin, ts)

    for i in range(inicio, fin + 1):
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        ts_local.agregar(TS.Simbolo(instr.variable, TS.TIPO_DATO.numero, i))
        procesar_instrucciones(instr.instrucciones, ts_local, app)


def procesar_realizar_durante(instr, ts, app):
    while True:
        ts_local = TS.TablaDeSimbolos(ts.simbolos)
        procesar_instrucciones(instr.instrucciones, ts_local, app)
        if not resolver_expresion_booleana(instr.exp_logica, ts):
            break


def resolver_cadena(expCad, ts):
    if isinstance(expCad, ExpresionConcatenar):
        exp1 = resolver_cadena(expCad.exp1, ts)
        exp2 = resolver_cadena(expCad.exp2, ts)
        return exp1 + exp2
    elif isinstance(expCad, ExpresionDobleComilla):
        return expCad.val
    elif isinstance(expCad, ExpresionCadenaNumerico):
        return str(resolver_expresion_aritmetica(expCad.exp, ts))
    elif isinstance(expCad, ExpresionCadenaBooleana):
        return str(resolver_expresion_booleana(expCad.exp, ts))
    elif isinstance(
        expCad, ExpresionIdentificador
    ):  # Agregar manejo para identificadores
        if expCad.id in ts.simbolos:
            return str(ts.obtener(expCad.id).valor)
        else:
            print(f"Error: Identificador '{expCad.id}' no definido.")
            return ""
    else:
        print(f"Error: Expresión cadena no válida: {expCad}")
        return ""


def resolver_expresion_logica(expLog, ts):
    exp1 = resolver_expresion_aritmetica(expLog.exp1, ts)
    exp2 = resolver_expresion_aritmetica(expLog.exp2, ts)
    if expLog.operador == OPERACION_LOGICA.MAYOR_QUE:
        return exp1 > exp2
    if expLog.operador == OPERACION_LOGICA.MENOR_QUE:
        return exp1 < exp2
    if expLog.operador == OPERACION_LOGICA.IGUAL:
        return exp1 == exp2
    if expLog.operador == OPERACION_LOGICA.DIFERENTE:
        return exp1 != exp2


def resolver_expresion_aritmetica(expNum, ts):
    if isinstance(expNum, ExpresionBinaria):
        exp1 = resolver_expresion_aritmetica(expNum.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expNum.exp2, ts)
        if expNum.operador == OPERACION_ARITMETICA.MAS:
            return exp1 + exp2
        if expNum.operador == OPERACION_ARITMETICA.MENOS:
            return exp1 - exp2
        if expNum.operador == OPERACION_ARITMETICA.POR:
            return exp1 * exp2
        if expNum.operador == OPERACION_ARITMETICA.DIVIDIDO:
            return exp1 / exp2
    elif isinstance(expNum, ExpresionNegativo):
        exp = resolver_expresion_aritmetica(expNum.exp, ts)
        return exp * -1
    elif isinstance(expNum, Expresionnumerito):
        return expNum.val
    elif isinstance(expNum, ExpresionIdentificador):
        if expNum.id in ts.simbolos:
            return ts.obtener(expNum.id).valor
        else:
            print(f"Error: variable '{expNum.id}' no definida.")
            return 0
    else:
        print("Error: Expresión aritmética no válida")
        return


def resolver_expresion_booleana(expBool, ts):
    if isinstance(expBool, ExpresionBooleana):
        return expBool.val
    elif isinstance(expBool, ExpresionLogica):
        exp1 = resolver_expresion_aritmetica(expBool.exp1, ts)
        exp2 = resolver_expresion_aritmetica(expBool.exp2, ts)
        if expBool.operador == OPERACION_LOGICA.MAYOR_QUE:
            return exp1 > exp2
        if expBool.operador == OPERACION_LOGICA.MENOR_QUE:
            return exp1 < exp2
        if expBool.operador == OPERACION_LOGICA.IGUAL:
            return exp1 == exp2
        if expBool.operador == OPERACION_LOGICA.DIFERENTE:
            return exp1 != exp2
    else:
        print("Error: Expresión booleana no válida")


def procesar_instrucciones(instrucciones, ts, app):
    ## lista de instrucciones recolectadas
    for instr in instrucciones:
        if isinstance(instr, exhibir):
            procesar_exhibir(instr, ts, app)
        elif isinstance(instr, Definicion):
            procesar_definicion(instr, ts)
        elif isinstance(instr, DefinicionProcedimiento):
            procesar_definicion_procedimiento(instr, ts)
        elif isinstance(instr, CallProcedimiento):
            procesar_call_procedimiento(instr, ts, app)
        elif isinstance(instr, Asignacion):
            procesar_asignacion(instr, ts)
        elif isinstance(instr, durante):
            procesar_durante(instr, ts, app)
        elif isinstance(instr, condicion):
            procesar_condicion(instr, ts, app)
        elif isinstance(instr, Alternativa):
            procesar_alternativa(instr, ts, app)
        elif isinstance(instr, iterar):
            procesar_iterar(instr, ts, app)
        elif isinstance(instr, RealizarDurante):
            procesar_realizar_durante(instr, ts, app)
        else:
            print("Error: instrucción no válida")


"""
f = open("./entrada.txt")
input = f.read()

instrucciones = g.parse(input)
ts_global = TS.TablaDeSimbolos()
turu = ExpresionIdentificador("turu")
ts_global.agregar(TS.Simbolo("turu", TS.TIPO_DATO.__bool__, True))
turu = ExpresionIdentificador("forusu")
ts_global.agregar(TS.Simbolo("forusu", TS.TIPO_DATO.__bool__, False))

procesar_instrucciones(instrucciones, ts_global)
"""