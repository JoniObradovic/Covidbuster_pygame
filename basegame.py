# Importit

from cmath import sin
import sys
import pygame
import os
import random
import math
import csv
import time
from pygame.locals import *
from pygame import mixer

#Pakotetaan peli odottamaan hiukan jotta ase ei ammu heti pelin alkaessa



#alusta
pygame.init()
# Kello ja framerate
clock = pygame.time.Clock()
# kehyksiä sekunnissa
FPS = 60
# mixer
mixer.init()
# räjähdys (Channel 0)
explosionSound = pygame.mixer.Sound('Sounds/weapons/explosionSound.wav')
explosionSound.set_volume(0.2)
#AWP soundi
rifleSound = pygame.mixer.Sound("Sounds/weapons/rifle.wav")
rifleSound.set_volume(0.1)
#Shotgun soundi
shotgunSound = pygame.mixer.Sound("Sounds/weapons/shotgun.wav")
# tyhjä lipas aseessa (4)
noAmmo = pygame.mixer.Sound("Sounds/weapons/noammo.wav")
noAmmo.set_volume(0.1)
# kerää ammuslaatikko (5)
reload = pygame.mixer.Sound("Sounds/weapons/reload.wav")
reload.set_volume(0.2)
# Korona kuolema sound (Channel 2)
coronaDeath = pygame.mixer.Sound("Sounds/animations/coronaDeathSound.wav")
coronaDeath.set_volume(0.1)
# hyppyääni (channel 3)
jumpSound = pygame.mixer.Sound("Sounds/animations/jumpSound.wav")
coronaDeath.set_volume(0.2)
# valitaan randomilla taustamusiikki 4 vaihtoehdosta
backgroundMusic = mixer.music.load(f"Sounds/BackgroundMusic/{random.randint(0,3)}.wav")
# asetetaan äänenvoimakkuus d
backgroundMusic = mixer.music.set_volume(0.05)
# soitetaan taustamusiikkia loputtomalla loopilla
#pygame.mixer.music.play(-1)


# Pelaajan toimintamuuttujat
move_left = False
move_right = False
attack = False
bomb = False
bombThrown = False
selectedWeapon = 1

#pommin pyöriminen
bombOnScreen = False
roll = True




def game(tason):

    gameLevel = tason


    # Kello ja framerate
    clock = pygame.time.Clock()
    # kehyksiä sekunnissa
    FPS = 60
    # mixer
    mixer.init()
    # räjähdys (Channel 0)
    explosionSound = pygame.mixer.Sound('Sounds/weapons/explosionSound.wav')
    explosionSound.set_volume(0.2)
    #AWP soundi
    rifleSound = pygame.mixer.Sound("Sounds/weapons/rifle.wav")
    rifleSound.set_volume(0.1)
    #Shotgun soundi
    shotgunSound = pygame.mixer.Sound("Sounds/weapons/shotgun.wav")
    # tyhjä lipas aseessa (4)
    noAmmo = pygame.mixer.Sound("Sounds/weapons/noammo.wav")
    noAmmo.set_volume(0.1)
    # kerää ammuslaatikko (5)
    reload = pygame.mixer.Sound("Sounds/weapons/reload.wav")
    reload.set_volume(0.2)
    # Korona kuolema sound (Channel 2)
    coronaDeath = pygame.mixer.Sound("Sounds/animations/coronaDeathSound.wav")
    coronaDeath.set_volume(0.1)
    # hyppyääni (channel 3)
    jumpSound = pygame.mixer.Sound("Sounds/animations/jumpSound.wav")
    coronaDeath.set_volume(0.2)
    # valitaan randomilla taustamusiikki 4 vaihtoehdosta
    backgroundMusic = mixer.music.load(f"Sounds/BackgroundMusic/{random.randint(0,3)}.wav")
    # asetetaan äänenvoimakkuus d
    backgroundMusic = mixer.music.set_volume(0.05)
    # soitetaan taustamusiikkia loputtomalla loopilla
    #pygame.mixer.music.play(-1)


    # Pelaajan toimintamuuttujat
    move_left = False
    move_right = False
    attack = False
    bomb = False
    bombThrown = False
    selectedWeapon = 1

    #pommin pyöriminen
    bombOnScreen = False
    roll = True


    # resoluutio ( X = Leveys pikseliä, Y = Korkeys pikseliä)
    scaleY = 0.6
    resolutionX = 1200
    resolutionY = int(resolutionX * scaleY)


    # peliruutu
    gameScreen = pygame.display.set_mode((resolutionX, resolutionY))
    # ruudun rect clamppia varten
    screen_rect = gameScreen.get_rect()
    screen_rect.center

    # Pelin toimintamuuttujat
    # Painovoima
    GRAVITY = 0.7
    #lähin mitä pelaaja pääsee ruudun reunoja ilman ruudun liikkumista
    MAXSCROLL = 450
    #scrollaajat
    scrollBackground = 0
    scrollScreen = 0
    #leveli rivit ja sarakkeet
    LEVELROWS = 16
    LEVELCOLUMS = 300
    #LEVELI
    #Määritellään tilen koko jotta ne on saman kokosia pelialueen läpi
    LEVELTILESIZE = resolutionY // LEVELROWS
    #montako erilaista leveliobjektia on
    LEVELTILETYPES = 25
    #levelimuuttuja jolla määritellään millä levelillä ollaan
    
    #item tilet yms
    ITEMTILESIZE = resolutionY // LEVELROWS


    # Lataa tekstuurit
    # Tausta
    # Ladataan scrollaavien taustojen layerit matriisiin, range kertoo montako mappia on ja joka mapilla on 4 layeria
    bgmatrix = []
    for row in range(0,4):
        levelrow = []
        for item in range(0,4):
            image = pygame.image.load(f"Models/Background/map{row}/layer{item}.png").convert_alpha()
            levelrow.append(image)
        bgmatrix.append(levelrow)


    # Levelitekstuurit listaan (leveltiletypes = tekstuurien määrä)
    tileTypeList = []
    #iteroidaan tyyppien määrän verran
    for item in range(LEVELTILETYPES):
        #ladataan tekstuurit kansiosta yksitellen
        texture = pygame.image.load(f"Models/Tile/{item}.png")
        #skaalataan tekstuuri tilen kokoiseksi
        texture = pygame.transform.scale(texture,(LEVELTILESIZE, LEVELTILESIZE))
        #lisätään tile listaan
        tileTypeList.append(texture)


    #Aseet

    #pistoolin modeli
    weaponModelPistol = pygame.image.load("Models/items/weapon1.png").convert_alpha()
    #rifle modeli
    weaponModelRifle = pygame.image.load("Models/items/weapon2.png").convert_alpha()
    #sniper modeli
    weaponModelSniper = pygame.image.load("Models/items/weapon3.png").convert_alpha()

    #projektiilit
    #pistooli
    projectileImagePistol = pygame.image.load("Models/Player/projectile/pistol.png").convert_alpha()
    #rifle
    projectileImageRifle = pygame.image.load("Models/Player/projectile/rifle.png").convert_alpha()
    #sniper
    projectileImageSniper = pygame.image.load("Models/Player/projectile/sniper.png").convert_alpha()

    # pommi
    bombImage = pygame.image.load("Models/Player/bomb/0.png").convert_alpha()
    # items
    healthPack = pygame.image.load("Models/items/0.png").convert_alpha()
    ammoPack = pygame.image.load("Models/items/1.png").convert_alpha()
    bombPack = pygame.image.load("Models/items/2.png").convert_alpha()
    # Crosshair
    crosshair1 = pygame.image.load("Models/crosshair.png").convert_alpha()
    crosshairRect = crosshair1.get_rect

    # kursori piiloon
    pygame.mouse.set_visible(False)

    #weaponwheel asiat
    show = False
    empty = pygame.image.load("weaponWheel/empty.png").convert_alpha()
    aselista = [weaponModelPistol, empty, empty, empty]
    listaLaskuri = [0] 
    mousepositionLista = [0,0]


    # dictionary item tyypeille
    itemImages = {"Health": healthPack, "Ammo": ammoPack, "Dynamite": bombPack, "Rifle": weaponModelRifle, "Sniper": weaponModelSniper}

    # Värejä
    WHITE   = (255, 255, 255)
    BLACK   = (0, 0, 0)
    RED     = (255, 0, 0)
    YELLOW  = (255, 255, 0)
    BLUE    = (0, 0, 255)
    GREEN   = (0, 140, 0)
    AQUA    = (0, 255, 255)

    #fontti
    textFont = pygame.font.SysFont("Futura", 20)
    smallfont = pygame.font.SysFont("Futura", 25)
    medfont = pygame.font.SysFont("Futura", 50)
    largefont = pygame.font.SysFont("Futura", 80)

    #vastustajaan healthiiin liittyvät muuttujat
    #lista johon kerätään vihollisten elämät kun niihin osuu
    enemyLista = []
    osumaLista = []

    #piirrä tekstejä ruudulle (itemit, ammukset, HP jne jne)
    # argumentit: | näytettävä teksti | fontin tyyli | tekstin väri | sijainti x,y |
    def drawText(text, font, textColor, x , y):
        #tallennetaan teksti kuvaan | teksti, reunanpehmennys, väri |
        image = font.render(text, True, WHITE)
        #piirretään kuva ruudulle
        gameScreen.blit(image, (x,y))


    # Piirrä tausta
    def draw_background():
        # täytetään tausta mustalla
        gameScreen.fill(BLACK)
        #haetaan valittu mappi
        mapid = gameLevel
        #tekstuurin maksimileveys uuden sijaiteja varten
        width = bgmatrix[mapid][0].get_width()
        #blitataan matrixista halutun mapin tekstuurit i * w blittaa tekstuureja peräkkäin sitä mukaa kun mappia edetään
        #scrollikerroin määrittää kyseisen tekstuurin nopeuden jolloin jokainen layer scrollaa vähän eri tahtiin
        for i in range(0,5):
            gameScreen.blit(bgmatrix[mapid][0], ((i * width)- scrollBackground * 0.4, 0))
            gameScreen.blit(bgmatrix[mapid][1], ((i * width) - scrollBackground * 0.6, resolutionY - bgmatrix[mapid][1].get_height()))
            gameScreen.blit(bgmatrix[mapid][2], ((i * width) - scrollBackground * 0.8, resolutionY - bgmatrix[mapid][2].get_height()))
            gameScreen.blit(bgmatrix[mapid][3], ((i * width) - scrollBackground * 1, resolutionY - bgmatrix[mapid][3].get_height()))
    




    # Yksikkö classi (Täällä luodaan pelaajayksiköt, määritellään liikkeet yksiköille, lisätään animaatiot yms yms yms)
    class Unit(pygame.sprite.Sprite):
        # pelaajan parametrit
        def __init__(self, charType, x, y, scale, speed, ammunition, bombs, health):
            self.laskin = 0
            pygame.sprite.Sprite.__init__(self)
            # luotavan yksikön tyyppi (player, enemy)
            self.charType = charType   
            # onko yksikkö hengissä
            self.alive = True
            # HP
            self.health = health
            # maksimi HP
            self.healthMax = self.health
            # nopeus
            self.speed = speed

            #asemodelit
            #asechekkaus
            self.checkPistol = True
            self.checkRifle = False
            self.checkSniper = False

            self.weaponType1 = weaponModelPistol
            self.weaponType2 = weaponModelRifle
            self.weaponType3 = weaponModelSniper

            

            if selectedWeapon == 1: 
                self.weaponrect = self.weaponType1.get_rect()
            elif selectedWeapon == 2:
                self.weaponrect = self.weaponType2.get_rect()
            elif selectedWeapon == 3:
                self.weaponrect = self.weaponType3.get_rect()
            self.weaponrect.center = (x, y)

            #panokset

            #pistol
            self.ammunition = ammunition
            #rifle
            self.ammunition2 = 500
            #sniper
            self.ammunition3 = 15
            #pommit
            self.bombs = bombs
            #Ultimate mittari
            self.ultcharge = 0
            # suuntanopeudet
            self.velocityY = 0
            # hyppäys
            self.jump = False
            self.isInAir = True
            # suunta
            self.direction = 1
            # suunnan vaihto
            self.flip = False
            # hyökkäys
            self.attack = False
            self.attackCD = 0
            # modelin animaatiolista
            self.animationList = []
            # indeksinumero
            self.frameIndex = 0
            # Päivitä aika
            self.refreshTime = pygame.time.get_ticks()
            # Animaation tyyppejä | 0 = idle | 1 = run | 2 = jump | 3 = attack | death = 4 | 5 = take_hit |
            self.animationType = 0
            #Vastustajan AI muuttujia
            self.movecount = 0
            #AI näkökyky, x,y, kuinka leveä näkökyky ja kuinka korkea näkökyky on. Isompi arov = näkee pitemmälle
            # x suuntaan näkökyky
            self.enemyVision_x = 400
            #y suuntaan näkökyky
            self.enemyVision_y = 30
            
            #AI näkökyky, x,y, kuinka leveä näkökyky ja kuinka korkea näkökyky on. Isompi arov = näkee pitemmälle
            self.visionAI_surface = pygame.Surface((self.enemyVision_x, self.enemyVision_y))
            self.visionAI = pygame.Rect(0, 0, self.enemyVision_x, self.enemyVision_y)
            self.enemyAFK = False
            self.enemyAFKcount = 0


            # Ladataan pelaajien kaikki animaatiot
            # Lisätään listaan kaikki animaatiotyypit joita pelaajalla on ja tallennetaan ne väliaikaisiin listoihin
            # jotka lisätään yhteen isompaan listaan, josta kaikki animaatiot sen jälkeen löytyy
            # Animaation tyyppejä | 0 = idle | 1 = run | 2 = jump | 3 = attack | death = 4 | 5 = take_hit | 6 = bomb |
            animationTypes = ['idle', 'run', 'jump', "attack", "death", "take_hit", "bomb",]
            for a in animationTypes:
                # resetoi väliaikainen kuvatallennuslista
                temporaryList = []
                # Laske kuvien määrä kansiossa (eri animaatioilla on eri määrä kuvia)
                framesInFolder = len(os.listdir(f"models/{self.charType}/{a}"))
                # looppaa laskettujen kuvien määrällä
                for item in range(framesInFolder):
                    # ladataan jokainen sprite vuorollaan,skaalataan se ja lisätään listaan
                    image = pygame.image.load(f"models/{self.charType}/{a}/{item}.png").convert_alpha()
                    image = pygame.transform.scale(image, (int(image.get_width() * scale), int(image.get_height() * scale)))
                    temporaryList.append(image)
                # Lisätään eri animaatiotyyppien animaatiot listoina listan sisälle
                self.animationList.append(temporaryList)

            # laitetaan kuva talteen jota voidaan käyttää
            self.animationimage = self.animationList[self.animationType][self.frameIndex]
            # luodaan surface-neliö ja keskitetään se modelin kanssa
            self.rect = self.animationimage.get_rect()
            self.rect.center = (x, y)
            #leveys ja korkeus
            self.width = self.animationimage.get_width()
            self.heigth = self.animationimage.get_height()
            #luodaan maski unitille                ###########################################
            self.mask = pygame.mask.from_surface(self.animationimage)

            


        # suorittaa kaikkia pelitilan päivityksiä
        def update(self):
            # piirrä viiva hiiren kohtaan aseesta
            pelaaja1.aimMouse()
            # päivitä animaatiot liikkeen mukana
            self.refreshAnimation()
            # onko yksikkö elossa
            self.isAlive()
            # hyökkäyksen viiveen hallinta

            self.mask = pygame.mask.from_surface(self.animationimage)
            if self.attackCD > 0:
                self.attackCD -= 1

        # määritellään pelaajan liike
        def movement(self, move_left, move_right, move_up, move_down):
            
            #ruudun scrollaus
            scrollScreen = 0
            # nollataan pelaajan liikemuuttujat
            deltaX = 0
            deltaY = 0
            #pidetään pelaaja peliruudun sisällä
            #pelaaja1.rect.clamp_ip(screen_rect)

            # Liike vasemmalle
            if move_left:
                # vähennetään x arvoa jolloin liikutaan vasemmalle
                deltaX -= self.speed
                # pelaajan suunta vasemmalle
                self.flip = True
                self.direction = -1
                self.animationUpdate(1)


            # Liike oikealle
            if move_right:
                # kasvatetaan x arvoa jolloin liikutaan oikealle
                deltaX += self.speed
                # pelaajan suunta oikealle
                self.flip = False
                self.direction = 1
                self.animationUpdate(1)
            
            #koronapallolle y-suuntainen liike
            if move_up:
                deltaY -= self.speed
                self.animationUpdate(1)
                self.laskin += 1
            
            if move_down:
                deltaY += self.speed
                self.animationUpdate(1)
                self.laskin += 1

            # Hyppy
            if self.jump == True and self.isInAir == False:
                # toistetaan hyppyefekti
                pygame.mixer.Channel(3).play(jumpSound)
                # määritellään hyppykorkeus (Y akselilla kun vähennetään lukua -> mennään ylöspäin)
                self.velocityY = -18
                self.jump = False
                self.isInAir = True

            # Painovoiman asetus
            # painovoima vetää pelaajaa alaspäin GRAVITY muuttujan määrittämällä luvulla
            if self.charType != "korona":
                self.velocityY += GRAVITY
            # Määritellään limitti ettei vauhti voi nousta yli tietyn arvon.
            if self.velocityY > 10:
                self.velocityY
            # lisätään hyppy liikemuuttujaan
            deltaY += self.velocityY

            # Collision pelaajat
            for tile in pelinKentta.blockList:
            # Collision x-akselilla [1 = tuplen rect lokero], surfacen sijainti x + deltaX, muut sijainnit default]
                if tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.width, self.heigth):
                    deltaX = 0
                    #jos AI osuu seinään, käännä AI toiseen suuntaan
                    if self.charType == "enemy" or self.charType == "korona":
                        #vaihdetaan suunta
                        self.direction *= -1
                        #liikelaskuri nollalle
                        self.movecount = 0

            # Collision y-akselilla [1 = tuplen rect lokero], surfacen sijainti x, surface sijainti y + deltaY, muut sijainnit default]
                if tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.width, self.heigth):
                    #katsotaan hypätäänkö (ollaan tason alapuolella ja Y menee miinukselle)
                    if self.velocityY < 0:
                        #nollataan nopeus Y
                        self.velocityY = 0
                        #Määrätään että tilen pohja - modelin pää on raja
                        deltaY = tile[1].bottom - self.rect.top
                    #katsotaan ollaanko tason yläpuolella (tiputaan kohti pintaa)
                    elif self.velocityY >= 0:
                        #nollataan nopeus Y
                        self.velocityY = 0
                        #hyppy falselle koska ollaan takaisin maassa
                        self.isInAir = False
                        #Määrätään että tilen yläreuna - modelin jalat on raja
                        deltaY = tile[1].top - self.rect.bottom       

            # Collision veden kanssa
            if pygame.sprite.spritecollide(self, waterGroup, False):
                self.health = 0
            # Jos tippuu mapista
            if self.rect.bottom > resolutionY:
                self.health = 0
            #end level
            #if pygame.sprite.spritecollide(self, exitGroup, False):
                #scene = gratz()
            #katsotaan ettei pelaaja mene reunojen ohi (rect vasemmasta reunasta + deltaX alle 0 tai rectin oikea reuna + deltaX on isompi kuin resoluutio x akselilla)
            if self.charType == "player":
                if self.rect.left + deltaX < 0 or self.rect.right + deltaX > resolutionX:
                    deltaX = 0

            # päivitetään surface-neliön sijainti kulkemaan pelaajan liikkeiden mukana
            self.rect.x += deltaX
            self.rect.y += deltaY

            # päivitetään ruudun scrollaus pelaajan liikkeen mukana
            # rajoitetaan scrollaus pelaajan liikeeseen
            if self.charType == "player":
                #katsotaan meneekö pelaaja 200 pikselin päähän oikeasta laidasta tai 200 pikselin päähän vasemmasta laidasta sekä katsotaan ettei scrollata mapin yli turhaan
                if (self.rect.right > resolutionX - MAXSCROLL and scrollBackground < (pelinKentta.levelLen * LEVELTILESIZE - resolutionX)) or (self.rect.left < MAXSCROLL and scrollBackground > deltaX):
                    #perutaan viimeisin liikemuutos
                    self.rect.x -= deltaX
                    #laitetaan scrollaus vastakkaiseen suuntaan pelaajan suunnasta
                    scrollScreen = -deltaX
            #palautetaan scrollaus
            return scrollScreen

        def ultimate(self):

            if self.ultcharge >= 0:          

                mousepos = [0,0]
                mousepos = pygame.mouse.get_pos()

                teleport = Detonation(self.rect.centerx, self.rect.centery, 1, 2)
                detonationGroup.add(teleport)

                self.rect.center = [mousepos[0], mousepos[1]]

                damage = Detonation(self.rect.centerx, self.rect.centery, 10, 1)
                detonationGroup.add(damage)

                for enemy in enemyGroup:
                    if pygame.sprite.spritecollide(enemy, detonationGroup, False):
                        if enemy.alive:
                            enemyLista.append(enemy)
                            osumaLista[0]= True
                            enemy.health -= 200          

                if self.ultcharge > 0:
                    self.ultcharge -= 100

        #tähtäys hiirellä
        def aimMouse(self):
            #haetaan hiiren position
            
            if show == True:
                mouseposition = mousepositionLista
            else:
                mouseposition = pygame.mouse.get_pos()
                mousepositionLista[0] = mouseposition[0]
                mousepositionLista[1] = mouseposition[1]
            mouseRect = crosshair1.get_rect()
            #lyödään rectin sentteri cursorin koordinaatteihin (0 = x, 1 = y)
            mouseRect.center = (mouseposition[0], mouseposition[1])
            #blitataan tähtäin ruudulle
            gameScreen.blit(crosshair1, (mouseRect.x, mouseRect.y))
            #talletetaan hiiren X ja Y sijainnit muuttujiin
            mouseDistanceX = mouseposition[0] - self.rect.centerx
            mouseDistanceY = -(mouseposition[1] - self.rect.centery)
            #Lasketaan tähtäyksen kulma
            self.aimAngle = math.degrees(math.atan2(mouseDistanceY, mouseDistanceX))
        


            #haetaan käytössä olevan aseen recti. distance on puolet assetin leveydestä eli matka keskipisteesä ja tämä luku on hypotenuusana koordinaattilaskuissa
            

            if selectedWeapon == 1: 
                self.weaponrect = self.weaponType1.get_rect()
                self.gun_distance = 32
                pos_correction = 2
                pos_correction_left = 1
            elif selectedWeapon == 2:
                self.weaponrect = self.weaponType2.get_rect()
                self.gun_distance = 54
                pos_correction = 5
                pos_correction_left = 2
            elif selectedWeapon == 3:
                self.weaponrect = self.weaponType3.get_rect()
                self.gun_distance = 62
                pos_correction = 10
                pos_correction_left = 5




            if self.alive:
                    
                

                #ympyrän puolikas välillä 90 astetta -> -90 astetta "oikea puoli"

                if self.aimAngle <= 90 and self.aimAngle >= -90:
                    self.flip = False
                    self.direction = 1

                        #ympyrän neljäsosa 0 - 90 astetta
                    if self.aimAngle > 0:

                        # aseen y-koordinaatti on rectin vasen yläkulma, jonka paikkaa muutetaan hiiren muuttaman kulman mukaisesti.

                        self.weapon_pos_y = self.rect.centery - math.sin(math.radians(self.aimAngle)) * self.gun_distance
                        self.weapon_pos_x = self.rect.centerx - pos_correction


                        #määritetään ammuksen lähtökoordinaatit

                        self.projectile_pos_y = self.rect.centery - math.sin(math.radians(self.aimAngle)) * self.gun_distance * 1.1
                        self.projectile_pos_x = self.rect.centerx + math.cos(math.radians(self.aimAngle)) * self.gun_distance * 1.1


                        #ympyrän neljäsosa 0 - -90 astetta
                    if self.aimAngle <= 0:

                        self.weapon_pos_y = self.rect.centery
                        self.weapon_pos_x = self.rect.centerx - pos_correction

                        self.projectile_pos_y = self.rect.centery - math.sin(math.radians(self.aimAngle)) * self.gun_distance * 1.1
                        self.projectile_pos_x = self.rect.centerx + math.cos(math.radians(self.aimAngle)) * self.gun_distance * 1.1



                    #aseen blittaus ja pyörittely
                    if selectedWeapon == 1:
                        gameScreen.blit(pygame.transform.rotate(self.weaponType1, self.aimAngle), (self.weapon_pos_x, self.weapon_pos_y))
                    elif selectedWeapon == 2:
                        gameScreen.blit(pygame.transform.rotate(self.weaponType2, self.aimAngle), (self.weapon_pos_x, self.weapon_pos_y))
                    elif selectedWeapon == 3:
                        gameScreen.blit(pygame.transform.rotate(self.weaponType3, self.aimAngle), (self.weapon_pos_x, self.weapon_pos_y))

                
                #ympyrän puolikas välillä 90 astetta -> -90 astetta "vasen puoli"

                elif self.aimAngle > 90 or self.aimAngle < -90:
                    self.flip = True
                    self.direction = -1


                        #ympyrän neljäsosa 90 - 180 astetta
                    if self.aimAngle > 90:

                        self.weapon_pos_y = self.rect.centery - math.sin(math.radians(self.aimAngle)) * self.gun_distance
                        self.weapon_pos_x = self.rect.centerx - abs(math.cos(math.radians(self.aimAngle)) * self.gun_distance) + pos_correction_left

                        self.projectile_pos_y = self.rect.centery - math.sin(math.radians(self.aimAngle)) * self.gun_distance * 1.1
                        self.projectile_pos_x = self.rect.centerx + math.cos(math.radians(self.aimAngle)) * self.gun_distance * 1.1 + 19

                
                        #ympyrän neljäsosa -90 - -180 astetta
                    if self.aimAngle <= -90:

                        self.weapon_pos_y = self.rect.centery
                        self.weapon_pos_x = self.rect.centerx - abs(math.cos(math.radians(self.aimAngle)) * self.gun_distance) + pos_correction_left

                        self.projectile_pos_y = self.rect.centery - math.sin(math.radians(self.aimAngle)) * self.gun_distance * 1.1
                        self.projectile_pos_x = self.rect.centerx + math.cos(math.radians(self.aimAngle)) * self.gun_distance * 1 + 19


                    if selectedWeapon == 1:
                        gameScreen.blit(pygame.transform.rotate(pygame.transform.flip(self.weaponType1, False, True), self.aimAngle), (self.weapon_pos_x, self.weapon_pos_y))
                    elif selectedWeapon == 2:
                        gameScreen.blit(pygame.transform.rotate(pygame.transform.flip(self.weaponType2, False, True), self.aimAngle), (self.weapon_pos_x, self.weapon_pos_y))
                    elif selectedWeapon == 3:
                        gameScreen.blit(pygame.transform.rotate(pygame.transform.flip(self.weaponType3, False, True), self.aimAngle), (self.weapon_pos_x, self.weapon_pos_y))           
            
            mouseRect.clamp_ip(screen_rect)

        

        # yksiköitten hyökkäys
        def shooting(self):
                if selectedWeapon == 1 and self.ammunition > 0:
                    if self.attackCD == 0:
                        self.attackCD = 15       
                        # määritetään projektiilin spawnauskohta
                        # kun juostaan oikealle
                        if move_right:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        # kun juostaan vasemmalle
                        elif move_left:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        # kun ollaan idlessä oikealle
                        elif self.direction == 1:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        #kun ollaan idlessä vasemmalle (!kusee atm!)
                        elif self.direction == 0:        
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        else:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        pelaaja1.ammunition -= 1
                        

                elif selectedWeapon == 2 and self.ammunition2 > 0:
                    if self.attackCD == 0:
                        self.attackCD = 5       
                        # määritetään projektiilin spawnauskohta
                        # kun juostaan oikealle
                        if move_right:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        # kun juostaan vasemmalle
                        elif move_left:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        # kun ollaan idlessä oikealle
                        elif self.direction == 1:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        #kun ollaan idlessä vasemmalle (!kusee atm!)
                        elif self.direction == 0:        
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        else:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        pelaaja1.ammunition2 -= 1
                
                elif selectedWeapon == 3 and self.ammunition3 > 0:
                    if self.attackCD == 0:
                        self.attackCD = 30       
                        # määritetään projektiilin spawnauskohta
                        # kun juostaan oikealle
                        if move_right:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        # kun juostaan vasemmalle
                        elif move_left:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        # kun ollaan idlessä oikealle
                        elif self.direction == 1:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        #kun ollaan idlessä vasemmalle (!kusee atm!)
                        elif self.direction == 0:        
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        else:
                            pygame.mixer.Channel(1).play(rifleSound)
                            projectile1 = Projectile(self.projectile_pos_x, self.projectile_pos_y, self.aimAngle)
                            projectileGroup.add(projectile1)

                        pelaaja1.ammunition3 -= 1
                                            
                else:
                    pygame.mixer.Channel(4).play(noAmmo)

        def enemyShooting(self):
            if self.attackCD == 0:
                    self.attackCD = 10
                    if self.direction == 1:
                        self.animationUpdate(1)
                        pygame.mixer.Channel(1).play(rifleSound)
                        projectile1 = Projectile(self.rect.centerx + (0.5 * self.rect.size[0]), self.rect.centery+5, 0)
                        projectileGroup2.add(projectile1)

                    else:
                        pygame.mixer.Channel(1).play(rifleSound)
                        projectile1 = Projectile(self.rect.centerx - (0.5 * self.rect.size[0]), self.rect.centery+5, 180)
                        projectileGroup2.add(projectile1)
                        self.animationUpdate(1)




        #vastustajien liike
        def enemyAI(self):
            
            #tarkastetaan että yksiköt/pelaaja on elossa
            
            if self.alive and pelaaja1.alive:
                # katsotaan onko vastustaja pelaajan lähellä
                if self.visionAI.colliderect(pelaaja1.rect):
                    self.animationUpdate(1)
                    #ammu pelaajaa
                    if self.charType == "enemy":
                        self.enemyShooting()
                    elif self.rect.colliderect(pelaaja1.rect):
                        self.animationUpdate(4)
                        enemyLista.append(pelaaja1)
                        osumaLista[0]= True
                        pelaaja1.health -= 10
                        self.kill()
                        
                    
                
                #luodaan rng AI liikkeille random afk moment
                if self.enemyAFK == False and random.randint(1,200) == 1:
                    self.enemyAFK = True
                    self.enemyAFKcount = 50
                    self.animationUpdate(0)

                else:
                    if self.enemyAFK == False:
                        if self.laskin <= 40:
                            enemyMovesUp = True
                        else:
                            enemyMovesUp = False
                            if self.laskin == 90:
                                self.laskin = 0
                        
                        #jos suunta 1 (oikea)
                        if self.direction == 1:
                            enemyMovesRight = True
                        #suunta 0 (vasen)    
                        else:
                            enemyMovesRight = False
                        #varmistetaan ettei koiteta mennä molempiin suuntiin
                        enemyMovesLeft = not enemyMovesRight
                        enemyMovesDown = not enemyMovesUp
                        #syötetään AI inputit liikefunktiolle
                        self.movement(enemyMovesLeft, enemyMovesRight, enemyMovesUp, enemyMovesDown)
                        self.movecount += 1
                        #AI näkökenttä niin että AI ei näe taakse
                        """((self.enemyVision_x/2) * self.direction) tarkoittaa että näkökenttä sijoittuu joko vasemmalle tai oikealle AI:sta riippuen kumpaan suuntaan se on menossa""" 
                        self.visionAI.center = (self.rect.centerx + ((self.enemyVision_x/2) * self.direction), self.rect.centery)

                        if self.movecount > LEVELTILESIZE:
                            self.direction *= -1
                            self.movecount *= -1
                    else:
                        self.enemyAFKcount -= 1
                        if self.enemyAFKcount <= 0:
                            self.enemyAFK = False
            #vastustaja scrollaus
            self.rect.x += scrollScreen
            
        # päivitetään animaatio
        def refreshAnimation(self):
            # määritellään animaatioiden nopeus (isompi numero = väljempi päivitys, pienempi numero = tiheämpi päivitys)
            REFRESH_COOLDOWN = 40
            # päivitetään kuva riippuen missä framessa ollaan
            self.animationimage = self.animationList[self.animationType][self.frameIndex]
            # katsotaan onko edellisestä päivityksestä kulunut tarpeeksi aikaa
            if pygame.time.get_ticks() - self.refreshTime > REFRESH_COOLDOWN:
                # päivitetään aika
                self.refreshTime = pygame.time.get_ticks()
                # lisätään indeksiin +1
                self.frameIndex += 1
            # Resetoidaan laskuri kun animaatiot on käyty loppuun
            if self.frameIndex >= len(self.animationList[self.animationType]):
                # tarkastetaan onko yksikkö kuollut ja rajoitetaan animaation looppimäärä
                if self.animationType == 4 or self.animationType == 7:
                    self.frameIndex = len(self.animationList[self.animationType]) - 1
                    self.kill()
                else:
                    self.frameIndex = 0

        # Tarkastetaan onko uusi animaatio eri kuin edellinen
        def animationUpdate(self, new_action):
            # Vertaillaan uutta animaatiota vanhaan
            if new_action != self.animationType:
                self.animationType = new_action
                # Päivitetään animaation asetukset
                self.frameIndex = 0
                self.refreshTime = pygame.time.get_ticks()

        #Katsotaan onko yksikön health nollissa
        def isAlive(self):
            if self.health <= 0:
                self.health = 0
                self.speed = 0
                self.alive = False
                self.animationUpdate(4)
                self.scrollBackground = 0
                self.scrollScreen = 0
                


        # piirrä pelaaja/vastustaja
        def render(self):
            gameScreen.blit(pygame.transform.flip(self.animationimage, self.flip, False), self.rect)
            #piirretään rect hitboxi
            #pygame.draw.rect(gameScreen, WHITE, self.rect, 1)

    class weaponWheel:
        
        def __init__(self, koko): #koko on kerroin
            self.mouseposition = pygame.mouse.get_pos()
            self.mousepositionRect = crosshair1.get_rect()
            self.mousepositionRect.center = (self.mouseposition[0], self.mouseposition[1])
            self.koko = koko
            #Ase valikko kun hiiri ei ole minkään alueen päällä -> mikään ei tummene
            self.wheel = pygame.image.load("weaponWheel/weapon_wheel.png").convert_alpha()
            #Oikea yläkulma tumma
            self.wheel_1 = pygame.image.load("weaponWheel/weapon_wheel_1.png").convert_alpha()
            #Oikea alakulma tumma
            self.wheel_2 = pygame.image.load("weaponWheel/weapon_wheel_2.png").convert_alpha()
            #vasen alakulma tumma
            self.wheel_3 = pygame.image.load("weaponWheel/weapon_wheel_3.png").convert_alpha()
            #vasen yläkulma tumma
            self.wheel_4 = pygame.image.load("weaponWheel/weapon_wheel_4.png").convert_alpha()

        def weaponWheel_active(self):
            global selectedWeapon
            #Luodaan asevalikko ja sen rect keskelle ruutua
            self.wheel = pygame.transform.scale(self.wheel, (int(self.wheel.get_width() * self.koko), int(self.wheel.get_height() * self.koko)))
            self.wheel_rect = self.wheel.get_rect()
            self.wheel_rect.center = ((resolutionX/2), (resolutionY/2))
                
            ase_1 = aselista[0]
            ase_1_scaled = pygame.transform.scale(aselista[0], (int(aselista[0].get_width() * self.koko), int(aselista[0].get_height() * self.koko)))
            ase_1_rect= ase_1_scaled.get_rect()
            ase_1_rect.center = ((resolutionX/2)+100, (resolutionY/2)-100)
            gameScreen.blit(ase_1_scaled, ase_1_rect)

            ase_2 = aselista[1]
            ase_2_scaled = pygame.transform.scale(aselista[1], (int(aselista[1].get_width() * self.koko), int(aselista[1].get_height() * self.koko)))
            ase_2_rect= ase_2_scaled.get_rect()
            ase_2_rect.center = ((resolutionX/2)+100, (resolutionY/2)+100)
            gameScreen.blit(ase_2_scaled, ase_2_rect)

            ase_3 = aselista[2]
            ase_3_scaled = pygame.transform.scale(aselista[2], (int(aselista[2].get_width() * self.koko), int(aselista[2].get_height() * self.koko)))
            ase_3_rect= ase_3_scaled.get_rect()
            ase_3_rect.center = ((resolutionX/2)-100, (resolutionY/2)+100)
            gameScreen.blit(ase_3_scaled, ase_3_rect)
                
            ase_4 = aselista[3]
            ase_4_scaled = pygame.transform.scale(aselista[3], (int(aselista[3].get_width() * self.koko), int(aselista[3].get_height() * self.koko)))
            ase_4_rect= ase_4_scaled.get_rect()
            ase_4_rect.center = ((resolutionX/2)-100, (resolutionY/2)-100)
            gameScreen.blit(ase_4_scaled, ase_4_rect)
                

                # jos hiiri ei osu mihinkään ruuduista -> mikään ruuduista ei tummene
            if  pygame.Rect.colliderect(self.mousepositionRect, self.wheel_rect) == False:
                gameScreen.blit(self.wheel, self.wheel_rect)
                    
            elif  pygame.Rect.colliderect(self.mousepositionRect, self.wheel_rect):
                # jos hiiri on keskikohdan ylä- ja oikealla puolella -> näytetään kuva jossa oikea ylä on tummennettu
                if pygame.mouse.get_pos()[0] > self.wheel_rect.center[0] and pygame.mouse.get_pos()[1] < self.wheel_rect.center[1]:
                    self.wheel_1 = pygame.transform.scale(self.wheel_1, (int(self.wheel_1.get_width() * self.koko), int(self.wheel_1.get_height() * self.koko)))
                    self.wheel_rect_1 = self.wheel_1.get_rect()
                    self.wheel_rect_1.center = ((resolutionX/2), (resolutionY/2))
                    gameScreen.blit(self.wheel_1, self.wheel_rect_1)
                    #jos asevalikko ei ole tyhjä kuvakkeen koko kasvaa  
                    if ase_1 != empty:
                        selectedWeapon = 1 
                        ase_1 = pygame.transform.scale(ase_1_scaled, (int(ase_1_scaled.get_width() * 1.5), int(ase_1_scaled.get_height() * 1.5)))
                        ase_1_rect= ase_1.get_rect()
                        ase_1_rect.center = ((resolutionX/2)+100, (resolutionY/2)-100)
                        gameScreen.blit(ase_1, ase_1_rect)
                #sama kuin edellinen mutta alaoikea
                if pygame.mouse.get_pos()[0] > self.wheel_rect.center[0] and pygame.mouse.get_pos()[1] >= self.wheel_rect.center[1]:
                    self.wheel_2 = pygame.transform.scale(self.wheel_2, (int(self.wheel_2.get_width() * self.koko), int(self.wheel_2.get_height() * self.koko)))
                    self.wheel_rect_2 = self.wheel_2.get_rect()
                    self.wheel_rect_2.center = ((resolutionX/2), (resolutionY/2))
                    gameScreen.blit(self.wheel_2, self.wheel_rect_2)
                    
                    #jos asevalikko ei ole tyhjä kuvakkeen koko kasvaa
                    if ase_2 != empty:
                        selectedWeapon = 2
                        ase_2 = pygame.transform.scale(ase_2_scaled, (int(ase_2_scaled.get_width() * 1.5), int(ase_2_scaled.get_height() * 1.5)))
                        ase_2_rect= ase_2.get_rect()
                        ase_2_rect.center = ((resolutionX/2)+100, (resolutionY/2)+100)
                        gameScreen.blit(ase_2, ase_2_rect)
                #sama kuin edellinen mutta alavasen
                if pygame.mouse.get_pos()[0] <= self.wheel_rect.center[0] and pygame.mouse.get_pos()[1] >= self.wheel_rect.center[1]:
                    self.wheel_3 = pygame.transform.scale(self.wheel_3, (int(self.wheel_3.get_width() * self.koko), int(self.wheel_3.get_height() * self.koko)))
                    self.wheel_rect_3 = self.wheel_3.get_rect()
                    self.wheel_rect_3.center = ((resolutionX/2), (resolutionY/2))
                    gameScreen.blit(self.wheel_3, self.wheel_rect_3)

                    #jos asevalikko ei ole tyhjä kuvakkeen koko kasvaa
                    if ase_3 != empty:
                        selectedWeapon = 3
                        ase_3 = pygame.transform.scale(ase_3_scaled, (int(ase_3_scaled.get_width() * 1.5), int(ase_3_scaled.get_height() * 1.5)))
                        ase_3_rect= ase_3.get_rect()
                        ase_3_rect.center =  ((resolutionX/2)-100, (resolutionY/2)+100)
                        gameScreen.blit(ase_3, ase_3_rect)
                #sama kuin edellinen mutta ylävasen
                if pygame.mouse.get_pos()[0] <= self.wheel_rect.center[0] and pygame.mouse.get_pos()[1] <= self.wheel_rect.center[1]:
                    self.wheel_4 = pygame.transform.scale(self.wheel_4, (int(self.wheel_4.get_width() * self.koko), int(self.wheel_4.get_height() * self.koko)))
                    self.wheel_rect_4 = self.wheel_4.get_rect()
                    self.wheel_rect_4.center = ((resolutionX/2), (resolutionY/2))
                    gameScreen.blit(self.wheel_4, self.wheel_rect_4)

                    #jos asevalikko ei ole tyhjä kuvakkeen koko kasvaa
                    if ase_4 != empty:
                        ase_4 = pygame.transform.scale(ase_4_scaled, (int(ase_4_scaled.get_width() * 1.5), int(ase_4_scaled.get_height() * 1.5)))
                        ase_4_rect= ase_4.get_rect()
                        ase_4_rect.center = ((resolutionX/2)-100, (resolutionY/2)-100)
                        gameScreen.blit(ase_4, ase_4_rect)
            # siirretään hiiri asevalikon keskelle kerran
            if 0 in listaLaskuri:
                pygame.mouse.set_pos((resolutionX/2, resolutionY/2))
                listaLaskuri.pop(0)
            


    #Classi levelille

    class WorldLevel():
        def __init__(self):
            #lista jossa on kentän asiat joissa tarvitaan collision
            self.blockList = []
        #prosessoidaan csv tiedoston data
        def levelData_process(self, data):
            self.levelLen = len(data[0])
            #iteroidaan tiedoston jokaisen valuen läpi indeksien avulla
            for yIndex, row in enumerate(data):
                for xIndex, tile in enumerate(row):
                    #tarkastetaan onko solun arvo yli -1 koska -1 tarkoittaa tyhjää paikkaa levelissä ja ne voidaan ignoree
                    if tile >= 0:
                        #haetaan tilelistasta oikea textuuri
                        texture = tileTypeList[tile]
                        #luodaan surface ja kohdennetaan se tileen
                        textureRect = texture.get_rect()
                        textureRect.x = xIndex * LEVELTILESIZE
                        textureRect.y = yIndex * LEVELTILESIZE
                        #luodaan tuple yksittäisille tileille
                        tileInformation = (texture, textureRect)
                        
                        #Selvitetään minkä tyyppinen tekstuuri on ja tarviiko se collisionia yms [tekstuurit 0-8 = maatekstuureja]
                        if tile >= 0 and tile <= 8:
                            #lisätään tekstuuri blocklistiin
                            self.blockList.append(tileInformation)
                        elif tile >= 9 and tile <= 10:
                            #vesitekstuurit
                            water = TileWater(texture, xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE)
                            waterGroup.add(water)
                        elif tile >= 11 and tile <= 14:
                            #boksit ja muu sälä
                            levelDecoration = TileDecorations(texture, xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE)
                            decorationGroup.add(levelDecoration)
                        elif tile == 15:
                            #Pelaaja
                            pelaaja1 = Unit("player", xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE, 1.5, 5, 50, 5, 100)
                            pelaaja1Group.add(pelaaja1)
                        elif tile == 16:
                            #Vastustaja
                            enemy = Unit("enemy", xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE, 1.5, 3, 1000, 0, 100)
                            enemyGroup.add(enemy)
                        elif tile == 17:
                            #ammuslaatikko
                            itemDrop2 = ItemDrops("Ammo", xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE)
                            itemDropGroup.add(itemDrop2)
                        elif tile == 18:
                            #dynamiitit
                            itemDrop3 = ItemDrops("Dynamite", xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE)
                            itemDropGroup.add(itemDrop3)
                        elif tile == 19:
                            #HP
                            itemDrop1 = ItemDrops("Health", xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE)
                            itemDropGroup.add(itemDrop1)
                        elif tile == 20 or tile == 24:
                            #levelistä poistuminen
                            exitLevel = TileExit(texture, xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE)
                            exitGroup.add(exitLevel)
                        elif tile == 21:
                            #Rifle
                            itemDrop4 = ItemDrops("Rifle", xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE)
                            itemDropGroup.add(itemDrop4)
                        elif tile == 22:
                            #Sniper
                            itemDrop5 = ItemDrops("Sniper", xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE)
                            itemDropGroup.add(itemDrop5)
                        elif tile == 23:
                            #Vastustaja
                            korona = Unit("korona", xIndex * LEVELTILESIZE, yIndex * LEVELTILESIZE, 1, 2, 0, 0, 15)
                            enemyGroup.add(korona)
                        

            return pelaaja1
            

        def drawLevel(self):
            #piirretään block tekstuuritdw
            for tile in self.blockList:
                #[rect][x koordinaatti]
                tile[1][0] += scrollScreen
                #blitataan blocklistista tuplet [0= tekstuuri, 1= surface]
                gameScreen.blit(tile[0], tile[1])

    #Classi vedelle
    class TileWater(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + ITEMTILESIZE // 2, y + (ITEMTILESIZE - self.image.get_height()))
        #scrollaus
        def update(self):
            self.rect.x += scrollScreen

    #Classi exitille
    class TileExit(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + ITEMTILESIZE // 2, y + (ITEMTILESIZE - self.image.get_height()))
        #scrollaus
        def update(self):
            self.rect.x += scrollScreen

    #Classi erilaisille levelin sälälle (kivet, ruoho jne)
    class TileDecorations(pygame.sprite.Sprite):
        def __init__(self, img, x, y):
            pygame.sprite.Sprite.__init__(self)
            self.image = img
            self.rect = self.image.get_rect()
            self.rect.midtop = (x + ITEMTILESIZE // 2, y + (ITEMTILESIZE - self.image.get_height()))
        #scrollaus
        def update(self):
            self.rect.x += scrollScreen




    #Classi erilaisille item dropeille
    class ItemDrops(pygame.sprite.Sprite):
        def __init__(self, dropType, x, y):
            pygame.sprite.Sprite.__init__(self)
            #dropin tyyppi (hp, ammo jne)
            self.dropType = dropType
            #lista johon droppien sprite lisätään
            self.image = itemImages[self.dropType]
            #luodaan surface 
            self.rect = self.image.get_rect()

            #luodaan itemille maski                             #####################################
            self.mask = pygame.mask.from_surface(self.image)

            #kohdistetaan surface (leveys = x argumentti + tilesize jaettuna 2 | korkeus = y argumentti - spriten korkeus)
            self.rect.midtop = (x + ITEMTILESIZE // 2, y + (ITEMTILESIZE - self.image.get_height())) 

            #lisätään spritegroupiin                            #################################### poistettu lopusta, ei tarvii erikseen jokaista lisätä
            pygame.sprite.Sprite.add(self, itemDropGroup)

        def update(self):
            #scrollaus
            self.rect.x += scrollScreen
            #piirretään rect hitboxi
            #pygame.draw.rect(gameScreen, WHITE, self.rect, 1)
            #tarkastetaan ottiko pelaaja dropin (item rect -> player rect) ################### muutettu spritecollideksi
            if pygame.sprite.spritecollide(self, pelaaja1Group,False,pygame.sprite.collide_mask):
                #tarkastetaan mikä droppi on otettu
                if self.dropType == "Health":
                    pelaaja1.health += 75
                    #tarkastetaan meneekö pelaajan HP yli max HP
                    if pelaaja1.health > pelaaja1.healthMax:
                        pelaaja1.health = pelaaja1.healthMax

                elif self.dropType == "Ammo":
                    pygame.mixer.Channel(5).play(reload)
                    pelaaja1.ammunition += 100
                    pelaaja1.ammunition2 += 400
                    pelaaja1.ammunition3 += 20

                elif self.dropType == "Dynamite":
                    pygame.mixer.Channel(5).play(reload)
                    pelaaja1.bombs += 15

                elif self.dropType == "Rifle":
                    aselista[1] = weaponModelRifle
                    pelaaja1.checkRifle = True

                elif self.dropType == "Sniper":
                    aselista[2] = weaponModelSniper
                    pelaaja1.checkSniper = True
                    
                    
                #poistetaan käytetty droppi
                self.kill()


    #Projektiiliclassit
    #Perusprojektiili
    class Projectile(pygame.sprite.Sprite):
        def __init__(self, x, y, angle):
            pygame.sprite.Sprite.__init__(self)

            # projektiilin kuva
            if selectedWeapon == 1:
                self.image = pygame.transform.rotate(projectileImagePistol, angle)
                self.speed = 15
                
            elif selectedWeapon == 2:
                self.image = pygame.transform.rotate(projectileImageRifle, angle)
                self.speed = 30
                
            elif selectedWeapon == 3:
                self.image = pygame.transform.rotate(projectileImageSniper, angle)
                self.speed = 90
            
            # Luodaan surface projektiilille
            self.rect = self.image.get_rect()
            # määritetään surface keskelle tekstuuria
            self.rect.center = (x, y)
            # projektiilin suunta
            self.angle = math.radians(angle)
            #lasketaan x ja y nopeudet kulman mukaan
            self.deltaX = math.cos(self.angle) * self.speed
            self.deltaY = -(math.sin(self.angle) * self.speed)
            #luodaan maski projectilelle                            ###################################
            self.mask = pygame.mask.from_surface(self.image)


        # päivitetään projektiili
        def update(self):

            # liikuta projektiilia
            self.rect.x += self.deltaX + scrollScreen
            self.rect.y += self.deltaY + scrollScreen
            # tarkastetaan onko projektiili mennyt ruudun ulkopuolelle ja poistetaan se
            if self.rect.right < 0 or self.rect.left > resolutionX:
                self.kill()
            if self.rect.top < 0 or self.rect.bottom > resolutionY:
                self.kill()
            #collision levelin kanssa
            for tile in pelinKentta.blockList:
                if tile[1].colliderect(self.rect):
                    self.kill()
            #tarkastetaan osuuko projektiili hahmoon sprite colliden avulla
            if pygame.sprite.spritecollide(pelaaja1, projectileGroup2, False, pygame.sprite.collide_mask):
                if pelaaja1.alive:
                    
                    pelaaja1.health -= 5
                    self.kill()
            # tarkastetaan osuuko projektiili vastustajaan ja vähennetään HP arvosta 25 ja tulostetaan se arvo pelaajan ylle
            # iteroidaan kaikkien vastustajien läpi groupissa
            for enemy in enemyGroup:
                # katsotaan törmääkö spritet
                if pygame.sprite.spritecollide(enemy, projectileGroup, False, pygame.sprite.collide_mask):          ########### collide_mask
                    # jos vastustaja on vielä elossa
                    if enemy.alive:
                        enemyLista.append(enemy)
                        osumaLista[0]= True
                        explode = Detonation(self.rect.x, self.rect.y, 1, 1)
                        detonationGroup.add(explode)
                        #vähennetään vastustajalta X hp
                        if selectedWeapon == 1:
                            enemy.health -= 15
                            pelaaja1.ultcharge += 5
                        elif selectedWeapon == 2:
                            enemy.health -= 30
                            pelaaja1.ultcharge += 5
                        elif selectedWeapon == 3:
                            enemy.health -= 150
                            pelaaja1.ultcharge += 25
                        #tuhotaan projektiili
                        self.kill()

    i = 0
    #printtaa näytölle vastustajan jäljellä olevan elämän
    def damageText():
        i = 0
        #käydään läpi viholliset vihollislistasta jotta elämä näkyy oikean vihollisen päällä
        for enemy in enemyLista:
            if enemy != pelaaja1:
                text = textFont.render(f'{enemy.health}', True, AQUA) #texti
                textRect = text.get_rect()  #textin rect
                textRect.center = (enemy.rect.centerx, (enemy.rect.top+i)) #texti lähtee vihollisen keskeltä päältä | i = muutos ylöspäin 
                gameScreen.blit(text, textRect.center) 
                i -= 1 # muutos ylöspäin 1 pikseli

        if pelaaja1 in enemyLista:   
            
            text = textFont.render(f'{pelaaja1.health}', True, GREEN) #texti
            textRect = text.get_rect()  #textin rect
            textRect.center = (pelaaja1.rect.centerx, (pelaaja1.rect.top+i)) #texti lähtee vihollisen keskeltä päältä | i = muutos ylöspäin 
            gameScreen.blit(text, textRect.center) 
            i -= 1 # muutos ylöspäin 1 pikseli


    #Pommi
    class Bomb(pygame.sprite.Sprite):
        def __init__(self, x, y, angle):
            pygame.sprite.Sprite.__init__(self)
            # Pommin ajastin
            self.timer = 100
            # Pommin Y nopeus
            self.velocityY = -12
            # Pommin nopeus
            self.speed = 7
            # Pommin tekstuuri
            self.image = bombImage
            self.orig_image = self.image
            # Luodaan surface pommille
            
            self.rect =self.image.get_rect()
            # määritetään surface keskelle tekstuuria
            self.rect.center = (x, y)
            self.width = self.image.get_width()
            self.height = self.image.get_height()
            # pommin suunta
            self.angle = angle
            #pommin pyörimisen muutos kulma
            self.rotationAngle = 0

            #luodaan maski                                                                                  ###################
            self.mask = pygame.mask.from_surface(self.image)
        
        def rotate(self):
            """Rotate the image of the sprite around its center."""
            # `rotozoom` usually looks nicer than `rotate`. Pygame's rotation
            # functions return new images and don't modify the originals.
            self.image = pygame.transform.rotate(self.orig_image, self.rotationAngle)
            # Create a new rect with the center of the old rect.
            self.rect = self.image.get_rect(center=self.rect.center)
        
        #pommin päivitykset
        def update(self):
            #haetaan globalista True/False muuttujat pommin pyörimistä varten
            roll = False
            bombOnScreen = False
            #lisätään pommeihin painovoima
            self.velocityY += GRAVITY
            deltaX = self.angle * self.speed
            deltaY = self.velocityY

            if pelaaja1.direction == 1:  

                if roll == True or self.rotationAngle != -360 and self.rotationAngle != -180:
                    if self.rotationAngle != 360 and self.rotationAngle != 180: 
                        self.rotationAngle -= 30
                    if self.rotationAngle < -360:
                        self.rotationAngle = 0
                    elif roll == False and self.rotationAngle == -180:
                        self.rotationAngle = -180
                    self.rotate()
            
                    
            elif pelaaja1.direction == -1:
                if roll == True or self.rotationAngle != 360 and self.rotationAngle != 180:
                    if self.rotationAngle != -360 and self.rotationAngle != -180:
                        self.rotationAngle += 30
                    if self.rotationAngle > 360:
                        self.rotationAngle = 0
                    elif roll == False and self.rotationAngle == 180:
                        self.rotationAngle = 180
                    self.rotate()

            #collision levelin kanssa
            for tile in pelinKentta.blockList:
                #collision seinien kanssa
                if tile[1].colliderect(self.rect.x + deltaX, self.rect.y, self.width, self.height):
                    #kun pommi osuu seinään sen pyöriminen loppuu
                    roll = False
                    self.angle *= -1
                    deltaX = self.angle * self.speed
                # Collision y-akselilla [1 = tuplen rect lokero], surfacen sijainti x, surface sijainti y + deltaY, muut sijainnit default]
                if tile[1].colliderect(self.rect.x, self.rect.y + deltaY, self.width, self.height):
                    #määritellään paljonko dynamiitti kimpoaa pinnoista
                    roll = False
                    self.speed = self.speed//2
                    #katsotaan hypätäänkö (ollaan tason alapuolella ja Y menee miinukselle)
                    if self.velocityY < 0:
                        roll = False
                        #nollataan nopeus Y
                        self.velocityY = 0
                        deltaY = tile[1].bottom - self.rect.top
                    #katsotaan ollaanko tason yläpuolella (tiputaan kohti pintaa)
                    elif self.velocityY >= 0:
                        #nollataan nopeus Y
                        self.velocityY = 0
                        #Määrätään että tilen yläreuna - modelin jalat on raja
                        deltaY = tile[1].top - self.rect.bottom         

        

            #päivitetään pommin sijainti
            self.rect.x += deltaX + scrollScreen
            self.rect.y += deltaY
            #Tarkastetaan osuuko pommi suoraan vastustajaan jolloin se räjähtää heti ################ tehty collide_mask
            for enemy in enemyGroup:
                if pygame.sprite.spritecollide(enemy, bombGroup, False, pygame.sprite.collide_mask):
                    if enemy.alive:
                        enemyLista.append(enemy)
                        osumaLista[0]= True
                        #toista räjähdys efekti
                        pygame.mixer.Channel(0).play(explosionSound)
                        self.kill()
                        #tunnistetaan että pommia ei ole enään ruudulla jolloin voidaan heittää uusi pommi
                        bombOnScreen = False
                        explode = Detonation(self.rect.x, self.rect.y, 3, 1)
                        detonationGroup.add(explode)
                        enemy.health -= 50
                        pelaaja1.ultcharge += 25

            #pommin räjäytyslaskenta
            self.timer -=1
            if self.timer <= 0:
                #toista räjähdys efekti
                pygame.mixer.Channel(0).play(explosionSound)
                self.kill()
                #tunnistetaan että pommia ei ole enään ruudulla jolloin voidaan heittää uusi pommi
                bombOnScreen = False
                explode = Detonation(self.rect.x, self.rect.y, 3, 1)
                detonationGroup.add(explode)
                #tee damagea kaikille jotka on lähellä
                
                if pygame.sprite.spritecollide(pelaaja1, detonationGroup, False):
                    pelaaja1.jump = True
                    pelaaja1.isInAir = True
                    
                    
                #if abs(self.rect.centerx - pelaaja1.rect.centerx) < ITEMTILESIZE and abs(self.rect.centery - pelaaja1.rect.centery) < ITEMTILESIZE:
                    #if pelaaja1.alive:
                        #pelaaja1.health -= 50
                for enemy in enemyGroup:
                    if pygame.sprite.spritecollide(enemy, detonationGroup, False, pygame.sprite.collide_mask):
                        if enemy.alive:
                            enemy.health -= 50
                            pelaaja1.ultcharge += 25

    #Räjähdykset
    class Detonation(pygame.sprite.Sprite):
        def __init__(self, x, y, scale, type):
            pygame.sprite.Sprite.__init__(self)
            #kuvalista
            detonationtype = type
            self.images = []
            #lisätän animaation kuvat listaan
            if detonationtype == 1:
                for item in range(0,29):
                    img = pygame.image.load(f"Models/Player/bombExplosion/{item}.png").convert_alpha()
                    #skaalaus
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    self.images.append(img)
            elif detonationtype == 2:
                for item in range(0,15):
                    img = pygame.image.load(f"Models/Player/teleport/{item}.png").convert_alpha()
                    #skaalaus
                    img = pygame.transform.scale(img, (int(img.get_width() * scale), int(img.get_height() * scale)))
                    self.images.append(img)

            #indeksimuuttuja animaation pyörittämiseen
            self.frameIndex = 0
            self.image = self.images[self.frameIndex]
            #Luodaan surface pommille
            self.rect = self.image.get_rect()
            #määritetään surface keskelle tekstuuria
            self.rect.center = (x, y)
            self.count = 0

        #räjäytysten päivitys    
        def update(self):
            #scrollaus
            self.rect.x += scrollScreen
            #animaationopeus (kauanko yksi kuva näkyy)
            DETONATIONSPEED = 2
            #päivitetään räjäytysanimaatio
            self.count += 1
            #loopataan laskurin mukana ja päivitetään näytettävä image listasta
            if self.count >= DETONATIONSPEED:
                self.count = 0
                self.frameIndex += 1
                #tarkastetaan onko animaatio suoritettu ja lopetetaan animaatio
                if self.frameIndex >= len(self.images):
                    self.kill()
                else:
                    self.image = self.images[self.frameIndex]




    # luodaan sprite-ryhmät
    enemyGroup = pygame.sprite.Group()
    projectileGroup = pygame.sprite.Group()
    projectileGroup2 = pygame.sprite.Group()
    bombGroup = pygame.sprite.Group()
    detonationGroup = pygame.sprite.Group()
    itemDropGroup = pygame.sprite.Group()
    pelaaja1Group = pygame.sprite.Group()
    crosshairGroup = pygame.sprite.Group()                      
    waterGroup = pygame.sprite.Group()
    decorationGroup = pygame.sprite.Group()
    exitGroup = pygame.sprite.Group()





    # LEVELIN LUONTI
    levels_Data = []
    # Tehdään lista jossa on rivimuuttuja * lokeromuuttuja verran -1
    # Iteroidaan rivimuuttujan määrä
    for rivi in range(LEVELROWS):
        # Luodaan rivi jossa column muuttujan verran soluja
        levelrow = [-1] * LEVELCOLUMS
        # Lisätään rivi levelilistaan
        levels_Data.append(levelrow)
    # Ladataan levelidata ja luodaan haluttu kenttä
    with open(f"Models/level{gameLevel}_data.csv", newline="") as csvfile:
        #luetaan csv (tiedosto, delimiter = millä merkillä erotellaan solut)
        reader = csv.reader(csvfile, delimiter=",")
        #pilkotaan data riveihin ja soluihin ja indeksoidaan ne [rowindex = rivin indeksit, tileindex = solujen indeksit]
        for rowindex, row in enumerate(reader):
            for tileindex, tile in enumerate(row):
                #lisätään data leveliin kohtaan rivi-indeksi|soluindeksi ja muutetaan string info numeroksi
                levels_Data[rowindex][tileindex] = int(tile)

    #Luodaan instanssi kenttäklassista
    pelinKentta = WorldLevel()
    #kutsutaan metodia jotta saadaan spawnattua kenttä ja modelit
    pelaaja1 = pelinKentta.levelData_process(levels_Data)

    start_time = pygame.time.get_ticks()
    osumaLista.append(False)


    # Main loop
    gameRunning = True
    while gameRunning:

        #jos osumalistaan tallennettu arvo on True
        if osumaLista[0] == True:
            if pygame.time.get_ticks() < start_time+400:
                damageText()
                pygame.display.update() 
            
            #jos aika menee yli 400ms
            else:   
                enemyLista.clear() #tyhjennetään lista johon viholliset on tallennettu
                osumaLista[0] = False #palautetaan osumalistaan arvo False
                i = 0  #palautetaan tekstin lähtöpaikka vihollisen päälle  
        else:
            start_time = pygame.time.get_ticks()
        
        #Ei päästä kursoria ulos peli-ikkunasta pelin aikana
        pygame.event.set_grab(True)
        # tickrate(FPS)
        clock.tick(FPS)

        # piirrä tausta
        draw_background()
        # piirrä leveli
        pelinKentta.drawLevel()
        # piirrä tekstejä
        drawText(f"Health: {pelaaja1.health}", textFont, WHITE, 45, 25)
        gameScreen.blit(healthPack, (5, 22))

        if selectedWeapon == 1:
            drawText(f"Ammunition: {pelaaja1.ammunition}", textFont, WHITE, 45, 75)
            gameScreen.blit(ammoPack, (5, 72))

        elif selectedWeapon == 2:
            drawText(f"Ammunition: {pelaaja1.ammunition2}", textFont, WHITE, 45, 75)
            gameScreen.blit(ammoPack, (5, 72))
            
        elif selectedWeapon == 3:
            drawText(f"Ammunition: {pelaaja1.ammunition3}", textFont, WHITE, 45, 75)
            gameScreen.blit(ammoPack, (5, 72))

        drawText(f"Dynamite: {pelaaja1.bombs}", textFont, WHITE, 45, 125)
        gameScreen.blit(bombPack, (5, 122))

        drawText(f"Ultimate: {pelaaja1.ultcharge}", textFont, WHITE, 45, 175)
        #gameScreen.blit(healthPack, (5, 22))

        # piirrä pelaaja ja animaatio
        pelaaja1.update()
        pelaaja1.render()


        #piirretään vastustajat
        for enemy in enemyGroup:
            enemy.enemyAI()
            enemy.update()
            enemy.render()
        

        #Päivitä ja piirrä sprite-ryhmiä
        projectileGroup.update()
        projectileGroup2.update()
        bombGroup.update()
        detonationGroup.update()
        itemDropGroup.update()
        decorationGroup.update()
        waterGroup.update()
        exitGroup.update()

        projectileGroup.draw(gameScreen)
        projectileGroup2.draw(gameScreen)
        bombGroup.draw(gameScreen)
        detonationGroup.draw(gameScreen)
        itemDropGroup.draw(gameScreen)
        decorationGroup.draw(gameScreen)
        waterGroup.draw(gameScreen)
        exitGroup.draw(gameScreen)

        # Onko pelaaja elossa
        if pelaaja1.alive:
            #päivitetään pelaajan toiminta ja animaatio
            #kun painetaan vasenta hiirtä
            if pygame.mouse.get_pressed()[0]:

                    attack = True
                    pelaaja1.shooting()
                    
            # heitä pommi jos Q ei ole pohjassa ja pommeja on jäljellä ja ruudulla ei ole toista pommia
            if bomb and bombThrown == False and pelaaja1.bombs > 0 and bombOnScreen == False:
                #pommi on ruudulla jolloin ei voida heittää toista
                bombOnScreen = True
                #laitetaan pommi pyörimään
                roll = True
                # pelaajan x = keskikohta + 0.2 * pelaajan leveys (0) * pelaajan suunta, y = pelaajan korkeus - 5, suunta
                bomb = Bomb(pelaaja1.rect.centerx + (0.2 * pelaaja1.rect.size[0] * pelaaja1.direction), pelaaja1.rect.top - 5, pelaaja1.direction)
                bombGroup.add(bomb)
                #vähennetään yksi pommi 
                pelaaja1.bombs -= 1
                #heittotarkastaja
                bombThrown = True
            if pelaaja1.isInAir:
                pelaaja1.animationUpdate(2)
            elif move_left or move_right:
                pelaaja1.animationUpdate(1)
            else:
                pelaaja1.animationUpdate(0)
            # yksikön liike ja ruudun scrollaus sekä taustan scrollaus
            scrollScreen = pelaaja1.movement(move_left, move_right,False,False)
            scrollBackground -= scrollScreen
            
        else:
            scrollScreen = 0
            scrollBackground = 0
            scene = deadbitch()

        # skannataan tapahtumia
        for event in pygame.event.get():

            # poistu pelistä
            if event.type == pygame.QUIT:
                gameRunning = False
                pygame.quit()
                sys.exit()

            # Kun nappi painetaan alas
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_1:
                    selectedWeapon = 1
                    
                if event.key == pygame.K_2 and pelaaja1.checkRifle == True:
                    selectedWeapon = 2
                    
                if event.key == pygame.K_3 and pelaaja1.checkSniper == True:
                    selectedWeapon = 3
                    
                # Suljetaan peli jos painetaan ESC
                if event.key == pygame.K_ESCAPE:
                    scene = mmenu()
                # Jos painetaan A
                if event.key == pygame.K_a:
                    move_left = True
                # Jos painetaan D
                if event.key == pygame.K_d:
                    move_right = True
                # Jos painetaan SPACE
                if event.key == pygame.K_SPACE and pelaaja1.alive:
                    pelaaja1.jump = True
                # Jos painetaan Q
                if event.key == pygame.K_q:
                    bomb = True
                #if event.key == pygame.K_e:
                    #show = True
                    #pygame.mouse.set_visible(True)

                if event.key == pygame.K_f:
                    pelaaja1.ultimate()

                

            # Kun napin painallus lopetetaan
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False
                if event.key == pygame.K_SPACE and pelaaja1.alive:
                    pelaaja1.jump = False
                if event.key == pygame.K_q:
                    bomb = False
                    bombThrown = False
                    bombOnScreen = False
                if event.key == pygame.K_e:
                    pygame.mouse.set_pos(mousepositionLista[0],mousepositionLista[1])
                    show = False
                    listaLaskuri.append(0)
                    pygame.mouse.set_visible(False)
        
        weapon_Wheel = weaponWheel(1.8)
        if show == True:
            selectedWeapon = weapon_Wheel.weaponWheel_active()
        pygame.display.update()
        

        pygame.display.update()

    pygame.quit()


























#  ___ ___   _  _____  ___ _  _____ _____ _   
#| __|_ _| | |/ / _ \/ __| |/ / __|_   _/_\  
#| _| | |  | ' < (_) \__ \ ' <| _|  | |/ _ \ 
#|___|___| |_|\_\___/|___/_|\_\___| |_/_/ \_\
                                             

                                             

    
    

pygame.init()
screen = pygame.display.set_mode((1200, 1200*0.6))
bg = pygame.image.load("Models/Menu/neula2.jpg")
hbg = pygame.image.load("Models/Menu/Help.png")
dbg = pygame.image.load("Models/Menu/Kuolema.png")
nlbg = pygame.image.load("Models/Menu/Nlevel.png")
SCENE_MENU = 0
SCENE_LEVEL = 1
SCENE_HELP = 2
SCENE_PLAY1 = 3
SCENE_PLAY2 = 4
SCENE_PLAY3 = 5
SCENE_DEAD = 6
SCENE_GRATZ = 7
SCENE_PAUSE = 8










 # _   _    _    ____  ____ ___    ____ _        _    ____ ____ ___ 
 #| \ | |  / \  |  _ \|  _ \_ _|  / ___| |      / \  / ___/ ___|_ _|
 #|  \| | / _ \ | |_) | |_) | |  | |   | |     / _ \ \___ \___ \| | 
 #| |\  |/ ___ \|  __/|  __/| |  | |___| |___ / ___ \ ___) |__) | | 
 #|_| \_/_/   \_\_|   |_|  |___|  \____|_____/_/   \_\____/____/___|
                                                                   
class Button:
    def __init__(self, text, width, height, pos, elevation, use):
        
        gui_font = pygame.font.Font(None, 30)
        self.pressed = False
        self.elevation = elevation
        self.dynamic_elecation = elevation
        self.original_y_pos = pos[1]
        self.use = use
        # top 
        self.top_rect = pygame.Rect(pos, (width, height))
        self.top_color = '#475F77'

        # bottom 
        self.bottom_rect = pygame.Rect(pos, (width, height))
        self.bottom_color = '#354B5E'
        # text
        self.text_surf = gui_font.render(text, True, '#FFFFFF')
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

    def draw(self):
        
        self.top_rect.y = self.original_y_pos - self.dynamic_elecation
        self.text_rect.center = self.top_rect.center

        self.bottom_rect.midtop = self.top_rect.midtop
        self.bottom_rect.height = self.top_rect.height + self.dynamic_elecation

        pygame.draw.rect(screen, self.bottom_color,
                         self.bottom_rect, border_radius=12)
        pygame.draw.rect(screen, self.top_color,
                         self.top_rect, border_radius=12)
        screen.blit(self.text_surf, self.text_rect)
        self.check_click()

    
            
    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            self.top_color = '#1E2A34'
            if pygame.mouse.get_pressed()[0]:
                self.dynamic_elecation = 0
                self.pressed = True
            else:
                self.dynamic_elecation = self.elevation
                if self.pressed == True:
                    if self.use == "START":
                        print("naps")
                        scene = level_menu()
                        
                    elif self.use == "QUIT":
                        quit()
                    
                    elif self.use == "BACKTOMENU":
                        scene = mmenu()

                    elif self.use == "HELP":
                        scene = help_menu()

                    elif self.use == "b1":
                        scene = game(1)

                    elif self.use == "b2":
                        scene = game(2)

                    elif self.use == "b3":
                        scene = game(3)

                    self.pressed = False


        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'












#  __  __    _    ___ _   _   __  __ _____ _   _ _   _ 
#|  \/  |  / \  |_ _| \ | | |  \/  | ____| \ | | | | |
#| |\/| | / _ \  | ||  \| | | |\/| |  _| |  \| | | | |
#| |  | |/ ___ \ | || |\  | | |  | | |___| |\  | |_| |
#|_|  |_/_/   \_\___|_| \_| |_|  |_|_____|_| \_|\___/

def mmenu():
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
    

    bstart = Button('Start game', 200, 40, (50, 450), 5, "START")
    bhelp = Button('Help?', 200, 40, (50, 500), 5, "HELP")
    bquit = Button('Quit', 200, 40, (50, 550), 5, "QUIT")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        screen.blit(bg, (0,0))
        bstart.draw()
        bhelp.draw()
        bquit.draw()
    
        pygame.display.update()
        clock.tick(60)













#_     _______     _______ _       __  __ _____ _   _ _   _ 
#| |   | ____\ \   / / ____| |     |  \/  | ____| \ | | | | |
#| |   |  _|  \ \ / /|  _| | |     | |\/| |  _| |  \| | | | |
#| |___| |___  \ V / | |___| |___  | |  | | |___| |\  | |_| |
#|_____|_____|  \_/  |_____|_____| |_|  |_|_____|_| \_|\___/ 
                                                             


def level_menu(): 

    pygame.mouse.set_visible(True)






    clock = pygame.time.Clock()
    
    bback = Button('Back', 200, 40, (50, 550), 5, "BACKTOMENU")
    blevel1 = Button('1', 200, 40, (500, 350), 5, "b1")
    blevel2 = Button('2', 200, 40, (500, 400), 5, "b2")
    blevel3 = Button('3', 200, 40, (500, 450), 5, "b3")
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        screen.blit(bg, (0,0))
        bback.draw()
        blevel1.draw()
        blevel2.draw()
        blevel3.draw()
        
    
        pygame.display.update()
        clock.tick(60)

















# _   _ _____ _     ____    __  __ _____ _   _ _   _ 
#| | | | ____| |   |  _ \  |  \/  | ____| \ | | | | |
#| |_| |  _| | |   | |_) | | |\/| |  _| |  \| | | | |
#|  _  | |___| |___|  __/  | |  | | |___| |\  | |_| |
#|_| |_|_____|_____|_|     |_|  |_|_____|_| \_|\___/ 



def help_menu(): 
    pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()
    
    bback = Button('Back', 200, 40, (500, 550), 5, "BACKTOMENU")
    
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        screen.blit(hbg, (0,0))
        bback.draw()
        
    
        pygame.display.update()
        clock.tick(60)











#    ____  _________  ________  __   ___    _   ______     __    _______    __________    _______   ______ 
#   / __ \/ ____/   |/_  __/ / / /  /   |  / | / / __ \   / /   / ____/ |  / / ____/ /   / ____/ | / / __ \
#  / / / / __/ / /| | / / / /_/ /  / /| | /  |/ / / / /  / /   / __/  | | / / __/ / /   / __/ /  |/ / / / /
# / /_/ / /___/ ___ |/ / / __  /  / ___ |/ /|  / /_/ /  / /___/ /___  | |/ / /___/ /___/ /___/ /|  / /_/ / 
#/_____/_____/_/  |_/_/ /_/ /_/  /_/  |_/_/ |_/_____/  /_____/_____/  |___/_____/_____/_____/_/ |_/_____/  
                                                                                                          




def deadbitch(): 
    pygame.mouse.set_visible(True)

    clock = pygame.time.Clock()
    
    bback = Button('Back', 200, 40, (500, 550), 5, "BACKTOMENU")
    
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        screen.blit(dbg, (0,0))
        bback.draw()
        
    
        pygame.display.update()
        clock.tick(60)


def gratz(): 

    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
    
    bback = Button('Back', 200, 40, (500, 550), 5, "BACKTOMENU")
    
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        screen.blit(nlbg, (0,0))
        bback.draw()
        
    
        pygame.display.update()
        clock.tick(60)





def pause():
    pygame.mouse.set_visible(True)
    clock = pygame.time.Clock()
    
    bback = Button('Back', 200, 40, (500, 550), 5, "BACKTOMENU")
    
    

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        
        bback.draw()
        
    
        pygame.display.update()
        clock.tick(60)














#Ei tartte ymmärtää

def main():
    
    scene = SCENE_MENU

    while True:
        if scene == SCENE_MENU:
            scene = mmenu()
        elif scene == SCENE_LEVEL:
            scene = level_menu()
        elif scene == SCENE_HELP:
            scene = help_menu()
        elif scene == SCENE_PLAY1:  
            pygame.mouse.set_visible(False)
            scene = game(1)           
        elif scene == SCENE_PLAY2:
            pygame.mouse.set_visible(False)
            scene = game(2)           
        elif scene == SCENE_PLAY3:
            pygame.mouse.set_visible(False)
            scene = game(3)
        elif scene == SCENE_DEAD:
            scene = deadbitch()
        elif scene == SCENE_GRATZ:
            scene = gratz()
            












main()
