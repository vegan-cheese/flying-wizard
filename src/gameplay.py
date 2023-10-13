import pygame
import random
import math


def create_obstacle(player_size: pygame.Vector2, obstacle_extra_space: int, game_window: pygame.Surface) -> list[int]:
    obstacle_1_height = random.randint(
        0, game_window.get_height() - round(player_size.y) - obstacle_extra_space)
    obstacle_2_height = game_window.get_height() - \
        round(player_size.y) - obstacle_extra_space - obstacle_1_height
    return [obstacle_1_height, obstacle_2_height, game_window.get_width(), False]


def gameplay_loop(window: pygame.Surface):
    clock = pygame.time.Clock()

    player_dimensions = pygame.Vector2(100, 100)

    # Make the player in the middle of the screen
    player_position = pygame.Vector2(
        window.get_width() / 2 - (player_dimensions.x / 2),
        window.get_height() / 2 - (player_dimensions.y / 2)
    )

    player_is_jumping = False
    player_jump_counter = 10
    player_y_velocity = 0
    player_collided = False

    player_image = pygame.transform.scale(pygame.image.load(
        "assets/images/wizard.png"), player_dimensions)

    jump_counter_start = 20
    jump_counter_end = -20

    # Spawn obstacles
    obstacle_width = 70
    obstacle_space = 150
    obstacles = []
    obstacles.append(create_obstacle(player_dimensions,
                     obstacle_space, window))

    obstacle_image = pygame.image.load("assets/images/obstacle.png")

    background_colour = pygame.Color(11, 226, 230)

    number_of_clouds = 3
    cloud_size = pygame.Vector2(210, 70)
    clouds = []
    for index in range(number_of_clouds):
        clouds.append([
            pygame.Vector2(window.get_width(), random.randint(0, window.get_height() - math.ceil(cloud_size.y))),
            random.randint(100, 500)
        ])
    cloud_image = pygame.transform.scale(pygame.image.load("assets/images/cloud.png"), cloud_size)

    score = 0
    font = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", 100)

    keep_window_open = True
    while keep_window_open:
        clock.tick(60)
        delta_time = clock.get_time() / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                keep_window_open = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_collided == False:
                    player_is_jumping = True
                    player_jump_counter = jump_counter_start

        if player_is_jumping:
            if player_jump_counter < jump_counter_end:
                # Player has finished jumping
                player_is_jumping = False
            else:
                # Player has not finished jumping
                player_y_velocity = player_jump_counter * \
                    abs(player_jump_counter)
                player_jump_counter -= 1
        else:
            # Player is not jumping, use gravity
            player_y_velocity = jump_counter_end * abs(jump_counter_end)

        player_position.y -= player_y_velocity * delta_time

        # If player is out of bounds
        if player_position.y < (0 - player_dimensions.y) or player_position.y > window.get_height():
            keep_window_open = False
            print("You lost!")

        player_rect = pygame.Rect(
            player_position.x, player_position.y, player_dimensions.x, player_dimensions.y)

        # Manage Obstacles
        delete_obstacles = []
        for index in range(len(obstacles)):
            # Move obstacle left
            if player_collided == False:
                obstacles[index][2] -= 200 * delta_time

            collided_with_obstacle_1 = player_rect.colliderect(pygame.Rect(
                obstacles[index][2], 0, obstacle_width, obstacles[index][0]))
            collided_with_obstacle_2 = player_rect.colliderect(pygame.Rect(
                obstacles[index][2], obstacles[index][0] + round(player_dimensions.y) + obstacle_space, obstacle_width, obstacles[index][1]))
            if collided_with_obstacle_1 or collided_with_obstacle_2:
                player_collided = True
                background_colour = pygame.Color(232, 137, 12)

            # If obstacle goes off screen, set it to be deleted
            if obstacles[index][2] < (0 - obstacle_width):
                # Set the obstacle to be deleted after, otherwise there will be errors with the for loop
                delete_obstacles.append(index)
            # If obstacle goes past the player, create a new obstacle and add to score
            elif obstacles[index][2] < player_position.x and obstacles[index][3] == False:
                obstacles.append(create_obstacle(
                    player_dimensions, obstacle_space, window))
                # Ensure no new obstacles are created by this obstacle's position
                obstacles[index][3] = True
                score += 1

        if len(delete_obstacles) > 0:
            for index in delete_obstacles:
                obstacles.pop(index)

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

        # Draw obstacles
        for obstacle in obstacles:
            window.blit(pygame.transform.scale(obstacle_image,
                        (obstacle_width, obstacle[0])), (obstacle[2], 0))
            window.blit(pygame.transform.scale(obstacle_image, (obstacle_width, obstacle[1])), (
                obstacle[2], obstacle[0] + round(player_dimensions.y) + obstacle_space))

        # Draw player
        window.blit(player_image, player_position)

        # Write score
        rendered_text = font.render(
            f"{score}", True, pygame.Color(255, 255, 255), None)

        window.blit(rendered_text, pygame.Vector2(20, 20))

        pygame.display.update()
