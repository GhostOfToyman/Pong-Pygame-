import pygame
import sys

# Classes


class Ball:
    def __init__(self, win, color, posX, posY, radius):
        self.win = win
        self.color = color
        self.posX = posX
        self.posY = posY
        self.radius = radius
        self.dx = 0
        self.dy = 0
        self.show()

    def show(self):
        pygame.draw.circle(self.win, self.color,
                           (self.posX, self.posY), self.radius)

    def start_moving(self):
        self.dx = 15
        self.dy = 5

    def move(self):
        self.posX += self.dx
        self.posY += self.dy

    def paddle_collision(self):
        self.dx = -self.dx

    def wall_collision(self):
        self.dy = -self.dy


class Paddle:
    def __init__(self, win, color, posX, posY, width, height):
        self.win = win
        self.color = color
        self.posX = posX
        self.posY = posY
        self.width = width
        self.height = height
        self.state = 'stopped'
        self.show()

    def show(self):
        pygame.draw.rect(self.win, self.color, (self.posX,
                         self.posY, self.width, self.height))

    def move(self):
        if self.state == 'up':
            self.posY -= 10

        elif self.state == 'down':
            self.posY += 10

    def clamp(self):
        if self.posY <= 0:
            self.posY = 0

        elif self.posY + self.height >= win_height:
            self.posY = win_height - self.height


class CollisionManager:
    def ball_and_paddle1(self, ball, paddle1):
        if ball.posY + ball.radius > paddle1.posY and ball.posY - ball.radius < paddle1.posY + paddle1.height:
            if ball.posX - ball.radius <= paddle1.posX + paddle1.width:
                return True

        return False

    def ball_and_paddle2(self, ball, paddle2):
        if ball.posY + ball.radius > paddle2.posY and ball.posY - ball.radius < paddle2.posY + paddle2.height:
            if ball.posX + ball.radius >= paddle2.posX:
                return True

        return False

    def ball_wall(self, ball):
        # Top collision
        if ball.posY - ball.radius <= 0:
            return True

        # Botton coll
        if ball.posY + ball.radius >= win_height:
            return True

        return False


pygame.init()


win_width = 900
win_height = 500
black = (0, 0, 0)
white = (255, 255, 255)
win = pygame.display.set_mode((win_width, win_height))
clock = pygame.time.Clock()
pygame.display.set_caption('PONG by GhostOfToyman')


def paint_black():
    win.fill(black)
    pygame.draw.line(win, white, (win_width//2, 0),
                     (win_width//2, win_height), 5)


paint_black()


# Objects

ball = Ball(win, white, win_width//2, win_height//2, 15)
paddle1 = Paddle(win, white, 15, win_height//2 - 60, 20, 120)
paddle2 = Paddle(win, white, win_width - 35, win_height//2 - 60, 20, 120)
collision = CollisionManager()

playing = False

# main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                ball.start_moving()
                playing = True

            if event.key == pygame.K_w:
                paddle1.state = 'up'

            if event.key == pygame.K_s:
                paddle1.state = 'down'

            if event.key == pygame.K_UP:
                paddle2.state = 'up'

            if event.key == pygame.K_DOWN:
                paddle2.state = 'down'

        if event.type == pygame.KEYUP:
            paddle1.state = 'stopped'
            paddle2.state = 'stopped'

    if playing:
        paint_black()
        # ball movement
        ball.move()
        ball.show()

        # paddle1
        paddle1.move()
        paddle1.clamp()
        paddle1.show()

        # paddle2
        paddle2.move()
        paddle2.clamp()
        paddle2.show()

        # Check collision
        if collision.ball_and_paddle1(ball, paddle1):
            ball.paddle_collision()

        if collision.ball_and_paddle2(ball, paddle2):
            ball.paddle_collision()

        if collision.ball_wall(ball):
            ball.wall_collision()

    pygame.display.update()
    pygame.time.Clock().tick(30)
