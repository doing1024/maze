class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self, x, y):
        return Point(self.x + x, self.y + y)


class Map:
    def __init__(self, mapstr):
        try:
            self.map = mapstr.split("\n")
        except:
            self.map = mapstr
        self.map = [list(l) for l in self.map]
        self.width = len(self.map[0])
        self.height = len(self.map)

    def get(self, point):
        try:
            return self.map[point.x][point.y]
        except IndexError:
            return "#"

    def set(self, point, c):
        try:
            self.map[point.x][point.y] = c
        except IndexError:
            pass

    def find(self, c):
        l = []
        for x in range(len(self.map)):
            line = self.map[x]
            for y in range(len(line)):
                if self.get(Point(x, y)) == c:
                    l.append(Point(x, y))
        return l


class Game:
    def __init__(self, map):
        with open(map, mode="r") as f:
            self.map = Map(f.read())
        self.player1 = self.map.find("A")[0]
        self.player2 = self.map.find("B")[0]
        self.up = lambda: self.move(-1, 0)
        self.down = lambda: self.move(1, 0)
        self.left = lambda: self.move(0, -1)
        self.right = lambda: self.move(0, 1)
        self.hup = lambda: self.hit(-1, 0)
        self.hdown = lambda: self.hit(1, 0)
        self.hleft = lambda: self.hit(0, -1)
        self.mapname = map
        self.hright = lambda: self.hit(0, 1)
        self.put = {}
        for x in range(1, 3):
            self.put[str(x)] = 0

    def __canmove(self, c):
        return c != "#" and c != "a" and c != "b"

    def __check(self, point):
        if (
            point.x < 0
            or point.x >= self.map.height
            or point.y < 0
            or point.y >= self.map.width
        ):
            return False
        if not self.__canmove(self.getMap().get(point)):
            return False
        for x in range(1, 3):
            if self.map.get(point) == str(x + 2) and self.put[str(x)] == 0:
                return False
        return True

    def reset(self):
        self.player1 = self.map.find("A")[0]
        self.player2 = self.map.find("B")[0]
        self.map = Map(self.mapname)
        self.put = {}
        for x in range(1, 3):
            self.put[str(x)] = 0

    def getMap(self):
        newmp = Map(self.map.map)
        for i in range(self.map.height):
            """
            if i < self.player.x - 2:
                continue
            elif i > self.player.x + 2:
                break
            """
            for j in range(self.map.width):
                """
                if j < self.player.y - 2:
                    continue
                elif j > self.player.y + 2:
                    break

                """
                if self.player1.x == i and self.player1.y == j:
                    newmp.set(Point(i, j), "a")
                elif self.player2.x == i and self.player2.y == j:
                    newmp.set(Point(i, j), "b")
        return newmp

    def move(self, xx, yy):
        # print("move")
        try:
            if self.__check(self.player2.move(xx, yy)):
                self.player2 = self.player2.move(xx, yy)
                if self.map.get(self.player2) == "1":
                    for x in range(1, 3):
                        if self.map.get(self.player2.move(-xx, -yy)) == str(x):
                            self.put[str(x)] -= 1
                    self.put["1"] += 1
                elif self.map.get(self.player2) == "2":
                    for x in range(1, 3):
                        if self.map.get(self.player2.move(-xx, -yy)) == str(x):
                            self.put[str(x)] -= 1
                    self.put["2"] += 1
                else:
                    for x in range(1, 3):
                        if self.map.get(self.player2.move(-xx, -yy)) == str(x):
                            self.put[str(x)] -= 1
        except IndexError:
            # print(f"move{x} {y} indexerror")
            pass
        print(f"print by move(red),put={self.put},x={xx},y={yy}")

    def hit(self, xx, yy):
        try:
            # print("hit")
            if self.__check(self.player1.move(xx, yy)):
                self.player1 = self.player1.move(xx, yy)
                if self.map.get(self.player1) == "1":
                    for x in range(1, 3):
                        if self.map.get(self.player1.move(-xx, -yy)) == str(x):
                            self.put[str(x)] -= 1
                    self.put["1"] += 1
                elif self.map.get(self.player1) == "2":
                    for x in range(1, 3):
                        if self.map.get(self.player1.move(-xx, -yy)) == str(x):
                            self.put[str(x)] -= 1
                    self.put["2"] += 1
                else:
                    for x in range(1, 3):
                        if self.map.get(self.player1.move(-xx, -yy)) == str(x):
                            self.put[str(x)] -= 1
        except IndexError:
            # print(f"hit{x} {y} indexerror")
            pass
        print(f"print by hit(green),put={self.put},x={xx},y={yy}")

    def win(self):
        for i in self.map.find("D"):
            if i.x == self.player1.x and i.y == self.player1.y:
                return True
            if i.x == self.player2.x and i.y == self.player2.y:
                return True
        return False
