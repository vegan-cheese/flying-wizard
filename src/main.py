import pygame
import random

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def create_window(window_size):
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Flying Wizard")
    return window


def create_obstacle(player_size: pygame.Vector2, obstacle_extra_space: int) -> list[int]:
    obstacle_1_height = random.randint(
        0, WINDOW_HEIGHT - round(player_size.y) - obstacle_extra_space)
    obstacle_2_height = WINDOW_HEIGHT - \
        round(player_size.y) - obstacle_extra_space - obstacle_1_height
    return [obstacle_1_height, obstacle_2_height, WINDOW_WIDTH, False]


def main():
    pygame.init()

    window = create_window((800, 600))

    clock = pygame.time.Clock()

    player_dimensions = pygame.Vector2(100, 100)

    # Make the player in the middle of the screen
    player_position = pygame.Vector2(
        WINDOW_WIDTH / 2 - (player_dimensions.x / 2),
        WINDOW_HEIGHT / 2 - (player_dimensions.y / 2)
    )

    player_is_jumping = False
    player_jump_counter = 10
    player_y_velocity = 0
    player_collided = False

    jump_counter_start = 20
    jump_counter_end = -20

    # Spawn obstacles
    obstacle_width = 70
    obstacle_space = 150
    obstacles = []
    obstacles.append(create_obstacle(player_dimensions, obstacle_space))

    background_colour = pygame.Color(0, 0, 0)

    score = 0

    keep_window_open = True
    while keep_window_open == True:
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
        if player_position.y < (0 - player_dimensions.y) or player_position.y > WINDOW_HEIGHT:
            keep_window_open = False
            print("You lost!")

        player_rect = pygame.Rect(
            player_position.x, player_position.y, player_dimensions.x, player_dimensions.y)

        # Manage Obstacles
        delete_obstacles = []
        for index in range(0, len(obstacles)):
            # Move obstacle left
            if player_collided == False:
                obstacles[index][2] -= 200 * delta_time

            collided_with_obstacle_1 = player_rect.colliderect(pygame.Rect(obstacles[index][2], 0, obstacle_width, obstacles[index][0]))
            collided_with_obstacle_2 = player_rect.colliderect(pygame.Rect(obstacles[index][2], obstacles[index][0] + round(player_dimensions.y) + obstacle_space, obstacle_width, obstacles[index][1]))
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
                    player_dimensions, obstacle_space))
                # Ensure no new obstacles are created by this obstacle's position
                obstacles[index][3] = True
                score += 1

        if len(delete_obstacles) > 0:
            for index in delete_obstacles:
                obstacles.pop(index)

        window.fill(background_colour)

        # Draw obstacles
        for obstacle in obstacles:
            pygame.draw.rect(window, pygame.Color(0, 0, 255),
                             pygame.Rect(obstacle[2], 0, obstacle_width, obstacle[0]))
            pygame.draw.rect(window, pygame.Color(0, 255, 0), pygame.Rect(
                obstacle[2], obstacle[0] + round(player_dimensions.y) + obstacle_space, obstacle_width, obstacle[1]))

        # Draw player
        pygame.draw.rect(window, pygame.Color(255, 0, 0), pygame.Rect(
            player_position.x, player_position.y, player_dimensions.x, player_dimensions.y)
        )

        # Write score
        font = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", 100)
        rendered_text = font.render(f"{score}", True, pygame.Color(255, 255, 255), None)

        window.blit(rendered_text, pygame.Vector2(20, 20))

        pygame.display.update()


if __name__ == "__main__":
    main()
else:
    print("main.py is not being run as a main file!")
