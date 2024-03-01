import pygame
import utils
import sys
import pyautogui

pygame.init()
# screen_width = pygame.display.Info().current_w
# screen_height = pygame.display.Info().current_h
screen_width = int(0.8 * pygame.display.Info().current_w)
screen_height = int(0.8 * pygame.display.Info().current_h)
refresh_rate = 30
frame_rate = 20 * refresh_rate
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height),
                                 pygame.RESIZABLE)
# pygame.display.set_caption('Pong with Hand Gestures: Menu')
background = pygame.image.load("bg_galaxy.png")
background_rect = background.get_rect(topleft=(0, 0))
visual_in = utils.gesture_capture.HandToPaddle()


def main():
    pygame.display.set_caption('Pong with Hand Gestures: Menu')
    while True:
        global screen
        screen.fill("black")
        screen.blit(background, background_rect)

        menu_mouse_pos = pygame.mouse.get_pos()

        menu_text = get_font(100).render("MAIN MENU", True, "#b68f40")
        menu_rect = menu_text.get_rect(center=(screen_width / 2,
                                               screen_height / 5))
        screen.blit(menu_text, menu_rect)

        play2d_button = (
            utils.button.Button(image=None, pos=(screen_width / 5,
                                                 2 * screen_height / 5),
                                text_input="PLAY SOLO", font=get_font(75),
                                base_color="#d7fcd4", hovering_color="White"))
        play2d_head2head_button = (
            utils.button.Button(image=None, pos=(4 * screen_width / 5,
                                                 2 * screen_height / 5),
                                text_input="PLAY 2 PLAYERS", font=get_font(75),
                                base_color="#d7fcd4", hovering_color="White"))
        play3d_button = (
            utils.button.Button(image=None, pos=(screen_width / 5,
                                                 3 * screen_height / 5),
                                text_input="PLAY IN 3D", font=get_font(75),
                                base_color="#d7fcd4", hovering_color="White"))
        settings3d_button = (
            utils.button.Button(image=None, pos=(4 * screen_width / 5,
                                                 3 * screen_height / 5),
                                text_input="3D SETTING", font=get_font(75),
                                base_color="#d7fcd4", hovering_color="White"))
        quit_button = (
            utils.button.Button(image=None, pos=(screen_width/2,
                                                 4 * screen_height / 5),
                                text_input="QUIT", font=get_font(75),
                                base_color="#d7fcd4", hovering_color="White"))

        finger_tip_mouse = visual_in.get_camera_to_mouse(screen_width,
                                                         screen_height)
        if finger_tip_mouse:
            pyautogui.moveTo(finger_tip_mouse)

        for button in [play2d_button, play2d_head2head_button,
                       play3d_button, settings3d_button, quit_button]:
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
                    play2d_solo()
                if play3d_button.check_for_input(menu_mouse_pos):
                    play3d_solo()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        # pygame.display.flip()
        clock.tick(frame_rate)


def play2d_solo():
    pygame.display.set_caption('Pong with Hand Gestures: Hand Solo')
    global screen
    gw = utils.game_mechanics.GameWorld2D(screen_width, screen_height)
    # visual_in = utils.gesture_capture.HandToPaddle()

    run = True
    while run:
        gw.update(visual_in.update())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False

            if event.type == pygame.VIDEORESIZE:
                gw.resize(event.w, event.h)
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)

        # screen.fill("black")
        screen.blit(background, background_rect)
        gw.render_elements(screen)
        pygame.display.flip()
        clock.tick(frame_rate)

    main()


def play3d_solo():
    pygame.display.set_caption('Pong with Hand Gestures: 3D Galaxy Far Far '
                               'Away')
    global screen
    gw = utils.game_mechanics.GameWorld3D(screen_width, screen_height,
                                          screen_height)
    # visual_in = utils.gesture_capture.HandToPaddle()

    run = True
    while run:
        gw.update(visual_in.update3d())

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False

            if event.type == pygame.VIDEORESIZE:
                gw.resize(event.w, event.h)
                screen = pygame.display.set_mode((event.w, event.h),
                                                 pygame.RESIZABLE)

        # screen.fill("black")
        screen.blit(background, background_rect)
        gw.render_cube_edges(screen, "White")
        gw.render_elements(screen)  # Need to uncomment
        pygame.display.flip()
        clock.tick(frame_rate)

    main()


def get_font(size):  # Returns a font in the desired size
    return pygame.font.SysFont("Arial", size)


if __name__ == '__main__':
    main()
