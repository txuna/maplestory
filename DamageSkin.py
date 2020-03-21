import pygame


class DamageSkin(pygame.sprite.Sprite):
    def __init__(self, game):
        self.game = game
        pygame.sprite.Sprite.__init__(self)
        self.DamageSkin_Group = pygame.sprite.Group()
    
    def GetSkinGroup(self):
        return self.DamageSkin_Group

    def Handler(self, KindOf, damage, pos):
        if KindOf == 'damage':
            damage_value = DamageValueSkin(self.game, damage, pos)
            self.DamageSkin_Group.add(damage_value)

        elif KindOf == 'effect':
            pass



'''
usertext = self.font.render('Lv.{}    {}'.format(str(level), name), True, WHITE, GRAY)
usertextRect = usertext.get_rect()
usertextRect.topleft = (20,445)
self.game.gamepad.blit(usertext, usertextRect)
'''
DAMAGE_COLOR = (180, 4, 174)
WHITE = (255, 255, 255)

class DamageEffectSkin(pygame.sprite.Sprite):
    def __init(self):
        pygame.sprite.Sprite.__init__(self)
        

    
class DamageValueSkin(pygame.sprite.Sprite):
    def __init__(self, game, damage, pos):
        self.font = pygame.font.Font('font/Maplestory_Bold.ttf', 20)
        pygame.sprite.Sprite.__init__(self)
        self.damage = damage
        self.game = game
        self.image = self.font.render(str(self.damage), True, DAMAGE_COLOR, WHITE)
        self.rect = self.image.get_rect()
        #피격 당한 몬스터의 위치 제공 필요
        self.rect.topleft = pos
        #객체가 생성되는 동시에 시간 셈 -> 2초가 지나면 해당 그룹에서 제거 
        self.Start_Ticks = pygame.time.get_ticks() 

    def update(self):
        self.CheckTime()

    def CheckTime(self):
        seconds = (pygame.time.get_ticks() - self.Start_Ticks)/1000
        if seconds >= 0.5:
            self.game.DamageSkin.GetSkinGroup().remove(self)
            return
        else:
            return
            ##self.game.gamepad.blit(self.damage_text, self.damage_rect)