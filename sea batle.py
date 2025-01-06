from random import randint
class BoardException(Exception):
    pass
class BoardOutException(BoardException):
    def __str__(self):
        return "Вы стреляете за доску!!!"
class BoardUsedException(BoardException):
    def __str__(self):
        return "Вы уже стреляли сюда!!!"
class BoardWrongShipException(BoardException):
    pass

class Dot:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return f'Dot({self.x}, {self.y})'


class Ship():
    def __init__(self, bow, long, orientation):
        self.bow = bow
        self.long = long
        self.operation = orientation          # 0 - ГОРИЗОНТ    1 - ВЕРТИКАЛЬ
        self.hp = long

    @property
    def dots(self):
        ship_dots = []
        for i in range(self.long):
            cur_x = self.bow.x
            cur_y = self.bow.y

            if self.operation == 0:
                cur_y -= i

            if self.operation == 1:
                cur_x += i

            ship_dots.append(Dot(cur_x, cur_y))

        return ship_dots

    def shooten(self, shot):
        return shot in self.dots

class Board:
    def __init__(self, hid = False, size = 6):
        self.hid = hid
        self.size = size
        self.count = 0
        
        self.field = [['O']*size for _ in range(size)]

        self.busy = []       #использованные точки
        self.ships = []


    def __str__(self):
        markup = ""
        markup += "  | 1 | 2 | 3 | 4 | 5 | 6 |"
        for i, row in enumerate(self.field):
            markup += f'\n{i + 1} | ' + ' | '.join(row) + ' |'

        if self.hid:
            markup = markup.replace("■", 'O')

        return markup


    def out (self, d):
        return not((0 <= d.x < self.size) and (0 <= d.y < self.size))

    def contour(self, ship, verb = False):
        near = [(-1, -1), (-1,0), (-1, 1), (0, -1), (0, 0), (0, 1), (1, -1), (1, 0), (1, 1)]

        for d in ship.dots:
            for dx, dy in near:
                cur = Dot(d.x + dx, d.y + dy)
                if not(self.out(cur)) and cur not in self.busy:
                    if verb:
                        self.field[cur.x][cur.y] = "."
                    self.busy.append(cur)

    def add_ship (self, ship):
        for d in ship.dots:
            if self.out(d) or d in self.busy:        # Проверка границ для расстановки
                raise BoardWrongShipException()
        for d in ship.dots:
            self.field[d.x][d.y] = '■'
            self.busy.append(d)

        self.ships.append(ship)
        self.contour(ship)

    def shot (self, d):
        if self.out(d):
            raise BoardOutException()
        if d in self.busy:
            raise BoardUsedException()
        
        self.busy.append(d)

        for ship in self.ships:
            if ship.shooten(d):
                ship.hp -= 1
                self.field[d.x][d.y] = 'X'
                if ship.hp == 0:
                    self.count += 1
                    self.contour (ship, verb = True)
                    print("Корабль потоплен!")
                    return True
                else:
                    print("Корабль подбит!")
                    return True
            
        self.field[d.x][d.y] = '.'
        print('Промах!')
        return False

    def begin(self):
        self.busy = []

    def defeat(self):
        return self.count == len(self.ships)


# ====================================================================================================================================================================  


class Players:
    def __init__(self, board, enemy):
        self.board = board
        self.enemy = enemy

    def ask(self):
        raise NotImplementedError()

    def move(self):
        while True:
            try:
                target = self.ask()
                repeat = self.enemy.shot(target)
                return repeat
            except BoardException as e:
                print(e)

class AI(Players):
    def ask(self):
        d = Dot(randint(0, 5), randint(0, 5))
        print(f'Ход противника: {d.x+1} {d.y+1}')
        return d

class User(Players):
    def ask(self):
        while True:
            cords = input("(Введите координаты!): ").split()

            if len(cords) != 2:
                print("Введите две цифры через пробел! (Х - номер строки, У - номер столбца)")
                continue

            x, y = cords

            if not(x.isdigit()) or not(y.isdigit()):
                print(" Введите числа! ")
                continue

            x, y = int(x), int(y)

            return Dot(x-1, y-1)

class Game:
    def __init__(self, size = 6):
        self.size = size
        self.greeting()
         
        pl = self.placement()
        co = self.random_board()
        co.hid = True
    
        self.ai = AI(co, pl)
        self.us = User(pl, co)

    def manually_board(self):           # Метод управления ручной расстановки кораблей
        
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
    
        print(f'Введите координаты для носовой части каждого корабля и его ориентацию на поле!!!')
        print("   формат ввода: Х Y O ")
        print("  X - номер строки    ")
        print("  Y - номер столбца   ")
        print("  O - Ориентация корабля (0 - Горизонтальная(нос корабля направлен вправо); 1 - Вертикальная(нос корабля направленн вверх))   ")
        print()
        print(board)

        for l in lens:
            while True:
                xyo = input(f"Введите координаты для {l} палубного корабля: ").split()
               
                if len(xyo) != 3:
                    print("Введены не корректные данные!!!")
                    print("Введите ТРИ цифры через пробел!")
                    continue

                x, y, o = xyo

                if not(x.isdigit()) or not(y.isdigit()) or not(o.isdigit()):
                    print("Введены не корректные данные!!!")
                    print("Введите ТРИ цифры через пробел!")
                    continue

                x, y, o = int(x), int(y), int(o)

                ship = Ship(Dot(x-1, y-1), l, o)

                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    print('Невозможно разместить корабль в заданных координатах!!!')
                    print("(Обратите внимание, не заходит ли корабль за границы поля или не пересекается с другими координатами)")
                    print()
                    input("Нажмите <ENTER>, чтобы продолжить...")
                    pass
            print("-" * 30)    
            print(board)

        board.begin()
        return board

    def try_board(self):
        lens = [3, 2, 2, 1, 1, 1, 1]
        board = Board(size = self.size)
        attempts = 0
        for l in lens:
            while True:
                attempts += 1
                if attempts > 2000:
                    return None
                ship = Ship(Dot(randint(0, self.size), randint(0, self.size)), l, randint(0,1))
                try:
                    board.add_ship(ship)
                    break
                except BoardWrongShipException:
                    pass
        board.begin()
        return board
    
    def random_board(self):
        board = None
        while board is None:
            board = self.try_board()
        return board

    def greeting(self):
        print("**********************")
        print("*  Добро пожаловать  *")
        print("*       в игру       *")
        print("*    МОРСКОЙ БОЙ!    *")
        print("**********************")
        print()
        print("     ! ВНИМАНИЕ !     ")
        print(" В игре используется  ")
        print("   топографическая    ")
        print("  система координат   ")
        print("   формат ввода: Х Y   ")
        print("  X - номер строки    ")
        print("  Y - номер столбца   ")
        print()
        input("Нажмите <ENTER>, чтобы начать игру...")

    def loop(self):
        num = 0
        while True:
            print()
            print("="*30)
            print("Поле Игрока:")
            print(self.us.board)
            print("_"*30)
            print("Поле противника:")
            print(self.ai.board)
            print("="*30)
            if num % 2 == 0:
                print("Ваш ход...")
                repeat = self.us.move()
            else:
                print("Ход противника!")
                repeat = self.ai.move()
            if repeat:
                num -= 1

            if self.ai.board.defeat():
                print("_"*30)
                print("Адмирал, мы победили!")
                break
            if self.us.board.defeat():
                print("_"*30)
                print("Адмирал, мы потерпели поражение...")
                break
            num +=1

    def placement(self):
        while True:
            question = input('Хотите расставить корабли сами? (Введите "Y", чтобы вручную разместить корабли или "N", чтобы разместить их случайно): ')
            if not question.isalpha() or question.lower() not in "yn":
                print("Введен не корректный ответ!!!")
                print()
                continue
            else:
                print("Ответ принят!")
                break
        if question.lower() == "y":
            return self.manually_board()
        elif question.lower() == "n":
            return self.random_board()
        

    def start(self):
        self.loop()

g = Game()
g.start()

