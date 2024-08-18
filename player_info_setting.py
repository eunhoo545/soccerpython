import pygame
import sys
import time
# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pygame Dropdown Menu Example")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)

# 폰트 설정
font = pygame.font.Font(None, 32)

# 드롭다운 설정
option = ["1", "2", "3","4","5"]
options = []
dropdowns= []
for i in range(3):
     dropdown_rect = pygame.Rect(500, 30+(i*50), 140, 32)
     dropdowns.append(dropdown_rect)

for k in range(3):
    a = []
    for j in range(5):
        option_rect = pygame.Rect(500,62+(j*32)+(k*50),140,32)
        a.append(option_rect)
    options.append(a)

print(options)
active = [False,False,False]

color_inactive = GRAY
color_active = BLACK
color = color_inactive
selected_option = options[0]
font = pygame.font.Font(None, 32)

done = False
while not done:
    screen.fill((0,0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(dropdowns)):
                if dropdowns[i].collidepoint(event.pos):
                    active[i] = True
                else:
                    active[i] = False
    for dropdown in dropdowns: 
        pygame.draw.rect(screen,BLUE,dropdown)
    for i in range(3):
        if active[i] == True:        
            lst = options[i]
            for option_rect in lst:
                pygame.draw.rect(screen,WHITE,option_rect)
    #print(active)
    pygame.display.flip()
    pygame.time.Clock().tick(30)

pygame.quit()
sys.exit()
