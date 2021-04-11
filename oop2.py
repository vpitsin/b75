from random import choice
import copy


class Field:
    def __init__(self):
        pass

    def __iter__(self):
        return iter(self.field)

    def create_field(self, boats):
        field = [['0'] * 6 for i in range(6)]

        for x, y in boats:
            field[y][x] = '■'
        self.field = field

        return iter(field)

    def print_pl_field(self):
        header = f" | {' | '.join([str(i) for i in range(1, 7)])} |"
        print('\nВаше поле:\n', header)
        for i, row in enumerate(self.field, start=1):
            print(f"{i} | {' | '.join(row)} |")

    def print_ai_field(self):
        header = f" | {' | '.join([str(i) for i in range(1, 7)])} |"
        print('\nПоле АИ без маски:\n', header)
        for i, row in enumerate(self.field, start=1):
            print(f"{i} | {' | '.join(row)} |")

    def print_ai_mask_field(self):
        header = f" | {' | '.join([str(i) for i in range(1, 7)])} |"

        print('\nПоле АИ:\n', header)
        mask_field = copy.deepcopy(self.field)
        for row in mask_field:
            for i in range(len(row)):
                if row[i] == '■':
                    row[i] = "0"

        for i, row in enumerate(mask_field, start=1):
            print(f"{i} | {' | '.join(row)} |")

    def return_field(self):
        return self.field


class Boat:
    def __init__(self):
        pass

    def gen_pl_boat(self):
        all_coords = [(y, x) for x in range(6) for y in range(6)]
        all_boats_coords = []
        all_busy_coords = []
        print("Введите расположение Ваших кораблей на поле. \n"
              "Для ориентации используйте '0' для горизонтального расположения и '1' для вертикального")

        size = ['трехпалубного'] + ['двухпалубного'] * 2 + ['однопалубного'] * 4
        size_num = [3, 2, 2, 1, 1, 1, 1]
        should_restart = True
        while should_restart:
            should_restart = False
            for i in range(len(size)):
                while not (set(all_coords).issubset(all_busy_coords)):
                    field = Field()
                    field.create_field(all_boats_coords)
                    field.print_pl_field()
                    try:
                        y = (input(f'Введите № строки  {size[i]} корабля: '))
                        x = (input(f'Введите № столбца  {size[i]} корабля: '))
                        if size_num[i] > 1:
                            o = (input(f'Введите ориентацию  {size[i]} корабля: '))
                        else:
                            o = 0
                        if (int(x) in range(1, 7)) and (int(y) in range(1, 7)) and (int(o) in (0, 1)):
                            x = int(x) - 1
                            y = int(y) - 1
                            o = int(o)
                            if o == 0 and x + size_num[i] - 1 < 6:  # горизонтальная ориентация
                                one_boat_coords = [(x, y) for x in
                                                   range(x, x + size_num[i])]  # генерим лодку координаты
                                one_boat_busy_coords = [[(x, y) for x in range(x - 1, x + size_num[i] + 1)] for y in
                                                        range(y - 1, y + 2)]
                                one_boat_busy_coords = one_boat_busy_coords[0] + one_boat_busy_coords[1] + \
                                                       one_boat_busy_coords[2]

                                try:
                                    if set(one_boat_coords).isdisjoint(all_busy_coords):
                                        all_boats_coords.extend(one_boat_coords)
                                        all_busy_coords.extend(one_boat_busy_coords)
                                        field.create_field(all_boats_coords)
                                        print("Корабль создан")
                                        break
                                    else:
                                        raise Exception
                                except Exception:
                                    print("Корабли пересекаются целиком или контурами")

                            elif o == 1 and y + size_num[i] - 1 < 6:  # вертикальная ориентация
                                one_boat_coords = [(x, y) for y in
                                                   range(y, y + size_num[i])]  # генерим лодку координаты
                                one_boat_busy_coords = [[(x, y) for y in range(y - 1, y + size_num[i] + 1)] for x in
                                                        range(x - 1, x + 2)]
                                one_boat_busy_coords = one_boat_busy_coords[0] + one_boat_busy_coords[1] + \
                                                       one_boat_busy_coords[2]

                                try:
                                    if set(one_boat_coords).isdisjoint(all_busy_coords):
                                        all_boats_coords.extend(one_boat_coords)
                                        all_busy_coords.extend(one_boat_busy_coords)
                                        field.create_field(all_boats_coords)
                                        print("Корабль создан")
                                        break
                                    else:
                                        raise Exception
                                except Exception:
                                    print("Корабли пересекаются целиком или контурами")
                            else:
                                print("Корабль выходит за пределы поля")
                        else:
                            raise Exception

                    except Exception:
                        if x.isdigit() and y.isdigit() and o.isdigit():
                            print("введенное значение в одном из пар-ров больше допустимого")
                        else:
                            print("Только целые цифры, алло")
                else:
                    print("Ну кто так корабли размещает то? Место на поле уже кончилось")
                    print("Создаем поле заново")
                    all_boats_coords.clear()
                    all_busy_coords.clear()
                    should_restart = True
                    break

        print("Все корабли созданы")
        self.all_boats_coords = all_boats_coords

    def gen_ai_boat(self):
        all_coords = [(y, x) for x in range(6) for y in range(6)]
        all_boats_coords = []
        all_busy_coords = []
        size_num = [3, 2, 2, 1, 1, 1, 1]

        should_restart = True

        while should_restart:
            should_restart = False

            for i in range(len(size_num)):
                while not (set(all_coords).issubset(all_busy_coords)):
                    x, y = choice(all_coords)
                    if size_num[i] > 1:
                        o = choice([0, 1])
                    else:
                        o = 0

                    if o == 0 and x + size_num[i] - 1 < 6:  # горизонтальная ориентация
                        one_boat_coords = [(x, y) for x in range(x, x + size_num[i])]  # генерим лодку координаты
                        one_boat_busy_coords = [[(x, y) for x in range(x - 1, x + size_num[i] + 1)] for y in
                                                range(y - 1, y + 2)]
                        one_boat_busy_coords = one_boat_busy_coords[0] + one_boat_busy_coords[1] + one_boat_busy_coords[
                            2]

                    elif o == 1 and y + size_num[i] - 1 < 6:  # вертикальная ориентация
                        one_boat_coords = [(x, y) for y in range(y, y + size_num[i])]  # генерим лодку координаты
                        one_boat_busy_coords = [[(x, y) for y in range(y - 1, y + size_num[i] + 1)] for x in
                                                range(x - 1, x + 2)]
                        one_boat_busy_coords = one_boat_busy_coords[0] + one_boat_busy_coords[1] + one_boat_busy_coords[
                            2]
                    else:
                        continue

                    if set(one_boat_coords).isdisjoint(all_busy_coords):
                        all_boats_coords.extend(one_boat_coords)
                        all_busy_coords.extend(one_boat_busy_coords)
                        # Field.player_field(self, all_boats_coords)
                        break
                    else:
                        continue
                else:
                    print("мы достигли лимита поля")
                    all_boats_coords.clear()
                    all_busy_coords.clear()
                    should_restart = True
                    break

        print("Поле AI сгенерировано")
        self.all_boats_coords = all_boats_coords

    def return_boat(self):
        return self.all_boats_coords


class Side:
    def __init__(self):
        pass

    def player_shoot(self, enemy=Field()):

        enemy_field = enemy.return_field()
        while True:
            try:
                enemy.print_ai_mask_field()
                y = (input('Введите № строки предполагаемого корабля: '))
                x = (input('Введите № столбца предполагаемого корабля: '))

                if ((int(x) in range(1, 7)) and (int(y) in range(1, 7))):
                    x = int(x) - 1
                    y = int(y) - 1

                    if enemy_field[y][x] == "0":
                        enemy_field[y][x] = "T"
                        print("Промах. Ход уходит AI")
                        print("__________________________")
                        break
                    elif enemy_field[y][x] == "■":
                        enemy_field[y][x] = "X"
                        if any(['■' in row for row in enemy_field]):
                            print("Попадание! Еще выстрел")
                        else:
                            enemy.print_ai_mask_field()
                            print("Все корабли злодейского АИ убиты!! \n"
                                  "Вы - победили! Аве, Цезарь")
                            return ("finish")

                    elif enemy_field[y][x] == "X" or enemy_field[y][x] == "T":
                        print("В клетку уже был сделан выстрел")
                    else:
                        print("неожиданное завершение")
                else:
                    raise Exception
            except Exception:
                if (x.isdigit() and y.isdigit()):
                    print("Обе координаты должны находиться в диапазоне от одного до шести")
                else:
                    print("Только цифры, причем целые, алло!")

    def ai_shoot(self, enemy=Field()):
        enemy_field = enemy.return_field()
        all_coords = [(y, x) for x in range(6) for y in range(6)]
        while True:
            x, y = choice(all_coords)
            if enemy_field[y][x] == "0":
                enemy_field[y][x] = "T"
                print("АИ делает промах! Ход уходит игроку")
                enemy.print_pl_field()
                print("__________________________")
                break  # ПРОМАХ, ЗАВЕРШИТЬ
            elif enemy_field[y][x] == "■":
                enemy_field[y][x] = "X"
                if any(['■' in row for row in enemy_field]):
                    print("АИ производит попадание! Еще выстрел")
                else:
                    print("Все корабли жалкого кожаного убиты!! \n"
                          "Машина одержала верх! Слава терминаторам!")
                    return "finish"

            elif enemy_field[y][x] == "X" or enemy_field[y][x] == "T":
                continue
            else:
                print("неожиданное завершение")


if __name__ == '__main__':
    ai_b = Boat()
    ai_b.gen_ai_boat()
    pl_b = Boat()
    pl_b.gen_pl_boat()

    ai_f = Field()
    ai_f.create_field(ai_b.return_boat())
    pl_f = Field()
    pl_f.create_field(pl_b.return_boat())    #чтобы не мучаться каждый раз создавая
    #pl_f.create_field([(0, 0), (1, 0), (2, 0), (0, 2), (0, 3), (0, 5), (1, 5), (2, 2), (5, 0), (5, 5), (4, 3)])
    pl_f.print_pl_field()
    pl_side = Side()
    ai_side = Side()
    print("Да начнется смертельная битва!")
    while True:
        print("\nХод игрока")
        if pl_side.player_shoot(ai_f) == "finish":
            break
        print("Ход АИ")
        if ai_side.ai_shoot(pl_f) == "finish":
            break
    print("Все, конец!")
