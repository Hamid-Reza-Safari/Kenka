import pygame
from pygame import mixer
from fighter import Fighter
from menu import Menu
from pause import PauseMenu
mixer.init()
pygame.init()

# Game Display Window
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


#Colors
RED = (255, 0 , 0 )
GREEN = (50,205,50)
WHITE = (255 , 255 , 255)
GRAY = (0,0,0)
YELLOW = (255, 255 , 0)




#define fighter variables
P1_SIZE = 200
P1_SCALE = 4
P1_OFFSET = [90, 79]
P1_DATA = [P1_SIZE, P1_SCALE, P1_OFFSET]
P2_SIZE = 200
P2_SCALE = 4
P2_OFFSET = [90, 79]
P2_DATA = [P2_SIZE, P2_SCALE, P2_OFFSET]

#load music and sounds
pygame.mixer.music.load("project/Assets/Sounds/bg_music.wav")
pygame.mixer.music.set_volume(0.15)
pygame.mixer.music.play(-1 , 0.0 )


#LOAD sound effects
attack1_fx = pygame.mixer.Sound("project/Assets/Sounds/attack1.wav")
attack1_fx.set_volume(0.5)

attack2_fx = pygame.mixer.Sound("project/Assets/Sounds/attack2.wav")
attack2_fx.set_volume(0.5)

death_fx = pygame.mixer.Sound("project/Assets/Sounds/death.wav")
death_fx.set_volume(0.5)

death_fx1 = pygame.mixer.Sound("project/Assets/Sounds/death.wav")
death_fx1.set_volume(0.5)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Kenka")

icon_image = pygame.image.load("project/Assets/icon/icon.png")
pygame.display.set_icon(icon_image)


# Background image
bg_image = pygame.image.load("project/Assets/BackGround/BackGround.png").convert_alpha()

#load spritesheets
warrior_sheet = pygame.image.load("project/Assets/Hero1/Hero1.png").convert_alpha()
wizard_sheet = pygame.image.load("project/Assets/Hero2/Hero2.png").convert_alpha()
# load vitory image
victory_img = pygame.image.load("project/Assets/icon/victory.png").convert_alpha()
#Define number of steps
WARRIOR_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]
WIZARD_ANIMATION_STEPS = [8, 8, 2, 6, 6, 4, 6]

#define font
count_font = pygame.font.Font("project/Assets/Font/turok.ttf" , 80)
score_font = pygame.font.Font("project/Assets/Font/turok.ttf" , 50)

#function text
def draw_text(text , font , text_col , x , y ) :
    img = font.render(text, True , text_col)
    screen.blit(img , (x,y))
# DRAW function for background
def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

# health bar
def draw_health_bar (health , x , y):
    ratio = health / 100
    pygame.draw.rect(screen , WHITE , (x - 5 , y - 5 , 410 , 40 ))
    pygame.draw.rect(screen , RED , (x , y , 400 , 30 ))
    pygame.draw.rect(screen , GREEN , (x , y , 400 * ratio , 30))

#pause menu
pause_menu = PauseMenu()


# Main game function
def main():
    #Create Fighters
    fighter_1 = Fighter(1 , 100, 470 , False , P1_DATA , warrior_sheet , WARRIOR_ANIMATION_STEPS , attack1_fx , death_fx)
    fighter_2 = Fighter(2 ,1100, 470, True , P2_DATA , wizard_sheet , WARRIOR_ANIMATION_STEPS ,  attack2_fx , death_fx1)
    #defiine game variabls
    last_count_update = pygame.time.get_ticks()
    intro_count = 3
    score = [0 , 0] #player scores [P1 , P2 ]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000




    # Creating the game's main loop
    main_menu = Menu()
    main_menu.run_menu()
    clock = pygame.time.Clock()
    run = True
     
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.mixer.music.pause()
                    # Pause the game and show the pause menu
                    result = pause_menu.run_menu()
                    if result == "resume":
                        # Resume the game
                        pygame.mixer.music.unpause()
                        continue
                    elif result == "reset":
                        # Reset the game
                        fighter_1 = Fighter(1, 100, 470, False, P1_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, attack1_fx, death_fx)
                        fighter_2 = Fighter(2, 1100, 470, True, P2_DATA, wizard_sheet, WARRIOR_ANIMATION_STEPS, attack2_fx, death_fx1)
                        score = [0, 0]
                        round_over = False
                        intro_count = 3
                        ROUND_OVER_COOLDOWN = 2000
                        last_count_update = pygame.time.get_ticks()
                    

        # Clear the screen
        screen.fill((0, 0, 0))

        # Draw BG
        draw_bg()

        
                    
        # Player stats
        draw_health_bar(fighter_1.health , 20 , 20)
        draw_health_bar(fighter_2.health , 855 , 20)
        # PLAYER 1 SCORE
        draw_text( "P1: " +str(score[0]) , score_font , YELLOW , 435, 5)
        # PLAYER 2 SCORE
        draw_text("P2: " + str(score[1])  , score_font , YELLOW , 745, 5)
        #UPDATE COUNTDOWN
        if intro_count <= 0 :
            #move Fighters
            fighter_1.move(SCREEN_WIDTH , SCREEN_HEIGHT , screen , fighter_2 , round_over)
            fighter_2.move(SCREEN_WIDTH , SCREEN_HEIGHT , screen , fighter_1 , round_over)
        else :
            #display count timer
            draw_text(str(intro_count),count_font , RED , SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 3)
            # update count timer
            if (pygame.time.get_ticks() - last_count_update) >= 1000 :
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()
                #Create Fighters
                fighter_1 = Fighter(1 , 100, 470 , False , P1_DATA , warrior_sheet , WARRIOR_ANIMATION_STEPS , attack1_fx , death_fx )
                fighter_2 = Fighter(2 ,1100, 470, True , P2_DATA , wizard_sheet , WARRIOR_ANIMATION_STEPS ,  attack2_fx , death_fx1)




        #update fighters
        fighter_1.update()
        fighter_2.update()
        #Draw Fighters
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        #check for player defeat
        if round_over == False :
            if fighter_1.alive == False :
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()

            elif fighter_2.alive == False :
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else :
            #display victory
            screen.blit(victory_img , (SCREEN_HEIGHT/2 + 150 , 200))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN :
                round_over = False
                intro_count = 3



        # Update display
        pygame.display.update()

        # Limit frame rate
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
   main()
