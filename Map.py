import pygame 

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
            "0                                0",
            "0                                0",
            "0                                0",
            "0                                0",
            "0                                0",
            "0                      mmmmmmm   0",
            "0             mmmmmmmmm          0",
            "0    mmmmmmmmm                   0",
            "0                                0",
            "0 p                              0",
            "mmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmmm",
        ]
        self.map_list = {'Start':self.StartMap}
        self.NumberOfMob = {'Start':3}

    def GetMaxMonster(self, MapSelect):
        return self.NumberOfMob[MapSelect]

    def GetMapGroup(self):
        return self.BlockGroup

    def GetSetPlayerPos(self):
        return self.PlayerSetPos

#Sprite Group 소유
    def Handler(self, MapSelect):
        self.PlayerSetPos = []
        self.BlockGroup = pygame.sprite.Group()
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
                x += 30
            y += 30
            x = 0


#pass명에는 아이템:돈 딕셔너리를 넣자. 각 지역 특색에 맞는 아이템들 
#나중에 json파일로 불러오기 
NpcRole = {
    'C' : {
            'Start' : 123, 'Forest':123
            },
    'W' : {
            'Start' : 123, 'Forest':123
            },
}
#벽은 쓰지 않는걸로 결정 
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
    def __init__(self, pos, role):
        pygame.sprite.Sprite.__init__(self)
        #self.world = Current_Villeage
        self.role = NpcRole[role][self.world]

#포탈마다 어디로 가는지 다르니 멤버변수 추가, self.NectPos
class MapPotal(pygame.sprite.Sprite):
    def __init__(self, pos, select):
        pygame.sprite.Sprite.__init__(self)
        self.NextPos = select #이부분도 위의 MapNPC처럼 만들기 