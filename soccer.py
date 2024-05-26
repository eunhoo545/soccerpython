import pygame
import sys
import time
import math
from map import lines
from game import throwin,goalkick,kickoff,calculate_angle,distance
ball_moving = False
FPS = 60
MAX_WIDTH = 1800
MAX_HEIGHT = 1000
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT))
pygame.init()
clock = pygame.time.Clock()
pi = 180
RED = (255,0,0)

myFont = pygame.font.SysFont( "centurygothic",40, False, False)
goalpost1 = pygame.image.load('goalpost1.png')





class Power():
	def __init__(self, max_power):
		self.power = 0
		self.power_grow = 0
		self.max_power = max_power
		self.power_growing = False
		self.firstpower = 0
class Map():
	throwin = False
	game = True
	goalkick = False
	cornerkick = False
	setpiece = False
def throwin(person,ball,y,map):
	time.sleep(1)
	map.setpiece = True
	print('throwin')
	map.throwin = True
	ball.x = ball.x
	ball.y = y- ball.radius
	ball_moving= False
	person.ball_following = False
	ball.speed = 0
	person.x = ball.x
	person.y = ball.y +20

	
def goalkick(person,ball,team,map):
	time.sleep(1)
	map.setpiece = True
	print('goalkick')
	map.goalkick = True
	
	if team == 'red':
		ball.x = 200
		ball.y = 370
		person.x = 20
		person.y = 370
	#ball_moving= False
	#person.ball_following = False
	#ball.speed = 0
	#person.x = ball.x
	#person.y = ball.y +20
def kickoff():
	print('kickoff')
def cornerkick():
	
	print('cornerkick')
	time.sleep(1)
	map.setpiece = True

def distance(x1, y1, x2, y2):       #거리계산
	return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
def calculate_angle(x1, y1, x2, y2):        #각도계산
	return math.atan2(y2 - y1, x2 - x1)

def main():
	global ball_moving
	ball_following = False
	homescore = 0
	awayscore = 0
	hometeam = []
	awayteam = []
	ball_angle = 0
	m_state = 0
	scoretext= myFont.render((str(homescore)+str(' - ')+str(awayscore)), True, (0,0,0))

	
	person = Person(15,936,502,'home',60)
	hometeam.append(person)
	person2 = Person(15,738,502,'home',60)
	hometeam.append(person2)
	person3 = Person(15,690,684,'home',60)
	hometeam.append(person3)
	person4 = Person(15,758,808,'home',60)
	hometeam.append(person4)
	person5 = Person(15,724,158,'home',60)
	hometeam.append(person5)
	person6 = Person(15,600,310,'home',60)
	hometeam.append(person6)
	person7 = Person(15,402,108,'home',60)
	hometeam.append(person7)
	person8 = Person(15,358,632,'home',60)
	hometeam.append(person8)
	person9 = Person(15,318,388,'home',60)
	hometeam.append(person9)
	person10 = Person(15,458,860,'home',60)
	hometeam.append(person10)
	person11 = Person(15,166,506,'home',60)
	hometeam.append(person11)
	person12 = Person(15,1030,396,'away',60)
	awayteam.append(person12)
	person13 = Person(15,1050,612,'away',60)
	awayteam.append(person13)
	person14 = Person(15,1042,828,'away',60)
	awayteam.append(person14)
	person15 = Person(15,1082,204,'away',60)
	awayteam.append(person15)
	person16 = Person(15,1240,458,'away',60)
	awayteam.append(person16)
	person17 = Person(15,1220,650,'away',60)
	awayteam.append(person17)
	person18 = Person(15,1362,864,'away',60)
	awayteam.append(person18)
	person19 = Person(15,1300,134,'away',60)
	awayteam.append(person19)
	person20 = Person(15,1406,368,'away',60)
	awayteam.append(person20)
	person21 = Person(15,1446,670,'away',60)
	awayteam.append(person21)
	person22 = Person(15,1624,498,'away',60)
	awayteam.append(person22)
	ball = Ball(12)
	map = Map()
	
	ball_angle = calculate_angle(person.x, person.y, ball.x, ball.y)

	while True:
		if person.x <= 0 + person.radius:
			person.x = 0 + person.radius
		if person.x >= 1800 - person.radius:
			person.x = 1800 - person.radius
		if person.y <= 0 + person.radius:
			person.y = 0 + person.radius
		if person.y >= 1000 - person.radius:
			person.y = 1000-person.radius
		
		#print(person.x,person.y)
		keys = pygame.key.get_pressed()
		if keys[pygame.K_a] and map.setpiece == False:
			person.x -= person.speed
		if keys[pygame.K_d] and map.setpiece == False:
			person.x += person.speed
		if keys[pygame.K_w] and map.setpiece == False:
			person.y -= person.speed
		if keys[pygame.K_s] and map.setpiece == False:
			person.y += person.speed        #플레이어 움직이기
		if keys[pygame.K_SPACE]:
			person.power.power_grow = 1
			person.power.power +=1
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
		if keys[pygame.K_a] and map.throwin:
			person.x -= 0.3
		if keys[pygame.K_d] and map.throwin:
			person.x += 0.3
		if keys[pygame.K_w] and map.throwin:
			person.y -= 0.3
		if keys[pygame.K_s] and map.throwin:
			person.y += 0.3   
		if m_state != 0:
			m_state +=1
		if m_state == 180:
			m_state = 0
		

		  # 플레이어가 공에 가까이 갔는지 확인
		


		# 공이 플레이어를 따라가게
		for i in hometeam:
			if distance(i.x, i.y, ball.x, ball.y) < ball.radius + i.radius and ball.speed < 3:
				i.ball_following = True
				ball_angle = calculate_angle(i.x, i.y, ball.x, ball.y)
			else:
				i.ball_following = False
			keys = pygame.key.get_pressed()
			if keys[pygame.K_k]:
				ball_angle += math.pi / 18
		for i in awayteam:
			if distance(i.x, i.y, ball.x, ball.y) < ball.radius + i.radius and ball.speed < 3:
				i.ball_following = True
				ball_angle = calculate_angle(i.x, i.y, ball.x, ball.y)
			else:
				i.ball_following = False
			keys = pygame.key.get_pressed()
			if keys[pygame.K_k]:
				ball_angle += math.pi / (math.inf * math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf* math.inf)
		


		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:  #SPACE를 눌러서 파워게이지 증가
					person.power.power_growing = True
		
			if event.type == pygame.KEYUP:     #SPACE를 떼면 슛
				if event.key == pygame.K_SPACE and person.ball_following == True and map.throwin == False:
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
				if event.key == pygame.K_SPACE and person.ball_following == True and map.goalkick == True:
					person.power.firstpower = 35
					person.power.power_growing = False
					person.ball_following = False
					person.power.power = 0
					ball_moving = True
					ball.speed = 5
					
					
				
			if person.power.power_growing and person.power.power < person.power.max_power:
				person.power.power += 0.5
		

		if ball_moving:
			ball.x -= math.cos(ball_angle) * ball.speed *person.power.firstpower
			ball.y -= math.sin(ball_angle) * ball.speed *person.power.firstpower
			print('ballmoving')
			ball.speed *= 0.99  # 공의 속도를 점점 감소시킴
			if ball.speed < 0.2:
				person.power.firstpower = 0
				ball_moving = False
				person.ball_following = False
			if ball.speed < 3 or ball_moving == False:
				map.throwin = False
				map.setpiece = False

		for i in hometeam:
			if i.ball_following:      #공이 선수한테 붙음					
				ball.x =i.x + math.cos(ball_angle) * 12 
				ball.y = i.y + math.sin(ball_angle) * 12
		for i in awayteam:
			if i.ball_following:      #공이 선수한테 붙음

				ball.x =i.x + math.cos(ball_angle) * 12 
				ball.y = i.y + math.sin(ball_angle) * 12


		if ball.y <= 70 - ball.radius  and map.setpiece == False: #스로인과 골킥 
			
			throwin(person,ball,50,map)
		if ball.y >= 940 + ball.radius  and map.setpiece == False:
			
			throwin(person,ball,960,map)

		if ball.x <= 120 - ball.radius and map.setpiece == False:
			if ball.y <350 or ball.y > 650:
				ball.x = 120-ball.radius
				ball_moving= False
				ball_following = False
				ball.speed = 0
				goalkick(person,ball,'red',map)
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
		if ball.x >= 1680 + ball.radius and map.setpiece == False:
			if ball.y <375 or ball.y > 625:
				ball.x = 1680+ball.radius
				ball_moving= False
				ball_following = False
				ball.speed = 0
				
				goalkick(person,ball,'blue',map)
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
		person2.draw()
		person3.draw()
		person4.draw()
		person5.draw()
		person6.draw()
		person7.draw()
		person8.draw()
		person9.draw()
		person10.draw()
		person11.draw()

		person22.draw()
		person12.draw()
		person13.draw()
		person14.draw()
		person15.draw()
		person16.draw()
		person17.draw()
		person18.draw()
		person19.draw()
		person20.draw()
		person21.draw()
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
	def shoot(self):
		print('shoot')
		#if self.ball_following == True:
			
	def pass1(self):
		print('pass')
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