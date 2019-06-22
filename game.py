import pygame
from pygame.locals import *
from random import randint


class Apple:
    side = 20

    def __init__(self, snake_x, snake_y, width, height):
        checked = False
        while not checked:
            self.x = randint(0, (width - self.side) / self.side) * self.side
            self.y = randint(0, (height - self.side) / self.side) * self.side
            if not ((self.x in snake_x) and (self.y in snake_y)):
                checked = True

    def draw(self, surface):
        pygame.draw.circle(surface, (0, 255, 0), (self.x + int(self.side / 2), self.y + int(self.side / 2)),
                           int(self.side / 2))


class Game:
    def isCollision(self,x1,y1,x2,y2,bsize):
        if x1 >= x2 and x1 < x2 + bsize:
            if y1 >= y2 and y1 < y2 + bsize:

                return True
        return False


class Player:
    side = 20
    direction = randint(0, 3)
    updateCountMax = 2
    updateCount = 0

    def __init__(self, length: object, width: object, height: object) -> object:
        self.length = length
        self.x = [randint((self.side * length) / self.side, (width - self.side * length) / self.side) * self.side]
        self.y = [randint((self.side * length) / self.side, (height - self.side * length) / self.side) * self.side]
        for i in range(1, length):
            if self.direction == 0:
                self.x.append(self.x[0] - i * self.side)
                self.y.append(self.y[0])
            if self.direction == 1:
                self.x.append(self.x[0] + i * self.side)
                self.y.append(self.y[0])
            if self.direction == 2:
                self.x.append(self.x[0])
                self.y.append(self.y[0] + i * self.side)
            if self.direction == 3:
                self.x.append(self.x[0])
                self.y.append(self.y[0] - i * self.side)

    def check_bounds(self, width, height):
        for i in range(self.length):
            if self.x[i] < 0:
                self.x[i] = self.x[i] + width
            if self.x[i] >= width:
                self.x[i] = self.x[i] - width
            if self.y[i] < 0:
                self.y[i] = self.y[i] + height
            if self.y[i] >= height:
                self.y[i] = self.y[i] - height


    def update(self):

        self.updateCount = self.updateCount + 1
        if self.updateCount > self.updateCountMax:

            for i in range(self.length - 1, 0, -1):
                self.x[i] = self.x[i - 1]
                self.y[i] = self.y[i - 1]

            if self.direction == 0:
                self.x[0] = self.x[0] + self.side
            if self.direction == 1:
                self.x[0] = self.x[0] - self.side
            if self.direction == 2:
                self.y[0] = self.y[0] - self.side
            if self.direction == 3:
                self.y[0] = self.y[0] + self.side

            self.updateCount = 0

    def moveRight(self):
        if self.direction!=1:
            self.direction = 0

    def moveLeft(self):
        if self.direction != 0:
            self.direction = 1

    def moveUp(self):
        if self.direction != 3:
            self.direction = 2

    def moveDown(self):
        if self.direction != 2:
            self.direction = 3

    def grow(self):
        self.length = self.length + 1
        if self.direction == 0:
            self.x.append(self.x[self.length-2] - self.side)
            self.y.append(self.y[self.length-2])
        if self.direction == 1:
            self.x.append(self.x[self.length-2] + self.side)
            self.y.append(self.y[self.length - 2])
        if self.direction == 2:
            self.y.append(self.y[self.length-2] + self.side)
            self.x.append(self.x[self.length - 2])
        if self.direction == 3:
            self.y.append(self.y[self.length-2] - self.side)
            self.x.append(self.x[self.length - 2])





class App:
    window_width = 500
    window_height = 400
    player = 1


    def __init__(self):
        self._running = True
        self._display_surf = None
        self.pause = False
        self.dead = False
        self.score = 0
        self.game = Game()
        self.player = Player(10, self.window_width, self.window_height)
        self.apple = Apple(self.player.x, self.player.y, self.window_width, self.window_height)

    def on_init(self):
        pygame.init()
        self.myfont = pygame.font.SysFont('Arial', 32)
        self._display_surf = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption('SNAKE')
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        self.player.update()

        for i in range(0, self.player.length):
            if self.game.isCollision(self.apple.x, self.apple.y, self.player.x[i], self.player.y[i], self.apple.side):
                self.apple.__init__(self.player.x, self.player.y, self.window_width, self.window_height)
                self.player.grow()
                self.score += 1
            pass

        for i in range(2, self.player.length):
            if self.game.isCollision(self.player.x[0], self.player.y[0], self.player.x[i], self.player.y[i], self.apple.side):
                self.dead = True
                self.pause = True


        self.player.check_bounds(self.window_width, self.window_height)

    def on_render(self):
        self._display_surf.fill((0, 0, 0))

        for i in range(self.player.length):
            pygame.draw.rect(self._display_surf, (255, 0, 0), (self.player.x[i], self.player.y[i],
                                                               self.player.side, self.player.side))
        if self.dead:
            self._score_surface = self.myfont.render(str(self.score), True, (255, 0, 0), (0, 0, 0))
        else:
            self._score_surface = self.myfont.render(str(self.score), True, (255, 255, 255), (0, 0, 0))
        self._display_surf.blit(self._score_surface, (self.window_width - 50, 20))

        self.apple.draw(self._display_surf)


        pygame.display.flip()

    def on_cleanup(self):
        pygame.quit()

    def pause_press(self):
        if self.pause and self.dead:
            self.player.__init__(10, self.window_width, self.window_height)
            self.score = 0
            self.pause = False
            self.dead = False
        elif self.pause and not self.dead:
            self.pause = False
        else:
            self.pause = True

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while self._running:
            pygame.time.delay(15)
            pygame.event.pump()

            for event in pygame.event.get():
                self.on_event(event)

            keys = pygame.key.get_pressed()

            if (keys[K_SPACE]):
                self.pause_press()
                pygame.time.delay(200)

            if (keys[K_ESCAPE]):
                self._running = False

            if not self.pause:

                if (keys[K_RIGHT]):
                    self.player.moveRight()

                if (keys[K_LEFT]):
                    self.player.moveLeft()

                if (keys[K_UP]):
                    self.player.moveUp()

                if (keys[K_DOWN]):
                    self.player.moveDown()



                self.on_loop()
                self.on_render()

        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()
