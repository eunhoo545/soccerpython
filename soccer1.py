import pygame
import sys
import time
import math


from map import lines
from game import throwin,goalkick,kickoff,calculate_angle,distance
import numpy as np
import random
ball_moving = False
FPS = 60
MAX_WIDTH = 1800
MAX_HEIGHT = 1000
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT))
pygame.init()
clock = pygame.time.Clock()
pi = 180
RED = (255,0,0)

myFont = pygame.font.SysFont( "centurygothic", False, False)
goalpost1 = pygame.image.load('goalpost1.png')


class Agent:
    def __init__(self, actions, learning_rate=0.01, discount_factor=0.9, epsilon=0.9):
        self.q_table = {}
        self.actions = actions
        self.lr = learning_rate
        self.gamma = discount_factor
        self.epsilon = epsilon

    def get_state(self, environment):
        # 위치와 속도를 상태로 변환
        state = tuple(environment.get_positions() + environment.get_velocities())
        return state

    def choose_action(self, state):
        # 엡실론-탐욕 정책
        if np.random.rand() < self.epsilon:
            return np.random.choice(self.actions)
        else:
            return max(self.q_table.get(state, {}), key=self.q_table.get(state, {}).get, default=np.random.choice(self.actions))
		
    def learn(self, state, action, reward, next_state):
        # Q-value 업데이트, Q-table 업데이트
        prev_value = self.q_table.get(state, {}).get(action, 0)
        future_value = max(self.q_table.get(next_state, {}).values(), default=0)
        self.q_table.setdefault(state, {})[action] = prev_value + self.lr * (reward + self.gamma * future_value - prev_value)
		
class Environment:
    def __init__(self, hometeam, awayteam, ball):
        self.hometeam = hometeam
        self.awayteam = awayteam
        self.ball = ball

    def get_positions(self):
        # 모든 플레이어와 공의 위치를 반환
        positions = []
        for player in self.hometeam + self.awayteam:
            positions.append((player.x, player.y))
        positions.append((self.ball.x, self.ball.y))
        return positions

    def get_velocities(self):
        # 모든 플레이어의 속도를 추정하는 함수(상태저장에 필요할것 같아서 선언)
        return [0] * (len(self.hometeam) + len(self.awayteam) + 1)  # 간단한 예제로 모두 0으로 설정



class Power():
	def __init__(self, max_power):
		self.power = 20
		self.power_grow = 0
		self.max_power = max_power
		self.power_growing = False
		self.firstpower = 0
class Map():
	throwin = False
	game = True
	goalkick = False
	cornerkick = False
def throwin(person,ball,y,map):
	time.sleep(1)
	print('throwin')
	map.throwin = True
	ball.x = ball.x
	ball.y = y- ball.radius
	ball_moving= False
	person.ball_following = False
	ball.speed = 0
	person.x = ball.x
	person.y = ball.y +20
	

def kickoff():
	print('kickoff')
	time.sleep(1)
def cornerkick():
	print('cornerkick')
	time.sleep(1)

def distance(x1, y1, x2, y2):#거리계산
	return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
def calculate_angle(x1, y1, x2, y2):        #각도계산
	return math.atan2(y2 - y1, x2 - x1)
def calculate_reward(action, environment):
    if action == 'shoot' and goal_scored(environment.ball):
        print("Goal scored! Reward: 20")
        return 20  # 골을 넣었을 때의 보상
    elif action == 'shoot' and not goal_scored(environment.ball):
        print("Missed shot! Reward: -2")
        return -2  # 슛을 쐈으나 골을 놓쳤을 때의 페널티
    elif action == 'pass' and pass_completed(environment.hometeam, environment.awayteam):
        return 5  # 패스가 성공했을 때의 보상
    else:
        return -1  #일단 나머지 동작에 대한 패널티


def setup_teams_and_ball():
    # 플레이어 생성
    hometeam = [
        Person(15, 930, 502, 'home', 40),
        Person(15, 738, 502, 'home', 40),
        Person(15, 690, 684, 'home', 40),
        Person(15, 758, 808, 'home', 40),
        Person(15, 724, 158, 'home', 40),
        Person(15, 600, 310, 'home', 40),
        Person(15, 402, 108, 'home', 40),
        Person(15, 358, 632, 'home', 40),
        Person(15, 318, 388, 'home', 40),
        Person(15, 458, 860, 'home', 40),
        Person(15, 166, 506, 'home', 40)
    ]
    awayteam = [
        Person(15, 1030, 396, 'away', 40),
        Person(15, 1050, 612, 'away', 40),
        Person(15, 1042, 828, 'away', 40),
        Person(15, 1082, 204, 'away', 40),
        Person(15, 1240, 458, 'away', 40),
        Person(15, 1220, 650, 'away', 40),
        Person(15, 1362, 864, 'away', 40),
        Person(15, 1300, 134, 'away', 40),
        Person(15, 1406, 368, 'away', 40),
        Person(15, 1446, 670, 'away', 40),
        Person(15, 1624, 498, 'away', 40)
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

def pass_completed(hometeam, awayteam):
    # 현재 공을 가진 선수를 찾음
    current_holder = next((player for player in hometeam + awayteam if player.ball_following), None)
    
    # 공을 가진 선수가 없으면 패스는 실패
    if not current_holder:
        return False
    
    # 공을 가진 선수의 팀 동료를 찾음 (같은 팀)
    teammates = [player for player in hometeam if current_holder.team == 'home'] + \
                [player for player in awayteam if current_holder.team == 'away']
    
    # 공이 패스된 후 새로운 선수에게 도달했는지 확인
    for teammate in teammates:
        if teammate != current_holder and distance(current_holder.x, current_holder.y, teammate.x, teammate.y) < 30:
            # 패스가 성공적으로 도달했음
            return True
    
    # 패스가 성공적으로 도달하지 못했음
    return False

def move_towards_ball(player, ball, speed):
    # 플레이어와 공 사이의 각도 계산
    angle = calculate_angle(player.x, player.y, ball.x, ball.y)
    # 각도를 사용하여 x, y 방향의 이동 계산
    player.x += math.cos(angle) * speed
    player.y += math.sin(angle) * speed


def main():
	global ball_moving
	person = Person(15,936,502,'home',40)
	agent = Agent(actions=['move_up', 'move_down', 'move_left', 'move_right', 'kick', 'pass', 'shoot'], learning_rate=0.01, discount_factor=0.9, epsilon=0.9)
	homescore = 0
	awayscore = 0
	hometeam = []
	awayteam = []
	hometeam, awayteam, ball = setup_teams_and_ball()
	environment = Environment(hometeam, awayteam, ball)
	ball_angle = 0
	m_state = 0
	scoretext= myFont.render((str(homescore)+str(' - ')+str(awayscore)), True, (0,0,0))

	ball = Ball(12)
	map = Map()
	ball_angle = calculate_angle(person.x, person.y, ball.x, ball.y)
	while True:
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
				if action == 'shoot':
					goal_x = 0 if person.team == 'home' else MAX_WIDTH 
					goal_y = MAX_HEIGHT / 2
					person.shoot(ball, goal_x, goal_y)
				elif action == 'pass':
					if person.ball_following == True:
						teammates = [p for p in (hometeam if person in hometeam else awayteam) if p != person]
						if teammates:
							print("pass1!!!!")
							target_player = random.choice(teammates)
							person.pass1(ball, target_player)
							print('pass complete')
							
			reward = calculate_reward(action, environment)
			next_state = agent.get_state(environment)
			agent.learn(state, action, reward, next_state)
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
			person.power.power_grow = 1
			person.power.power +=1
		if keys[pygame.K_k]:
			ball_angle += math.pi / 18
		if not(keys[pygame.K_SPACE]):
			person.power.power_grow = 0
			person.power.power = 0
		if keys[pygame.K_m] and m_state==0:
					ball.x -= 100
					m_state +=1

		if m_state != 0:
			m_state +=1
		if m_state == 180:
			m_state = 0
		

		if not any(player.ball_following for player in hometeam + awayteam):  
			# 모든 선수가 공을 따라가지 않을 때 가장 가까운 녀석 찾기
			closest_player = min(hometeam + awayteam, key=lambda p: distance(p.x, p.y, ball.x, ball.y))
			#해당 플레이어가 공을 향해 이동할 수 있게
			move_towards_ball(closest_player, ball, closest_player.speed)

		# 플레이어가 공에 가까이 갔는지 확인
		# 공이 플레이어를 따라가게
		for i in hometeam:
			if distance(i.x, i.y, ball.x, ball.y) < ball.radius + i.radius and ball.speed < 3:
				i.ball_following = True
				ball_angle = calculate_angle(i.x, i.y, ball.x, ball.y)
			else:
				i.ball_following = False
		for i in awayteam:
			if distance(i.x, i.y, ball.x, ball.y) < ball.radius + i.radius and ball.speed < 3:
				i.ball_following = True
				ball_angle = calculate_angle(i.x, i.y, ball.x, ball.y)
			else:
				i.ball_following = False
		


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					person.power.power_growing = True
			if event.type == pygame.KEYUP:     #SPACE를 때면 슛
				if event.key == pygame.K_SPACE and person.ball_following == True:
					person.power.firstpower = (person.power.power/person.power.max_power)
					person.power.power_growing = False
					person.ball_following = False
					person.power.power = 0
					ball_moving = True
					ball.speed = 5
				if event.key == pygame.K_SPACE and person.ball_following == True and map.throwin == True:
					person.power.firstpower = 0.5
					person.power.power_growing = False
					person.ball_following = False
					person.power.power = 0
					ball_moving = True
					ball.speed = 5
					map.throwin = False
				
			if person.power.power_growing and person.power.power < person.power.max_power:
				person.power.power += 0.5

		if ball_moving:
			print(ball_moving)
			print("패스중")
			ball.x -= math.cos(ball_angle) * ball.speed *-1
			ball.y -= math.sin(ball_angle) * ball.speed *-1
			ball.speed *= 0.99  # 공의 속도를 점점 감소시킴
			if ball.speed < 0.2:
				person.power.firstpower = 0
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


		if ball.y <= 70 - ball.radius and not map.throwin: #스로인과 골킥 
			throwin(person,ball,50,map)
		if ball.y >= 940 + ball.radius and not map.throwin:
			throwin(person,ball,960,map)

		if ball.x <= 120 - ball.radius:
			if ball.y <350 or ball.y > 650:
				ball.x = 120-ball.radius
				ball_moving= False
				ball_following = False
				ball.speed = 0
				#goalkick(person,ball.x,map)
			else:
				print('골1')
				awayscore += 1
				scoretext= myFont.render((str(homescore)+str(' - ')+str(awayscore)), True, (0,0,0))
				time.sleep(1)
				ball.x = 905
				ball.y = 505
				ball_moving = False
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
				#goalkick(person,ball.x,map)
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


		if person.power.power/person.power.max_power >= 1:
			person.power.power = person.power.max_power          
		clock.tick(FPS)
		screen.fill((48,131,43))
		lines()
		pygame.draw.rect(screen, (0,0,0), (20, 20, 20, 200))
		pygame.draw.rect(screen, RED, (20, 220 - (person.power.power / person.power.max_power) * 200, 20, (person.power.power / person.power.max_power) * 200))
		person.draw()
		for i in range(len(hometeam)):
			hometeam[i].draw()
			awayteam[i].draw()
		
		ball.draw(person)
		#Physics.simulate()
		#Player.simulate()
		pygame.draw.line(screen,(255,255,255),(0,5),(30,5),10)
		#post1()
		#post2()
		#screen.blit(scorepic, [60, 25])
		screen.blit(scoretext, [173, 56])
		screen.blit(goalpost1, [1300,285])
		pygame.display.update()



class Ball(): #공
	def __init__(self,radius):
		self.x = 905
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
	def __init__(self,radius,x,y,team,max_power):
		self.x = x
		self.y = y
		self.radius = radius
		self.speed = 2
		self.team = team
		self.power = Power(max_power)
		self.ball_following = False

	def moveup(self):
		self.y -= self.speed
	def movedown(self):
		self.y += self.speed
	def moveright(self):
		self.x += self.speed
	def moveleft(self):
		self.x -= self.speed
	def shoot(self, ball, goal_x, goal_y):
		global ball_angle
		if self.ball_following:
			goal_x += 1800
			print("GOALXY: ", goal_x, goal_y)
			angle_to_goal = calculate_angle(self.x, self.y, goal_x, goal_y)
			angle_diff = abs(angle_to_goal - math.pi)  # 골대가 가로로 위치한다고 가정할 때
    
			if angle_diff < math.radians(5):  # +- 5도
				global ball_moving
				ball.speed = 10  
				ball_angle = angle_to_goal  # 슛의 방향 설정
				ball_moving = True
				self.ball_following = False
				print('Shoot towards goal at angle:', math.degrees(angle_to_goal))
			else:
				print('Angle벗어남')


	def pass1(self, ball, target_player):
		if self.ball_following:
			global ball_moving
			angle = calculate_angle(self.x, self.y, target_player.x, target_player.y)
			angle_ball = calculate_angle(self.x, self.y, ball.x, ball.y)
			angle_difference = abs(angle - angle_ball)
			print(angle, angle_ball, angle_difference)
			if angle_difference < 0.3:  # 0.1 라디안 이내의 차이를 허용
				print("angle same")
				self.ball_following = False
				ball_moving = True
				ball.speed = 5
			# 공의 위치와 속도를 업데이트합니다.
			# 플레이어와 공의 상태를 업데이트합니다.
			self.power.firstpower = 0
			self.power.power = 0
			self.power.power_growing = False


	def calculate_angle(x1, y1, x2, y2): 
		return math.atan2(y2 - y1, x2 - x1)

	def draw(self):
		if self.team == 'home':
			self.color = (255,0,0)
		if self.team == 'away':
			self.color = (0,0,255)
		pygame.draw.circle(screen,self.color,(self.x,self.y),self.radius)        

	
	
if __name__ == '__main__':
	main()