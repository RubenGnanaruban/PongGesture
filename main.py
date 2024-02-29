import pygame
import utils
import sys

pygame.init()
screen_width = int(0.8 * pygame.display.Info().current_w)
screen_height = int(0.8 * pygame.display.Info().current_h)
frame_rate = 120
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height),
                                 pygame.RESIZABLE)
pygame.display.set_caption('Pong with Hand Gestures: Menu')
background = pygame.image.load("bg_galaxy.png")
background_rect = background.get_rect(topleft=(0, 0))


def main():
    while True:
        global screen
        screen.fill("black")
        screen.blit(background, background_rect)

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(screen_width/2, 100))
        screen.blit(menu_text, menu_rect)

        play2d_button = (
            utils.button.Button(image=None, pos=(screen_width/2, 250),
                                text_input="PLAY SOLO", font=get_font(75),
                                base_color="#d7fcd4", hovering_color="White"))
        play3d_button = (
            utils.button.Button(image=None, pos=(screen_width/2, 400),
                                text_input="PLAY IN 3D", font=get_font(75),
                                base_color="#d7fcd4", hovering_color="White"))
        quit_button = (
            utils.button.Button(image=None, pos=(screen_width/2, 550),
                                text_input="QUIT", font=get_font(75),
                                base_color="#d7fcd4", hovering_color="White"))

        for button in [play2d_button, play3d_button, quit_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.VIDEORESIZE:
                # gw.resize(event.w, event.h) # Need to address this
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play2d_button.check_for_input(menu_mouse_pos):
                    play2d()
                if play3d_button.check_for_input(menu_mouse_pos):
                    play3d()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        # pygame.display.flip()
        clock.tick(frame_rate)


def play2d():
    global screen
    gw = utils.game_mechanics.GameWorld2D(screen_width, screen_height)
    visual_in = utils.gesture_capture.HandToPaddle()

    run = True
    while run:
        gw.update(visual_in.update())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.VIDEORESIZE:
                gw.resize(event.w, event.h)
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)

        screen.fill("black")
        screen.blit(background, background_rect)
        gw.render_elements(screen)
        pygame.display.flip()
        clock.tick(frame_rate)

    main()


def play3d():
    global screen
    gw = utils.game_mechanics.GameWorld3D(screen_width, screen_height,
                                          screen_height)
    visual_in = utils.gesture_capture.HandToPaddle()

    run = True
    while run:
        gw.update(visual_in.update3d())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.VIDEORESIZE:
                gw.resize(event.w, event.h)
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)

        screen.fill("black")
        screen.blit(background, background_rect)
        gw.render_elements(screen)  # Need to uncomment
        pygame.display.flip()
        clock.tick(frame_rate)

    main()


def get_font(size):  # Returns a font in the desired size
    return pygame.font.SysFont("Arial", size)


if __name__ == '__main__':
    main()
