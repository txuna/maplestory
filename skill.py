import pygame 


class SkillClass(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.CanSkill = True
        self.Start_Ticks = 0
        self.SkillGroup = pygame.sprite.Group()

    def NowSkill(self):
        return self.CanSkill

    #플레이어의 방향 체크
    def Decision_Skill(self, skill_name, skillinfo):
        if skill_name == 'Arrow': #스킬에 따른 좌표 설정
            pos = self.game.player.GetPlayerPos()
            arrow = BasicArrow(self.game, pos, skillinfo[skill_name]['NumberOf_Attack'], skillinfo[skill_name]['NumberOf_Mob'], skillinfo[skill_name]['damage_percent'])
            self.SkillGroup.add(arrow)  
            return True

    def GetSkillGroup(self):
        return self.SkillGroup


'''
    #나중에 Player Class로 옮기기 
    #CanSkill도 PlayerClass에서 
    def Handler(self, skill_name):
        #Start_Ticks가 0이 아니라는 것은  쿨다운을 하고 있다는뜻
        if self.CanSkill != True or self.Start_Ticks != 0: 
            return False
        self.Decision_Skill(skill_name)):
            return False
        else:
            self.CanSkill = False
        #self.CoolDown()
        return True
'''


#TODO json 파일로 저장 데미지 퍼센트 및 관통성, 등등 체크 
Arrow = pygame.image.load('images/skill/arrow.png')
Arrow = pygame.transform.scale(Arrow, (70, 50))

#NumberOf : 한번에 몇대 
#NumberMob : 한번에 몇명

class BasicArrow(pygame.sprite.Sprite):
    def __init__(self, game, pos, NumberOf, NumberMob, Damage_Percent):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = Arrow
        self.rect = self.image.get_rect()
        self.rect.midleft = pos
        self.damage = self.game.player.Attack() * (Damage_Percent/100)
        self.speed = 10
        self.distance_x = 300
        self.StartPos_x = pos[0]
        self.NumberOf = NumberOf
        self.NumberMob = NumberMob 

#몬스터에 맞았다면 Tru #설치형 스킬이라면 
    def Check_Collision(self):
        if not(self.game.MonsterObj.GetMonsterGroup()): #맵에 몬스터가 존재하지 않는다면
            return False
        #collided = pygame.sprite.groupcollide(self.game.SkillObj.GetSkillGroup(), self.game.MonsterObj.GetMonsterGroup(), False, True)
        mob_collisions = pygame.sprite.spritecollide(self, self.game.MonsterObj.GetMonsterGroup(), False)
        if mob_collisions:
            mob = mob_collisions[0]
            if mob.GetDamage(self.damage, self.NumberOf):
                self.game.MonsterObj.GetMonsterGroup().remove(mob)
                self.game.player.Increment_Exp(mob.GiveExp())
                return True
            return True
        else:
            return False


    def update(self):
        self.rect.x += self.speed
        #collision
        if self.Check_Collision():
            self.game.SkillObj.GetSkillGroup().remove(self) 
            #self.game.SkillObj.CanSkill = True
            #print("asds")
            return
        if (self.rect.x - self.StartPos_x) >= self.distance_x:
            self.game.SkillObj.GetSkillGroup().remove(self)
            #self.game.SkillObj.CanSkill = True
        return


        #공격에 맞았거나 사거리가 다 되었다면 
        
