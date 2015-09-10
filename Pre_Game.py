import Pygame


def Instructions():
    """another instruction function for the player to view the instructions even during the battle"""
    instruction = False
    try:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                instruction = True
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pygame.quit()  
            else:
                raise ValueError
        
    except ValueError:
        Instructions()
        
    return instruction

