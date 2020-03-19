import pygame 
import json
from tkinter import *
import tkinter.messagebox

#사다리는 어떻게?
#충돌 처리는 바닥만 , 장애물은 따로 클래스 만들어야 하나 
class MapClass(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.StartMap = [
            "0000000000000000000000000000000000",
            "0                                0",
            "0                                0",
            "0                                0",
            "0                                0",
            "0                           B    0",
            "0                        mmmmmm  0",
            "0                      m         0",
            "0       mmmmmmmm                 0",
            "0                                0",
            "0                mmmmmm          0",
            "0       mmmmmmm                  0",
            "0  p                             0",
            "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",
        ]
        self.GetNpcData()
        self.map_list = {'Start':self.StartMap}
        self.NumberOfMob = {'Start':3}

    def GetNpcData(self):
        with open('json/npc.json', encoding='utf-8') as npcinfo:
            self.npcinfo = json.load(npcinfo)

    def Check_NpcCollision(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            #print("asds")
            for npc in self.NpcGroup:
                self.clicked = npc.rect.collidepoint(event.pos)
                if self.clicked:
                    self.Show_TextBox(npc)
                    return
        return 


    def Show_TextBox(self, npc):
        tkinter.messagebox.showinfo("Quest", npc.npcinfo['talk'])

    def GetMaxMonster(self, MapSelect):
        return self.NumberOfMob[MapSelect]

    def GetMapGroup(self):
        return self.BlockGroup

    def GetNpcGroup(self):
        return self.NpcGroup

    def GetSetPlayerPos(self):
        return self.PlayerSetPos

#Sprite Group 소유
    def Handler(self, MapSelect):
        self.BlockGroup = pygame.sprite.Group()
        self.NpcGroup = pygame.sprite.Group()
        self.PlayerSetPos = []
        map_select = self.map_list[MapSelect]
        x = y = 0
        for row_index, row in enumerate(map_select):
            for col_index, col in enumerate(row):
                if col == ' ' or col == '0':
                    pass
                elif col == 'm': #만약 위에 p라면 해당 좌표 기억
                    if map_select[row_index-1][col_index] == 'p':
                        self.PlayerSetPos = [x,y-2] #+1은 닿기위한 보정값
                    block = MapBlock([x, y])
                    self.BlockGroup.add(block)
                elif col == 'B':
                    npc = MapNPC([x,y], self.npcinfo[col])
                    self.NpcGroup.add(npc)
                x+=30
            y += 30
            x = 0


#pass명에는 아이템:돈 딕셔너리를 넣자. 각 지역 특색에 맞는 아이템들 
#나중에 json파일로 불러오기 

#벽은 쓰지 않는걸로 결정 
StartNpc = pygame.image.load('images/npc/npc.png')
StartNpc = pygame.transform.scale(StartNpc, (60, 60))
StartBlock = pygame.image.load('images/map/soil.jpg')
StartBlock = pygame.transform.scale(StartBlock, (30, 30))

class MapWall(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = StartBlock ###change 
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

class MapLadder(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = StartBlock ###change 
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


class MapBlock(pygame.sprite.Sprite):
    def __init__(self, pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = StartBlock 
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]

#npc마다 역할이 다르니 객체에 하나의 멤버변수 추가, self.role
class MapNPC(pygame.sprite.Sprite):
    def __init__(self, pos, npcinfo):
        pygame.sprite.Sprite.__init__(self)
        self.image = StartNpc
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]-30
        self.npcinfo = npcinfo
        print(pos)
        #self.world = Current_Villeage
        #self.role = NpcRole[role][self.world]

#포탈마다 어디로 가는지 다르니 멤버변수 추가, self.NectPos
class MapPotal(pygame.sprite.Sprite):
    def __init__(self, pos, select):
        pygame.sprite.Sprite.__init__(self)
        self.NextPos = select #이부분도 위의 MapNPC처럼 만들기 