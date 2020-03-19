import pygame 

class SkillClass(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.CanSkill = True

    def NowSkill(self):
        return self.CanSkill

    #플레이어의 방향 체크
    def Decision_Skill(self, skill_name):
        if skill_name == 'Arrow':
            pos = self.game.player.GetPlayerPos()
            arrow = BasicArrow(self.game, pos)
            self.SkillGroup.add(arrow)
            #마나 체크 

    def Handler(self, skill_name):
        if self.CanSkill != True:
            #print("OK..")
            return False
        self.SkillGroup = pygame.sprite.Group()
        self.Decision_Skill(skill_name)
        self.CanSkill = False
        return True
    
    def GetSkillGroup(self):
        return self.SkillGroup


#json 파일로 저장 데미지 퍼센트 및 관통성, 등등 체크 
Arrow = pygame.image.load('images/skill/arrow.png')
Arrow = pygame.transform.scale(Arrow, (70, 50))

class BasicArrow(pygame.sprite.Sprite):
    def __init__(self, game, pos):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = Arrow
        self.rect = self.image.get_rect()
        self.rect.midleft = pos
        self.damage = self.game.player.Attack()
        self.speed = 10
        self.distance_x = 300
        self.StartPos_x = pos[0]

#몬스터에 맞았다면 True
    def Check_Collision(self):
        if not(self.game.MonsterObj.GetMonsterGroup()): #맵에 몬스터가 존재하지 않는다면
            return False
        #collided = pygame.sprite.groupcollide(self.game.SkillObj.GetSkillGroup(), self.game.MonsterObj.GetMonsterGroup(), False, True)
        mob_collisions = pygame.sprite.spritecollide(self, self.game.MonsterObj.GetMonsterGroup(), False)
        if mob_collisions:
            mob = mob_collisions[0]
            if mob.GetDamage(self.damage):
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
            self.game.SkillObj.CanSkill = True
            #print("asds")
            return
        if (self.rect.x - self.StartPos_x) >= self.distance_x:
            self.game.SkillObj.GetSkillGroup().remove(self)
            self.game.SkillObj.CanSkill = True
        return


        #공격에 맞았거나 사거리가 다 되었다면 
        
