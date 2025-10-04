import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
start_bg = pygame.transform.scale(pygame.image.load("start_screen.jpg"), (WIDTH, HEIGHT))
reg_bg = pygame.transform.scale(pygame.image.load("reg.jpg"), (WIDTH, HEIGHT))

pygame.display.set_caption("NASA Agriculture Game")

font = pygame.font.SysFont("Arial", 32)
input_font = pygame.font.SysFont("Arial", 36)

STATE_START = "start"
STATE_REG = "registration"
STATE_MAIN = "main_game"
game_state = STATE_START

start_button = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 50, 240, 100)

input_box = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 45, 200, 40)
player_name = ""
active_input = False

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_state == STATE_START:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                if start_button.collidepoint(mx, my):
                    print("🚀 Moving to Registration")
                    game_state = STATE_REG

        elif game_state == STATE_REG:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active_input = True
                else:
                    active_input = False

            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    print(f"✅ Player Name: {player_name}")
                    game_state = STATE_MAIN
                elif event.key == pygame.K_BACKSPACE:
                    player_name = player_name[:-1]
                else:
                    player_name += event.unicode

    if game_state == STATE_START:
        screen.blit(start_bg, (0, 0))

    elif game_state == STATE_REG:
        screen.blit(reg_bg, (0, 0))
        pygame.draw.rect(screen, (255, 255, 255), input_box, 0)
        name_surface = input_font.render(player_name, True, (0, 0, 0))
        screen.blit(name_surface, (input_box.x + 10, input_box.y + 10))

    elif game_state == STATE_MAIN:
        screen.fill((20, 20, 50))
        msg = font.render(f"Welcome {player_name}! 🌱", True, (255, 255, 255))
        screen.blit(msg, (100, HEIGHT//2))

    pygame.display.flip()
