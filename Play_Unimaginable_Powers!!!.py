def main():
    """ Main Program """
    
    pygame.init()

    #set resolution
    WIDTH = 1100
    HEIGHT = 680

    stop = False
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    
    #set the title
    pygame.display.set_caption("One Piece-RPG")
    
    player = Player_ship(50, 50)
    
    movingsprites = pygame.sprite.Group()
    movingsprites.add(player)
    
    oceans = [Ocean1(),
              Ocean2(),
              Ocean3(),
              Ocean4(),
              Ocean5(),
              Ocean6(),
              Ocean7(),
              Ocean8(),
              Ocean9()]
    
    current_ocean_no = 0
    current_ocean = oceans[current_ocean_no]
    
    background_images = ["underwater.jpg",
                         "underwater1.jpg",
                         "underwater2.jpg",
                         "underwater3.jpg",
                         "underwater4.jpg",
                         "underwater5.jpg",
                         "underwater6.jpg",
                         "underwater7.jpg",
                         "underwater8.jpg"]
    
    clock = pygame.time.Clock()

    background_image = pygame.image.load(background_images[current_ocean_no]).convert_alpha()
    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))        
    
    finish = False
    key = False
    set_name = False
    character_name = ""
    instruction = False
    
    cover_sound = pygame.mixer.Sound('Luffy quote.wav')
    sailing_sound = pygame.mixer.Sound("pirate battle.wav")
    cover_sound.play()

    pieces_of_map = 0
    
    while finish != True:
        
        #play the sound
        sailing_sound.play()
        #show the cover untill the player press enter
        if key == False:
            key = Cover()
            
        #show option all the character        
        if key == True and set_name == False:
            character_name, set_name = Character_name()
            
        #show instructions
        if key == True and set_name == True and instruction == False:
            instruction = Instructions()
            
        #any collide would lead to next file for battle    
        if key == True and set_name == True and instruction == True:
            collide = pygame.sprite.groupcollide(movingsprites, current_ocean.enemy_sprites, False, True)
            for collision in collide:
                stop = True
                #clear events and the pirate ship stop moving
##                pygame.event.clear()
                player.change_x = 0
                player.change_y = 0
                
                battle = One_piece_charaters.main(WIDTH, HEIGHT, stop, character_name, current_ocean_no, pieces_of_map)
                
##                pygame.event.clear()
                player.change_x = 0
                player.change_y = 0
                
                stop = False
                pygame.time.wait(500)

        
        #events occur here 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finish = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                finish = True
                
            if event.type == pygame.KEYDOWN and key == True and set_name == True and instruction == True:

                if event.key == pygame.K_f:
                    #full screen
                    WIDTH = 1366
                    HEIGHT = 767
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
                    
                if event.key == pygame.K_n:
                    #now resolution
                    WIDTH = 1100
                    HEIGHT = 680
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))

                if event.key == pygame.K_i:
                    instruction = False
                    instruction = Instructions()

                #movements    
                if event.key == pygame.K_LEFT:
                    player.image = pygame.image.load(player.facing[2]).convert_alpha()
                    player.image = pygame.transform.scale(player.image,(70, 50))
                    player.changespeed(-10, 0)
                if event.key == pygame.K_RIGHT:
                    player.image = pygame.image.load(player.facing[3]).convert_alpha()
                    player.image = pygame.transform.scale(player.image,(70, 50))
                    player.changespeed(10, 0)
                if event.key == pygame.K_UP:
                    player.image = pygame.image.load(player.facing[0]).convert_alpha()
                    player.image = pygame.transform.scale(player.image,(50, 70))
                    player.changespeed(0, -10)
                if event.key == pygame.K_DOWN:
                    player.image = pygame.image.load(player.facing[1]).convert_alpha()
                    player.image = pygame.transform.scale(player.image,(50, 70))
                    player.changespeed(0, 10)
                    
            if event.type == pygame.KEYUP and key == True and instruction == True:
                if event.key == pygame.K_LEFT:                    
                    player.changespeed(10, 0)
                if event.key == pygame.K_RIGHT:                    
                    player.changespeed(-10, 0)
                if event.key == pygame.K_UP:                    
                    player.changespeed(0, 10)
                if event.key == pygame.K_DOWN:                   
                    player.changespeed(0, -10)

        #show image of the instructions, cover and option of characters            
        if set_name == False and key == True:
            image = pygame.image.load("choose character.png").convert_alpha()
            image = pygame.transform.scale(image,(WIDTH, HEIGHT))
            
        if key == False and set_name == False:            
            image = pygame.image.load("cover.jpg").convert_alpha()
            image = pygame.transform.scale(image,(WIDTH, HEIGHT))
            
            font = pygame.font.Font(None, 100)
            text_image = font.render("Press Enter", True, (0, 0, 0))
            text_rect = text_image.get_rect(centerx = WIDTH/2, centery=50)
            
        if key == True and set_name == True:
            image = pygame.image.load("instructions.png").convert_alpha()
            image = pygame.transform.scale(image,(WIDTH, HEIGHT))
            
        #the for loop below is for enemies  to toward the player ships and also not touch other enemy ships, if they do they would move apart    
        i = 0   
        for enemy in current_ocean.list_of_enemies:
            if key == True and stop == False and instruction == True:
                if enemy.rect.x > player.rect.x and pygame.sprite.collide_rect(current_ocean.list_of_enemies[i], current_ocean.list_of_enemies[i-1]) == False:
                    enemy.rect.x -= 2
                    enemy.image = pygame.image.load(enemy.ship_directions[2]).convert_alpha()
                    enemy.image = pygame.transform.scale(enemy.image,(100, 50))
                elif enemy.rect.x > player.rect.x and pygame.sprite.collide_rect(current_ocean.list_of_enemies[i], current_ocean.list_of_enemies[i-1]) == True:
                    enemy.rect.x += random.choice([2, -2, 3, -3])
                    enemy.image = pygame.image.load(enemy.ship_directions[2]).convert_alpha()
                    enemy.image = pygame.transform.scale(enemy.image,(100, 50))
                    
                if enemy.rect.x < player.rect.x and pygame.sprite.collide_rect(current_ocean.list_of_enemies[i], current_ocean.list_of_enemies[i-1]) == False:
                    enemy.rect.x += 2
                    enemy.image = pygame.image.load(enemy.ship_directions[3]).convert_alpha()
                    enemy.image = pygame.transform.scale(enemy.image,(100, 50))
                elif enemy.rect.x < player.rect.x and pygame.sprite.collide_rect(current_ocean.list_of_enemies[i], current_ocean.list_of_enemies[i-1]) == True:
                    enemy.rect.x -= random.choice([2, -2, 3, -3])
                    enemy.image = pygame.image.load(enemy.ship_directions[3]).convert_alpha()
                    enemy.image = pygame.transform.scale(enemy.image,(100, 50))
                    
                if enemy.rect.y > player.rect.y and pygame.sprite.collide_rect(current_ocean.list_of_enemies[i], current_ocean.list_of_enemies[i-1]) == False:
                    enemy.rect.y -= 2
                    enemy.image = pygame.image.load(enemy.ship_directions[0]).convert_alpha()
                    enemy.image = pygame.transform.scale(enemy.image,(30, 100))
                elif enemy.rect.y > player.rect.y and pygame.sprite.collide_rect(current_ocean.list_of_enemies[i], current_ocean.list_of_enemies[i-1]) == True:
                    enemy.rect.y += random.choice([2, -2, 3, -3])
                    enemy.image = pygame.image.load(enemy.ship_directions[0]).convert_alpha()
                    enemy.image = pygame.transform.scale(enemy.image,(30, 100))
                    
                if enemy.rect.y < player.rect.y and pygame.sprite.collide_rect(current_ocean.list_of_enemies[i], current_ocean.list_of_enemies[i-1]) == False:
                    enemy.rect.y += 2
                    enemy.image = pygame.image.load(enemy.ship_directions[1]).convert_alpha()
                    enemy.image = pygame.transform.scale(enemy.image,(30, 100))
                elif enemy.rect.y < player.rect.y and pygame.sprite.collide_rect(current_ocean.list_of_enemies[i], current_ocean.list_of_enemies[i-1]) == True:
                    enemy.rect.y -= random.choice([2, -2, 3, -3])
                    enemy.image = pygame.image.load(enemy.ship_directions[1]).convert_alpha()
                    enemy.image = pygame.transform.scale(enemy.image,(30, 100))
                    
                enemy.move(current_ocean.ocean_obstacle_list)    
                i += 1    
            
        # --- Game Logic ---
        player.move(current_ocean.ocean_obstacle_list)

        # the four if statements below are for the player to not go out the range of the world map
        # they also trigger the next room
        # if player go down or up room number will be add or minus three
        # if player go left or right room number would be add or minus one
        if player.rect.x < -10:

            oceans = [Ocean1(),
                      Ocean2(),
                      Ocean3(),
                      Ocean4(),
                      Ocean5(),
                      Ocean6(),
                      Ocean7(),
                      Ocean8(),
                      Ocean9()]
            
            if str(current_ocean_no) not in "036":
                current_ocean_no -= 1
                current_ocean = oceans[current_ocean_no]
    
                player.rect.x = (WIDTH-50)
            else:
                player.rect.x = -10
            background_image = pygame.image.load(background_images[current_ocean_no]).convert_alpha()
            background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
            
            
        if player.rect.x > (WIDTH-50):

            oceans = [Ocean1(),
                      Ocean2(),
                      Ocean3(),
                      Ocean4(),
                      Ocean5(),
                      Ocean6(),
                      Ocean7(),
                      Ocean8(),
                      Ocean9()]
            
            if str(current_ocean_no) not in "258":
                current_ocean_no += 1
                current_ocean = oceans[current_ocean_no]
                player.rect.x = -10
            else:
                player.rect.x = (WIDTH-50)
            background_image = pygame.image.load(background_images[current_ocean_no]).convert_alpha()
            background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
            
        if player.rect.y < -25:

            oceans = [Ocean1(),
                      Ocean2(),
                      Ocean3(),
                      Ocean4(),
                      Ocean5(),
                      Ocean6(),
                      Ocean7(),
                      Ocean8(),
                      Ocean9()]
            
            if str(current_ocean_no) not in "012":
                current_ocean_no -= 3
                current_ocean = oceans[current_ocean_no]
                player.rect.y = (HEIGHT-50)
            else:
                player.rect.y = -25
            background_image = pygame.image.load(background_images[current_ocean_no]).convert_alpha()
            background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
            
            
        if player.rect.y > (HEIGHT-50):
            oceans = [Ocean1(),
                      Ocean2(),
                      Ocean3(),
                      Ocean4(),
                      Ocean5(),
                      Ocean6(),
                      Ocean7(),
                      Ocean8(),
                      Ocean9()]
            
            if str(current_ocean_no) not in "678":
                current_ocean_no += 3
                current_ocean = oceans[current_ocean_no]
                
                player.rect.y = -25
            else:
                player.rect.y = (HEIGHT-50)
            
            background_image = pygame.image.load(background_images[current_ocean_no]).convert_alpha()
            background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
            
        if key == True and set_name == True and instruction == True:
            screen.blit(background_image, [0,0])

            current_ocean.ocean_obstacle_list.draw(screen)
            current_ocean.enemy_sprites.draw(screen)
            movingsprites.draw(screen)
        elif key == False:
            screen.blit(image, [0,0])
            screen.blit(text_image, text_rect)
        elif key == True and set_name == False:
            screen.blit(image, [0,0])
        elif key == True and set_name == True and instruction == False:
            screen.blit(image, [0,0])
        
        pygame.display.flip()

        clock.tick(80)
                       
    pygame.quit()

if __name__ == "__main__":
    main()


def main(WIDTH, HEIGHT, stop, character_name, current_ocean_no, pieces_of_map):
    """main loop"""
    pygame.init() 

    #remain the resolution as the previous file has
    if WIDTH == 1366 and HEIGHT == 767:
        screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((WIDTH, HEIGHT))

    #set the title
    pygame.display.set_caption("One Piece-RPG")

    player = Player(100, 100, character_name)
    if character_name == "Luffy":
        player_status = Luffy(100, 100, character_name)
    elif character_name == "Zoro":
        player_status = Zoro(100, 100, character_name)
    elif character_name == "Sanji":
        player_status = Sanji(100, 100, character_name)
    else:
        player_status = Luffy(100, 100, character_name)
    
    character = pygame.sprite.Group()
    character.add(player)
    
    clock = pygame.time.Clock()

    #munch_sound = pygame.mixer.Sound('crunch.wav')

    background_image = pygame.image.load("battle.jpg").convert_alpha()
    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))        
    
    finish = False

    enemy_minions = pygame.sprite.Group()
    small_bosses = pygame.sprite.Group()
    big_boss = pygame.sprite.Group()

    #store list of multiple minions and small boss onjects
    list_of_minions = []
    list_of_small_bosses = []

    #generate multiple minions
    for minions in range(random.randrange(3, 5)):
        y = random.randint(minions*40,500)
        minion = Enemy_minions(800,y)
        list_of_minions.append(minion)
        enemy_minions.add(minion)
    #gnerate ultiple small boss
    if current_ocean_no != 4:
        for small_boss in range(random.randrange(1, 2)):
            y = random.randint(small_boss*20,500)
            boss = Small_boss(850,y)
            list_of_minions.append(boss)
            small_bosses.add(boss)
    #big boss only show on the center of the map
    if current_ocean_no == 4 and pieces_of_map >= 8:
        big = Big_boss(880, 200)
        big_boss.add(big)
        
    shut_down = False
    
    pygame.event.clear()
    player.change_x = 0
    player.change_y = 0

    instruction = True
    sailing_sound = pygame.mixer.Sound("pirate battle.wav")
    win = False
    
    while finish != True:
        if instruction == False:
            instruction = Instructions()
            
        sailing_sound.play()
        dead = False
        count_deaths = 0
        for m in list_of_minions:
            if list_of_minions[count_deaths].health <= 0:
                count_deaths += 1

        count_dead_boss = 0
        for s in list_of_small_bosses:
            if list_of_small_bosses[count_dead_boss].health <= 0:
                count_dead_boss += 1
                
        if current_ocean_no != 4:
            if count_dead_boss == len(list_of_small_bosses) and count_deaths == len(list_of_minions):
                finish = True
                shut_down = True
                
                
        elif current_ocean_no == 4:
            if big.health <= 0 and count_deaths == len(list_of_minions):
                background_image = pygame.image.load("winning.jpg").convert_alpha()
                background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
                win = True
                enemy_minions.empty()
                small_bosses.empty()
                big_boss.empty()
                character.empty()
            
        #events occur here 
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                finish = True
                shut_down = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                finish = True
                shut_down = True
     
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_i:
                    instruction = False
                    instruction = Instructions()
                
                if event.key == pygame.K_f:
                    WIDTH = 1366
                    HEIGHT = 767
                    screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
                    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
                    
                if event.key == pygame.K_n:
                    WIDTH = 1100
                    HEIGHT = 680
                    screen = pygame.display.set_mode((WIDTH, HEIGHT))
                    background_image = pygame.transform.scale(background_image,(WIDTH, HEIGHT))
                    
                    
                if event.key == pygame.K_LEFT and instruction == True:
                    player.image = pygame.image.load(player.images[0]).convert_alpha()
                    if character_name == "Luffy":
                        player.image = pygame.transform.scale(player.image,(33, 43))
                    if character_name == "Zoro":
                        player.image = pygame.transform.scale(player.image,(31, 57))
                    if character_name == "Sanji":
                        player.image = pygame.transform.scale(player.image,(20, 48))
                    player.changespeed(-5, 0)
                    
                if event.key == pygame.K_RIGHT  and instruction == True:
                    player.image = pygame.image.load(player.images[0]).convert_alpha()
                    if character_name == "Luffy":
                        player.image = pygame.transform.scale(player.image,(33, 43))
                    if character_name == "Zoro":
                        player.image = pygame.transform.scale(player.image,(31, 57))
                    if character_name == "Sanji":
                        player.image = pygame.transform.scale(player.image,(20, 48))
                    player.image = pygame.transform.flip(player.image, 180, 0)
                    player.changespeed(5, 0)
                if event.key == pygame.K_UP  and instruction == True:
                    player.image = pygame.image.load(player.images[0]).convert_alpha()
                    if character_name == "Luffy":
                        player.image = pygame.transform.scale(player.image,(33, 43))
                    if character_name == "Zoro":
                        player.image = pygame.transform.scale(player.image,(31, 57))
                    if character_name == "Sanji":
                        player.image = pygame.transform.scale(player.image,(20, 48))
                    player.changespeed(0, -5)
                if event.key == pygame.K_DOWN  and instruction == True:
                    player.image = pygame.image.load(player.images[0]).convert_alpha()
                    if character_name == "Luffy":
                        player.image = pygame.transform.scale(player.image,(33, 43))
                    if character_name == "Zoro":
                        player.image = pygame.transform.scale(player.image,(31, 57))
                    if character_name == "Sanji":
                        player.image = pygame.transform.scale(player.image,(20, 48))
                    player.changespeed(0, 5)
                    
            if event.type == pygame.KEYUP and instruction == True:
                
                if event.key == pygame.K_LEFT:                    
                    player.changespeed(5, 0)
                if event.key == pygame.K_RIGHT:                    
                    player.changespeed(-5, 0)
                if event.key == pygame.K_UP:                    
                    player.changespeed(0, 5)
                if event.key == pygame.K_DOWN:                   
                    player.changespeed(0, -5)
                    
        player.move()

        if instruction == False:
            image = pygame.image.load("instructions.png").convert_alpha()
            image = pygame.transform.scale(image,(WIDTH, HEIGHT))
            

        # --- Game Logic ---
        
        if player.rect.x <= 0:
            player.rect.x = 0
                        
        if player.rect.x >= (WIDTH-30):
            player.rect.x = (WIDTH-30)
            
            
        if player.rect.y <= 0:
            player.rect.y = 0
            
            
        if player.rect.y >= (HEIGHT-40):
            player.rect.y = (HEIGHT-40)
            
        if instruction == False:
            screen.blit(image, [0,0])
        else:
            screen.blit(background_image, [0,0])
            character.draw(screen)
            enemy_minions.draw(screen)
            small_bosses.draw(screen)
            big_boss.draw(screen)
            
        pygame.display.flip()

        clock.tick(80)

##    if shut_down == True:     
##        pygame.quit()

if __name__ == "__main__":
    current_ocean_no = 0
    WIDTH = 1000
    HEIGHT = 600
    stop = True
    name = "Luffy"
    pieces_of_map = 8
    main(WIDTH, HEIGHT, stop, name, current_ocean_no, pieces_of_map)
    

