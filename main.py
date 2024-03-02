import pygame
import utils
import sys
import pyautogui

pygame.init()
screen_width = int(0.8 * pygame.display.Info().current_w)
screen_height = int(0.8 * pygame.display.Info().current_h)
refresh_rate = 30
interpolation_steps = 50
frame_rate = interpolation_steps * refresh_rate
clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height),
                                 pygame.RESIZABLE)
background = pygame.image.load("bg_galaxy.png")
background_rect = background.get_rect(topleft=(0, 0))


def main():
    pygame.display.set_caption('Pong with Hand Gestures: Menu')
    visual_in = utils.gesture_capture.HandToPaddle()
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
        # settings_button = (
        #     utils.button.Button(image=None, pos=(4 * screen_width / 5,
        #                                          3 * screen_height / 5),
        #                         text_input="SETTINGS", font=get_font(75),
        #                         base_color="#d7fcd4", hovering_color="White"))
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
                       play3d_button, quit_button]:
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
                if play2d_head2head_button.check_for_input(menu_mouse_pos):
                    play2d_2player()
                if play3d_button.check_for_input(menu_mouse_pos):
                    play3d_solo()
                if quit_button.check_for_input(menu_mouse_pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(refresh_rate)


def play2d_solo():
    pygame.display.set_caption('Pong with Hand Gestures: Hand Solo')
    visual_in = utils.gesture_capture.HandToPaddle()
    global screen
    gw = utils.game_mechanics.GameWorld2D(screen_width, screen_height)

    # Screen and camera are limited by their frame rates. But running the
    # whole model at that slow rate would make the delta displacements too
    # much to account for collisions (at higher speeds).
    # Therefore, we decouple updating the elements and renderings.
    # flag_dont_render is used to skip rendering for all but onc in every 50
    # interpolation_steps

    flag_dont_render = 1
    pad_updated = visual_in.update2d()

    run = True
    while run:
        if not (flag_dont_render % interpolation_steps):
            pad_updated = visual_in.update2d()

        gw.update(pad_updated)

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

        if not (flag_dont_render % interpolation_steps):
            # screen.fill("black")
            screen.blit(background, background_rect)
            gw.render_elements(screen)
            pygame.display.flip()

        flag_dont_render = (flag_dont_render + 1) % interpolation_steps
        clock.tick(frame_rate)

    main()


def play2d_2player():
    pygame.display.set_caption('Pong with Hand Gestures: Two\'s Complement')
    global screen
    visual_in = utils.gesture_capture.Hands2ToPaddles()
    gw = utils.game_mechanics.GameWorld2D2Players(screen_width, screen_height)

    # player1's hand on the right side of the screen, and
    # player2's hand on the left side of the screen

    flag_dont_render = 1
    pad1_updated, pad2_updated = visual_in.update2d()

    run = True
    while run:
        if not (flag_dont_render % interpolation_steps):
            pad1_updated, pad2_updated = visual_in.update2d()

        gw.update_2player(pad1_updated, pad2_updated)

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

        if not (flag_dont_render % interpolation_steps):
            # screen.fill("black")
            screen.blit(background, background_rect)
            gw.render_elements(screen)
            pygame.display.flip()

        flag_dont_render = (flag_dont_render + 1) % interpolation_steps
        clock.tick(frame_rate)

    main()


def play3d_solo():
    pygame.display.set_caption('Pong with Hand Gestures: in a 3D Galaxy Far '
                               'Far Away')
    visual_in = utils.gesture_capture.HandToPaddle()
    global screen
    gw = utils.game_mechanics.GameWorld3D(screen_width, screen_height,
                                          screen_height)
    flag_dont_render = 1
    pad_updated = visual_in.update3d()

    run = True
    while run:
        if not (flag_dont_render % interpolation_steps):
            pad_updated = visual_in.update3d()

        gw.update(pad_updated)

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

        if not (flag_dont_render % interpolation_steps):
            # screen.fill("black")
            screen.blit(background, background_rect)
            gw.render_cube_edges(screen, "White")
            gw.render_elements(screen)  # Need to uncomment
            pygame.display.flip()

        flag_dont_render = (flag_dont_render + 1) % interpolation_steps
        clock.tick(frame_rate)

    main()


def get_font(size):  # Returns a font in the desired size
    return pygame.font.SysFont("Arial", size)


if __name__ == '__main__':
    main()
