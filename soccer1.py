import pygame
import sys
import time
import math

import start1
from map import lines
from game import throwin,goalkick,kickoff,calculate_angle,distance
import numpy as np
import random
import pickle  # Q-테이블을 파일로 저장하고 불러오기 위한 모듈


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
X = False
myFont = pygame.font.SysFont( "centurygothic", 15, False, False)
startf = pygame.font.SysFont( "centurygothic", 50, True, False)
goalpost1 = pygame.image.load('goalpost1.png')
goalpost2 = pygame.image.load('goalpost1.png')
#a = pygame.image.load('')


class Agent:

    def __init__(self, actions, learning_rate=0.01, discount_factor=0.9, epsilon=0.9):
        self.q_table = {}
        self.actions = actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

    def get_state(self, environment):
        positions = environment.get_positions()
        return tuple(positions)

    def choose_action(self, state):
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        else:
            return max(self.q_table.get(state, {}), key=self.q_table.get(state, {}).get, default=np.random.choice(self.actions))

    def learn(self, state, action, reward, next_state):
        prev_value = self.q_table.get(state, {}).get(action, 0)
        future_value = max(self.q_table.get(next_state, {}).values(), default=0)
        self.q_table.setdefault(state, {})[action] = prev_value + self.lr * (reward + self.gamma * future_value - prev_value)

    def save_q_table(self, filename):
        with open(filename, 'wb') as f:
            pickle.dump(self.q_table, f)

    def load_q_table(self, filename):
        try:
            with open(filename, 'rb') as f:
                self.q_table = pickle.load(f)
        except FileNotFoundError:
            print(f"File {filename} not found. Starting with an empty Q-table.")


class Environment:
    def __init__(self, hometeam, awayteam, ball):
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.ball = ball

    def get_positions(self):
        players = self.hometeam + self.awayteam
        distances = [(distance(player.x, player.y, self.ball.x, self.ball.y), player) for player in players]
        distances.sort(key=lambda x: x[0])
        closest_players = distances[:3]
        positions = [(player.x // 100 * 100, player.y // 100 * 100) for _, player in closest_players]
        positions.append((self.ball.x // 100 * 100, self.ball.y // 100 * 100))
        return positions



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
    global teammates
    global current_holder
    current_holder = next((player for player in hometeam + awayteam if player.ball_following), None)
    if not current_holder:
        return False
    teammates = [player for player in hometeam if current_holder in hometeam] + \
                [player for player in awayteam if current_holder in awayteam]
    return False


def shoot_completed(hometeam, awayteam):
    global current_holder
    current_holder = next((player for player in hometeam + awayteam if player.ball_following), None)
    return False


def distance(x1, y1, x2, y2):#거리계산
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
def calculate_angle(x1, y1, x2, y2):        #각도계산
    return math.atan2(y2 - y1, x2 - x1)
def calculate_reward(action, environment):
    global current_holder
    current_holder = next((player for player in environment.hometeam + environment.awayteam if player.ball_following), None)
    teammates = [player for player in environment.hometeam if current_holder in environment.hometeam] + \
                [player for player in environment.awayteam if current_holder in environment.awayteam]

    if action in ['move_left', 'move_right']:
        for player in environment.hometeam + environment.awayteam:
            if current_holder is not None:
                if current_holder.team == 'home' and player in environment.hometeam and action == 'move_right':
                    return 10000
                elif current_holder.team == 'away' and player in environment.awayteam and action == 'move_left':
                    return 10000
            else:
                return -9000

    if action == 'intercept' and current_holder is None:
        for player in environment.hometeam + environment.awayteam:
            if player.ball_following:
                if player.team != current_holder.team and distance(player.x, player.y, environment.ball.x, environment.ball.y) < player.radius + environment.ball.radius:
                    return 150

    if action == 'shoot' and shoot_completed(environment.hometeam, environment.awayteam):
        return 150000
    if action == 'pass' and pass_completed(environment.hometeam, environment.awayteam):
        return 1000
    else:
        return -10

    
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
    goal_y_min = 370
    goal_y_max = 630
    home_goal_x = 0
    away_goal_x = 1800

    if (ball.y >= goal_y_min and ball.y <= goal_y_max):
        if ball.x <= ball.radius + home_goal_x:
            return 'away'
        elif ball.x >= away_goal_x - ball.radius:
            return 'home'
    return None




    
     
def move_towards_ball(player, ball, speed):
    angle = calculate_angle(player.x, player.y, ball.x, ball.y)
    player.x += math.cos(angle) * speed
    player.y += math.sin(angle) * speed     
def main():
    global ball_moving
    global ball_angle
    agent = Agent(actions=['move_up', 'move_down', 'move_left', 'move_right', 'kick', 'pass', 'search', 'intercept', 'shoot'], learning_rate=0.01, discount_factor=0.9, epsilon=0.9)
    agent.load_q_table('q_table.pkl')
    homescore = 0
    awayscore = 0
    hometeam = []
    awayteam = []
    hometeam, awayteam, ball = setup_teams_and_ball()
    environment = Environment(hometeam, awayteam, ball)

    scoretext = myFont.render((str(homescore) + str(' - ') + str(awayscore)), True, (0, 0, 0))
    startt = startf.render('test',True,(255,255,255))
    ball = Ball(12)
    map = Map()
    start_time = time.time()
    
    while True:
        if ball.x <= 120 - ball.radius:
            if ball.y <350 or ball.y > 650:
                print('g')
            else:
                print('골1')
                
                awayscore += 1
                
                scoretext= myFont.render((str(homescore)+str(' - ')+str(awayscore)), True, (0,0,0))
                time.sleep(1)
                ball.x = 905
                ball.y = 505
                ball_moving = False
        if ball.x >= 1680 + ball.radius:
            if ball.y <375 or ball.y > 625:
                print('g')
            else:
                homescore += 1
                print('골2')
                scoretext= myFont.render((str(homescore)+str(' - ')+str(awayscore)), True, (59,7,68))
                time.sleep(1)
                ball.x = 905
                ball.y = 505
                ball_moving = False
                if ball.y <370:
                    ball.y = 370
                if ball.y >630:
                    ball.y = 630
        if time.time() - start_time > 120:  # 120초가 지나면 Q-테이블 저장 및 게임 재시작
            agent.save_q_table('q_table.pkl')
            main()
            return
        def game_start():
            if time.time() - start_time > 0:
                return True
            return False
        
        if game_start():
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
                state = agent.get_state(environment)
                action = agent.choose_action(state)
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
                        if person.ball_following:
                            teammates = [p for p in (hometeam if person in hometeam else awayteam) if p != person]
                            if teammates:
                                target_player = random.choice(teammates)
                                person.pass1(ball, target_player)
                    elif action == 'search':
                        person.search()
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
                            if current_holder.team == 'home':
                                x1 = 1691
                                x2 = 1786
                                y1 = 354
                                y2 = 657

                            if abs(distance(current_holder.x, current_holder.y, (x1 + x2) / 2, (y1 + y2) / 2)) < 500:
                                current_holder.shoot1(ball, x1, x2, y1, y2)
                else:
                    if action == 'intercept':
                        person.intercept(ball)
                reward = calculate_reward(action, environment)
                next_state = agent.get_state(environment)
                agent.learn(state, action, reward, next_state)

            if not any(player.ball_following for player in hometeam + awayteam):
                closest_player = min(hometeam + awayteam, key=lambda p: distance(p.x, p.y, ball.x, ball.y))
                move_towards_ball(closest_player, ball, closest_player.speed)

            for i in hometeam:
                d = distance(i.x, i.y, ball.x, ball.y)
                if 0 <= d < ball.radius + i.radius and ball.speed < 3:
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
                    agent.save_q_table('q_table.pkl')
                    pygame.quit()
                    sys.exit()

            if ball_moving:
                ball.x -= math.cos(ball_angle) * ball.speed * -1
                ball.y -= math.sin(ball_angle) * ball.speed * -1
                ball.speed *= 0.99
                if ball.speed < 0.2:
                    ball_moving = False
                    person.ball_following = False
            for i in hometeam:
                if i.ball_following:
                    ball.x = i.x + math.cos(ball_angle) * 12
                    ball.y = i.y + math.sin(ball_angle) * 12
            for i in awayteam:
                if i.ball_following:
                    ball.x = i.x + math.cos(ball_angle) * 12
                    ball.y = i.y + math.sin(ball_angle) * 12

            clock.tick(FPS)
            if game_start():
                screen.fill((48, 131, 43))
                lines()
                person.draw()
                for i in range(len(hometeam)):
                    hometeam[i].draw()
                    awayteam[i].draw()
                ball.draw(person)
                pygame.draw.line(screen, (255, 255, 255), (0, 5), (30, 5), 10)
                screen.blit(scoretext, [173, 56])
                
                pygame.transform.flip(goalpost2, True, False)

                screen.blit(goalpost1, [1300, 285])
                screen.blit(goalpost2, [-373, 285])
            pygame.display.update()
        else:
            screen.fill((255,255,255))
            screen.blit(startt, [900,500])

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
                ball.speed = 4
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