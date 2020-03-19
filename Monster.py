import json 
import pygame 
import random

#몬스터 그룹을 만들때에 한 맵에 나오는 몬스터들끼리 그룹화 하기 
#monster_number로 어떤 몬스터를 가지고올것인지 결정한다. 
#Slime : 0
#Orange_Mushroom : 1

monster_img = []
monster_name = {
    0:'Slime',
    1:'Orange_Mushroom',
}
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
        self.Attacked = False #공격받고 있다면 위헤 health bar 올리기 
        self.game = game
        self.image = monster_img[monster_number]
        self.CanJump = False #True
        self.jump_count = 10
        self.Fallen = True
        self.move_count = 0
        self.direction = 1
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.GetData()
        self.name = monster_name[monster_number]

    def GetData(self):
        with open('json/monster.json', encoding='utf-8') as monsterinfo:
            self.mobinfo = json.load(monsterinfo)

    def Check_Collision(self):
        collisions = pygame.sprite.spritecollide(self, self.game.MapObj.GetMapGroup(), False)
        if collisions:
            for collision in collisions:
                if (collision.rect.top+10 >= self.rect.bottom):
                    self.rect.bottom = collision.rect.top-3 #+1해서 보정값 세워야하나
                    self.CanJump = False #점프 못하게 방지 
                    self.jump_count = 10
                    self.Fallen = False
                else: 
                    continue

    #랜덤으로 움직일지 아닐지 결정   jump_count를 바탕으로 점프가 끝나고 나서야 할지 말지 체크 
    def decision_jump(self):
        if self.CanJump == True or self.mobinfo[self.name]['CanJump'] == False: #여기에 몬스터가 점프 속성이 있는지 체크
            return False #현재 점프중이다.
        else:
            return True #점프중이 아님

    def MakeMoveCount(self):
        return random.choice([0,0, 0, 0,10,14,20])

    def decision_direction(self):
        return random.choice([1, -1])

    def update(self):
        if self.decision_jump(): #점프중이 아닐때 True를 반환함
            self.CanJump = random.choice(TrueFalse)
        if self.move_count == 0:
            self.move_count = self.MakeMoveCount()
            self.direction = self.decision_direction()
        else:
            self.move()
            self.move_count -= 1
        self.jump()

    def move(self):
        x = 2 * self.direction
        if self.rect.right+x >= 1024 or self.rect.left+x<=0:
            return
        else:
            self.rect.x+=x
        self.Fallen = True
        self.Check_Collision()

    def jump(self):
        if self.CanJump:
            if self.jump_count <= 0:
                self.rect.y += (1 ** 2)*10
                self.jump_count -= 1
                self.Check_Collision()
            elif self.jump_count > 0 and self.jump_count <= 10:
                self.rect.y -= (self.jump_count ** 2) * 0.015
                self.jump_count -= 1
            else:
                self.jump_count = 10
                self.CanJump = False
        elif self.Fallen:
            self.rect.y += (1**2)*10
            self.Check_Collision()
        
#대미지 x ( 100 / (100 + 방어력) ) 

    def Attack(self):
        return self.mobinfo[self.name]['damage']

#플레이어의 데미지를 받음 
    def GetDamage(self, damage):
        damage = self.Cal_Damage(damage)
        if self.mobinfo[self.name]['hp'] - damage <= 0:
            return True  #몬스터 사망 
        else:
            self.mobinfo[self.name]['hp'] -= damage
            return False

#방어력 공식 계산
    def Cal_Damage(self, damage):
        return damage * (100 / (100 * self.mobinfo[self.name]['defence']))

    def Health(self):
        pass

    def DropItem(self):
        pass



