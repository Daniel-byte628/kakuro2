import os
import random
import copy
from tabulate import tabulate
from termcolor import colored

def crear_sudoku_aleatorio(numero):
    board = [[0 for _ in range(numero)] for _ in range(numero)]
    fill_board(board)
    return board

def fill_board(board):
    rows = len(board)
    cols = len(board[0])
    
    for row in range(rows):
        for col in range(cols):
            if board[row][col] == 0:
                numbers = list(range(1, 10))
                random.shuffle(numbers)
                for num in numbers:
                    if is_valid_move(board, row, col, num):
                        board[row][col] = num
                        if fill_board(board):
                            return True
                        board[row][col] = 0
                return False
    return True

def is_valid_move(board, row, col, num):
    rows = len(board)
    cols = len(board[0])
    
    # Verificar fila
    if num in board[row]:
        return False
    
    # Verificar columna
    if num in [board[i][col] for i in range(rows)]:
        return False
    
    return True



def encontrar_celda_vacia(tablero, numero):
    for i in range(numero):
        for j in range(numero):
            if tablero[i][j] == 0:
                return (i, j)
    return None



def colocar_celdas_negras(tablero, numero):
    total_celdas = numero * numero

    # Calcula la cantidad de celdas negras como un porcentaje del total
    porcentaje_celdas_negras = 0.4  # Usamos el 40% de celdas negras
    cantidad_celdas_negras = int(total_celdas * porcentaje_celdas_negras)

    # Coloca las celdas negras de manera aleatoria
    for _ in range(cantidad_celdas_negras):
        fila, columna = random.randint(0, numero-1), random.randint(0, numero-1)
        tablero[fila][columna] = 'X'

def verificar_interior_tablero(tablero):
    tamano_tablero = len(tablero)

    for fila in range(1, tamano_tablero - 1):
        for columna in range(1, tamano_tablero - 1):
            if tablero[fila][columna] != "X":
                arriba = tablero[fila - 1][columna] == "X"
                abajo = tablero[fila + 1][columna] == "X"
                izquierda = tablero[fila][columna - 1] == "X"
                derecha = tablero[fila][columna + 1] == "X"

                if arriba and abajo and izquierda and derecha:
                    tablero[fila][columna] = "X"


def verificar_esquinas_y_bordes(tablero):
    tamano_tablero = len(tablero)

    # Verificar esquina superior izquierda
    if tablero[0][0] != "X":
        derecha = tablero[0][1] == "X"
        abajo = tablero[1][0] == "X"

        if derecha and abajo:
            tablero[0][0] = "X"

    # Verificar esquina superior derecha
    if tablero[0][tamano_tablero - 1] != "X":
        izquierda = tablero[0][tamano_tablero - 2] == "X"
        abajo = tablero[1][tamano_tablero - 1] == "X"

        if izquierda and abajo:
            tablero[0][tamano_tablero - 1] = "X"

    # Verificar esquina inferior izquierda
    if tablero[tamano_tablero - 1][0] != "X":
        derecha = tablero[tamano_tablero - 1][1] == "X"
        arriba = tablero[tamano_tablero - 2][0] == "X"

        if derecha and arriba:
            tablero[tamano_tablero - 1][0] = "X"

    # Verificar esquina inferior derecha
    if tablero[tamano_tablero - 1][tamano_tablero - 1] != "X":
        izquierda = tablero[tamano_tablero - 1][tamano_tablero - 2] == "X"
        arriba = tablero[tamano_tablero - 2][tamano_tablero - 1] == "X"

        if izquierda and arriba:
            tablero[tamano_tablero - 1][tamano_tablero - 1] = "X"

    # Verificar borde horizontal superior
    for columna in range(1, tamano_tablero - 1):
        if tablero[0][columna] != "X":
            izquierda = tablero[0][columna - 1] == "X"
            derecha = tablero[0][columna + 1] == "X"
            abajo = tablero[1][columna] == "X"

            if izquierda and derecha and abajo:
                tablero[0][columna] = "X"

    # Verificar borde horizontal inferior
    for columna in range(1, tamano_tablero - 1):
        if tablero[tamano_tablero - 1][columna] != "X":
            izquierda = tablero[tamano_tablero - 1][columna - 1] == "X"
            derecha = tablero[tamano_tablero - 1][columna + 1] == "X"
            arriba = tablero[tamano_tablero - 2][columna] == "X"

            if izquierda and derecha and arriba:
                tablero[tamano_tablero - 1][columna] = "X"

    # Verificar borde vertical izquierdo
    for fila in range(1, tamano_tablero - 1):
        if tablero[fila][0] != "X":
            arriba = tablero[fila - 1][0] == "X"
            abajo = tablero[fila + 1][0] == "X"
            derecha = tablero[fila][1] == "X"

            if arriba and abajo and derecha:
                tablero[fila][0] = "X"

    # Verificar borde vertical derecho
    for fila in range(1, tamano_tablero - 1):
        if tablero[fila][tamano_tablero - 1] != "X":
            arriba = tablero[fila - 1][tamano_tablero - 1] == "X"
            abajo = tablero[fila + 1][tamano_tablero - 1] == "X"
            izquierda = tablero[fila][tamano_tablero - 2] == "X"

            if arriba and abajo and izquierda:
                tablero[fila][tamano_tablero - 1] = "X"


def colocar_celdas_negras_suma(tablero):
    tamano_tablero = len(tablero)

    for fila in range(tamano_tablero):
        for columna in range(tamano_tablero):
            if tablero[fila][columna] != "X":
                encontrado = False

                # Verificar que no haya una sumatoria hasta que haya una X o se pase del tablero (columnas)

                col = columna + 1
                while col < tamano_tablero and tablero[fila][col] != "X":
                    if tablero[fila][col] == "P":
                        encontrado = True
                        break
                    col += 1

                # Verificar a la izquierda
                col = columna - 1
                while col >= 0 and tablero[fila][col] != "X":
                    if tablero[fila][col] == "P":
                        encontrado = True
                        break
                    col -= 1

                # Verificar que no haya una sumatoria hasta que haya una X o se pase del tablero (filas)

                fil = fila + 1
                while fil < tamano_tablero and tablero[fil][columna] != "X":
                    if tablero[fil][columna] == "P":
                        encontrado = True
                        break
                    fil += 1

                # Verificar arriba
                fil = fila - 1
                while fil >= 0 and tablero[fil][columna] != "X":
                    if tablero[fil][columna] == "P":
                        encontrado = True
                        break
                    fil -= 1

               # Verifica si las coordenadas de las celdas arriba y abajo están dentro de los límites del tablero.
                if (
                    0 <= fila < tamano_tablero - 1
                    and 0 <= columna < tamano_tablero - 1
                    and isinstance(tablero[fila - 1][columna], int)
                    and isinstance(tablero[fila + 1][columna], int)
                    and isinstance(tablero[fila][columna - 1], int)
                    and isinstance(tablero[fila][columna + 1], int)
                ):
                    encontrado = True

                # Si las condiciones anteriores no se cumplen, verifica si las coordenadas de las celdas arriba y abajo están dentro de los límites y contienen la cadena 'X'.
                elif (
                    0 <= fila < tamano_tablero - 1
                    and 0 <= columna < tamano_tablero - 1
                    and tablero[fila - 1][columna] == 'X'
                    and tablero[fila + 1][columna] == 'X'
                    and tablero[fila][columna - 1] == 'X'
                    and tablero[fila][columna + 1] == 'X'
                ):
                    encontrado = True

                elif (
                    fila< tamano_tablero - 1
                    and isinstance(tablero[fila + 1][columna], int)
                    and isinstance(tablero[fila - 1][columna], int)
                ):
                    encontrado = True

                elif (
                    columna< tamano_tablero - 1
                    and isinstance(tablero[fila][columna + 1], int)
                    and isinstance(tablero[fila][columna - 1], int)
                ):
                    encontrado = True

                elif not encontrado:
                    tablero[fila][columna] = "P"

    return tablero


def verificar_numeros_con_sumatoria(tablero):
    tamano_tablero = len(tablero)

    for fila in range(tamano_tablero):
        for columna in range(tamano_tablero):
            if isinstance(tablero[fila][columna], int):
                encontrado = False
                col = columna + 1
                while col < tamano_tablero and tablero[fila][col] != "X":
                    if tablero[fila][col] == "P":
                        encontrado = True
                        break
                    col += 1

                 # Verificar a la izquierda
                col = columna - 1
                while col >= 0 and tablero[fila][col] != "X":
                    if tablero[fila][col] == "P":
                        encontrado = True
                        break
                    col -= 1

                # Verificar que no haya una sumatoria hasta que haya una X o se pase del tablero (filas)

                fil = fila + 1
                while fil < tamano_tablero and tablero[fil][columna] != "X":
                    if tablero[fil][columna] == "P":
                        encontrado = True
                        break
                    fil += 1

                # Verificar arriba
                fil = fila - 1
                while fil >= 0 and tablero[fil][columna] != "X":
                    if tablero[fil][columna] == "P":
                        encontrado = True
                        break
                    fil -= 1

                if (
                    tablero[fila][columna] == "P"
                ):
                    encontrado = True

                if not encontrado:
                    tablero[fila][columna] = "X"



def imprimir_tablero(tablero):
    max_width = max(max(len(str(celda)) for celda in fila) for fila in tablero)
    
    for fila in tablero:
        fila_str = ""
        for celda in fila:
            if isinstance(celda, tuple):
                suma_fila, suma_columna = celda
                suma_fila_str = str(
                    suma_fila) if suma_fila is not None else " "
                suma_columna_str = str(
                    suma_columna) if suma_columna is not None else " "
                suma_celda_str = "[dim]{} / {}[default]".format(
                    suma_fila_str, suma_columna_str)
                # Aplicar colorama al texto de la celda
                suma_celda_str = colored(suma_celda_str, 'magenta')
                # Centrar el texto y ajustar el ancho de la celda
                fila_str += suma_celda_str.center(max_width + 8)
            else:
                celda_str = "   {}   ".format(celda).center(max_width + 8)
                fila_str += celda_str
        print(fila_str)



def calcular_promedios(tablero):
    tamano_tablero = len(tablero)

    # Itera a través de todas las celdas del tablero
    for fila in range(tamano_tablero):
        for columna in range(tamano_tablero):
            celda_actual = tablero[fila][columna]

            # Si la celda actual es 'P', calcula las sumatorias de fila y columna hasta encontrar una 'X'.
            if celda_actual == 'P':
                sumatoria_fila = 0
                sumatoria_columna = 0

                # Sumatoria de fila hacia arriba
                fila_arriba = fila - 1
                while fila_arriba >= 0 and tablero[fila_arriba][columna] != 'X':
                    sumatoria_fila += tablero[fila_arriba][columna]
                    fila_arriba -= 1

                # Sumatoria de fila hacia abajo
                fila_abajo = fila + 1
                while fila_abajo < tamano_tablero and tablero[fila_abajo][columna] != 'X':
                    sumatoria_fila += tablero[fila_abajo][columna]
                    fila_abajo += 1

                # Sumatoria de columna hacia la izquierda
                columna_izquierda = columna - 1
                while columna_izquierda >= 0 and tablero[fila][columna_izquierda] != 'X':
                    sumatoria_columna += tablero[fila][columna_izquierda]
                    columna_izquierda -= 1

                # Sumatoria de columna hacia la derecha
                columna_derecha = columna + 1
                while columna_derecha < len(tablero[fila]) and tablero[fila][columna_derecha] != 'X':
                    sumatoria_columna += tablero[fila][columna_derecha]
                    columna_derecha += 1

                # Calcula el valor de la celda como la sumatoria de fila dividida por la sumatoria de columna
                # Calcula el valor de la celda como una cadena que contiene la sumatoria de fila y columna separadas por "/"
                if sumatoria_columna != 0 or sumatoria_fila != 0:
                    tablero[fila][columna] = str(sumatoria_fila) + "/" + str(sumatoria_columna)


    return tablero

def reemplazar_numeros_con_vacios(tablero):
    for fila in range(len(tablero)):
        for columna in range(len(tablero)):
            if isinstance(tablero[fila][columna], int):
                tablero[fila][columna] = "-"
    return tablero

def crear_tablero_kakuro_aleatorio(tablero_sudoku, numero):
    colocar_celdas_negras(tablero_sudoku, numero)
    verificar_esquinas_y_bordes(tablero_sudoku)
    verificar_interior_tablero(tablero_sudoku)
    colocar_celdas_negras_suma(tablero_sudoku)
    verificar_numeros_con_sumatoria(tablero_sudoku)
    calcular_promedios(tablero_sudoku)
    return tablero_sudoku

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    
def llenar_tablero(tablero_kakuro, tablero_verificar):
    while True:
        input("Presiona Enter para continuar...")
        clear_screen() 
        print("EL TABLERO KAKURO:")
        print("\n")
        imprimir_tablero(tablero_kakuro)
        print("\n")
        fila = input("Ingresa el número de fila (1-{}), o 'q' para salir: ".format(len(tablero_kakuro)))
        
        if fila.lower() == 'q':
            break
        
        columna = input("Ingresa el número de columna (1-{}): ".format(len(tablero_kakuro[0])))
        numero = input("Ingresa el número (1-9) o '-' para colocar (X y / no se pueden cambiar): ")

        if fila.isdigit() and columna.isdigit():
            fila = int(fila) - 1  # Restar 1 para ajustar a la indexación de Python
            columna = int(columna) - 1
            if 0 <= fila < len(tablero_kakuro) and 0 <= columna < len(tablero_kakuro[0]):
                celda_actual = tablero_kakuro[fila][columna]
                if celda_actual != 'X' and '/' not in celda_actual:
                    if numero.isdigit() and 1 <= int(numero) <= 9 or numero == '-':
                        tablero_kakuro[fila][columna] = numero
                        tablero_verificar[fila][columna] = numero
                    else:
                        print("El número debe estar en el rango de 1 a 9, o puedes ingresar '-'.")
                else:
                    print("No puedes cambiar la 'X' ni los números dentro de '/'.")
            else:
                print("Las coordenadas están fuera del rango del tablero.")
        else:
            print("Por favor, ingresa coordenadas válidas y un número o '-' válido.")

def verificar_tablero(tablero_kakuro, tablero_verificar):
    for i in range(len(tablero_kakuro)):
        for j in range(len(tablero_kakuro[i])):
            celda_actual = tablero_kakuro[i][j]
            if celda_actual == '-':
                print("El tablero no está bien. La celda en la fila {} y columna {} no tiene un número.".format(i+1, j+1))
                return False  # El tablero no es correcto
            elif celda_actual != 'X' and '/' not in celda_actual:
                try:
                    numero_celda = int(celda_actual)
                except ValueError:
                    print("El tablero no está bien. El número en la fila {} y columna {} debe ser {}.".format(i+1, j+1, tablero_verificar[i][j]))
                    return False  # El tablero no es correcto
                numero_verificar = int(tablero_verificar[i][j])
                if numero_celda != numero_verificar:
                    print("El tablero no está bien. El número en la fila {} y columna {} debe ser {}.".format(i+1, j+1, numero_verificar))
                    return False  # El tablero no es correcto
    return True  # El tablero es correcto


def bienvenida_kakuro():
    print("¡Bienvenido a Kakuro!\n")
    print("Autor: Daniel G\n")
    print("Kakuro es un rompecabezas numérico que combina elementos de Sudoku y crucigramas.")
    print("El objetivo es llenar el tablero con números del 1 al 9, sin repetir números en la misma fila o columna,")
    print("de manera que se cumplan las sumas indicadas en las celdas. Cada celda con un número representa una")
    print("suma horizontal o vertical. Por ejemplo, 1/ significa que la suma horizontal debe ser 1 y /1 significa")
    print("que la suma vertical debe ser 1.\n")
    print("Tamaños del tablero recomendados:")
    print("- 9x9\n- 8x8\n- 6x6\n- 4x4\n")

if __name__ == "__main__":
    bienvenida_kakuro()
    
    while True:
        entrada = input("Escoge el tamaño del tablero (3-9): ")

        # Verifica si la entrada es un número
        if entrada.isdigit():
            numero = int(entrada)
            print("\n")
            if numero in [3, 4, 5, 6, 7, 8, 9]:
                break
            else:
                print("Por favor, elige uno de los tamaños RECOMENDADOS (4, 6, 8, 9).\n")
        else:
            print("Por favor, ingresa un número válido.\n")

    tablero_sudoku = crear_sudoku_aleatorio(numero)
   
    print("\n")
    tablero_verificar = copy.deepcopy(tablero_sudoku)
    tablero_kakuro = crear_tablero_kakuro_aleatorio(tablero_sudoku, numero)
   
    reemplazar_numeros_con_vacios(tablero_kakuro)
    while True:
        imprimir_tablero(tablero_kakuro)
        print("\n")
        llenar_tablero(tablero_kakuro, tablero_verificar)
        
        if verificar_tablero(tablero_kakuro, tablero_verificar):
            print("¡El tablero está correcto!")
            break
        else:
            print("El tablero no está correcto.")
            continuar = input("¿Deseas continuar? (S/n): ")
            if continuar.lower() == 'n':
                break
    
    print("Gracias por usar Kakuro.")
            








