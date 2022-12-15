
import pygame
import sys

#  ___ ___   _  _____  ___ _  _____ _____ _   
#| __|_ _| | |/ / _ \/ __| |/ / __|_   _/_\  
#| _| | |  | ' < (_) \__ \ ' <| _|  | |/ _ \ 
#|___|___| |_|\_\___/|___/_|\_\___| |_/_/ \_\
                                             

                                             

    
    

pygame.init()
screen = pygame.display.set_mode((1200, 1200*0.6))

bg = pygame.image.load("Models/Menu/neula2.jpg")


SCENE_MENU = 0
SCENE_LEVEL = 1



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
                    self.pressed = False
        else:
            self.dynamic_elecation = self.elevation
            self.top_color = '#475F77'






def mmenu():

    clock = pygame.time.Clock()
    

    bstart = Button('Start game', 200, 40, (50, 400), 5, "START")
    bsettings = Button("Settings", 200, 40, (50, 450), 5, "Sanna marin on kissa MIAUMIAU")
    bhelp = Button('Help?', 200, 40, (50, 500), 5, "KISSA")
    bquit = Button('Quit', 200, 40, (50, 550), 5, "QUIT")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        screen.fill('#DCDDD8')
        screen.blit(bg, (0,0))
        bstart.draw()
        bsettings.draw()
        bhelp.draw()
        bquit.draw()
    
        pygame.display.update()
        clock.tick(60)


def level_menu(): 








    clock = pygame.time.Clock()
    
    bback = Button('Back', 200, 40, (50, 550), 5, "BACKTOMENU")
    blevel1 = Button('1', 200, 40, (500, 350), 5, "tapaittes")
    blevel2 = Button('2', 200, 40, (500, 400), 5, "tapaittes")
    blevel3 = Button('3', 200, 40, (500, 450), 5, "tapaittes")
    blevel4 = Button('4', 200, 40, (500, 500), 5, "tapaittes")

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
        blevel4.draw()
    
        pygame.display.update()
        clock.tick(60)



def main():
    
    scene = SCENE_MENU

    while True:
        if scene == SCENE_MENU:
            scene = mmenu()
        elif scene == SCENE_LEVEL:
            scene = level_menu()


main()