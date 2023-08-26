import pygame
import random
import time

# Inicialização do Pygame
pygame.init()

# Configurações da janela
window_size = 1000
window = pygame.display.set_mode((window_size, window_size))
pygame.display.set_caption("Labirinto Aleatório (Busca em Profundidade)")

Kdiv = 2
cuboTamX = 50 // Kdiv
cuboTamY = 50 // Kdiv
cuboX = (window_size - cuboTamX)//2
cuboY = window_size - cuboTamY - 10
velCubo = 1
cubo_image_original = pygame.image.load("images/cubo.png")
novo_tamanho = (cubo_image_original.get_width() // Kdiv, cubo_image_original.get_height() // Kdiv)

# Cores
red = (255, 0, 0)
black = (0, 0, 0)
white = (255, 255, 255)
rngcolor = (random.randint(1, 254), random.randint(1, 254), random.randint(1, 254))

# Tamanho da célula do labirinto
cell_size = 25


# Tamanho total do quadrado do labirinto
maze_square_size = 825

# Ajustar as dimensões do labirinto para caber no quadrado
maze_rows = maze_square_size // cell_size
maze_cols = maze_square_size // cell_size

# Centralizar o labirinto na tela
start_row = (maze_rows-2) // 2
start_col = (maze_cols-2) // 2

# Calcular o deslocamento horizontal para centralizar o labirinto
horizontal_offset = (window_size - (maze_cols * cell_size)) // 2

# Calcular o deslocamento vertical para centralizar o labirinto
vertical_offset = (window_size - (maze_rows * cell_size)) // 2

# Função para criar uma matriz vazia
def create_empty_matrix(rows, cols):
    return [[0 for _ in range(cols)] for _ in range(rows)]

# Função para gerar o labirinto usando1busca em profundidade
def generate_maze_dfs(matrix, row, col):
    matrix[row][col] = 1
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    random.shuffle(directions)
    for dr, dc in directions:
        new_row, new_col = row + 2 * dr, col + 2 * dc
        if 0 <= new_row < maze_rows and 0 <= new_col < maze_cols and matrix[new_row][new_col] == 0:
            matrix[row + dr][col + dc] = 1
            generate_maze_dfs(matrix, new_row, new_col)

# Criar uma matriz vazia para o labirinto
maze = create_empty_matrix(maze_rows, maze_cols)

# Iniciar a geração do labirinto a partir do centro
generate_maze_dfs(maze, start_row, start_col)

# Definir a posição da saída na última coluna e na última linha
exit_row = 0
exit_col = maze_cols - 2
maze[exit_row][exit_col] = 1

exitPosx = exit_col * cell_size + horizontal_offset
exitPosy = exit_row * cell_size + vertical_offset - 12

#Posição inicial do cubo
element_row = maze_rows - 2
element_col = maze_cols - 32

element_global_x = element_col * cell_size + horizontal_offset
element_global_y = element_row * cell_size + vertical_offset - 12

Kdiv = 2
cuboTamX = 50// Kdiv
cuboTamY = 50 // Kdiv
cuboX = element_global_x
cuboY = element_global_y
velCubo = 1
cubo_image_original = pygame.image.load("images/cubo.png")
novo_tamanho = (cubo_image_original.get_width() // Kdiv, cubo_image_original.get_height() // Kdiv)

# Variável para controle do tempo
next_maze_time = time.time()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Movimentação do cubo
    keys = pygame.key.get_pressed()
    cubo_image = pygame.transform.scale(cubo_image_original, novo_tamanho)
    cubo_image_original = pygame.image.load("images/cubo.png")
    if keys[pygame.K_a]:
        cuboX -= velCubo
        cubo_image_original = pygame.image.load("images/esquerda.png")
    if keys[pygame.K_d]:
        cuboX += velCubo
        cubo_image_original = pygame.image.load("images/direita.png")
    if keys[pygame.K_w]:
        cuboY -= velCubo
        cubo_image_original = pygame.image.load("images/cima.png")
    if keys[pygame.K_s]:
        cuboY += velCubo
        cubo_image_original = pygame.image.load("images/baixo.png")
    cuboX = max(0, min(cuboX, window_size - cuboTamX))
    cuboY = max(0, min(cuboY, window_size - cuboTamY))

    if cuboX == exitPosx and cuboY == exitPosy:
        maze = create_empty_matrix(maze_rows, maze_cols)
        generate_maze_dfs(maze, start_row, start_col)
        exit_row = 0
        exit_col = maze_cols - 2
        maze[exit_row][exit_col] = 1
        cuboX = element_global_x
        cuboY = element_global_y

    window.fill(white)

    for row in range(maze_rows):
        for col in range(maze_cols):
            if maze[row][col] == 1:
                # Ajustar as coordenadas x multiplicando por cell_size, adicionando o deslocamento horizontal e centralizando verticalmente
                x = col * cell_size + horizontal_offset
                y = row * cell_size + vertical_offset

                # Centralizar verticalmente subtraindo half_cell_size da coordenada y
                half_cell_size = cell_size // 2
                y -= half_cell_size

                pygame.draw.rect(window, white, (x, y, cell_size, cell_size))
            else:
                x = col * cell_size + horizontal_offset
                y = row * cell_size + vertical_offset
                half_cell_size = cell_size // 2
                y -= half_cell_size
                pygame.draw.rect(window, black, (x, y, cell_size, cell_size))  # Pintar as áreas não visitadas
    #desenhar saída
    pygame.draw.rect(window, red, (exitPosx, exitPosy, cuboTamX, cuboTamY))
    #desenhar cubo
    pygame.draw.rect(window, rngcolor, (cuboX, cuboY, cuboTamX, cuboTamY))
    #desenhar spawn
    pygame.draw.rect(window, rngcolor, (element_global_x, element_global_y, cuboTamX, cuboTamY))
    window.blit(cubo_image, (cuboX, cuboY))
    pygame.display.flip()


# Encerrar o Pygame
pygame.quit()