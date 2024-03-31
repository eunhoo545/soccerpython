import pygame
import sys
import math

FPS = 60
MAX_WIDTH = 1000
MAX_HEIGHT = 800
pygame.init()
RED = (255, 0, 0)
clock = pygame.time.Clock()
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT))




def distance(x1, y1, x2, y2):
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5

def main():
    power = 0
    max_power = 20
    ball = Ball(30)
    person = Person(20)
    ball_angle = 0
    power_grow = 0
    m_state = 0
    while True:
        #게임 로직 키 입력 구현
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            person.x -= person.speed
        if keys[pygame.K_d]:
            person.x += person.speed
        if keys[pygame.K_w]:
            person.y -= person.speed
        if keys[pygame.K_s]:
            person.y += person.speed
        if keys[pygame.K_SPACE]:
            power_grow = 1
            power +=1
        if keys[pygame.K_k]:
            ball_angle += math.pi / 18
        if keys[pygame.K_m] and m_state==0:
            ball.x -= 100
            m_state +=1
        if not(keys[pygame.K_SPACE]):
            power_grow = 0
            power = 0

        if m_state != 0:
            m_state +=1
        if m_state == 180:
            m_state = 0

        #공과, 플레이어 사이의 distance구하기
        distance_to_ball = distance(person.x, person.y, ball.x, ball.y)
        print(m_state)

        if distance_to_ball < 50:
            ball_following = True
        else:
            ball_following = False
        
        if ball_following:
            ball.x = person.x + math.cos(ball_angle) * 30 
            ball.y = person.y + math.sin(ball_angle) * 30
        
        #게임 종료 구현(x표시)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        clock.tick(FPS)
        screen.fill((48,131,43))
        pygame.draw.rect(screen, RED, (20, 20, 20, 200))
        pygame.draw.rect(screen, (0,0,0), (20, 220 - (power / max_power) * 200, 20, (power / max_power) * 200))
        ball.draw()
        person.draw()
        pygame.display.update()

 
class Ball():
    def __init__(self,radius):
        self.x = 905
        self.y = 505
        self.radius = radius
        self.speed = 5
    def draw(self):
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.radius)

class Person():
    def __init__(self,radius):
        self.x = 805
        self.y = 505
        self.radius = radius
        self.speed = 5
    def draw(self):
        pygame.draw.circle(screen,(255,0,0),(self.x,self.y),self.radius)        

    
if __name__ == '__main__':
    main()


        
