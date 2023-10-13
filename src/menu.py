import pygame
import math
import random

def start_menu(window: pygame.Surface) -> bool:
    allow_next_scene_start = True

    clock = pygame.time.Clock()

    play_button_area = pygame.Vector2(200, 100)
    play_button_rect = pygame.Rect(
        (window.get_width() / 2) - (play_button_area.x / 2),
        ((window.get_height() / 3) * 2) - 100,
        play_button_area.x,
        play_button_area.y
    )

    quit_button_area = pygame.Vector2(200, 100)
    quit_button_rect = pygame.Rect(
        (window.get_width() / 2) - (quit_button_area.x / 2),
        ((window.get_height() / 3) * 2) + 20,
        quit_button_area.x,
        quit_button_area.y
    )

    background_colour = pygame.Color(11, 226, 230)

    title_font = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", math.floor(play_button_area.y) - 20)
    rendered_title_text = title_font.render("Flying Wizard", True, pygame.Color(255, 255, 255))
    title_text_position = pygame.Vector2((window.get_width() / 2) - (rendered_title_text.get_width() / 2), 100)

    play_button_font = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", math.floor(play_button_area.y) - 20)
    rendered_play_button_text = play_button_font.render("Play", True, pygame.Color(255, 255, 255))
    play_button_text_position = pygame.Vector2(play_button_rect.left + ((play_button_area.x - rendered_play_button_text.get_width()) / 2), play_button_rect.top)

    quit_button_font = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", math.floor(quit_button_area.y) - 20)
    rendered_quit_button_text = quit_button_font.render("Quit", True, pygame.Color(255, 255, 255))
    quit_button_text_position = pygame.Vector2(quit_button_rect.left + ((quit_button_area.x - rendered_quit_button_text.get_width()) / 2), quit_button_rect.top)

    number_of_clouds = 3
    cloud_size = pygame.Vector2(210, 70)
    clouds = []
    for index in range(number_of_clouds):
        clouds.append([
            pygame.Vector2(window.get_width(), random.randint(0, window.get_height() - math.ceil(cloud_size.y))),
            random.randint(100, 500)
        ])
    cloud_image = pygame.transform.scale(pygame.image.load("assets/images/cloud.png"), cloud_size)


    keep_window_open = True
    while keep_window_open:
        clock.tick()
        delta_time = clock.get_time() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_window_open = False
                allow_next_scene_start = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # Mouse button 1 (left click) pressed
                    if play_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        # Play button was clicked
                        keep_window_open = False
                        # Game will load into next scene if allow_next_scene_start == True
                    if quit_button_rect.collidepoint(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                        # Quit button was clicked
                        # End game
                        keep_window_open = False
                        allow_next_scene_start = False


        window.fill(background_colour)

        for index in range(number_of_clouds):
            # Move cloud right
            clouds[index][0].x -= clouds[index][1] * delta_time

            # If cloud is out of bounds, reset position and change height and speed
            if clouds[index][0].x < 0 - cloud_size.x:
                clouds[index][0].x = window.get_width()
                clouds[index][0].y = random.randint(0, window.get_height() - math.ceil(cloud_size.y))
                clouds[index][1] = random.randint(100, 500)

            # Draw cloud
            window.blit(cloud_image, clouds[index][0])

        # Title
        window.blit(rendered_title_text, title_text_position)

        # Draw play button
        pygame.draw.rect(window, pygame.Color(0, 0, 0), play_button_rect)
        # Play button text
        window.blit(rendered_play_button_text, play_button_text_position)

        # Draw quit button
        pygame.draw.rect(window, pygame.Color(0, 0, 0), quit_button_rect)
        # Quit button text
        window.blit(rendered_quit_button_text, quit_button_text_position)

        pygame.display.update()

    return allow_next_scene_start