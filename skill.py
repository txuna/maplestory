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
        self.NumberOf_Attack = skillinfo[skill_name]['NumberOf_Attack']
        self.NumberOf_Mob = skillinfo[skill_name]['NumberOf_Mob']
        self.damage_percent = skillinfo[skill_name]['damage_percent']
        if skill_name == 'Arrow': #스킬에 따른 좌표 설정
            pos = list(self.game.player.GetPlayerPos())
            arrow1 = BasicArrow(self.game, pos, self.NumberOf_Attack, self.NumberOf_Mob, self.damage_percent)
            pos[1] -= 20
            arrow2 = BasicArrow(self.game, pos, self.NumberOf_Attack, self.NumberOf_Mob, self.damage_percent)
            self.SkillGroup.add(arrow1)
            self.SkillGroup.add(arrow2)  
            return True
        elif skill_name == 'BoomShot': #스킬에 따른 좌표 설정
            pos = list(self.game.player.GetPlayerPos())
            boom = BoomShot(self.game, pos, self.NumberOf_Attack, self.NumberOf_Mob, self.damage_percent)
            self.SkillGroup.add(boom)
            return True

    def GetSkillGroup(self):
        return self.SkillGroup


Arrow = pygame.image.load('images/skill/arrow.png')
Arrow = pygame.transform.scale(Arrow, (70, 50))

Boom = pygame.image.load('images/skill/boom.png')
Boom = pygame.transform.scale(Boom, (50, 50))
        

class BasicArrow(pygame.sprite.Sprite):
    def __init__(self, game, pos, NumberOf, NumberMob, Damage_Percent):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = Arrow
        self.rect = self.image.get_rect()
        self.rect.midleft = pos
        self.damage = self.game.player.Attack() * (Damage_Percent/100)
        self.distance_x = 300
        self.StartPos_x = pos[0]
        self.NumberOf = NumberOf
        self.NumberMob = NumberMob 
        self.speed = 10

    #몬스터에 맞았다면 Tru #설치형 스킬이라면  상속으로 해?
    def Check_Collision(self):
        if not(self.game.MonsterObj.GetMonsterGroup()): #맵에 몬스터가 존재하지 않는다면
            return False
        mob_collisions = pygame.sprite.spritecollide(self, self.game.MonsterObj.GetMonsterGroup(), False)
        if mob_collisions:
            mob = mob_collisions[0]
            if mob.GetDamage(self.damage, self.NumberOf): #몬스터가 사망했다면
                self.game.player.Increment_Exp(mob.GiveExp())
                return True
            return True
        else:
            return False

    def update(self):
        self.rect.x += self.speed
        if self.Check_Collision():
            self.game.SkillObj.GetSkillGroup().remove(self) 
            return
        if (self.rect.x - self.StartPos_x) >= self.distance_x:
            self.game.SkillObj.GetSkillGroup().remove(self)
        return

class BoomShot(pygame.sprite.Sprite):
    def __init__(self, game, pos, NumberOf, NumberMob, Damage_Percent):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = Boom
        self.rect = self.image.get_rect()
        self.rect.midleft = pos
        self.damage = self.game.player.Attack() * (Damage_Percent/100)
        self.distance_x = 400
        self.StartPos_x = pos[0]
        self.NumberOf = NumberOf
        self.NumberMob = NumberMob   
        self.jump_count = 10  
        self.goup = False
        self.speed = 15

    def Check_Collision(self):
        if not(self.game.MonsterObj.GetMonsterGroup()): #맵에 몬스터가 존재하지 않는다면
            return False
        mob_collisions = pygame.sprite.spritecollide(self, self.game.MonsterObj.GetMonsterGroup(), False)
        if mob_collisions:
            mob = mob_collisions[0]
            if mob.GetDamage(self.damage, self.NumberOf): #몬스터가 사망했다면
                self.game.player.Increment_Exp(mob.GiveExp())
                return True
            return True
        ## 바닥에 맞았을 경우 
        else:
            floors = pygame.sprite.spritecollide(self, self.game.MapObj.GetMapGroup(), False)
            if floors and self.goup == False: #올라가고 있는 타이밍이라면 pass
                return True
            else:
                return False

    def update(self):
        self.rect.x += self.speed
        if self.jump_count >= -10: 
            if self.jump_count >= 0: #상승중
                self.goup = True
            else:
                self.goup = False
            self.rect.y -= (self.jump_count * abs(self.jump_count)) * 0.5
            self.jump_count -= 1
        else:
            self.jump_count = 10
        self.rect.y += (1 ** 2)*10
        if self.Check_Collision():
            self.game.SkillObj.GetSkillGroup().remove(self)
            return
        if (self.rect.x - self.StartPos_x) >= self.distance_x:
            self.game.SkillObj.GetSkillGroup().remove(self)
        return
        

