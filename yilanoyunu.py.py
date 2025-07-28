import pygame
import random

# ---------- Ayarlar ----------
pygame.init()
WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 20
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Seviye Sistemi & Labirentli Yılan Oyunu")
CLOCK = pygame.time.Clock()
FPS = 10

# Renkler
WHITE = (255,255,255)
BLUE = (0, 0, 255)

# Metin fontu
font = pygame.font.SysFont('arial', 24)

# Görseller
def load_and_scale(path):
    try:
        img = pygame.image.load(path)
        return pygame.transform.scale(img, (BLOCK_SIZE, BLOCK_SIZE))
    except:
        return None

apple_img = load_and_scale("apple.png")
brick_img = load_and_scale("brick.png")

# ---------- Level Haritaları ----------
levels = [
    [],  # Level 1 – boş
    [(WIDTH//2, HEIGHT//2)],  # Level 2 – ortada 1 taş
    [(x, HEIGHT//2) for x in range(200, 400, BLOCK_SIZE)],  # Level 3
    [(WIDTH//3, y) for y in range(0, HEIGHT, BLOCK_SIZE)],  # Level 4
    [(x,200) for x in range(100,500,BLOCK_SIZE)] + [(x,400) for x in range(100,500,BLOCK_SIZE)],  #5
    [(300,y) for y in range(100,500,BLOCK_SIZE) if y!=300],  #6
    [(x,y) for x in range(100,500,60) for y in range(100,500,60)],  #7
    [(WIDTH//2,y) for y in range(0,HEIGHT,BLOCK_SIZE)] + [(x,HEIGHT//2) for x in range(0,WIDTH,BLOCK_SIZE)],  #8
    [(x,y) for x in range(100,500,40) for y in range(100,500,40) if (x+y)%80!=0],  #9
    [(x,y) for x in range(0,WIDTH,BLOCK_SIZE) for y in range(0,HEIGHT,BLOCK_SIZE) if x%120==0 and y%120==0]  #10
]

level_index = 0
score = 0
high_score = 0

# Yılan & Yem ayarları
snake = [(WIDTH//2, HEIGHT//2)]
snake_dir = "RIGHT"
next_dir = "RIGHT"

def spawn_food():
    while True:
        pos = (random.randrange(0,WIDTH//BLOCK_SIZE)*BLOCK_SIZE,
               random.randrange(0,HEIGHT//BLOCK_SIZE)*BLOCK_SIZE)
        if pos not in snake and pos not in levels[level_index]:
            return pos

food = spawn_food()

# ---------- Yardımcı Fonksiyonlar ----------
def draw_background():
    c1, c2 = (170,215,81),(162,209,73)
    for y in range(0,HEIGHT,BLOCK_SIZE):
        for x in range(0,WIDTH,BLOCK_SIZE):
            clr = c1 if (x//BLOCK_SIZE+y//BLOCK_SIZE)%2==0 else c2
            pygame.draw.rect(SCREEN,clr,pygame.Rect(x,y,BLOCK_SIZE,BLOCK_SIZE))

def draw_obstacles():
    for obs in levels[level_index]:
        if brick_img:
            SCREEN.blit(brick_img, obs)
        else:
            pygame.draw.rect(SCREEN,(100,100,100),pygame.Rect(obs[0],obs[1],BLOCK_SIZE,BLOCK_SIZE))

def game_over():
    global snake, snake_dir, next_dir, food, high_score, score, level_index
    if score > high_score:
        high_score = score
    msg = pygame.font.SysFont('arial',48).render("OYUN BİTTİ!", True, (255,0,0))
    sub = pygame.font.SysFont('arial',28).render("Bir tuşa bas = yeniden!", True, WHITE)
    SCREEN.fill((0,0,0))
    SCREEN.blit(msg, msg.get_rect(center=(WIDTH//2,HEIGHT//2-30)))
    SCREEN.blit(sub, sub.get_rect(center=(WIDTH//2,HEIGHT//2+20)))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type==pygame.QUIT:
                pygame.quit(); exit()
            if e.type==pygame.KEYDOWN:
                score=0
                level_index=0
                snake=[(WIDTH//2,HEIGHT//2)]
                snake_dir=next_dir="RIGHT"
                food = spawn_food()
                return

# ---------- Oyun Döngüsü ----------
running = True
while running:
    # Olaylar
    for e in pygame.event.get():
        if e.type==pygame.QUIT:
            running=False
        if e.type==pygame.KEYDOWN:
            if e.key in [pygame.K_UP,pygame.K_w]: next_dir="UP"
            if e.key in [pygame.K_DOWN,pygame.K_s]: next_dir="DOWN"
            if e.key in [pygame.K_LEFT,pygame.K_a]: next_dir="LEFT"
            if e.key in [pygame.K_RIGHT,pygame.K_d]: next_dir="RIGHT"
    # Yön kısıtı
    if next_dir=="UP" and snake_dir!="DOWN": snake_dir="UP"
    if next_dir=="DOWN" and snake_dir!="UP": snake_dir="DOWN"
    if next_dir=="LEFT" and snake_dir!="RIGHT": snake_dir="LEFT"
    if next_dir=="RIGHT" and snake_dir!="LEFT": snake_dir="RIGHT"

    # Yeni baş
    x,y = snake[0]
    if snake_dir=="UP": y-=BLOCK_SIZE
    if snake_dir=="DOWN": y+=BLOCK_SIZE
    if snake_dir=="LEFT": x-=BLOCK_SIZE
    if snake_dir=="RIGHT": x+=BLOCK_SIZE
    new = (x,y)

    # Çarpma kontrolü
    if x<0 or x>=WIDTH or y<0 or y>=HEIGHT or new in snake or new in levels[level_index]:
        game_over()
        continue

    snake.insert(0,new)
    if new==food:
        score+=10
        food = spawn_food()
    else:
        snake.pop()

    # Seviye geçişi
    if score >= (level_index+1)*200 and level_index<9:
        level_index+=1
        snake=[(WIDTH//2,HEIGHT//2)]
        snake_dir=next_dir="RIGHT"
        food = spawn_food()

    # Çizimler
    draw_background()
    draw_obstacles()
    if apple_img:
        SCREEN.blit(apple_img, food)
    else:
        pygame.draw.rect(SCREEN,(255,0,0),pygame.Rect(food[0],food[1],BLOCK_SIZE,BLOCK_SIZE))
    for i,seg in enumerate(snake):
        pygame.draw.rect(SCREEN, BLUE, pygame.Rect(seg[0],seg[1],BLOCK_SIZE,BLOCK_SIZE))
        if i==0:
            o=5; r=3
            pygame.draw.circle(SCREEN,WHITE,(seg[0]+o,seg[1]+o),r)
            pygame.draw.circle(SCREEN,WHITE,(seg[0]+BLOCK_SIZE-o,seg[1]+o),r)

    # Metin
    SCREEN.blit(font.render(f"Skor: {score}",True,WHITE),(10,10))
    SCREEN.blit(font.render(f"Seviye: {level_index+1}",True,WHITE),(10,40))
    SCREEN.blit(font.render(f"Yüksek Skor: {high_score}",True,WHITE),(10,70))

    pygame.display.flip()
    CLOCK.tick(FPS)

pygame.quit()
