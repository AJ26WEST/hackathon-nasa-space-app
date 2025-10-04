import cv2
import pygame
import sys

pygame.init()
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("NASA Agriculture Game")

start_bg = pygame.transform.scale(pygame.image.load("start_screen.jpg"), (WIDTH, HEIGHT))
reg_bg = pygame.transform.scale(pygame.image.load("reg.jpg"), (WIDTH, HEIGHT))

font = pygame.font.SysFont("Arial", 32)
input_font = pygame.font.SysFont("Arial", 36)

STATE_START = "start"
STATE_REG = "registration"
STATE_VIDEO = "video"
STATE_MAIN = "main_game"
game_state = STATE_START

start_button = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 50, 240, 100)
input_box = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 - 45, 200, 40)

player_name = ""
active_input = False

video_path = "Black Hole.mp4"  # Your video file path
video_played = False
clock = pygame.time.Clock()

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
                    game_state = STATE_REG

        elif game_state == STATE_REG:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_box.collidepoint(event.pos):
                    active_input = True
                else:
                    active_input = False
            if event.type == pygame.KEYDOWN and active_input:
                if event.key == pygame.K_RETURN:
                    game_state = STATE_VIDEO
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

    elif game_state == STATE_VIDEO:
        if not video_played:
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                print("Error: Could not open video.")
                game_state = STATE_MAIN
            else:
                while cap.isOpened():
                    ret, frame = cap.read()
                    if not ret:
                        # Loop the video by resetting to first frame
                        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                        continue

                    frame = cv2.resize(frame, (WIDTH, HEIGHT))
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    frame_surface = pygame.surfarray.make_surface(frame.swapaxes(0, 1))
                    screen.blit(frame_surface, (0, 0))

                    # Overlay welcome message
                    welcome_text = font.render(f"Welcome {player_name} 🌱", True, (255, 255, 255))
                    rect_bg = pygame.Surface((welcome_text.get_width() + 20, welcome_text.get_height() + 10))
                    rect_bg.set_alpha(150)
                    rect_bg.fill((0, 0, 0))
                    screen.blit(rect_bg, (20, 20))
                    screen.blit(welcome_text, (30, 25))

                    pygame.display.update()

                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            cap.release()
                            pygame.quit()
                            sys.exit()

                    clock.tick(30)

                cap.release()
                video_played = True
                game_state = STATE_MAIN
        else:
            game_state = STATE_MAIN

    elif game_state == STATE_MAIN:
        screen.fill((20, 20, 50))
        msg = font.render(f"Welcome {player_name}! 🌱", True, (255, 255, 255))
        screen.blit(msg, (100, HEIGHT // 2))

    if game_state != STATE_VIDEO:
        pygame.display.flip()
        clock.tick(60)
