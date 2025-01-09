#Thư viện
import pygame
import math
import random
pygame.init ()

game_play=True

#Tiêu đề và icon cho game
pygame.display.set_caption('Game bắn súng tọa độ')
icon=pygame.image.load(r'image/Player.png')
pygame.display.set_icon(icon)

#Thêm background và địa hình cho game
bg=pygame.image.load(r'image/Background.png')
bg=pygame.transform.scale2x(bg)

bg1=pygame.image.load(r'image/Mặt đất.png')
bg1=pygame.transform.scale2x(bg1)
bg1_rect=bg1.get_rect(bottomleft=(0,600))

#Thông báo của game
over=pygame.image.load(r'image/thông báo game over.png')
over=pygame.transform.scale2x(over)
over_rect=bg1.get_rect(center=(480,100))

win=pygame.image.load(r'image/thông báo win.png')
win=pygame.transform.scale2x(win)
win_rect=win.get_rect(center=(480,200))

#Chỉ số player
hp_player = 1000
atk_player = 300

#Chỉ số kẻ thù
hp_enemy = 900
atk_enemy = 200

game_play = False

#Người chơi
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image=pygame.image.load(r'image/Player.png')
        self.image=pygame.transform.scale2x(self.image)
        self.rect=self.image.get_rect(center=(100,200))
        
        self.hp = hp_player
        self.atk = atk_player
            
    def update(self, mouse_pos):
        dx = mouse_pos[0] - self.rect.centerx
        dy = mouse_pos[1] - self.rect.centery
        self.angle = math.degrees(math.atan2(dy, dx))   
            
    def check_pl(self, v_p):
        if self.rect.bottom >= bg1_rect.top:
            self.rect.bottom == bg1_rect.top
            v_p = 0
        else:
            self.rect.y+=v_p
            v_p+=p_p
        return self.rect.y, v_p
    
    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 5
        border_thickness = 2

        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.bottom + 5
        health_ratio = self.hp / hp_player
        
        pygame.draw.rect(
        screen, 
        (0, 0, 0), 
        (bar_x - border_thickness, 
         bar_y - border_thickness, 
         bar_width + 2 * border_thickness, 
         bar_height + 2 * border_thickness)
        )

        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))
    
#Kẻ thù
class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image=pygame.image.load(r'image/Enemy.png')
        self.image=pygame.transform.scale2x(self.image)
        random_x = random.randint(300, W - 50)
        self.rect=self.image.get_rect(center=(random_x,200))
        
        self.hp = hp_enemy
        self.atk = atk_enemy
        
        self.player = player
        self.move_distance = 0
        self.move_step = random.randint(50,150)
        self.attacked_count = 0
        self.move_speed = 1
        self.move = True

    def check_en(self, v_e):
        if  self.rect.bottom >= bg1_rect.top:
            self.rect.bottom = bg1_rect.top
            v_e = 0
        else:
            self.rect.y+=v_e
            v_e+=p_e
        return  self.rect.y, v_e
    
    def move_and_attack(self):
        dx = players.rect.centerx - self.rect.centerx
        dy = players.rect.centery - self.rect.centery
        distance = math.sqrt(dx**2 + dy**2)
        
        if distance > 50:
            dx /= distance
            dy /= distance
            
            if self.move_distance < self.move_step:
                self.rect.x += dx * self.move_speed
                self.rect.y += dy * self.move_speed
                self.move_distance += self.move_speed
                print(self.move_distance)
            else:
                self.move = False
                            
        elif distance <=50:           
            if self.attacked_count < 1:
                players.hp -= self.atk
                print(players.hp)
                if players.hp <= 0:
                    players.kill()
                self.attacked_count += 1
            else:
                self.move = False
    
    def draw_health_bar(self, screen):
        bar_width = 50
        bar_height = 5
        border_thickness = 2

        bar_x = self.rect.centerx - bar_width // 2
        bar_y = self.rect.bottom + 5
        health_ratio = self.hp / hp_enemy
        
        pygame.draw.rect(
        screen, 
        (0, 0, 0), 
        (bar_x - border_thickness, 
         bar_y - border_thickness, 
         bar_width + 2 * border_thickness, 
         bar_height + 2 * border_thickness)
        )

        pygame.draw.rect(screen, (255, 0, 0), (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(screen, (0, 255, 0), (bar_x, bar_y, bar_width * health_ratio, bar_height))
        
#Đạn
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image=pygame.image.load(r'image/bullet.png')
        self.image=pygame.transform.scale2x(self.image)
        self.rect=self.image.get_rect(center = (x, y))
        
        self.angle = math.radians(angle)
        self.speed = 10
        self.vx = self.speed * math.cos(self.angle)
        self.vy = self.speed * math.sin(self.angle)
        self.gravity = 0.1

    def update(self):
        self.vy += self.gravity
        
        self.rect.x += self.vx
        self.rect.y += self.vy

        if self.rect.bottom < 0 or self.rect.top > H or self.rect.left < 0 or self.rect.right > W:
            self.kill()
            
        if self.rect.bottom >= bg1_rect.top:
            self.kill()
        
        hit_enemies = pygame.sprite.spritecollide(self, enemy_group, False)    
        if hit_enemies:
            for enemies in hit_enemies:
                enemies.hp -= players.atk
                print(enemies.hp)
                if enemies.hp <= 0:
                    enemies.kill()
            self.kill()

#Hàm
def draw_simulated_trajectory(screen, x, y, angle):

    speed = 10
    gravity = 0.1
    time_step = 0.1
    trajectory = []
    
    vx = speed * math.cos(math.radians(angle))
    vy = speed * math.sin(math.radians(angle))
    
    while y < H:
        x += vx * time_step
        y += vy * time_step
        vy += gravity * time_step
        
        trajectory.append((x, y))
        
        if x < 0 or x > W or y > H:
            break
        
        if y >= bg1_rect.top:
            trajectory.append((x, bg1_rect.top))
            break
        
    for point in trajectory:
        pygame.draw.circle(screen, (0, 0, 255), (int(point[0]), int(point[1])), 2)
        
#Cửa sổ game
W, H = 960, 600
screen=pygame.display.set_mode((W,H))

#Khởi tạo đối tượng
players = Player()
player_group = pygame.sprite.Group()
player_group.add(players)

num_enemies = 0
enemy_group = pygame.sprite.Group()
for _ in range(num_enemies):
    enemies = Enemy(players)
    enemy_group.add(enemies)

bullet_group = pygame.sprite.Group()

#Hằng trọng lực
p_p = 0.5
p_e = 0.25

#Tốc độ rơi
v_p = 0
v_e = 0

#lượt đấu
font = pygame.font.Font(None, 36)
turn = 'player'

turn_delay_time = 3000
last_turn_end_time = 0

level = 0
dead = 0

#Vòng lặp xử lí game
running = True

while  running:
    current_time = pygame.time.get_ticks()
    mouse_pos = pygame.mouse.get_pos()
    
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and turn == 'player':
                bullets = Bullet(players.rect.centerx, players.rect.centery, players.angle)
                bullet_group.add(bullets)
                turn = 'enemy'
                last_turn_end_time = current_time 
                
    screen.fill((255, 255, 255))  
    screen.blit(bg,(0,0))
    screen.blit(bg1,bg1_rect)
    
    turn_text = font.render(f"Turn: ", True, (0, 0, 0))
    turn_part = font.render(f"{turn.capitalize()}", True, (255, 0, 0))
    level_text = font.render(f"Level: ", True, (0, 0, 0))
    level_part = font.render(f" {level}", True, (255, 0, 0))
    start_text = font.render(f"Press right mouse to start a game", True, (255, 0, 0))
    again_text = font.render(f"Press right mouse to play again", True, (255, 0, 0))

    if game_play:
        if players.hp <= 0:
            game_play = False
            dead += 1      
        elif len(enemy_group) == 0:
            if level > 3:
                screen.blit(win, win_rect)
                screen.blit(again_text, (250, 360))
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 3:
                        game_play = True
            else:
                level += 1
                num_enemies += 1
                for _ in range(num_enemies):
                    enemies = Enemy(players)
                    enemy_group.add(enemies)
                turn = 'player'
        else:
            screen.blit(turn_text, (10, 10))
            screen.blit(turn_part, (75, 10))
            screen.blit(level_text, (10, 50))
            screen.blit(level_part, (80, 50))
            if turn == 'player':
                players.update(mouse_pos)
                draw_simulated_trajectory(screen, players.rect.centerx, players.rect.centery, players.angle)
                for enemies in enemy_group:
                    enemies.move_distance = 0
                    enemies.attacked_count = 0
                    enemies.move_step = random.randint(50, 100)
                    enemies.move = True
                                              
            if turn == 'enemy':
                if current_time - last_turn_end_time >= turn_delay_time:
                    if enemies.move:
                        for enemies in enemy_group:
                            enemies.move_and_attack()
                    else:
                        turn = 'player'
                        last_turn_end_time = current_time
    else:
        if dead >= 1:
            screen.blit(over, over_rect)
            screen.blit(again_text, (250, 200))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    game_play = True
        else:
            screen.blit(start_text, (250, 250))
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 3:
                    game_play = True
            
    bullet_group.update()
           
    players.rect.y, v_p = players.check_pl(v_p)
    players.draw_health_bar(screen)
    for enemy in enemy_group:
        enemy.rect.y, v_e = enemy.check_en(v_e)
        enemy.draw_health_bar(screen)
            
    enemy_group.draw(screen)    
    player_group.draw(screen)
    bullet_group.draw(screen)

    pygame.display.update()