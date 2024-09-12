import pygame

def show_game_over(screen, font):
    screen.fill((0, 0, 0))
    game_over_text = font.render("游戏结束", True, (255, 0, 0))
    screen.blit(game_over_text, (75, 250))
    pygame.display.flip()
    pygame.time.wait(3000)
