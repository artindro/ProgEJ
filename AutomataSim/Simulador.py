# Simulador de Automatas
# Es bastante sencillo dentro de todo, tenemos una serie de listas y un diccionario para poner los valores
# de una tupla.

# Tupla de 5
estados = []
alfabetos = []
estado_inicio = ""
estados_aceptados = []
transicion = {}

#  Aca Entra la cadena que puede aceptar o rechazar el DFD
input_string = ""

# Los estados y la entrada del alfabeto se representara como una lista de cadenas Ej: "s1 s2 s3 s4, etc"
print("Introduzca los estados del autómata separados por espacios: ", end="")
estados = input().split()

# Introducimos los simbolos que vamos a usar, generalmente 0, 1 pero pueden ser otras cosas.
print("Introduzca los alfabetos de los autómatas separados por espacios: ", end="")
alfabetos = input().split()

# Estados de inicio, donde empieza el automata.
print("Introduzca el estado de inicio del autómata: ", end="")
estado_inicio = input()
# Mismo, excepto que van los que acepta.
print("Introduzca los estados de aceptación del autómata separados por espacios: ", end="")
estados_aceptados = input().split()

# La función de transición es un diccionario donde
# Las transiciones son un poco mas complicadas
# Es todo un diccionario que va a tomar la siguiente forma:
# (estado_actual, entrada) ➔ proximo_estado
# e.j:
#    (q0, 0) ---> q1
#    (q1, 1) ---> q2
# Despues para poder comparar los estados tenemos dos loops "for", uno dentro del otro.
# Uno es para los estados y el otro para los alfabetos. (Eso si el . guarda como "None", osea camino muerto
# o rechazado)

print("Ingrese los siguientes estados para lo siguiente (ingrese . para estado muerto/rechazado)")
for estado in estados:
    for a in alfabetos:
        print(f"\t  {a}")
        print(f"{estado}\t---->\t", end="")
        dest = input()
        
        # Los estados rechazados se representan como None en el diccionario
        if dest == ".":
            transicion[(estado, a)] = None
        else:
            transicion[(estado, a)] = dest
            
print("Introduzca la cadena de entrada para ejecutar el autómata: ", end="")
input_string = input()

# Comience a analizar la cadena de entrada con el estado actual como estado de inicio
estado_actual = estado_inicio

for char in input_string:
    # Transición al siguiente estado utilizando el estado actual y el alfabeto de entrada
    estado_actual = transicion[(estado_actual, char)]
    
    # Compruebe si el DFA entra en un estado inactivo/rechazado
    if estado_actual is None:
        print("Rechazado")
        break
else:
    # Cuando se analiza la cadena completa, compruebe si el estado final es un estado aceptado
    if (estado_actual in estados_aceptados):
        print("Aceptado")
    else:
        print("Rechazado")