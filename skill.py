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


Arrow = pygame.image.load('images/skill/arrow.png')
Arrow = pygame.transform.scale(Arrow, (70, 50))

class SkillObject:
    def __init__(self):
        pass

    #몬스터에 맞았다면 Tru #설치형 스킬이라면  상속으로 해?
    def Check_Collision(self, obj):
        if not(obj.game.MonsterObj.GetMonsterGroup()): #맵에 몬스터가 존재하지 않는다면
            return False
        #collided = pygame.sprite.groupcollide(self.game.SkillObj.GetSkillGroup(), self.game.MonsterObj.GetMonsterGroup(), False, True)
        mob_collisions = pygame.sprite.spritecollide(obj, obj.game.MonsterObj.GetMonsterGroup(), False)
        if mob_collisions:
            mob = mob_collisions[0]
            if mob.GetDamage(obj.damage, obj.NumberOf): #몬스터가 사망했다면
                obj.game.player.Increment_Exp(mob.GiveExp())
                return True
            return True
        else:
            return False
        

class BasicArrow(pygame.sprite.Sprite, SkillObject):
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

    def update(self):
        self.rect.x += self.speed
        if super().Check_Collision(self):
            self.game.SkillObj.GetSkillGroup().remove(self) 
            return
        if (self.rect.x - self.StartPos_x) >= self.distance_x:
            self.game.SkillObj.GetSkillGroup().remove(self)
        return

        
