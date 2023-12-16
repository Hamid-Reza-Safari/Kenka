import pygame
import sys

class Menu:
    def __init__(self):
        # Initialize Pygame
        pygame.init()

        # Set up the screen
        self.screen_width, self.screen_height = 1280, 720
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Kenka")

        # Set up fonts
        self.font = pygame.font.Font("project/Assets/Font/turok.ttf", 80)
        
        # Set up colors
        self.white = (255, 255, 255)
        self.yellow = (255, 255, 0)
    
        # Set up buttons
        self.start_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 - 50, 200, 90)
        self.quit_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 100, 200, 100)

        # Initialize button state
        self.selected_button = "start"
        
    def menu_bg(self, bg_image_path): 
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 720
        bg_image = pygame.image.load(bg_image_path).convert_alpha()
        scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.screen.blit(scaled_bg, (0, 0))

    def draw_buttons(self):
        # Draw buttons without background
        start_text = self.font.render("Start", True, self.yellow if self.selected_button == "start" else self.white)
        start_text_rect = start_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(start_text, start_text_rect)

        quit_text = self.font.render("Quit", True, self.yellow if self.selected_button == "quit" else self.white)
        quit_text_rect = quit_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))
        self.screen.blit(quit_text, quit_text_rect)

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_button = "quit"
                    elif event.key == pygame.K_UP:
                        self.selected_button = "start"
                    elif event.key == pygame.K_RETURN:
                        if self.selected_button == "start":
                            print("Start button selected!")
                            # Add your start game logic here
                            return
                        elif self.selected_button == "quit":
                            pygame.quit()
                            sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.start_button_rect.collidepoint(event.pos):
                        print("Start button clicked!")
                        # Add your start game logic here
                        return
                    elif self.quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            # Get mouse position
            mouse_x, mouse_y = pygame.mouse.get_pos()
    
            # Check if the mouse is over the buttons
            start_button_hovered = self.start_button_rect.collidepoint(mouse_x, mouse_y)
            quit_button_hovered = self.quit_button_rect.collidepoint(mouse_x, mouse_y)

            # Update selected button based on mouse position
            if start_button_hovered:
                self.selected_button = "start"
            elif quit_button_hovered:
                self.selected_button = "quit"

            # Background image
            self.menu_bg("project/Assets/BackGround/MenuGround.png")

            # Kebinds photos
            #player 1 text
            RED = (255, 0 , 0 )
            self.Pfont = pygame.font.Font("project/Assets/Font/turok.ttf", 40)
            P1_text = self.Pfont.render("Player 1 KeyBinds", True , RED)
            self.screen.blit(P1_text,(100,250))
            #player 1 picture
            P1_KB = pygame.image.load("project/Assets/Hero1/keybinds2.png")
            self.screen.blit(P1_KB,(30,300) )
            #player 2 text
            self.Pfont = pygame.font.Font("project/Assets/Font/turok.ttf", 40)
            P2_text = self.Pfont.render("Player 2 KeyBinds", True , RED)
            self.screen.blit(P2_text,(870,150))
            #player 2 picture
            P2_KB = pygame.image.load("project/Assets/Hero2/kb3.png")
            P2_KB1 = pygame.image.load("project/Assets/Hero2/kb4.png")
            self.screen.blit(P2_KB,(800,200) )
            self.screen.blit(P2_KB1,(850,400))



            self.draw_buttons()
            
            # Draw title
            title_text = self.font.render("Kenka", True, self.white)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
            self.screen.blit(title_text, title_rect)

            # Update the display
            pygame.display.flip()

            # Cap the frame rate
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    menu_instance = Menu()
    menu_instance.run_menu()
