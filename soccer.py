import pygame
import sys
import time
import math
from map import post1,post2,lines 
from game import throwin,goalkick,kickoff,calculate_angle,distance

FPS = 60
MAX_WIDTH = 1800
MAX_HEIGHT = 1000
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT))
pygame.init()
clock = pygame.time.Clock()
pi = 180
RED = (255,0,0)









class Power():
    def __init__(self, max_power):
        self.power = 0
        self.power_grow = 0
        self.max_power = max_power
        self.power_growing = False
        self.firstpower = 0
#class Map():
def throwin():
    print('throwin')
def goalkick():
    print('goalkick')
def kickoff():
    print('kickoff')

def distance(x1, y1, x2, y2):       #거리계산
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
def calculate_angle(x1, y1, x2, y2):        #각도계산
    return math.atan2(y2 - y1, x2 - x1)

def main():
    hometeam = []
    awayteam = []
    ball_angle = 0
    m_state = 0
    person = Person(15,500,500,'away')
    awayteam.append(person)
    ball = Ball(12)
    power= Power(40)
    person2 = Person(15,800,400,'home')
    hometeam.append(person2)
    person3 = Person(15,1000,200,'home')
    hometeam.append(person3)
    person4 = Person(15,300,200,'away')
    awayteam.append(person4)
    person5 = Person(15,600,700,'home')
    hometeam.append(person5)
    ball_moving = False
    ball_angle = calculate_angle(person.x, person.y, ball.x, ball.y)

    while True:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            person.x -= person.speed
        if keys[pygame.K_d]:
            person.x += person.speed
        if keys[pygame.K_w]:
            person.y -= person.speed
        if keys[pygame.K_s]:
            person.y += person.speed        #플레이어 움직이기
        if keys[pygame.K_SPACE]:
            power.power_grow = 1
            power.power +=1
        if keys[pygame.K_k]:
            ball_angle += math.pi / 18
        if not(keys[pygame.K_SPACE]):
            power.power_grow = 0
            power.power = 0
        if keys[pygame.K_m] and m_state==0:
                    ball.x -= 100
                    m_state +=1

        if m_state != 0:
            m_state +=1
        if m_state == 180:
            m_state = 0
            
          # 플레이어가 공에 가까이 갔는지 확인
        if distance(person.x, person.y, ball.x, ball.y) < ball.radius + person.radius and ball.speed < 3:
            ball_following = True
            ball_angle = calculate_angle(person.x, person.y, ball.x, ball.y)
        else:
            ball_following = False

        # 공이 플레이어를 따라가게
        

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:  #SPACE를 눌러서 파워게이지 증가
                    power.power_growing = True
            if event.type == pygame.KEYUP:     #SPACE를 때면 슛
                if event.key == pygame.K_SPACE and ball_following == True:
                    power.firstpower = (power.power/power.max_power)
                    power.power_growing = False
                    ball_following = False
                    power.power = 0
                    ball_moving = True
                    ball.speed = 5
                
            if power.power_growing and power.power < power.max_power:
                power.power += 0.5
        

        if ball_moving:
            ball.x -= math.cos(ball_angle) * ball.speed *power.firstpower
            ball.y -= math.sin(ball_angle) * ball.speed *power.firstpower
            
            ball.speed *= 0.99  # 공의 속도를 점점 감소시킴
            if ball.speed < 0.2:
                power.firstpower = 0
                ball_moving = False
                ball_following = False
            
    
        
        if ball_following:      #공이 선수한테 붙음
            
            ball.x = person.x + math.cos(ball_angle) * 12 
            ball.y = person.y + math.sin(ball_angle) * 12


        if ball.y <= 70 - ball.radius: #스로인과 골킥 
            ball.y = 70- ball.radius
            ball_moving= False
            ball_following = False
            ball.speed = 0
            throwin()
        if ball.y >= 940 + ball.radius:
            ball.y = 940+ ball.radius
            ball_moving= False
            ball_following = False
            ball.speed = 0
            throwin()

        if ball.x <= 120 - ball.radius:
            if ball.y <350 or ball.y > 650:
                ball.x = 120-ball.radius
                ball_moving= False
                ball_following = False
                ball.speed = 0
                goalkick()
            else:
                print('골1')
                if ball.y <370:
                    ball.y = 370
                if ball.y >630:
                    ball.y = 630
        if ball.x >= 1680 + ball.radius:
            if ball.y <375 or ball.y > 625:
                ball.x = 1680+ball.radius
                ball_moving= False
                ball_following = False
                ball.speed = 0
                goalkick()
            else:
                print('골2')
                if ball.y <370:
                    ball.y = 370
                if ball.y >630:
                    ball.y = 630


        if power.power/power.max_power >= 1:
            power.power = power.max_power          
        clock.tick(FPS)
        screen.fill((48,131,43))
        lines()
        pygame.draw.rect(screen, (0,0,0), (20, 20, 20, 200))
        pygame.draw.rect(screen, RED, (20, 220 - (power.power / power.max_power) * 200, 20, (power.power / power.max_power) * 200))
        person.draw()
        person2.draw()
        person3.draw()
        person4.draw()
        person5.draw()
        ball.draw()
        #Physics.simulate()
        #Player.simulate()
        pygame.draw.line(screen,(255,255,255),(0,5),(30,5),10)
        post1()
        post2()

        pygame.display.update()









class Ball(): #공
    def __init__(self,radius):
        self.x = 905
        self.y = 505
        self.radius = radius
        self.speed = 0
    def draw(self):
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.radius)
    
class Person(): #선수
    def __init__(self,radius,x,y,team):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 2
        self.team = team
    def draw(self):
        if self.team == 'home':
            self.color = (0,0,255)
        if self.team == 'away':
            self.color = (255,0,0)
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)        

    
    
if __name__ == '__main__':
    main()