import pygame
from Player import Player
import sys
from Map import *
from Monster import *
from skill import *

'''
쉽게 상황으로 설명을 하면
1. 발사키를 눌르면 event가 발생
2. event 가 발생하면 총알 발사(객체 생성)
3. 생성된 개체는 게임 안의 sprite group 에 add
4. bullet group 안에도 들어감
5. 이후 총알이 적과 충돌하면
6. 충돌한 총알 객체를 group에서 제거
'''
'''
그럼 
'''

WHITE = (255, 255, 255)
pad_width = 1024
pad_height = 512

forest_background = pygame.image.load('images/map/forest.jpg')
forest_background = pygame.transform.scale(forest_background, (1024, 512))

class Game:
    def __init__(self):
        pygame.init()
        self.OnceSkill = 0
        self.Max_Mob = 0
        self.Current_Mob = 0
        self.LookAt = True #True is right False is left LookAt
        self.make_map = True
        self.clock = pygame.time.Clock()
        self.pad_width = 1024
        self.pad_height = 512
        self.gamepad = pygame.display.set_mode((pad_width, pad_height))
        pygame.display.set_caption('MapleStory')
        self.player_dict = {'x':300, 'y':200}

    #여러 복수객체들의 경우 pygame.sprite.Group()화 시켜야하는것인가 
    def new(self):
        self.SkillObj = SkillClass(self)
        self.MapObj =  MapClass()
        self.player = Player(self) #플레이어 객체 
        self.playerGroup = pygame.sprite.Group()
        self.MonsterObj = MonsterClass(self)
        self.playerGroup.add(self.player)

#특정 개체수 미만으로 떨어지면 지속적으로 생성
    def LoadMonster(self):
        if self.Max_Mob == 0: #만약 몬스터가 없는 지역이라면
            return
        self.MonsterObj.MakeMonster(self.Max_Mob)
        self.MonsterGroup = self.MonsterObj.GetMonsterGroup()
        self.MonsterGroup.update()
        self.MonsterGroup.draw(self.gamepad)
            
#플레이어의 하단 정보를 불러옴 
    def GetBottomBar(self):
        self.player.Draw_BottomBar()

#지속적으로 맵을 로딩
    def LoadMap(self):
        self.gamepad.blit(forest_background, (0,0))
        self.MapGroup = self.MapObj.GetMapGroup()
        self.MapGroup.draw(self.gamepad)
        self.NpcGroup = self.MapObj.GetNpcGroup()
        self.NpcGroup.draw(self.gamepad)

#포탈에 진입시 맵을 생성함. 그리고 맵에 나타나는 몬스터수 생성 
    def MakeMap(self):
        self.MapObj.Handler(self.player.GetCurrentPos()) #Current_Pos
        self.MonsterObj.InitGroup() #몬스터 그룹 초기화
        self.Max_Mob = self.MapObj.GetMaxMonster(self.player.GetCurrentPos())

    def Check_NpcCollision(self, event):
        self.MapObj.Check_NpcCollision(event)

    def run(self):
        self.playing = True
        self.new()
        while self.playing:
            self.clock.tick(60)    
            if self.make_map == True: #True라면 맵을 만든다. 
                self.MakeMap()
                #맵 로드하고 플레이어 위치 설정 
                self.player.SetPos(self.MapObj.GetSetPlayerPos())
                self.make_map = False

            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.playing = False
                self.Check_NpcCollision(event)
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT]:
                self.LookAt = False
                self.player.move(-2, 0)
            if key[pygame.K_RIGHT]:
                self.LookAt = True
                self.player.move(2, 0)
            if key[pygame.K_LALT ]:
                self.player.CanJump = True 
            if key[pygame.K_LCTRL]: #기본공격
                if self.OnceSkill == 0:
                    self.OnceSkill += 1
                    self.player.skill('Arrow')
                    #self.SkillObj.Handler('Arrow')
                elif self.OnceSkill == 1:
                    self.OnceSkill +=1 
                elif self.OnceSkill == 2:
                    self.OnceSkill += 1
                elif self.OnceSkill == 3:
                    self.OnceSkill = 0


            self.gamepad.fill(WHITE)
            self.LoadMap()
            self.gamepad.blit(self.player.image, self.player.rect)
            self.GetBottomBar()
            self.LoadMonster()
            self.player.update(self.LookAt)
            self.player.jump()
            #현재 스킬 사용중이라면 CanAttack은 공격 가능 여부변수고 공격중인가 아닌가에 대한 변수가 아님
            #skill 그룹에 뭔가가 있나 없나로 판단 
            if self.SkillObj.GetSkillGroup():
                self.SkillObj.GetSkillGroup().update()
                self.SkillObj.GetSkillGroup().draw(self.gamepad)
            
            pygame.display.flip() #화면 전체를 업데이트함. pygame.display.update()와 같지만 이 update는 인수가 있다면 그 인수만 update


game = Game()
game.run()