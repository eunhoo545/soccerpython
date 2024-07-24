import pygame
import sys
import time
import math

from map import lines
from game import throwin,goalkick,kickoff,calculate_angle,distance
import numpy as np
import random
ball_moving = False
ball_angle = 0
current_holder = None
FPS = 60
MAX_WIDTH = 1800
MAX_HEIGHT = 1000
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT))
pygame.init()
clock = pygame.time.Clock()
pi = 180
RED = (255,0,0)

myFont = pygame.font.SysFont( "centurygothic", 15, False, False)
goalpost1 = pygame.image.load('goalpost1.png')
goalpost2 = pygame.image.load('goalpost1.png')


class Agent:
     
    def __init__(self, actions, learning_rate=0.01, discount_factor=0.9, epsilon=0.9):
        
        self.q_table = {}
        self.actions = actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

    def get_state(self, environment):
        # 위치와 속도를 상태로 변환
        state = tuple(environment.get_positions())
        return state

    def choose_action(self, state):
        # 엡실론-탐욕 정책
        if np.random.rand() < self.epsilon:
            #print("90%")
            return np.random.choice(self.actions)
        else:
            #print("10%")
            return max(self.q_table.get(state, {}), key=self.q_table.get(state, {}).get, default=np.random.choice(self.actions))
    
    def learn(self, state, action, reward, next_state):
        # Q-value 업데이트, Q-table 업데이트
        #예를들어서 3,4에 있다고 가정할 때
        #그리고 입력state도 3,4 일 경우
        #print(self.q_table)
        
        
        prev_value = self.q_table.get(state, {}).get(action, 0)
        future_value = max(self.q_table.get(next_state, {}).values(), default=0)
        self.q_table.setdefault(state, {})[action] = prev_value + self.lr * (reward + self.gamma * future_value - prev_value)
        #print(self.q_table)
        
class Environment:
    def __init__(self, hometeam, awayteam, ball):
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.ball = ball

    def get_positions(self):
        # 모든 플레이어와 공의 위치를 반환
        positions = []
        for player in self.hometeam + self.awayteam:
            positions.append(((player.x//100)*100, (player.y//100)*100))
        positions.append(((self.ball.x//100)*100, (self.ball.y//100)*100))
        return positions

    def get_velocities(self):
        # 모든 플레이어의 속도를 추정하는 함수(상태저장에 필요할것 같아서 선언)
        return [0] * (len(self.hometeam) + len(self.awayteam) + 1)  # 간단한 예제로 모두 0으로 설정


#class Power():
#    def __init__(self, max_power):
#        self.power = 20
#        self.power_grow = 0
#        self.max_power = max_power
#        self.power_growing = False
#        self.firstpower = 0
class Map():
    throwin = False
    game = True
    goalkick = False
    cornerkick = False
def throwin(person,ball,y,map):
    time.sleep(1)
    #print('throwin')
    map.throwin = True
    ball.x = ball.x
    ball.y = y- ball.radius
    ball_moving= False
    person.ball_following = False
    ball.speed = 0
    person.x = ball.x
    person.y = ball.y +20
    

def kickoff():
    #print('kickoff')
    time.sleep(1)
def cornerkick():
    #print('cornerkick')
    time.sleep(1)
def pass_completed(hometeam, awayteam):
    # 현재 공을 가진 선수를 찾음

    global teammates
    global current_holder
    #print("CURRENT HOLDER: ", current_holder)
    current_holder = next((player for player in hometeam + awayteam if player.ball_following), None)
    
    # 공을 가진 선수가 없으면 패스는 실패
    if not current_holder:
        return False
    
    # 공을 가진 선수의 팀 동료를 찾음 (같은 팀)
    teammates = [player for player in hometeam if current_holder in hometeam] + \
                [player for player in awayteam if current_holder in awayteam]
    
    #for teammate in teammates:
      #  if teammate != current_holder and distance(current_holder.x, current_holder.y, teammate.x, teammate.y) < 30:
       #     return True
        
    return False
def shoot_completed(hometeam, awayteam):
    

    global current_holder
    #print("CURRENT HOLDER: ", current_holder)
    current_holder = next((player for player in hometeam + awayteam if player.ball_following), None)
    
    
    
   
    
   
        
    return False
def distance(x1, y1, x2, y2):#거리계산
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
def calculate_angle(x1, y1, x2, y2):        #각도계산
    return math.atan2(y2 - y1, x2 - x1)
def calculate_reward(action, environment):
    global current_holder
    current_holder = next((player for player in hometeam + awayteam if player.ball_following), None)
    teammates = [player for player in hometeam if current_holder in hometeam] + \
                [player for player in awayteam if current_holder in awayteam]
    # if action == 'shoot' and goal_scored(environment.ball):
    #     print("Goal scored! Reward: 10")
    #     return 10  # 골을 넣었을 때의 보상
    # if action == 'shoot' and not goal_scored(environment.ball):
    #     #print("Missed shot! Reward: -2")
    #     return -2  # 슛을 쐈으나 골을 놓쳤을 때의 페널티
    if action in ['move_left', 'move_right']:  # 왼쪽 또는 오른쪽으로 이동할 때
        for players in hometeam + awayteam:
            if current_holder is not None:
                if current_holder.team == 'home' and players.team == 'home' and action == 'move_right':
                    return 100
                elif current_holder.team == 'away' and players.team == 'away' and action == 'move_left':
                    return 100 
            else:
                return -90
        
	#calculate reward 함수 안에서..       
    if action == 'intercept' and current_holder is None:
        for player in hometeam + awayteam:
            if player.ball_following:
                if player.team != current_holder.team and distance(player.x, player.y, ball.x, ball.y) < player.radius + ball.radius:
                    return 150
    
    
    if action == 'shoot' and shoot_completed(environment.hometeam, environment.awayteam):
            
        return 35000 
    if action == 'pass' and pass_completed(environment.hometeam, environment.awayteam):
         # 패스가 성공했을 때의 보상
    
        #if current_holder in hometeam:
            #print('red')
            
        #if current_holder in awayteam:
            #print('blue')
            
        return 5000 
    else:
        return -10  #일단 나머지 동작에 대한 패널티
    
    
#이후에 뻇는걸 추가
def setup_teams_and_ball():
    global hometeam
    global awayteam
    # 플레이어 생성
    hometeam = [
        Person(15, 930, 502, 'home', ),
        Person(15, 738, 502, 'home', ),
        Person(15, 690, 684, 'home', ),
        Person(15, 758, 808, 'home', ),
        Person(15, 724, 158, 'home', ),
        Person(15, 600, 310, 'home', ),
        Person(15, 402, 108, 'home', ),
        Person(15, 358, 632, 'home', ),
        Person(15, 318, 388, 'home', ),
        Person(15, 458, 860, 'home', ),
        Person(15, 166, 506, 'home', )
    ]
    awayteam = [
        Person(15, 1030, 396, 'away', ),
        Person(15, 1050, 612, 'away', ),
        Person(15, 1042, 828, 'away', ),
        Person(15, 1082, 204, 'away', ),
        Person(15, 1240, 458, 'away', ),
        Person(15, 1220, 650, 'away', ),
        Person(15, 1362, 864, 'away', ),
        Person(15, 1300, 134, 'away', ),
        Person(15, 1406, 368, 'away', ),
        Person(15, 1446, 670, 'away', ),
        Person(15, 1624, 498, 'away', )
    ]
    
    # 공 생성
    ball = Ball(12)
    
    return hometeam, awayteam, ball
def goal_scored(ball):
    # 골 x좌표 y좌표 값으로 골판단
    goal_y_min = 370 
    goal_y_max = 630 
    home_goal_x = 0 
    away_goal_x = 1800

    # 공의 위치 확인
    if (ball.y >= goal_y_min and ball.y <= goal_y_max):
        if ball.x <= ball.radius + home_goal_x:  # 홈 팀 골 지역에 들어갔는지 확인
            return 'away'  # away 팀이 골을 넣음
        elif ball.x >= away_goal_x - ball.radius:  # 원정 팀 골 지역에 들어갔는지 확인
            return 'home'  # home 팀이 골을 넣음
    return None 





     
def move_towards_ball(player, ball, speed):
    angle = calculate_angle(player.x, player.y, ball.x, ball.y)
    player.x += math.cos(angle) * speed
    player.y += math.sin(angle) * speed     

def main():
    global ball_moving
    global ball_angle
    #person = Person(15,936,502,'home',40)
    agent = Agent(actions=['move_up', 'move_down', 'move_left', 'move_right', 'kick', 'pass', 'search','intercept','shoot'], learning_rate=0.01, discount_factor=0.9, epsilon=0.9)
    homescore = 0
    awayscore = 0
    hometeam = []
    awayteam = []
    hometeam, awayteam, ball = setup_teams_and_ball()
    environment = Environment(hometeam, awayteam, ball)
    
    m_state = 0
    scoretext= myFont.render((str(homescore)+str(' - ')+str(awayscore)), True, (0,0,0))

    ball = Ball(12)
    map = Map()
    f = 0
    while True:
        global current_holder
        if ball.x < 50:
            ball.x = 50
        if ball.x > 1750:
            ball.x = 1750
        if ball.y < 20:
            ball.y = 20
        if ball.y > 980:
            ball.y = 980
        
        for person in hometeam + awayteam:
            if person.x < 50:
                person.x = 50
            if person.x > 1750:
                person.x = 1750
            if person.y < 20:
                person.y = 20
            if person.y > 980:
                person.y = 980
            state = agent.get_state(environment)
            #print(state)
            action = agent.choose_action(state)
            #print(action)
            if action == 'move_up':
                person.moveup()
            elif action == 'move_down':
                person.movedown()
            elif action == 'move_left':
                person.moveleft()
            elif action == 'move_right':
                person.moveright()
            if person.ball_following:
                if action == 'pass':
                    if person.ball_following == True:
                        teammates = [p for p in (hometeam if person in hometeam else awayteam) if p != person]
                        if teammates:
                            #print("pass!!!!")
                            target_player = random.choice(teammates)
                            person.pass1(ball, target_player)
                            #print('pass complete')
                elif action == 'search':
                    #print('search')
                    person.search()
                    # 액션 선택하는 부분 
                elif action == 'shoot':
                    
                    x1 = 0
                    x2 = 0
                    y1 = 0
                    y2 = 0
 
                    if current_holder is not None:    
                        if current_holder.team == 'away':
                            x1 = 18
                            x2 = 111
                            y1 = 354
                            y2 = 657
                        if current_holder.team =='home':
                            x1 = 1691
                            x2 = 1786
                            y1= 354
                            y2 = 657


                        
                        if abs(distance(current_holder.x,current_holder.y, (x1+x2)/2, (y1+y2)/2)) < 500:
                            current_holder.shoot1(ball, x1,x2,y1,y2)
                            print('shoot')
                        #print('pass complete')
            else:
                if action == 'intercept' and current_holder is not None and distance(person.x,person.y,current_holder.x,current_holder.y) < 300:
                    #print("intercept")
                    person.intercept(ball)
            reward = calculate_reward(action, environment)
            next_state = agent.get_state(environment)
            agent.learn(state, action, reward, next_state)
                       

              



        if not any(player.ball_following for player in hometeam + awayteam):  
            # 모든 선수가 공을 따라가지 않을 때 가장 가까운 녀석 찾기
            closest_player = min(hometeam + awayteam, key=lambda p: distance(p.x, p.y, ball.x, ball.y))
            #해당 플레이어가 공을 향해 이동할 수 있게
            move_towards_ball(closest_player, ball, closest_player.speed)

        # 플레이어가 공에 가까이 갔는지 확인
        # 공이 플레이어를 따라가게
        for i in hometeam:
            d = distance(i.x, i.y, ball.x, ball.y)
            if  0 <= d and d < ball.radius + i.radius and ball.speed < 3:
                i.ball_following = True
                
            else:
                i.ball_following = False
        for i in awayteam:
            if distance(i.x, i.y, ball.x, ball.y) < ball.radius + i.radius and ball.speed < 3:
                i.ball_following = True
        
            else:
                i.ball_following = False
        


        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if ball_moving:
            ball.x -= math.cos(ball_angle) * ball.speed *-1
            ball.y -= math.sin(ball_angle) * ball.speed *-1
            ball.speed *= 0.99  # 공의 속도를 점점 감소시킴
            if ball.speed < 0.2:
                #
                # person.power.firstpower = 0
                ball_moving = False
                person.ball_following = False
        for i in hometeam:
            if i.ball_following:      #공이 선수한테 붙음
                ball.x = i.x + math.cos(ball_angle) * 12 
                ball.y = i.y + math.sin(ball_angle) * 12
        for i in awayteam:
            if i.ball_following:      #공이 선수한테 붙음
                ball.x = i.x + math.cos(ball_angle) * 12 
                ball.y = i.y + math.sin(ball_angle) * 12      
        
        
        clock.tick(FPS)
        screen.fill((48,131,43))
        lines()
        #pygame.draw.rect(screen, (0,0,0), (20, 20, 20, 200))
        #pygame.draw.rect(screen, RED, (20, 220 - (person.power.power / person.power.max_power) * 200, 20, (person.power.power / person.power.max_power) * 200))
        person.draw()
        for i in range(len(hometeam)):
            hometeam[i].draw()
            awayteam[i].draw()
        ball.draw(person)
        pygame.draw.line(screen,(255,255,255),(0,5),(30,5),10)
        screen.blit(scoretext, [173, 56])
        pygame.transform.flip(goalpost2, True, False)


        screen.blit(goalpost1, [1300,285])
        screen.blit(goalpost2, [-373,285])
        pygame.display.update()
        if f == 0:
            #print(agent.q_table)
            f = 1


class Ball(): #공
    def __init__(self,radius):
        self.x = 1100
        self.y = 505
        self.radius = radius
        self.speed = 0
    def draw(self,person):
        if person.ball_following == True:
            dx = person.x - self.x
            dy = person.y - self.y
            pygame.draw.circle(screen,(0,0,0),(self.x+(2*dx),self.y+(2*dy)),self.radius)
        else:
            pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.radius)
    
class Person(): #선수
    def __init__(self,radius,x,y,team):
        self.x = x
        self.y = y
        self.radius = radius
        self.speed = 2
        self.team = team
        
        self.ball_following = False
        

    def moveup(self):
        self.y -= self.speed
    def movedown(self):
        self.y += self.speed
    def moveright(self):
        self.x += self.speed
    def moveleft(self):
        self.x -= self.speed

    def search(self):
        global ball_angle
        if self.ball_following:
            ball_angle += pi/1800
        

    def pass1(self, ball, target_player):
        if self.ball_following:
            global ball_moving
            self.search()
            angle = calculate_angle(self.x, self.y, target_player.x, target_player.y)
            angle_ball = calculate_angle(self.x, self.y, ball.x, ball.y)
            angle_difference = abs(angle - angle_ball)
            #print(angle, angle_ball, angle_difference)
            if angle_difference < 0.1:  # 0.1 라디안 이내의 차이를 허용
                self.ball_following = False
                ball_moving = True
                ball.speed = 5
            #self.power.firstpower = 0
            #self.power.power = 0
            #self.power.power_growing = False
    def shoot1(self, ball, x1, x2, y1, y2):
        print(x1,x2,y1,y2)
        if self.ball_following:
            global ball_moving
            angle = calculate_angle(self.x, self.y, (x1+x2)/2, (y1+y2)/2)
            angle_ball = calculate_angle(self.x, self.y, ball.x, ball.y)
            angle_difference = abs(angle - angle_ball)
            #print(angle, angle_ball, angle_difference)
            if angle_difference < 0.2:  # 0.1 라디안 이내의 차이를 허용
                self.ball_following = False
                ball_moving = True
                ball.speed = 7
            #self.power.firstpower = 0
            #self.power.power = 0
            #self.power.power_growing = False

    def calculate_angle(x1, y1, x2, y2): 
        return math.atan2(y2 - y1, x2 - x1)

    def draw(self):
        if self.team == 'home':
            self.color = (255,0,0)
        if self.team == 'away':
            self.color = (0,0,255)
        pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)
    def intercept(self, ball):
        #print(self.team)
        global current_holder
        if current_holder is not None:
            #print(current_holder.team)
            if (not self.ball_following)  and (current_holder is not None) and (self.team != current_holder.team):
                #print("move")
                move_towards_ball(self, ball, self.speed) 
if __name__ == '__main__':
    main()