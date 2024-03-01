import pygame
import random
import utils.effects

TOL_DIST = 10
SCALE_FACT_MIN = 0.5
PAD_FACTOR = 0.2
V_DEL = 0.02
FRICTION_FACTOR = 0.2


class GameWorld2D:

    def __resize(self, width, height):
        self.game_width = width
        self.game_height = height
        self.pad_height = int(height * PAD_FACTOR)
        self.pad_rect = pygame.Rect(width - self.pad_width,
                                    (height - self.pad_height) / 2,
                                    self.pad_width, self.pad_height)
        self.ball_radius = int(self.pad_height * 0.2)
        self.ball_rect = pygame.Rect(width / 2 - self.ball_radius,
                                     height / 2 - self.ball_radius,
                                     2 * self.ball_radius,
                                     2 * self.ball_radius)

    def __init__(self, width, height):
        self.pad_width = 20
        self.__resize(width, height)
        self.ball_v_x = 9 * V_DEL * random.choice((1, -1))
        self.ball_v_y = 10 * V_DEL * random.choice((1, -1))
        self.score_hit = 0
        self.score_miss = 0
        self.level_minus_1 = 0
        self.score_font = pygame.font.SysFont("Arial", self.pad_height)
        self.score_sound = pygame.mixer.Sound("score.ogg")
        self.miss_sound = pygame.mixer.Sound("pong.ogg")
        self.ball_x = width / 2
        self.ball_y = height / 2
        self.pad_y = height / 2
        self.pad_v_y_avg = 0

    def resize(self, width, height):
        self.__resize(width, height)
        self.ball_x = width / 2
        self.ball_y = height / 2
        self.pad_y = height / 2

    def restart(self):
        self.ball_rect.x = int(0.5 * self.game_width)
        self.ball_rect.y = int(0.5 * self.game_height)
        self.ball_v_x *= random.choice((1, -1))
        self.ball_v_y *= random.choice((1, -1))
        self.ball_x = self.game_width / 2
        self.ball_y = self.game_width / 2
        self.pad_y = self.ball_y

    def score_up(self):
        self.score_hit += 1
        self.level_minus_1 += 1

        pygame.mixer.Sound.play(self.score_sound)

        # Continue in the same direction with a speed increase of 1
        self.ball_v_x += V_DEL * self.ball_v_x / abs(self.ball_v_x)
        self.ball_v_y += V_DEL * self.ball_v_y / abs(self.ball_v_y)

    def score_down(self):
        self.score_miss += 1

        pygame.mixer.Sound.play(self.miss_sound)

    def difficulty_level_to_color(self):
        # color is mapped from red to violet as the difficulty level goes
        # up. Maximum difficulty can be hard coded
        MAX_LEVEL = 50
        wavelength = 750 - (370/MAX_LEVEL) * self.level_minus_1
        return utils.effects.wavelength_to_rgb(wavelength)

    def render_elements(self, screen):
        # Paddle
        pygame.draw.rect(screen, pygame.Color('chocolate1'), self.pad_rect)

        # Color of the ball is updated corresponding to the difficulty level
        color_ball = self.difficulty_level_to_color()
        pygame.draw.ellipse(screen, pygame.Color(color_ball), self.ball_rect)

        font_hits = self.score_font.render(str(self.score_hit), True,
                                           pygame.Color('white'))
        font_misses = self.score_font.render(str(self.score_miss), True,
                                             pygame.Color('white'))

        hits_rect = font_hits.get_rect(midleft=(self.game_width / 2 + 40,
                                                self.pad_height))
        misses_rect = font_misses.get_rect(midright=(self.game_width / 2 - 40,
                                                     self.pad_height))

        screen.blit(font_hits, hits_rect)
        screen.blit(font_misses, misses_rect)

    def update(self, pad_y):
        if pad_y:
            # First we find the average velocity of the pad. Time delta will
            # be taken into account via a factor later
            self.pad_v_y_avg = pad_y - self.pad_y
            self.pad_y = pad_y
            self.pad_rect.y = pad_y
            if self.pad_rect.top <= 0:
                self.pad_rect.top = 0
                self.pad_y = self.pad_rect.y
            if self.pad_rect.bottom >= self.game_height:
                self.pad_rect.bottom = self.game_height
                self.pad_y = self.pad_rect.y

        self.ball_x += self.ball_v_x
        self.ball_y += self.ball_v_y
        self.ball_rect.x = int(self.ball_x)
        self.ball_rect.y = int(self.ball_y)

        # Bouncing off the paddle
        if self.ball_rect.colliderect(self.pad_rect) and self.ball_v_x > 0:
            self.score_up()
            # primary paddle surface
            if abs(self.ball_rect.right - self.pad_rect.left) < TOL_DIST:
                self.ball_v_x *= -1  # elastic collision, e = 1
                # Let's address the Kinetic friction due to the impulse
                # (J_x = 2 * mass * v_x).
                # Simplifying
                # Impulsive friction J_y = mu_kinetic * J_x. Combining, we get
                # Del_v_y = sign(v_pad_y - v_ball_y) * 2 * mu_kinetic * v_x
                # ball_v_y_final = ball_v_y_initial (+/-) 2 * mu_kinetic * v_x
                # (Taking static friction, and non-linear mu_kinetic)

                sign_of_friction = self.pad_v_y_avg - self.ball_v_y
                sign_of_friction /= abs(sign_of_friction)
                self.ball_v_y += (sign_of_friction * FRICTION_FACTOR
                                  * abs(self.ball_v_x))

            # top edge of the paddle
            if (abs(self.ball_rect.bottom - self.pad_rect.top) < TOL_DIST and
                    self.ball_v_y > 0):
                self.ball_v_y *= -1
                # Need to add friction

            # bottom edge of the paddle
            if (abs(self.ball_rect.top - self.pad_rect.bottom) < TOL_DIST and
                    self.ball_v_y < 0):
                self.ball_v_y *= -1
                # Need to add friction

        # Collision with top and bottom boundaries
        if (self.ball_rect.top <= 0
                or self.ball_rect.bottom >= self.game_height):
            self.ball_v_y *= -1

        # Collision with left wall
        if self.ball_rect.left <= 0:
            self.ball_v_x *= -1

        # Letting the ball past right wall
        if self.ball_rect.right >= self.game_width:
            self.score_down()
            self.restart()


class GameWorld3D(GameWorld2D):
    # Let's set up a right-handed coordinate system.
    # Top left corner as the origin, and
    # X horizontal,
    # Y Vertically down,
    # Z into the screen
    def __resize3d(self, width, depth):
        self.game_depth = depth
        self.pad_depth = int(depth * PAD_FACTOR)
        self.pad_rect_bottom_view = pygame.Rect(width - self.pad_width,
                                                (depth - self.pad_depth) / 2,
                                                self.pad_width, self.pad_depth)
        self.ball_rect_bottom_view = pygame.Rect(width / 2 - self.ball_radius,
                                                 depth / 2 - self.ball_radius,
                                                 2 * self.ball_radius,
                                                 2 * self.ball_radius)

    def __init__(self, width, height, depth):
        GameWorld2D.__init__(self, width, height)
        self.__resize3d(width, depth)
        self.ball_z = depth / 2
        self.pad_z = depth / 2
        self.pad_v_z_avg = 0
        self.ball_v_z = 9 * V_DEL * random.choice((1, -1))

    def resize(self, width, height):
        GameWorld2D.resize(self, width, height)
        # When resizing the game window, make the depth the same as the height
        self.__resize3d(width, height)
        self.ball_z = height / 2
        self.pad_z = height / 2

    def restart(self):
        GameWorld2D.restart(self)
        self.ball_rect_bottom_view.y = int(0.5 * self.game_depth)
        self.ball_v_z *= random.choice((1, -1))
        self.ball_z = self.game_depth / 2
        self.pad_z = self.ball_z

    def score_up(self):
        GameWorld2D.score_up(self)
        # Continue in the same direction with a speed increase of 1
        self.ball_v_z += V_DEL * self.ball_v_z / abs(self.ball_v_z)

    # Using a simple transformation we project the 3d point onto the 2d
    # screen. Single vanishing point projection is used where the vanishing
    # point is set at the middle of the screen in x-y plane and at infinity
    # along z direction.
    def scale_perspective(self, z):
        return 1 - (1 - SCALE_FACT_MIN) * z / self.game_depth

    def transform_to_2d(self, point3d, scale_perspective=-1):
        if scale_perspective < 0:
            scale_factor = (1 - (1 - SCALE_FACT_MIN) * point3d[2] /
                            self.game_depth)
        else:
            scale_factor = scale_perspective
        point2d_x = ((point3d[0] - self.game_width / 2) * scale_factor
                     + self.game_width / 2)
        point2d_y = ((point3d[1] - self.game_height / 2) * scale_factor
                     + self.game_height / 2)
        return [int(point2d_x), int(point2d_y)]

    def project_pad(self, screen):
        p1 = self.transform_to_2d((self.pad_rect.left, self.pad_rect.top,
                                   self.pad_rect_bottom_view.top))
        p2 = self.transform_to_2d((self.pad_rect.left, self.pad_rect.top,
                                   self.pad_rect_bottom_view.bottom))
        p3 = self.transform_to_2d((self.pad_rect.left, self.pad_rect.bottom,
                                   self.pad_rect_bottom_view.bottom))
        p4 = self.transform_to_2d((self.pad_rect.left, self.pad_rect.bottom,
                                   self.pad_rect_bottom_view.top))
        pygame.draw.polygon(screen, pygame.Color('chocolate1'), [p1, p2, p3,
                                                                 p4])

    def project_ball(self, screen, ball_color):
        ball_scale = self.scale_perspective(self.ball_rect_bottom_view.y)
        center = self.transform_to_2d((self.ball_rect.x, self.ball_rect.y),
                                      ball_scale)
        ball_radius_proj = int(ball_scale * self.ball_radius)
        ball_rect_proj = pygame.Rect(center[0] - ball_radius_proj,
                                     center[1] - ball_radius_proj,
                                     2 * ball_radius_proj,
                                     2 * ball_radius_proj)
        pygame.draw.ellipse(screen, pygame.Color(ball_color), ball_rect_proj)

    def render_cube_edges(self, screen, edge_color):
        points_front_plane = [[0, 0],
                              [self.game_width, 0],
                              [self.game_width, self.game_height],
                              [0, self.game_height]]

        points_back_plane = []
        for p_front in points_front_plane:
            p_3d = p_front + [self.game_depth]
            points_back_plane.append(self.transform_to_2d(p_3d))

        for i in range(4):
            pygame.draw.aaline(screen, edge_color, points_back_plane[i],
                               points_front_plane[i])
            pygame.draw.aaline(screen, edge_color, points_back_plane[i],
                               points_back_plane[(i + 1) % 4])

    def render_elements(self, screen):
        # Paddle
        self.project_pad(screen)
        # pygame.draw.rect(screen, pygame.Color('chocolate1'), self.pad_rect)

        # Color of the ball is updated corresponding to the difficulty level
        color_ball = self.difficulty_level_to_color()
        self.project_ball(screen, color_ball)
        # pygame.draw.ellipse(screen, pygame.Color(color_ball), self.ball_rect)

        font_hits = self.score_font.render(str(self.score_hit), True,
                                           pygame.Color('white'))
        font_misses = self.score_font.render(str(self.score_miss), True,
                                             pygame.Color('white'))

        hits_rect = font_hits.get_rect(midleft=(self.game_width / 2 + 40,
                                                self.pad_height))
        misses_rect = font_misses.get_rect(midright=(self.game_width / 2 - 40,
                                                     self.pad_height))

        screen.blit(font_hits, hits_rect)
        screen.blit(font_misses, misses_rect)

    def update(self, pad_yz):
        if pad_yz:
            # First we find the average velocity of the pad. Time delta will
            # be taken into account via a factor later

            # Update the paddle y position
            self.pad_v_y_avg = pad_yz[0] - self.pad_y
            self.pad_y = pad_yz[0]
            self.pad_rect.y = pad_yz[0]
            if self.pad_rect.top <= 0:
                self.pad_rect.top = 0
                self.pad_y = self.pad_rect.y
            if self.pad_rect.bottom >= self.game_height:
                self.pad_rect.bottom = self.game_height
                self.pad_y = self.pad_rect.y

            # Update the paddle z position
            self.pad_v_z_avg = pad_yz[1] - self.pad_z
            self.pad_z = pad_yz[1]
            self.pad_rect_bottom_view.y = pad_yz[1]
            if self.pad_rect_bottom_view.top <= 0:
                self.pad_rect_bottom_view.top = 0
                self.pad_z = self.pad_rect_bottom_view.y
            if self.pad_rect_bottom_view.bottom >= self.game_depth:
                self.pad_rect_bottom_view.bottom = self.game_depth
                self.pad_z = self.pad_rect_bottom_view.y

        self.ball_x += self.ball_v_x
        self.ball_y += self.ball_v_y
        self.ball_z += self.ball_v_z
        self.ball_rect_bottom_view.x = int(self.ball_x)
        self.ball_rect_bottom_view.y = int(self.ball_z)
        self.ball_rect.x = int(self.ball_x)
        self.ball_rect.y = int(self.ball_y)

        # Bouncing off the paddle if collision detected on both views
        if self.ball_rect.colliderect(self.pad_rect) and self.ball_v_x > 0\
                and self.ball_rect_bottom_view.colliderect(
                self.pad_rect_bottom_view):
            self.score_up()
            # primary paddle surface
            if abs(self.ball_rect.right - self.pad_rect.left) < TOL_DIST:
                self.ball_v_x *= -1

                sign_of_friction_y = self.pad_v_y_avg - self.ball_v_y
                sign_of_friction_y /= abs(sign_of_friction_y)
                self.ball_v_y += (sign_of_friction_y * FRICTION_FACTOR
                                  * abs(self.ball_v_x))

                sign_of_friction_z = self.pad_v_z_avg - self.ball_v_z
                sign_of_friction_z /= abs(sign_of_friction_z)
                self.ball_v_z += (sign_of_friction_z * FRICTION_FACTOR
                                  * abs(self.ball_v_x))

            # top edge of the paddle
            if (abs(self.ball_rect.bottom - self.pad_rect.top) < TOL_DIST and
                    self.ball_v_y > 0):
                self.ball_v_y *= -1
                # Need to add friction

            # bottom edge of the paddle
            if (abs(self.ball_rect.top - self.pad_rect.bottom) < TOL_DIST and
                    self.ball_v_y < 0):
                self.ball_v_y *= -1
                # Need to add friction

            # side edge of the paddle closer to the player
            if (abs(self.ball_rect_bottom_view.bottom
                    - self.pad_rect_bottom_view.top) < TOL_DIST and
                    self.ball_v_z > 0):
                self.ball_v_z *= -1

            # side edge of the paddle farther from the player
            if (abs(self.ball_rect_bottom_view.top -
                    self.pad_rect_bottom_view.bottom) < TOL_DIST and
                    self.ball_v_z < 0):
                self.ball_v_z *= -1

        # Collision with top and bottom boundaries
        if (self.ball_rect.top <= 0
                or self.ball_rect.bottom >= self.game_height):
            self.ball_v_y *= -1

        # Collision with closer and farther boundaries
        if (self.ball_rect_bottom_view.top <= 0
                or self.ball_rect_bottom_view.bottom >= self.game_width):
            self.ball_v_z *= -1

        # Collision with left wall
        if self.ball_rect.left <= 0:
            self.ball_v_x *= -1

        # Letting the ball past right wall
        if self.ball_rect.right >= self.game_width:
            self.score_down()
            self.restart()
