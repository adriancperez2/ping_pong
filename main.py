# -----------------------------------------
# making game pong => python
# -----------------------------------------

# import modules
import pygame

# initialize pygame
sucess, fails = pygame.init()
print(f"Sucesses: {sucess}, Fails: {fails}")
pygame.font.init()

# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
TOMOTO = (255, 99, 71)

# CLOCK
clock = pygame.time.Clock()
# create screen and define variables
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 700
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# caption
pygame.display.set_caption("Pong || yossef")


# paddle class
class paddle:
    def __init__(self, x, y, width, height):
        self.x = self.original_x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5

    def draw(self):
        pygame.draw.rect(
            SCREEN, WHITE, (self.x, self.y, self.width, self.height))

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.y > 0:
            left_paddle.y -= self.vel
        elif keys[pygame.K_s] and left_paddle.y < SCREEN_HEIGHT - left_paddle.height:
            left_paddle.y += self.vel

        if keys[pygame.K_UP] and right_paddle.y > 0:
            right_paddle.y -= self.vel
        elif keys[pygame.K_DOWN] and right_paddle.y < SCREEN_HEIGHT - right_paddle.height:
            right_paddle.y += self.vel

    def rest(self):
        self.y = (SCREEN_HEIGHT - self.height) // 2
        self.x = self.original_x


left_paddle = paddle(20, (SCREEN_HEIGHT - 130) // 2, 13, 130)
right_paddle = paddle(SCREEN_WIDTH - 20 - 13,
                      (SCREEN_HEIGHT - 130) // 2, 13, 130)

# ball class


class Ball:
    MAX_VEL = 5

    def __init__(self, x, y, radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VEL
        self.y_vel = 0

    def draw(self):
        pygame.draw.circle(SCREEN, WHITE, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1


ball = Ball(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, 10)


# for handling collisions between ball and paddles (move the ball)
def handle_collisions(ball, left_paddle, right_paddle):
    # if ball top or bottom
    if ball.y + ball.radius >= SCREEN_HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # if  ball hits left paddle
    if ball.x_vel < 0:
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                # the equation
                middle_of_paddle = left_paddle.y + left_paddle.height // 2
                differecne_in_y = middle_of_paddle - ball.y
                reduction_factor = (left_paddle.height / 2) / ball.MAX_VEL
                ball.y_vel = differecne_in_y / reduction_factor
                ball.y_vel *= -1
    else:
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                middle_y = right_paddle.y + right_paddle.height / 2
                difference_in_y = middle_y - ball.y
                reduction_factor = (right_paddle.height / 2) / ball.MAX_VEL
                y_vel = difference_in_y / reduction_factor
                ball.y_vel = -1 * y_vel


# scores for both players
left_score = 0
right_score = 0


def score():
    font = pygame.font.SysFont("comicsans", 50)
    left_text = font.render(f"Score: {left_score}", 1, WHITE)
    right_text = font.render(f"Score: {right_score}", 1, WHITE)
    SCREEN.blit(left_text, (SCREEN_WIDTH // 4 -
                left_text.get_width() + 50, 20))
    SCREEN.blit(right_text, (SCREEN_WIDTH *
                (3/4) - right_text.get_width() + 50, 20))


def draw():
    # clear screen and fill it with color
    SCREEN.fill(TOMOTO)

    left_paddle.draw()
    right_paddle.draw()
    ball.draw()
    # make a line in the middle
    for i in range(10, SCREEN_HEIGHT, SCREEN_HEIGHT // 20):
        pygame.draw.rect(SCREEN, WHITE, (SCREEN_WIDTH // 2 - 5, i, 10, 20))

    # show score
    score()
    # update
    pygame.display.flip()
    pygame.display.update()


def main():
    win_conunt = 4
    run = True
    while run:
        clock.tick(60)

        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # move paddles
        left_paddle.move()
        right_paddle.move()

        # handle collisions
        handle_collisions(ball, left_paddle, right_paddle)

        if ball.x < 0:
            global right_score
            right_score += 1
            ball.reset()
            left_paddle.rest()
            right_paddle.rest()
        elif ball.x > SCREEN_WIDTH:
            global left_score
            left_score += 1
            ball.reset()
            left_paddle.rest()
            right_paddle.rest()

        # win condition
        won = False
        if left_score >= win_conunt:
            won = True
            winner = "Left Player Won!"
        elif right_score >= win_conunt:
            won = True
            winner = "Right Player Won!"
        if won:
            font = pygame.font.SysFont("comicsans", 100)
            text = font.render(winner, 1, WHITE)
            SCREEN.blit(text, (SCREEN_WIDTH // 2 -
                        text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(3000)
            left_score = 0
            right_score = 0
            ball.reset()
            left_paddle.rest()
            right_paddle.rest()
            

        # move ball
        ball.move()
        draw()
        score()


if __name__ == "__main__":
    main()
