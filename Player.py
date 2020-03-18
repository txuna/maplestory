import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game #Start Game Hander Class 
        self.jump_count = 10
        self.CanJump = False
        #self.Way = False #False : 하강, True : 상승
        self.Fallen = True
        self.resize = []
        self.images = []

        self.images.append (pygame.image.load ('images/walk1.png'))
        self.images.append (pygame.image.load ('images/walk2.png'))
        self.images.append (pygame.image.load ('images/walk3.png'))
        self.images.append (pygame.image.load ('images/walk4.png'))
        self.images.append (pygame.image.load ('images/walk5.png'))
        self.images.append (pygame.image.load ('images/walk6.png'))
        self.images.append (pygame.image.load ('images/walk7.png'))
        self.images.append (pygame.image.load ('images/walk8.png'))
        self.images.append (pygame.image.load ('images/walk9.png'))
        self.images.append (pygame.image.load ('images/walk10.png'))
        
        self.index = 0
        for image in self.images:
            self.resize.append(pygame.transform.scale(image, (60, 80)))
        self.image = self.resize[self.index]
        self.rect = self.image.get_rect()
        #self.rect.center = (100, 410)

    #지형과 몬스터 벽에 대한 Collision 체크 필요 
    #rect 객체의 Low부분 충돌 체크 필요  이부분이  안된다면 지형을 선으로 해서 페이크 현상 줘야함 
   
    #스페이스를 눌렀을 때 충돌체크를 검사한다. 이때는 NPC검사 
    #리턴값은 충돌된 객체들이다. 
    #플레이어가 점프중일때 충돌된 객체는 무시하되 점프하고 내려올때 
    #플레이어의 Low.y와 충돌된 객체의 High.Y외 비교한다. 
    #낙하 기능을 만들어야됨 .
    #측면에 대한 충돌이 안되기때문에 이미 충돌이 되고 나서야 충돌이 가능하다. 그래서 collision.rect.top + 1 점프수치도 애매해서 center로 변경 
    def Check_Collision(self):
        collisions = pygame.sprite.spritecollide(self, self.game.MapObj.GetMapGroup(), False)
        if collisions:
            for collision in collisions:
                #print(collision.rect.top+10, self.rect.bottom)
                #점프가 하강일때 올라갈때는 무시
                #print(collision.rect.top, self.rect.bottom, self.Way)#480  451 False
                if (collision.rect.top+10 >= self.rect.bottom):
                    #print(collision.rect.top+10, self.rect.bottom)
                    self.rect.bottom = collision.rect.top-3#+1해서 보정값 세워야하나
                    #print(collision.rect.top-10, self.rect.bottom, self.Way)
                    self.CanJump = False #점프 못하게 방지 
                    self.jump_count = 10
                    self.Fallen = False
                else: 
                    continue

    #낙화 기능 점프 방지를 해야하니 move쓰지 않고 canjump에 False넣고 반복문 #CanFall 이라는 변수를 둬야할듯 
    def SetPos(self, pos):
        #self.Check_Collision()
        #print("player : ",pos )
        #self.rect.bottomleft = pos
        self.rect.right = pos[0]
        self.rect.bottom = pos[1]-100 

    def update(self, LookAt): #현재 바라보고 있는 방향 인자로 넣음 
        original= {'x':self.rect.x, 'y':self.rect.y}
        self.index+=1
        if self.index >= len(self.resize):
            self.index = 0
        self.image = self.resize[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = original['x']
        self.rect.y = original['y']

    #move에 Collision을 체크하자. #Move는 맵 콜리전 체크가 필요한가. 
    def move(self, x, y):
        if (self.rect.right+x >= 1024) or (self.rect.x+x <= 0):
            return
        if (self.rect.y+y >= 512) or (self.rect.y+y <= 0):
            return
        self.rect.x += x
        self.rect.y += y
        self.Fallen = True
        self.Check_Collision()

#jump_count가 양수가 된다면 하강중임  #낙하할 땐 Collision까지 낙하 
    def jump(self):
        if self.CanJump:
            if self.jump_count <= 0: #낙하   
                self.rect.y += (1 ** 2) * 10
                self.jump_count -= 1
                self.Check_Collision()
            elif self.jump_count > 0 and self.jump_count <= 10: #상승
                self.rect.y -= (self.jump_count ** 2) * 0.23
                self.jump_count -= 1    
            else:
                self.jump_count = 10
                self.CanJump = False
        elif self.Fallen: #떨어지는 타이밍
            self.rect.y += (1**2) * 10
            self.Check_Collision()
            #print(self.rect.bottom)


#TODO 블럭으로 점프할때 2단 점프가 되는 경우가 있음.
