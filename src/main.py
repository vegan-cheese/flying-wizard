import pygame
import gameplay
import menu

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600


def create_window(window_size):
    window = pygame.display.set_mode(window_size)
    pygame.display.set_caption("Flying Wizard")
    return window

def main():
    pygame.init()

    window = create_window((WINDOW_WIDTH, WINDOW_HEIGHT))

    play_game = menu.start_menu(window)

    if play_game:
        gameplay.gameplay_loop(window)


if __name__ == "__main__":
    main()
else:
    print("main.py is not being run as a main file!")
