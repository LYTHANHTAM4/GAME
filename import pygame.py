import pygame
import random

# Khởi tạo Pygame
pygame.init()

# Kích thước cửa sổ
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Turn-based Combat Game")

# Màu sắc
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Lớp nhân vật
class Character:
    def __init__(self, name, health, attack, defense):
        self.name = name
        self.health = health
        self.attack = attack
        self.defense = defense
        self.is_alive = True
    
    def take_damage(self, damage):
        if self.health - damage > 0:
            self.health -= damage
        else:
            self.health = 0
            self.is_alive = False

    def attack_enemy(self, enemy):
        damage = random.randint(self.attack - 5, self.attack + 5) - enemy.defense
        if damage < 0:
            damage = 0
        enemy.take_damage(damage)
        return damage

    def heal(self, amount):
        if self.health + amount <= 100:
            self.health += amount
        else:
            self.health = 100

    def get_status(self):
        return f"{self.name}: HP {self.health}/100"

# Tạo các nhân vật
player = Character("Player", 100, 20, 5)
enemy = Character("Enemy", 100, 15, 4)

# Hàm hiển thị thông tin
def display_battle():
    screen.fill(WHITE)
    font = pygame.font.SysFont("Arial", 24)

    player_status = font.render(player.get_status(), True, BLACK)
    enemy_status = font.render(enemy.get_status(), True, BLACK)

    screen.blit(player_status, (20, 20))
    screen.blit(enemy_status, (20, 60))

    pygame.display.flip()

# Vòng lặp game
running = True
turn = "player"
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if player.is_alive and enemy.is_alive:
        if turn == "player":
            display_battle()
            font = pygame.font.SysFont("Arial", 32)
            action_text = font.render("Press 'a' to attack or 'h' to heal", True, BLACK)
            screen.blit(action_text, (20, 100))
            pygame.display.flip()

            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                damage = player.attack_enemy(enemy)
                print(f"{player.name} attacks {enemy.name} for {damage} damage!")
                turn = "enemy"
            elif keys[pygame.K_h]:
                player.heal(20)
                print(f"{player.name} heals for 20 HP!")
                turn = "enemy"
        
        elif turn == "enemy":
            display_battle()
            pygame.display.flip()
            pygame.time.delay(1000)  # Chờ 1 giây cho hành động của enemy
            action = random.choice(["attack", "heal"])

            if action == "attack":
                damage = enemy.attack_enemy(player)
                print(f"{enemy.name} attacks {player.name} for {damage} damage!")
            elif action == "heal":
                enemy.heal(15)
                print(f"{enemy.name} heals for 15 HP!")

            turn = "player"

        # Kiểm tra kết thúc trò chơi
        if not player.is_alive:
            print("Player has been defeated!")
            running = False
        elif not enemy.is_alive:
            print("Enemy has been defeated!")
            running = False

    pygame.time.delay(100)  # Làm cho vòng lặp game mượt mà hơn

# Thoát Pygame
pygame.quit()
