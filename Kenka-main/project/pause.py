import pygame
import sys

class PauseMenu:
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
        self.resume_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 - 50, 200, 50)
        self.reset_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 100, 200, 50)
        self.quit_button_rect = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 250, 200, 50)

        # Initialize button state
        self.selected_button = "resume"

    def menu_bg(self, bg_image_path):
        bg_image = pygame.image.load(bg_image_path).convert_alpha()
        scaled_bg = pygame.transform.scale(bg_image, (self.screen_width, self.screen_height))
        self.screen.blit(scaled_bg, (0, 0))

    def draw_buttons(self):
        resume_text = self.font.render("Resume", True, self.yellow if self.selected_button == "resume" else self.white)
        resume_text_rect = resume_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 - 50))
        self.screen.blit(resume_text, resume_text_rect)

        reset_text = self.font.render("Reset", True, self.yellow if self.selected_button == "reset" else self.white)
        reset_text_rect = reset_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))
        self.screen.blit(reset_text, reset_text_rect)

        quit_text = self.font.render("Quit", True, self.yellow if self.selected_button == "quit" else self.white)
        quit_text_rect = quit_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 250))
        self.screen.blit(quit_text, quit_text_rect)

    def run_menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        self.selected_button = "reset"
                    elif event.key == pygame.K_UP :
                        self.selected_button = "resume"
                    elif event.key == pygame.K_ESCAPE :
                        return "resume"
                    elif event.key == pygame.K_RETURN:
                        if self.selected_button == "resume" :
                            print("Resume button selected!")
                            return "resume"
                        elif self.selected_button == "quit":
                            pygame.quit()
                            sys.exit()
                        elif self.selected_button == "reset":
                            print("Reset button selected!")
                            return "reset"
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.resume_button_rect.collidepoint(event.pos):
                        print("Resume button clicked!")
                        return "resume"
                    elif self.reset_button_rect.collidepoint(event.pos):
                        print("Reset button clicked!")
                        return "reset"
                    elif self.quit_button_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            mouse_x, mouse_y = pygame.mouse.get_pos()

            resume_button_hovered = self.resume_button_rect.collidepoint(mouse_x, mouse_y)
            reset_button_hovered = self.reset_button_rect.collidepoint(mouse_x, mouse_y)
            quit_button_hovered = self.quit_button_rect.collidepoint(mouse_x, mouse_y)

            if resume_button_hovered:
                self.selected_button = "resume"
            elif reset_button_hovered:
                self.selected_button = "reset"
            elif quit_button_hovered:
                self.selected_button = "quit"

            self.menu_bg("project/Assets/BackGround/BackGround.png")
            self.draw_buttons()
            
            title_text = self.font.render("Paused", True, self.white)
            title_rect = title_text.get_rect(center=(self.screen_width // 2, 50))
            self.screen.blit(title_text, title_rect)

            pygame.display.flip()
            pygame.time.Clock().tick(60)

if __name__ == "__main__":
    pause_menu_instance = PauseMenu()
    pause_menu_instance.run_menu()
