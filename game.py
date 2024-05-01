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