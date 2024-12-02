import pygame
import heapq
import time
import random

# Inicializar o Pygame
pygame.init()

# Configurações da janela (tamanho da tela ajustado para 30x30)
WIDTH, HEIGHT = 600, 600  # Ajustando a janela para caber o mapa 30x30
ROWS, COLS = 30, 30  # Tamanho da grade para 30x30 células
CELL_SIZE = WIDTH // COLS  # Ajuste automático do tamanho da célula

WHITE, BLACK, RED, GREEN, BLUE, GREY = (255, 255, 255), (0, 0, 0), (255, 0, 0), (0, 255, 0), (0, 0, 255), (200, 200, 200)

# Inicializar a tela
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dijkstra with Random and Predefined Maps")

# Fonte para mensagens
font = pygame.font.Font(None, 36)

# Variáveis globais para início e fim
start = None
end = None

# Gerar grade aleatória 
def generate_random_grid(rows, cols):
    grid = []
    for i in range(rows):
        row = []
        for j in range(cols):
            if random.random() < 0.2:  # 20% de chance de ser um obstáculo
                row.append(-1)
            else:
                row.append(random.randint(1, 10))  # Pesos entre 1 e 10
        grid.append(row)
    return grid

def generate_predefined_grid():
    # Criar um mapa inicial com todas as células como obstáculos
    grid = [[-1] * COLS for _ in range(ROWS)]

    # Criar o ponto de entrada único (início compartilhado na coluna 0)
    grid[20][0] = 1
    grid[19][0] = 1
    grid[18][0] = 1
    grid[17][0] = 1
    grid[16][0] = 1
    grid[15][0] = 1 
    grid[14][0] = 1
    grid[13][0] = 1
    grid[12][0] = 1
    grid[11][0] = 1
    grid[10][0] = 1

    # Criar a divisão das três pistas nas colunas de 1 a 4
    for col in range(1, 5):
        grid[10][col] = random.randint(2, 5)  # Linha superior (pista 1)
        grid[15][col] = random.randint(1, 3)  # Linha do meio (pista 2)
        grid[20][col] = random.randint(4, 7)  # Linha inferior (pista 3)

    # Criar as três pistas paralelas nas colunas de 5 a 23
    for col in range(5, 24):
        grid[10][col] = random.randint(2, 5)  # Linha superior (pista 1)
        grid[15][col] = random.randint(1, 3)  # Linha do meio (pista 2)
        grid[20][col] = random.randint(4, 7)  # Linha inferior (pista 3)

    # Convergir todas as pistas para a coluna 25
    for row in range(10, 21):  # Linhas entre 10 e 20 convergem gradualmente
        grid[row][24] = random.randint(1, 3)  # Ajuste antes da convergência

    # Ajustar o ponto de convergência final (linha 15, coluna 25)
    for col in range(24, 26):
        grid[15][col] = 1  # Convergência no ponto final (coluna 25, linha central)

    return grid






# Inicializar a grade com o mapa aleatório
grid = generate_random_grid(ROWS, COLS)

# Função para desenhar a grade
def draw_grid():
    for row in range(ROWS):
        for col in range(COLS):
            rect = pygame.Rect(col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            if grid[row][col] == -1:
                color = BLACK  # Obstáculo
            elif start == (row, col):
                color = RED  # Ponto inicial
            elif end == (row, col):
                color = BLUE  # Ponto final
            else:
                weight = grid[row][col]
                intensity = 255 - (weight - 1) * 20  # Ajustar a intensidade da cor
                color = (intensity, intensity, intensity)  # Tons de cinza
            pygame.draw.rect(screen, color, rect)
            pygame.draw.rect(screen, GREY, rect, 1)

# Função para desenhar o caminho final
def draw_path(path):
    for x, y in path:
        rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        pygame.draw.rect(screen, GREEN, rect)
        pygame.draw.rect(screen, GREY, rect, 1)

# Função para exibir mensagens na caixa de diálogo
def show_message_in_box(message, color):
    # Caixa de diálogo
    box_width = WIDTH - 40
    box_height = 60
    box_x = 20
    box_y = HEIGHT - box_height - 20
    pygame.draw.rect(screen, (0, 0, 0), (box_x, box_y, box_width, box_height))  # Caixa de fundo preta
    pygame.draw.rect(screen, GREY, (box_x, box_y, box_width, box_height), 3)  # Borda cinza

    # Texto da mensagem
    text = font.render(message, True, color)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT - 40))
    screen.blit(text, text_rect)

# Função para calcular a posição do clique na grade
def get_cell_from_mouse(pos):
    x, y = pos
    row = x // CELL_SIZE
    col = y // CELL_SIZE
    return (col, row)  # Inverter para (linha, coluna)

# Algoritmo de Dijkstra com visualização do percurso
def dijkstra_visualized(start, end):
    pq = []
    heapq.heappush(pq, (0, start))
    distances = {start: 0}
    parents = {start: None}
    visited = set()

    while pq:
        cost, current = heapq.heappop(pq)
        if current in visited:
            continue
        visited.add(current)

        # Visualizar cada célula visitada durante o processo
        draw_grid()
        for visited_cell in visited:
            rect = pygame.Rect(visited_cell[1] * CELL_SIZE, visited_cell[0] * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, (200, 200, 0), rect)  # Cor amarela para as células visitadas
            pygame.draw.rect(screen, GREY, rect, 1)
        pygame.display.update()
        time.sleep(0.05)  # Controla a velocidade de visualização da busca

        if current == end:
            break

        x, y = current
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < ROWS and 0 <= ny < COLS and grid[nx][ny] != -1:
                new_cost = cost + grid[nx][ny]
                if (nx, ny) not in distances or new_cost < distances[(nx, ny)]:
                    distances[(nx, ny)] = new_cost
                    parents[(nx, ny)] = current
                    heapq.heappush(pq, (new_cost, (nx, ny)))

    # Verificar se o ponto final é alcançável
    if end not in parents:
        return None

    # Reconstruir o caminho
    path = []
    current = end
    while current is not None:
        path.append(current)
        current = parents.get(current)
    path.reverse()
    return path

# Função para mover o personagem
def move_character(path):
    for pos in path:
        x, y = pos
        rect = pygame.Rect(y * CELL_SIZE, x * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        draw_grid()
        draw_path(path)  # Mostrar o caminho enquanto o personagem anda
        pygame.draw.circle(screen, RED, (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2), CELL_SIZE // 3)
        pygame.display.update()
        time.sleep(0.1)

# Loop principal
running = True
path = []
path_not_found = False
use_predefined = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:  # Clique do mouse
            pos = pygame.mouse.get_pos()
            cell = get_cell_from_mouse(pos)
            if grid[cell[0]][cell[1]] != -1:  # Apenas em células livres
                if not start:
                    start = cell
                elif not end:
                    end = cell
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and start and end:  # Calcula o caminho
                path = dijkstra_visualized(start, end)
                path_not_found = path is None
            if event.key == pygame.K_RETURN and path and not path_not_found:  # Move o bonequinho
                move_character(path)
            if event.key == pygame.K_r:  # Pressionar R para gerar nova grade aleatória
                grid = generate_random_grid(ROWS, COLS)
                start, end, path = None, None, []
                path_not_found = False
                use_predefined = False
            if event.key == pygame.K_p:  # Pressionar P para usar o mapa predefinido
                grid = generate_predefined_grid()
                start, end, path = None, None, []
                path_not_found = False
                use_predefined = True

    screen.fill(BLACK)
    draw_grid()
    if path:
        draw_path(path)
    
    # Exibir mensagens
    if path_not_found:
        show_message_in_box("Caminho impossível de alcançar!", BLUE)
    elif path:
        show_message_in_box("Parabéns! Caminho encontrado!", GREEN)
    elif use_predefined:
        show_message_in_box("Usando o mapa predefinido!", WHITE)

    pygame.display.flip()

pygame.quit()
