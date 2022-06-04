import pygame # importation de la librairie pygame
import sys # pour fermer correctement l'application
import random


# lancement des modules inclus dans pygame
pygame.init()

#définir les fps
clock = pygame.time.Clock()
fps = 60

screen_width = 600
screen_height = 800

screen = pygame.display.set_mode((screen_width,   screen_height))
pygame.display.set_caption('Space Invanders')





#définir le font
font30 = pygame.font.SysFont('Constantia', 30)
font40 = pygame.font.SysFont('Constantia', 40)

#définir les variables du jeu
rows = 5
cols = 5
alien_cooldown = 1000
last_alien_shot = pygame.time.get_ticks()
countdown = 3
last_count = pygame.time.get_ticks()
game_over = 0#0 n'est pas terminé, 1 signifie que le joueur a gagné, -1 signifie que le joueur a perdu

#définir les couleurs
red = (255, 0, 0)
green = (0, 255, 0)
white = (255, 255, 255)

# chargement de l'image de fond
bg = pygame.image.load("img/background.png")

def draw_bg():
    screen.blit(bg, (0, 0))



#définir une fonction pour pouvoir ajouter du texte
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

# creation du joueur
class Vaisseau(pygame.sprite.Sprite):
    def __init__(self, x, y, health):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/vaisseau.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.health_start = health
        self.health_remaining = health
        self.last_shot = pygame.time.get_ticks()


    def update(self):
        #vitesse de déplacement
        speed = 8
        #la variable de recharge de notre Vaisseau
        cooldown = 500
        game_over = 0


        #ajouter noutre touche sur le clavier avec "key"
        key = pygame.key.get_pressed()
        if key[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if key[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += speed


        time_now = pygame.time.get_ticks()
        #Pour tirer
        if key[pygame.K_SPACE] and time_now - self.last_shot > cooldown:

            balle = Balles(self.rect.centerx, self.rect.top)
            balle_group.add(balle)
            self.last_shot = time_now


        #mise à jour avec "mask"
        self.mask = pygame.mask.from_surface(self.image)


        #dessiner la barre de vie
        pygame.draw.rect(screen, red, (self.rect.x, (self.rect.bottom + 10), self.rect.width, 15))
        if self.health_remaining > 0:
            pygame.draw.rect(screen, green, (self.rect.x, (self.rect.bottom + 10), int(self.rect.width * (self.health_remaining / self.health_start)), 15))
        elif self.health_remaining <= 0:

            self.kill()
            game_over = -1
        return game_over



# creation de la balle
class Balles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/balle.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y -= 5
        if self.rect.bottom < 0:
            self.kill()
        if pygame.sprite.spritecollide(self, alien_group, True):
            self.kill()


# creation des ennemis
class Aliens(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien" + str(random.randint(1, 5)) + ".png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.move_counter = 0
        self.move_direction = 1

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 75:
            self.move_direction *= -1
            self.move_counter *= self.move_direction
class Alien_Balles(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("img/alien_balle.png")
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]

    def update(self):
        self.rect.y += 2
        if self.rect.top > screen_height:
            self.kill()
        if pygame.sprite.spritecollide(self, vaisseau_group, False, pygame.sprite.collide_mask):
            self.kill()

            #Pour réduire la barre de vie du vaisseau
            vaisseau.health_remaining -= 1






#Il faut créer les groupes de "sprites" (avec sprite)
vaisseau_group = pygame.sprite.Group()
balle_group = pygame.sprite.Group()
alien_group = pygame.sprite.Group()
alien_balle_group = pygame.sprite.Group()



def create_aliens():
    #Générer nos aliens
    for row in range(rows):
        for item in range(cols):
            alien = Aliens(100 + item * 100, 100 + row * 70)
            alien_group.add(alien)

create_aliens()


#créer notre joueur "avec le vaisseau"
vaisseau = Vaisseau(int(screen_width / 2), screen_height - 100, 3)
vaisseau_group.add(vaisseau)
run = True
while run:

    clock.tick(fps)

    #dessiner notre fond (backgrounf)
    draw_bg()


    if countdown == 0:
        #créer des balles extraterrestres aléatoires

        time_now = pygame.time.get_ticks()
        #tirer
        if time_now - last_alien_shot > alien_cooldown and len(alien_balle_group) < 5 and len(alien_group) > 0:
            attacking_alien = random.choice(alien_group.sprites())
            alien_balle = Alien_Balles(attacking_alien.rect.centerx, attacking_alien.rect.bottom)
            alien_balle_group.add(alien_balle)
            last_alien_shot = time_now

        #vérifier si tous les extraterrestres ont été tués
        if len(alien_group) == 0:
            game_over = 1

        if game_over == 0:
            #mettre à jour le vaisseau spatial
            game_over = vaisseau.update()

            #mettre à jour les groupes de sprites
            balle_group.update()
            alien_group.update()
            alien_balle_group.update()
        else:
            if game_over == -1:
                draw_text('GAME OVER!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))
            if game_over == 1:
                draw_text('VICTOIRE!', font40, white, int(screen_width / 2 - 100), int(screen_height / 2 + 50))

    if countdown > 0:
        draw_text('PRÊT!', font40, white, int(screen_width / 2 - 110), int(screen_height / 2 + 50))
        draw_text(str(countdown), font40, white, int(screen_width / 2 - 10), int(screen_height / 2 + 100))
        count_timer = pygame.time.get_ticks()
        if count_timer - last_count > 1000:
            countdown -= 1
            last_count = count_timer





    #dessiner des groupes de sprites
    vaisseau_group.draw(screen)
    balle_group.draw(screen)
    alien_group.draw(screen)
    alien_balle_group.draw(screen)



    #la gestion d'évenements
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False


    pygame.display.update()

pygame.quit()