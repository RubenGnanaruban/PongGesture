import pygame
import random


class GameWorld:

    def __resize(self, width, height):
        self.game_width = width
        self.game_height = height
        self.pad_height = int(height * 0.15)
        self.pad_rect = pygame.Rect(self.game_width - self.pad_width,
                                    (self.game_height - self.pad_height) / 2,
                                    self.pad_width, self.pad_height)
        self.ball_radius = int(self.pad_height * 0.12)
        self.ball_rect = pygame.Rect(self.game_width / 2 - self.ball_radius,
                                     self.game_height / 2 -
                                     self.ball_radius, 2 * self.ball_radius,
                                     2 * self.ball_radius)

    def __init__(self, width, height):
        self.pad_width = 20
        self.__resize(width, height)
        self.ball_v_x = 8 * random.choice((1, -1))
        self.ball_v_y = 6 * random.choice((1, -1))
        self.score_hit = 0
        self.score_miss = 0
        self.level = 1
        self.score_font = pygame.font.SysFont("Arial", self.pad_height)

    def resize(self, width, height):
        self.__resize(width, height)

    def restart(self):
        self.ball_rect.x = int(0.5 * self.game_width)
        self.ball_rect.y = int(0.5 * self.game_height)
        self.ball_v_x *= random.choice((1, -1))
        self.ball_v_y *= random.choice((1, -1))

    def score_up(self):
        self.score_hit += 1
        self.level += 1
        # Continue in the same direction with a speed increase of 1
        self.ball_v_x += self.ball_v_x/abs(self.ball_v_x)
        self.ball_v_y += self.ball_v_y / abs(self.ball_v_y)

    def score_down(self):
        self.score_miss += 1

    def render_elements(self, screen):
        pygame.draw.rect(screen, pygame.Color('chocolate1'), self.pad_rect)
        pygame.draw.ellipse(screen, pygame.Color('firebrick1'), self.ball_rect)

        font_hits = self.score_font.render(str(self.score_hit), True,
                                           pygame.Color('white'))
        font_misses = self.score_font.render(str(self.score_miss), True,
                                             pygame.Color('white'))
        font_level = self.score_font.render(str(self.level), True,
                                            pygame.Color('white'))

        hits_rect = font_hits.get_rect(midleft=(self.game_width / 2 + 40,
                                                self.pad_height))
        misses_rect = font_misses.get_rect(midright=(self.game_width / 2 - 40,
                                                     self.pad_height))
        level_rect = font_level.get_rect(midleft=(40, self.pad_height))

        screen.blit(font_hits, hits_rect)
        screen.blit(font_misses, misses_rect)
        screen.blit(font_level, level_rect)

    def update(self, pad_y):
        if pad_y:
            self.pad_rect.y = pad_y
            # self.x = position(0)
            # self.y = position(1)
            if self.pad_rect.top <= 0:
                self.pad_rect.top = 0
            if self.pad_rect.bottom >= self.game_height:
                self.pad_rect.bottom = self.game_height

        self.ball_rect.x += self.ball_v_x
        self.ball_rect.y += self.ball_v_y

        # Bouncing off the paddle
        if self.ball_rect.colliderect(self.pad_rect) and self.ball_v_x > 0:
            self.score_up()
            if abs(self.ball_rect.right - self.pad_rect.left) < 10:
                self.ball_v_x *= -1
            elif (abs(self.ball_rect.bottom - self.pad_rect.top) < 10 and
                  self.ball_v_y > 0):
                self.ball_v_y *= -1
            elif (abs(self.ball_rect.top - self.pad_rect.bottom) < 10 and
                  self.ball_v_y < 0):
                self.ball_v_y *= -1

        # Collision with top and bottom boundaries
        if (self.ball_rect.top <= 0
                or self.ball_rect.bottom >= self.game_height):
            self.ball_v_y *= -1

        # Collision with left wall
        if self.ball_rect.left <= 0:
            self.ball_v_x *= -1

        # Letting the ball past left wall
        if self.ball_rect.right >= self.game_width:
            self.score_down()
            self.restart()
