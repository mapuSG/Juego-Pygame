import pygame
import random

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
screen_width = 800
screen_height = 600

# Colores
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Crear la ventana del juego
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Mi Juego")

clock = pygame.time.Clock()

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50))
        self.image.fill(blue)
        self.rect = self.image.get_rect()
        self.rect.centerx = screen_width // 2
        self.rect.bottom = screen_height - 10
        self.speed_x = 0
        self.score = 0

    def update(self):
        self.speed_x = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.speed_x = -5
        if keys[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > screen_width:
            self.rect.right = screen_width

# Clase del enemigo
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(red)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 3)

# Clase de los amigos
class Friend(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))  # Color verde para los amigos
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, screen_width - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.speed_y = random.randint(1, 3)

    def update(self):
        self.rect.y += self.speed_y
        if self.rect.top > screen_height:
            self.rect.x = random.randint(0, screen_width - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.speed_y = random.randint(1, 3)

# Crear grupos de sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
friends = pygame.sprite.Group()

# Crear jugador
player = Player()
all_sprites.add(player)

# Crear enemigos
for _ in range(20):
    enemy = Enemy()
    all_sprites.add(enemy)
    enemies.add(enemy)

# Crear amigos
for _ in range(15):
    friend = Friend()
    all_sprites.add(friend)
    friends.add(friend)

# Variable para almacenar el estado del juego
game_state = "menu"

# Bucle principal del juego
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Verificar las pulsaciones de teclas solo en el estado de menú
        if game_state == "menu" and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                game_state = "playing"
            elif event.key == pygame.K_2:
                print("Instrucciones: Si pasas por un cuadrado verde, suma puntos. Si pasas por uno rojo, resta puntos.")
            elif event.key == pygame.K_3:
                running = False

    if game_state == "playing":
        # Actualizar
        all_sprites.update()

        # Comprobar colisiones con enemigos
        enemy_collisions = pygame.sprite.spritecollide(player, enemies, True)
        for enemy_collision in enemy_collisions:
            player.score -= 10
            print("Puntuación:", player.score)

        # Comprobar colisiones con amigos
        friend_collisions = pygame.sprite.spritecollide(player, friends, True)
        for friend_collision in friend_collisions:
            player.score += 10
            print("Puntuación:", player.score)

        # Dibujar
        screen.fill(black)
        all_sprites.draw(screen)
        pygame.display.flip()

    elif game_state == "menu":
        # Dibujar el menú en pantalla
        screen.fill(black)
        font = pygame.font.Font(None, 36)
        text1 = font.render("1. Iniciar juego", True, white)
        text2 = font.render("2. Instrucciones", True, white)
        text3 = font.render("3. Cerrar juego", True, white)
        screen.blit(text1, (screen_width // 2 - text1.get_width() // 2, screen_height // 2 - 50))
        screen.blit(text2, (screen_width // 2 - text2.get_width() // 2, screen_height // 2))
        screen.blit(text3, (screen_width // 2 - text3.get_width() // 2, screen_height // 2 + 50))
        pygame.display.flip()

    # Controlar la velocidad de actualización
    clock.tick(60)

# Salir del juego
pygame.quit()
