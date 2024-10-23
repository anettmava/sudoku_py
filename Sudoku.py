import pygame   #Para instalar esta libreria poner pip install pygame en la terminal
import requests   #Para instalar esta libreria poner pip install requests en la terminal

width = 550   #Medida en pixeles
bg_color = (0, 0, 0)  #El color de fondo 
original_grid_element_color = (255, 182, 193) #Color de los números en RGB
buffer = 5

response = requests.get("https://sugoku.onrender.com/board?difficulty=easy")   #Solicita API link de generador de sudoku 
grid = response.json()['board']   #Regresa los datos de los datos en formato json
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]     #Esta variable se usa como comparación y se anota de esta manera para que si se manipula un dato no afecte el otro rango

def is_valid_move(board, row, col, num):   #uFunción para verificar que el número ingresado por el usuario sea el correcto 
    if num in board[row] or num in [board[i][col] for i in range(9)]:     #Revisa si el número ya esta en una columna o fila
        return False
    
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)   #Determina la posición inicial de los recuadros
    for i in range(start_row, start_row + 3):    #Revisa si el número ya esta en el recuadro
        for j in range(start_col, start_col + 3): 
            if board[i][j] == num:
                return False
    
    return True  #Si cumple las condiciones es válido

def insert(win, position): #Función para insertar un número en el tablero
    i, j = position[1] - 1, position[0] - 1  #Ajusta los indices para empezar en 0
    myfont = pygame.font.SysFont('Sans Serif', 35)  #Tipo y tamaño de letra de lo que el usario inserte 

    while True:    #Si se presiona una tecla entra a ese ciclo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  #Si el usario se sale de la ventana
                return   #Sale de la función y termina el programa
            if event.type == pygame.KEYDOWN:  #Si una tecla es presioanda
                if grid_original[i][j] != 0:   #Si la celda es un número original
                    return     #Sale de la función para evitar que se editen los números originales
                if event.unicode.isnumeric():  #Si la tecla presionada es númerica
                    num = int(event.unicode)   #Lo convierte en integer
                    if is_valid_move(grid, i, j, num): #Si es válido el número ingresado por el usuario lo ponen en el trablero
                        pygame.draw.rect(win, bg_color, (position[0]*50 + buffer, position[1]*50 + buffer, 50 - 2*buffer, 50 - 2*buffer))
                        value = myfont.render(str(num), True, (255, 255, 255))
                        win.blit(value, (position[0]*50 + 15, position[1]*50 + 15))
                        grid[i][j] = num    #Pone el número ingresado por el usuario
                        pygame.display.update()
                    return
def display_instructions():  #Función para mandar la pantalla de las instrucciones
    pygame.init()
    instr_width = 400
    instr_height = 200
    instr_win = pygame.display.set_mode((instr_width, instr_height)) #Despliega el tablero del tamaño declarado previamente
    pygame.display.set_caption("Instructions")  #Título de la ventana

    myfont = pygame.font.SysFont('Sans Serif', 25)   #El tipo y tamaño de letra especificada para la ventana
    instructions = [
        "-Welcome to Sudoku!",
        "-Click on a cell to select it.",
        "-Type a number to fill the cell.",
        "-Numbers from the original puzzle",
        " cannot be changed.",
        "-Press 'Esc' to exit the game.",
        "-Press any key to start the game."
    ]

    y_offset = 20
    for line in instructions:
        text = myfont.render(line, True, (255, 182, 193))
        instr_win.blit(text, (20, y_offset))
        y_offset += 20

    pygame.display.update()

    wait = True 
    while wait:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    quit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                    main()

def main():   #Función para iniciar la pantalla del tablero
    pygame.init()
    win = pygame.display.set_mode((width, width)) #Despliega la pantalla segun la medida declarada en "width" 
    pygame.display.set_caption("Sudoku") #El titulo del tablero
    win.fill(bg_color)  #Pone el color de fondo declarado como un valor RGB  
    myfont = pygame.font.SysFont('Sans Serif', 35) #Tipo y tamaño de letra

    #Para dibujar las líneas del tablero
    for i in range(0, 10):
        if i % 3 == 0: #Cada tercer línea se cumple la condición
            pygame.draw.line(win, (255, 255, 255), (50 + 50*i, 50), (50 + 50*i, 500), 6) #Se cambia el ancho de la línea para que parezca en negritas; vertical
            pygame.draw.line(win, (255, 255, 255), (50, 50 + 50*i), (500, 50 + 50*i), 6) #Se cambia el ancho de la línea para que parezca en negritas; horizontal

        pygame.draw.line(win, (255, 255, 255), (50 + 50*i, 50), (50 + 50*i, 500), 2)   #Línea vertical, (win, (color), (coordenadas (x, y) punto inicial linea), (coordenadas (x, y) punto final linea), ancho de línea)
        pygame.draw.line(win, (255, 255, 255), (50, 50 + 50*i), (500, 50 + 50*i), 2)    #Línea horizontal, (win, (color), (coordenadas (x, y) punto inicial linea), (coordenadas (x, y) punto final linea), ancho de línea)
    pygame.display.update()  # Se actualiza y muestra las lineas en el tablero

    for i in range(0, len(grid[0])):
        for j in range(0, len(grid[0])):   #El API link regresa una lista de lista, por lo tanto se usan dos fors para poder recorrer los elemntos de las listas dentro de la lista
            if (0 < grid[i][j] < 10):  #Este rango es de 0 a 10 porque son nueve números
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color)  #Imprime los números la lista solicitada en el API key, con la fuente especificada
                win.blit(value, ((j + 1)*50 + 15, (i+1)*50 + 15 ))   #j es el valor en el x, e i es el valor en el eje y 
    pygame.display.update()

    while True:
        for case in pygame.event.get():
            if case.type == pygame.MOUSEBUTTONUP and case.button == 1:   #Si se da click izquierdo
                pos = pygame.mouse.get_pos()  #Da la posición del mouse 
                insert(win, (pos[0]//50, pos[1]//50))   #Lllma la posición del mouse dentro del tablero
            if case.type == pygame.QUIT:   #Si el usario cierra la ventana 
                pygame.quit()
                return   #Sale del programa
display_instructions()