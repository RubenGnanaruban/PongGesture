import pygame
import utils


def main():
    pygame.init()
    clock = pygame.time.Clock()

    screen_width = int(0.8 * pygame.display.Info().current_w)
    screen_height = int(0.8 * pygame.display.Info().current_h)
    frame_rate = 120
    gw = utils.game_mechanics.GameWorld(screen_width, screen_height)

    screen = pygame.display.set_mode((screen_width, screen_height),
                                     pygame.RESIZABLE)
    pygame.display.set_caption('Pong with Hand Gestures')
    background = pygame.image.load("bg_galaxy.png")
    background_rect = background.get_rect(topleft=(0, 0))

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

        # screen.fill("black")
        screen.blit(background, background_rect)
        gw.render_elements(screen)
        # pygame.draw.rect(screen, pygame.Color('chocolate1'), gw.pad_rect)
        # pygame.draw.ellipse(screen, pygame.Color('firebrick1'), gw.ball_rect)
        pygame.display.flip()
        clock.tick(frame_rate)

    pygame.quit()


if __name__ == '__main__':
    main()
