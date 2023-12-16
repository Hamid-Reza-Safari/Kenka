import pygame


class Fighter():
    def __init__(self, player , x, y , flip, data , sprite_sheet , animation_steps , sound , death):
        self.player = player
        self.size = data [0]
        self.image_scale = data[1]
        self.offset = data[2]
        self.flip = flip
        self.action = 0#0:idle #1:run #2:jump #3:attack1 #4: attack2 #5:hit #6:death
        self.frame_index = 0
        self.animation_list = self.load_images(sprite_sheet, animation_steps)
        self.image = self.animation_list[self.action][self.frame_index]
        self.update_time = pygame.time.get_ticks()
        self.rect = pygame.Rect(x, y, 140, 180)
        # Velocity
        self.vel_y = 0
        self.running = False
        #JUMP
        self.jump = False
        self.jump_cooldown = 0
        # Attack Type
        self.attacking = False
        self.attack_type = 0
        self.attack_cooldown = 0
        self.hit = False
        self.health = 100
        self.alive = True
        self.attack_sound = sound
        self.death_sound = death
    def load_images(self, sprite_sheet, animation_steps):
        animation_list = []

        sheet_width, sheet_height = sprite_sheet.get_size()  # Get the size of the sprite sheet

        for y, animation in enumerate(animation_steps):
            temp_img_list = []

            for x in range(animation):
                # Calculate the top-left coordinates of the subsurface
                left = x * self.size
                top = y * self.size

                # Check if the subsurface is within the bounds of the sprite sheet
                if left + self.size <= sheet_width and top + self.size <= sheet_height:
                    temp_img = sprite_sheet.subsurface(left, top, self.size, self.size)

                    temp_img_list.append(pygame.transform.scale(temp_img , (self.size * self.image_scale , self.size * self.image_scale )))


            animation_list.append(temp_img_list)

        return animation_list

    def move(self , SCREEN_WIDTH , SCREEN_HEIGHT , surface , target , round_over):
        SPEED = 5
        GRAVITY = 2
        dx = 0
        dy = 0
        self.running = False
        self.attack_type = 0
        # Get key presses
        keys = pygame.key.get_pressed()
        #can't do anything but walk while attacking
        if self.attacking == False and self.alive == True and round_over == False :
            #player 2 movement
            if self.player == 1  :
                # Movement
                if keys[pygame.K_a]  :
                        dx = -SPEED
                        self.running = True
                if keys[pygame.K_d] :
                    dx = SPEED
                    self.running = True
                    #Jump
                if keys[pygame.K_w] and not self.jump and self.jump_cooldown == 0 :
                    self.vel_y = - 25
                    self.jump = True
                    self.jump_cooldown = 60
                    #attack
                if keys[pygame.K_e] or keys[pygame.K_q] :
                    self.attack( target)
                        # Q or E ?
                if keys[pygame.K_e]  :
                    self.attack_type = 1
                if keys[pygame.K_q] :
                    self.attack_type = 2
            #Player 2 movement
            if self.player == 2  :
                # Movement
                if keys[pygame.K_j] or keys[pygame.K_LEFT]:
                        dx = -SPEED
                        self.running = True
                if keys[pygame.K_l] or keys[pygame.K_RIGHT]:
                    dx = SPEED
                    self.running = True
                    #Jump
                if keys[pygame.K_i]  and not self.jump and self.jump_cooldown == 0 or keys[pygame.K_UP] and not self.jump and self.jump_cooldown == 0:
                    self.vel_y = - 25
                    self.jump = True
                    self.jump_cooldown = 60
                    #attack
                if keys[pygame.K_u] or keys[pygame.K_o] or keys[pygame.K_KP0] or keys[pygame.K_KP_PERIOD]:
                    self.attack(target)
                        # U or O ?
                if keys[pygame.K_u] or keys[pygame.K_KP0]:
                    self.attack_type = 1
                if keys[pygame.K_o] or keys[pygame.K_KP_PERIOD] :
                    self.attack_type = 2


        #apply gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        # Update player position
        self.rect.x += dx
        self.rect.y += dy
        # Making sure player stays on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 650:
            self.rect.bottom = 650
            self.jump = False


        #ensure Player looking at each other
        if target.rect.centerx > self.rect.centerx :
             self.flip = False
        else :
             self.flip = True


        #reduce attack cooldown
        if self.attack_cooldown > 0 :
            self.attack_cooldown -= 1
        #reduce jump cooldown
        if self.jump_cooldown > 0:
            self.jump_cooldown -= 1
    #handle animation
    def update(self) :
        if self.health <= 0 :
            self.health = 0
            self.alive = False
            self.death_sound.play()
            self.update_action(6) # DEAD
        #check player action
        elif self.hit == True :
            self.update_action(5) # HIT
        elif self.attacking == True:
            if self.attack_type == 1:
                self.update_action(3) # ATTACK 1
            elif self.attack_type == 2:
                self.update_action(4) # ATTACK 2

        elif self.jump == True :
            self.update_action(2) # JUMP
        elif self.running == True :
         self.update_action(1) # run
        else :
            self.update_action(0) # idle
        animation_cooldown = 55
        #update image
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if pygame.time.get_ticks() - self.update_time > animation_cooldown:
            self.frame_index += 1
            self.update_time = pygame.time.get_ticks()
        if self.frame_index >= len(self.animation_list[self.action]):
             # if player is dead  end the animation
             if self.alive == False :
                 self.frame_index = len(self.animation_list[self.action]) - 1
             else :
                 self.frame_index = 0
                    # CHECK FOR ATTACK
                 if self.action == 3 or self.action == 4 :
                        self.attacking = False
                        self.attack_cooldown = 30
                    # check if damage taken
                 if self.action == 5 :
                        self.hit = False
                        #
                        self.attacking = False
                        self.attack_cooldown = 20


    def attack (self , target) :
        if self.attack_cooldown == 0 :
            # attack
            self.attacking = True
            self.attack_sound.play()
            attacking_rect = pygame.Rect(self.rect.centerx - (2 * self.rect.width * self.flip) , self.rect.y , 2 * self.rect.width , self.rect.height)
            if attacking_rect.colliderect(target.rect) :
                target.health -= 10
                target.hit = True
    
    





    def update_action(self , new_action):
        #check if the new action is diffrent to previous
        if new_action != self.action :
            self.action = new_action
            #update animation settings
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self, surface):
        img = pygame.transform.flip(self.image , self.flip , False)

        surface.blit(img,(self.rect.x - (self.offset[0] * self.image_scale), self.rect.y - (self.offset[1] * self.image_scale)))

    