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

    def restart_pos(self):
        self.posX = win_width//2
        self.posY = win_height//2
        self.dx = 0
        self.dy = 0
        self.show()


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

    def restart_pos(self):
        self.posY = win_height//2 - self.height//2
        self.state = 'stopped'
        self.show()


class Score:
    def __init__(self, win, points, posX, posY):
        self.win = win
        self.points = points
        self.posX = posX
        self.posY = posY
        self.font = pygame.font.SysFont('monospace', 80, bold=True)
        self.label = self.font.render(self.points, 0, white)
        self.show()

    def show(self):
        self.win.blit(
            self.label, (self.posX - self.label.get_rect().width // 2, self.posY))

    def increase(self):
        points = int(self.points) + 1
        self.points = str(points)
        self.label = self.font.render(self.points, 0, white)

    def restart(self):
        self.points = '0'
        self.label = self.font.render(self.points, 0, white)


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

    def goal_paddle1(self, ball):
        return ball.posX - ball.radius >= win_width

    def goal_paddle2(self, ball):
        return ball.posX - ball.radius <= 0


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


def restart():
    paint_black()
    score1.restart()
    score2.restart()
    ball.restart_pos()
    paddle1.restart_pos()
    paddle2.restart_pos()


paint_black()


# Objects

ball = Ball(win, white, win_width//2, win_height//2, 15)
paddle1 = Paddle(win, white, 15, win_height//2 - 60, 20, 120)
paddle2 = Paddle(win, white, win_width - 35, win_height//2 - 60, 20, 120)
collision = CollisionManager()
score1 = Score(win, '0', win_width//4, 15)
score2 = Score(win, '0', win_width - win_width//4, 15)

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

            if event.key == pygame.K_r:
                restart()
                playing = False

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

        if collision.goal_paddle1(ball):
            paint_black()
            score1.increase()
            ball.restart_pos()
            paddle1.restart_pos()
            paddle2.restart_pos()
            playing = False

        if collision.goal_paddle2(ball):
            paint_black()
            score2.increase()
            ball.restart_pos()
            paddle1.restart_pos()
            paddle2.restart_pos()
            playing = False

    score1.show()
    score2.show()

    pygame.display.update()
    pygame.time.Clock().tick(30)
