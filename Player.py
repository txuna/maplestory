import pygame
import json 

WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (204, 0, 0)
BLUE = (0, 0, 128)
YELLOW = (255, 255, 0)

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

        self.font = pygame.font.Font('font/deliver.ttf', 26)
        #플레이어의 정보 로드
        self.GetData()
        #아래 코드 리팩토링 하기 
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

    def GetCurrentPos(self):
        return self.userinfo['info']['Current_Pos']
    
    def GetData(self):
        with open('json/player.json', encoding='utf-8') as playerinfo:
            self.userinfo = json.load(playerinfo)

    def SaveData(self):
        with open('json/player.json', 'w', encoding='utf-8') as playerinfo:
            json.dump(self.userinfo, playerinfo, indent='\t')
        self.GetData()

    def Check_Collision(self):
        #몬스터와의 충돌
        #몬스터와 충돌이후 3초간 무적 상태 
        mob_collisions = pygame.sprite.spritecollide(self, self.game.MonsterObj.GetMonsterGroup(), False)
        if mob_collisions:
            for collision in mob_collisions:
                if self.GetDamage(collision.Attack()): #True라면 사망
                    return "Death"
                else:
                    continue
        
        #바닥과의 충돌
        floor_collisions = pygame.sprite.spritecollide(self, self.game.MapObj.GetMapGroup(), False)
        if floor_collisions:
            for collision in floor_collisions:
                if (collision.rect.top+10 >= self.rect.bottom):
                    self.rect.bottom = collision.rect.top-3
                    self.CanJump = False #점프 못하게 방지 
                    self.jump_count = 10
                    self.Fallen = False
                else: 
                    continue

    def GetPercent(self, cur, max, len):
        return (len * (1 - ((max-cur)/max)))

    def Draw_BottomBar(self):
        pygame.draw.rect(self.game.gamepad, GRAY , (0, 422, 1024, 90))
        pygame.draw.line(self.game.gamepad, WHITE, (200, 422), (200, 512))
        pygame.draw.line(self.game.gamepad, WHITE, (700, 422), (700, 512))
        name = self.userinfo['info']['username']
        level = self.userinfo['stat']['level']
        usertext = self.font.render('Lv.{}    {}'.format(str(level), name), True, WHITE, GRAY)
        usertextRect = usertext.get_rect()
        usertextRect.topleft = (20,445)
        self.game.gamepad.blit(usertext, usertextRect)
        #[0] current, [1] is max
        hp = self.userinfo['stat']['hp']
        hp_percent = self.GetPercent(hp[0], hp[1], 150)
        mp = self.userinfo['stat']['mp']
        mp_percent = self.GetPercent(mp[0], mp[1], 150)
        exp = self.userinfo['stat']['exp']
        exp_percent = self.GetPercent(exp[0], exp[1], 400)

        hptext = self.font.render('HP', True, WHITE, GRAY)
        hptextRect = hptext.get_rect()
        hptextRect.topleft = (210, 432)
        self.game.gamepad.blit(hptext, hptextRect)
        pygame.draw.rect(self.game.gamepad, WHITE , (260, 437, 150, 25)) #150
        pygame.draw.rect(self.game.gamepad, RED , (260, 437, hp_percent, 25))
        
        mptext = self.font.render('MP', True, WHITE, GRAY)
        mptextRect = mptext.get_rect()
        mptextRect.topleft = (450, 432)
        self.game.gamepad.blit(mptext, mptextRect)
        pygame.draw.rect(self.game.gamepad, WHITE , (500, 437, 150, 25)) #150
        pygame.draw.rect(self.game.gamepad, BLUE , (500, 437, mp_percent, 25))

        exptext = self.font.render('EXP', True, WHITE, GRAY)
        exptextRect = exptext.get_rect()
        exptextRect.topleft = (210, 477)
        self.game.gamepad.blit(exptext, exptextRect)
        pygame.draw.rect(self.game.gamepad, WHITE , (275, 480, 400, 25)) #400
        pygame.draw.rect(self.game.gamepad, YELLOW , (275, 480, exp_percent,25))
   
    #낙화 기능 점프 방지를 해야하니 move쓰지 않고 canjump에 False넣고 반복문 #CanFall 이라는 변수를 둬야할듯 
    def SetPos(self, pos):
        #self.Check_Collision()
        #print("player : ",pos )
        #self.rect.bottomleft = pos
        self.rect.right = pos[0]
        self.rect.bottom = pos[1]-100 

#테스트용 L_CTRL, (화살 발사)
#스킬류가 있어서 음 일단 test용 Attack으로 진행 
    def Attack(self):
        return self.userinfo['stat']['damage']

    def SetHealth(self):
        pass

#몬스터로 인한 공격
    def GetDamage(self, damage):
        damage = self.Cal_Damage(damage)
        if self.userinfo['stat']['hp'][0] - damage <= 0:
            return True #사망 
        else:
            self.userinfo['stat']['hp'][0] -= damage
            self.SaveData()
            return False

    def Cal_Damage(self, damage):
        return damage * (100 / (100 * self.userinfo['stat']['defensive']))


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
