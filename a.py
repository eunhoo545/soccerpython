import pygame

FPS = 60
MAX_WIDTH = 1800
MAX_HEIGHT = 1000
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((MAX_WIDTH,MAX_HEIGHT))

def main():
    ball = Ball(15)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    print("space")
        
        clock.tick(FPS)
        screen.fill((48,131,43))
        lines()
        ball.draw()
        Physics.simulate()
        Player.simulate()
        
        post1()
        post2()
        
        
            
        pygame.display.update()

class Physics():
    objects = []
    def __init__(self,x,y,color,radius):
        self.x = x
        self.y = y
        self.color = color
        self.radius = radius
        self.speedx = 0
        self.speedy = 0
        Physics.objects.append(self)
    def draw(self):
        return pygame.draw.circle(screen, self.color, (self.x, self.y),self.radius)
    def move(self,x,y):
        self.x += x
        self.y += y
    def setspeed(self,x,y):
        self.speedx = x
        self.speedy = y
    def addspeed(self,x,y):
        self.speedx += x
        self.speedy += y
    def collisionCheck():
        for p in Physics.objects:
           for l in Physics.objects:
                cX =  (abs(( p.x - l.x ))*(p.radius/(p.radius+l.radius)))
                cY = (abs(( p.y - l.y ))*(p.radius/(p.radius+l.radius)))
                if p == l:
                    continue
                distance = (( p.x - l.x )**2 + ( p.y - l.y )**2 )**0.5
                if distance < p.radius+l.radius:
                    if p.x < l.x:
                        centerX = p.x + cX
                    if p.x > l.x:
                        centerX = p.x - cX
                    if p.y > l.y:
                        centerY = p.y - cY
                    if p.y < l.y:
                        centerY = p.y + cY
                    print(time.time(), p.name, p.x,p.y, l.name, l.x,l.y, 'center', centerX , centerY)
                    p.move((p.x-centerX)/FPS*4,(p.y-centerY)/FPS*4)
                    l.move((l.x-centerX)/FPS*4,(l.y-centerY)/FPS*4)
    def simulate():
        for i in Physics.objects:
            i.move(i.speedx,i.speedy)
            i.addspeed(-(i.speedx*0.023),-(i.speedy*0.023))
            i.draw()
        Physics.collisionCheck()
        
def post1():
    pygame.draw.rect(screen,(255,255,255),(15,360,100,7)) 
    pygame.draw.rect(screen,(255,255,255),(15,640,100,7)) 
    pygame.draw.rect(screen,(255,255,255),(15,360,7,280)) 
    pygame.draw.rect(screen,(255,255,255),(110,360,5,280)) 
    pygame.draw.rect(screen,(255,255,255),(95,360,5,280)) 
    pygame.draw.rect(screen,(156,171,171),(20,375,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,385,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,395,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,405,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,415,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,425,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,435,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,445,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,455,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,465,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,475,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,485,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,495,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,505,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,515,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,525,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,535,75,3))
    pygame.draw.rect(screen,(156,171,171),(20,545,75,3))  
    pygame.draw.rect(screen,(156,171,171),(20,555,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,565,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,575,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,585,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,595,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,605,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,615,75,3))
    pygame.draw.rect(screen,(156,171,171),(20,625,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(20,635,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(25,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(35,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(45,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(55,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(65,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(75,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(85,367,3,273))            
    
    
   
    pygame.draw.rect(screen,(156,171,171),(100,375,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,385,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,395,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,405,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,415,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,425,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,435,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,445,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,455,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,465,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,475,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,485,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,495,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,505,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,515,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,525,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,535,12,3))
    pygame.draw.rect(screen,(156,171,171),(100,545,12,3))  
    pygame.draw.rect(screen,(156,171,171),(100,555,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,565,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,575,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,585,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,595,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,605,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,615,12,3))
    pygame.draw.rect(screen,(156,171,171),(100,625,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(100,635,12,3)) 
    
def post2():
    pygame.draw.rect(screen,(255,255,255),(1685,360,100,7)) 
    pygame.draw.rect(screen,(255,255,255),(1685,640,100,7)) 
    pygame.draw.rect(screen,(255,255,255),(1780,360,7,287)) 
    pygame.draw.rect(screen,(255,255,255),(1685,360,5,280)) 
    pygame.draw.rect(screen,(255,255,255),(1700,360,5,280)) 
    pygame.draw.rect(screen,(156,171,171),(1705,375,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,385,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,395,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,405,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,415,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,425,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,435,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,445,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,455,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,465,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,475,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,485,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,495,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,505,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,515,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,525,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,535,75,3))
    pygame.draw.rect(screen,(156,171,171),(1705,545,75,3))  
    pygame.draw.rect(screen,(156,171,171),(1705,555,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,565,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,575,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,585,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,595,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,605,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,615,75,3))
    pygame.draw.rect(screen,(156,171,171),(1705,625,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1705,635,75,3)) 
    pygame.draw.rect(screen,(156,171,171),(1775,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(1765,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(1755,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(1745,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(1735,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(1725,367,3,273)) 
    pygame.draw.rect(screen,(156,171,171),(1715,367,3,273))            
    
    
   
    pygame.draw.rect(screen,(156,171,171),(1688,375,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,385,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,395,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,405,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,415,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,425,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,435,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,445,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,455,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,465,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,475,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,485,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,495,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,505,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,515,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,525,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,535,12,3))
    pygame.draw.rect(screen,(156,171,171),(1688,545,12,3))  
    pygame.draw.rect(screen,(156,171,171),(1688,555,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,565,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,575,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,585,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,595,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,605,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,615,12,3))
    pygame.draw.rect(screen,(156,171,171),(1688,625,12,3)) 
    pygame.draw.rect(screen,(156,171,171),(1688,635,12,3)) 

def lines():
    pygame.draw.rect(screen,(47,164,47),(0,0,100,1000))
    pygame.draw.rect(screen,(47,164,47),(200,0,100,1000))
    pygame.draw.rect(screen,(47,164,47),(400,0,100,1000))
    pygame.draw.rect(screen,(47,164,47),(600,0,100,1000))
    pygame.draw.rect(screen,(47,164,47),(800,0,100,1000))
    pygame.draw.rect(screen,(47,164,47),(1000,0,100,1000))
    pygame.draw.rect(screen,(47,164,47),(1200,0,100,1000))
    pygame.draw.rect(screen,(47,164,47),(1400,0,100,1000))
    pygame.draw.rect(screen,(47,164,47),(1600,0,100,1000)) 

    pygame.draw.rect(screen,(255,255,255),(120,70,10,860)) 
    pygame.draw.rect(screen,(255,255,255),(1670,70,10,860)) #골라인
    pygame.draw.rect(screen,(255,255,255),(120,70,1560,10))
    pygame.draw.rect(screen,(255,255,255),(120,930,1560,10)) #사이드라인

    pygame.draw.rect(screen,(255,255,255),(900,70,10,860)) #하프라인

    pygame.draw.rect(screen,(255,255,255),(120,650,70,10))
    pygame.draw.rect(screen,(255,255,255),(120,350,70,10))
    pygame.draw.rect(screen,(255,255,255),(1600,350,70,10))
    pygame.draw.rect(screen,(255,255,255),(1600,650,70,10))
    pygame.draw.rect(screen,(255,255,255),(190,350,10,310))
    pygame.draw.rect(screen,(255,255,255),(1600,350,10,310)) #골 에어리어

    pygame.draw.rect(screen,(255,255,255),(120,230,220,10))
    pygame.draw.rect(screen,(255,255,255),(120,770,220,10))
    pygame.draw.rect(screen,(255,255,255),(340,230,10,550))
    pygame.draw.rect(screen,(255,255,255),(1450,230,220,10))
    pygame.draw.rect(screen,(255,255,255),(1450,770,220,10))
    pygame.draw.rect(screen,(255,255,255),(1450,230,10,550))  #페널티박스

    pygame.draw.circle(screen,(255,255,255),[905,505],145,10) #센터 서클
    pygame.draw.circle(screen,(255,255,255),[905,505],10) #센터 마크
    pygame.draw.arc(screen,(255,255,255),[100,50,50,50],3*3.14/2,3.14*2  ,5)
    pygame.draw.arc(screen,(255,255,255),[100,910,50,50],0,3.14/2  ,5)
    pygame.draw.arc(screen,(255,255,255),[1650,50,50,50],3.14,3*3.14/2  ,5)
    pygame.draw.arc(screen,(255,255,255),[1650,910,50,50],3.14/2,3.14  ,5) 
    pygame.draw.circle(screen,(255,255,255),[280,500],10)
    pygame.draw.circle(screen,(255,255,255),[1520,500],10)
        

class Player(Physics):
    players = []
    def __init__(self,x,y,color,radius,name):
        super().__init__(x,y,color,radius)

        self.name = name
        self.destx = self.x
        self.desty = self.y
        self.runacc = 0.02
        self.rundec = 0.1
        Player.players.append(self)
    def think(self):
        self.run()
    def run(self):
        d = ((self.x - self.destx)**2 + (self.y - self.desty)**2)**0.5
        if d == 0:
            return
        if d > self.radius:    
            self.addspeed((self.destx - self.x)/d * self.runacc,((self.desty-self.y)/d*self.runacc))
    def simulate():
        for i in Player.players:
            i.think()

#class Ball(Physics):
    #def __init__(self,x,y,color,radius):
        #super().__init__(x,y,color,radius)


class Goalkeeper(Physics):
     def __init__(self,x,y,color,radius,name):
        super().__init__(x,y,color,radius)
        self.name = name


class Ball():
    def __init__(self,radius):
        self.x = 905
        self.y = 505
        self.radius = radius
    def draw(self):
        pygame.draw.circle(screen,(0,0,0),(self.x,self.y),self.radius)
    
        

    
    
# 현실의 비율을 플레이어한테 적용해서 20픽셀을 1미터로 정했다.
player1 = Player(150,200,(0,0,255),20,'박지성')
player2 = Player(100,250,(0,0,205),20,'호날두')
player3 = Player(100,300,(0,0,155),20,'메시')
player3.destx = 1700
player3.desty = 535
player2.destx = 900
player2.desty = 500
player1.destx = 1000
player1.desty = 1000

goalkeeper1 = Goalkeeper(1640,510,(0,255,0),25,'d')

#ball = Physics(200,200,(0,0,0),5)
#goalkeeper1 = Goalkeeper(300,200,(0,255,0),25,'d')


if __name__ == '__main__':
    main()