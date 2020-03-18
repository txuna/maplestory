import json 
import pygame 
import random

#몬스터 그룹을 만들때에 한 맵에 나오는 몬스터들끼리 그룹화 하기 
#monster_number로 어떤 몬스터를 가지고올것인지 결정한다. 

monster_img = []

slime = pygame.image.load('images/monster/slime.png')
monster_img.append(pygame.transform.scale(slime, (60, 60)))
TrueFalse = [True, False]

test_pos = [(800, 100), (700, 100), (600, 100)]

class MonsterClass(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.InitGroup()
        self.Currnet_Mob = 0

    def MakeMonster(self, Max_Mob):
        if self.Currnet_Mob+1 == Max_Mob:
            return
        for index, _ in enumerate(range(self.Currnet_Mob, Max_Mob, 1)):
            mob = Monster(self.game, 0, test_pos[index])
            self.Currnet_Mob+=1
            self.MonsterGroup.add(mob)
   
    def GetMonsterGroup(self):
        return self.MonsterGroup
    
    def InitGroup(self):
        self.MonsterGroup = pygame.sprite.Group()


class Monster(pygame.sprite.Sprite):
    def __init__(self, game, monster_number, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = monster_img[monster_number]
        self.CanJump = True
        self.jump_count = 10
        self.Fallen = True
        self.rect = self.image.get_rect()
        self.rect.center = pos

    def Check_Collision(self):
        collisions = pygame.sprite.spritecollide(self, self.game.MapObj.GetMapGroup(), False)
        if collisions:
            for collision in collisions:
                if (collision.rect.top+10 >= self.rect.bottom):
                    self.rect.bottom = collision.rect.top-3#+1해서 보정값 세워야하나
                    self.CanJump = False #점프 못하게 방지 
                    self.jump_count = 10
                    self.Fallen = False
                else: 
                    continue

    #랜덤으로 움직일지 아닐지 결정   jump_count를 바탕으로 점프가 끝나고 나서야 할지 말지 체크 
    def decision_jump(self):
        if self.CanJump == True:
            return False #현재 점프중이다.
        else:
            return True #점프중이 아님

    def update(self):
        if self.decision_jump(): #점프중이 아닐때 True를 반환함
            self.CanJump = random.choice(TrueFalse)
        self.move()
        #self.move(random.choice([0,2,2,2,-2,-2,-2]))
        self.jump()

    def move(self):
        x = -2
        self.rect.x+=x
        self.Check_Collision()

    def jump(self):
        if self.CanJump:
            if self.jump_count <= 0:
                self.rect.y += (1 ** 2)*10
                self.jump_count -= 1
                self.Check_Collision()
            elif self.jump_count > 0 and self.jump_count <= 10:
                self.rect.y -= (self.jump_count ** 2) * 0.1
                self.jump_count -= 1
            else:
                self.jump_count = 10
                self.CanJump = False
        elif self.Fallen:
            self.rect.y += (1**2)*10
            self.Check_Collision()
        

    def GetDamage(self):
        pass

    def SetHealth(self):
        pass

    def DropItem(self):
        pass



