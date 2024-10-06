import os
import sys
import pygame
import game


class Gui:
    def __init__(self):
        self.l = 0
        self.game = game.Game(f"mp{self.l}.txt")
        self.W = 1000
        self.H = 1000
        self.size = min(1000 / self.game.map.width, 1000 / self.game.map.height)
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.W, self.H))
        self.readimages()
        self.clock = pygame.time.Clock()
        self.FPS = 60
        self.black = (0, 0, 0)
        self.imagetype = {
            "a": "player1",
            "b": "player2",
            "#": "wall",
            "A": None,
            "B": None,
            ".": None,
            "D": "door",
            "d": "door",
            "1": "1",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
        }
        self.win = False
        self.timer = {
            pygame.K_UP: 0,
            pygame.K_DOWN: 0,
            pygame.K_LEFT: 0,
            pygame.K_RIGHT: 0,
            pygame.K_w: 0,
            pygame.K_s: 0,
            pygame.K_a: 0,
            pygame.K_d: 0,
        }
        self.tmer = 10

    def readimages(self):
        self.image = {}
        for i in os.listdir("./image"):
            self.image[i.split(".")[0]] = pygame.image.load(f"./image/{i}").convert()
            self.image[i.split(".")[0]].set_colorkey(([0, 0, 0]))

    def main(self):
        self.clock.tick(self.FPS)
        self.screen.fill(self.black)
        mp = self.game.getMap()
        self.drawMap(mp)
        pygame.display.flip()
        self.checkEvent()
        if self.game.win() and (not self.win):
            pygame.mixer.Sound("win.ogg").play()
            print("win at level", self.l)
            self.win = True

    def drawMap(self, mp):
        for i in range(mp.height):
            for j in range(mp.width):
                if self.imagetype[mp.get(game.Point(i, j))] == None:
                    continue
                self.screen.blit(
                    pygame.transform.scale(
                        self.image[self.imagetype[mp.get(game.Point(i, j))]],
                        (self.size, self.size),
                    ),
                    (0 + j * self.size, 0 + i * self.size),
                )

    def checkEvent(self):
        for event in pygame.event.get():
            if event == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.game.reset()
                    self.win = False
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_n:
                    try:
                        self.l += 1
                        self.game = game.Game(f"mp{self.l}.txt")
                        self.win = False
                    except FileNotFoundError:
                        pass
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and self.timer[pygame.K_UP] <= 0:
            self.game.up()
            self.timer[pygame.K_UP] = self.tmer
        elif keys[pygame.K_DOWN] and self.timer[pygame.K_DOWN] <= 0:
            self.game.down()
            self.timer[pygame.K_DOWN] = self.tmer
        elif keys[pygame.K_LEFT] and self.timer[pygame.K_LEFT] <= 0:
            self.game.left()
            self.timer[pygame.K_LEFT] = self.tmer
        elif keys[pygame.K_RIGHT] and self.timer[pygame.K_RIGHT] <= 0:
            self.game.right()
            self.timer[pygame.K_RIGHT] = self.tmer

        if keys[pygame.K_w] and self.timer[pygame.K_w] <= 0:
            self.game.hup()
            self.timer[pygame.K_w] = self.tmer
        elif keys[pygame.K_s] and self.timer[pygame.K_s] <= 0:
            self.game.hdown()
            self.timer[pygame.K_s] = self.tmer
        elif keys[pygame.K_a] and self.timer[pygame.K_a] <= 0:
            self.game.hleft()
            self.timer[pygame.K_a] = self.tmer
        elif keys[pygame.K_d] and self.timer[pygame.K_d] <= 0:
            self.game.hright()
            self.timer[pygame.K_d] = self.tmer
        self.timer[pygame.K_UP] -= 1
        self.timer[pygame.K_DOWN] -= 1
        self.timer[pygame.K_LEFT] -= 1
        self.timer[pygame.K_RIGHT] -= 1

        self.timer[pygame.K_w] -= 1
        self.timer[pygame.K_s] -= 1
        self.timer[pygame.K_a] -= 1
        self.timer[pygame.K_d] -= 1


if __name__ == "__main__":
    gui = Gui()
    while True:
        gui.main()
