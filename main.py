import random

from pygame import*
from random import*
window = display.set_mode((700, 500))
display.set_caption('Shooter')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

class Gsprite(sprite.Sprite):
    def __init__(self, pimage, px, py, pspeed, ph, pw):
        super().__init__()
        self.image = transform.scale(image.load(pimage), (ph, pw))
        self.speed = pspeed
        self.rect = self.image.get_rect()
        self.rect.x = px
        self.rect.y = py
        self.w = pw
        self.h = ph
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
    def dviz(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 700 - 80:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 7, self.rect.top, -15, 15, 10)
        bullets.add(bullet)


lost = 0
popadanie = 0

class Enemy(Gsprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y >= 500:
            self.rect.y = 0
            self.rect.x = randint(5, 700-self.w-5)
            lost += 1
            loss.play()


class Bullet(Gsprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <= 0:
            self.kill()

bullets = sprite.Group()
rocket = Gsprite("rocket.png", 350, 410, 8, 60, 80)
monsters = sprite.Group()
tarelka1 = Enemy("ufo.png", randint(0, 700), 0, randint(1, 5), 80, 60)
tarelka2 = Enemy("ufo.png", randint(0, 700), 0, randint(1, 5), 80, 60)
tarelka3 = Enemy("ufo.png", randint(0, 700), 0, randint(1, 5), 80, 60)
tarelka4 = Enemy("ufo.png", randint(0, 700), 0, randint(1, 5), 80, 60)
tarelka5 = Enemy("ufo.png", randint(0, 700), 0, randint(1, 5), 80, 60)
monsters.add(tarelka1)
monsters.add(tarelka2)
monsters.add(tarelka3)
monsters.add(tarelka4)
monsters.add(tarelka5)



game = True
clock = time.Clock()
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)

shot = mixer.Sound('shot.ogg')
win = mixer.Sound('pobeda.ogg')
loss = mixer.Sound("loss.ogg")
pop = mixer.Sound("pop.ogg")


font.init()
font1 = font.Font(None, 36)
font2 = font.Font(None, 58)

win_label = font2.render("WIN", 0, (255, 255, 255))
lose = font2.render("LOSS", 0, (255, 255, 255))

finish = False

while game:
    if finish != True:
        window.blit(background, (0, 0))
        rocket.reset()
        rocket.dviz()
        monsters.update()
        monsters.draw(window)
        bullets.draw(window)
        bullets.update()
        if sprite.spritecollide(rocket, monsters, False):
            finish = True
            window.blit(lose, (200, 200))
        list2 = sprite.groupcollide(monsters, bullets, True, True)
        for sp in list2:
            tarelka6 = Enemy("ufo.png", randint(0, 700), 0, randint(1, 5), 80, 60)
            monsters.add(tarelka6)
            popadanie += 1
            pop.play()
        if popadanie >= 15:
            finish = True
            window.blit(win_label, (200, 200))
            win.play()
        if lost >= 10:
            finish = True
            window.blit(lose, (200, 200))
            loss.play()

        textl = font1.render("пропущено: " + str(lost), 0, (255, 255, 255))
        text2 = font1.render("Убито: " + str(popadanie), 0, (255, 255, 255))

        window.blit(text2, (25, 50))
        window.blit(textl, (25, 25))


    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                shot.play()

    display.update()
    clock.tick(60)
