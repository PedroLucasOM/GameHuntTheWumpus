import msvcrt
import os
import random
import sys
import time
from os.path import exists

import pygame

EMPTY = ""
PLAYER = "X"
MONSTER = "1"
DEAD_MONSTER = "x"
STENCH = "2"
ABYSS = "3"
BREEZE = "4"
GOLD = "5"


def build_game(nickname, commands):
    BUILD_BOARD = []

    SIZE_BOARD = choose_level()
    LIMIT_BOARD = SIZE_BOARD - 1

    for i in range(SIZE_BOARD):
        row = [EMPTY] * SIZE_BOARD
        BUILD_BOARD.append(row)

    BUILD_BOARD[LIMIT_BOARD][0] = PLAYER

    summon_abyss_and_monster_and_gold(BUILD_BOARD, LIMIT_BOARD, pick_int(0.18 * (SIZE_BOARD ** 2)))

    summom_stenchs_and_breezes(BUILD_BOARD, LIMIT_BOARD, SIZE_BOARD)

    play_game(BUILD_BOARD, SIZE_BOARD, LIMIT_BOARD, nickname, SIZE_BOARD, commands)


def choose_level():
    clear_display()
    level = input("Difficult Level: [Input 1 to Easy Maze; Input 2 to Hard Maze; Input 3 to Pro Maze]: ")
    while level != "1" and level != "2" and level != "3":
        clear_display()
        print("Incorrect informed level!")
        level = int(input(
            "What the level wanted? [Input 1 to Easy Made; Input 2 to Hard Made; Input 3 to Pro Made; 4 to Exit Execution]: "))
        if level == "4":
            sys.exit()
    if level == "1":
        return 4
    elif level == "2":
        return 6
    elif level == "3":
        return 10


def message_init():
    string = "Welcome to Hunt The Wumpus!"
    value = ""
    for i in string:
        clear_display()
        value = value + i
        print(value)
        time.sleep(0.04)


def clear_display():
    os.system('cls' if os.name == 'nt' else 'clear')


def pick_int(value):
    integer = int(value)
    real = value - integer
    return integer + 1 if real >= 0.5 else integer


def can_put(row, column, LIMIT_BOARD):
    return (row >= 0 and column >= 0) and (row <= LIMIT_BOARD and column <= LIMIT_BOARD)


def canot_positing(row, column, BUILD_BOARD, LIMIT_BOARD):
    check = []
    checks = [[row - 1, row - 1, column, 0], [column - 1, row, column - 1, 0], [row + 1, row + 1, column, LIMIT_BOARD],
              [column + 1, row, column + 1, LIMIT_BOARD]]

    for i in checks:
        if i[3] == 0:
            if i[0] >= 0:
                check.append(1) if (BUILD_BOARD[i[1]][i[2]] != ABYSS) else check.append(1)
        elif i[3] == LIMIT_BOARD:
            if i[0] <= LIMIT_BOARD:
                check.append(1) if (BUILD_BOARD[i[1]][i[2]] != ABYSS) else check.append(1)
    return True if 0 in check else False


def summon_abyss_and_monster_and_gold(BUILD_BOARD, LIMIT_BOARD, loops):
    for i in range(loops + 2):
        row = random.randint(0, LIMIT_BOARD)
        column = random.randint(0, LIMIT_BOARD)
        if i != loops + 1:
            while ((row == LIMIT_BOARD - 1 and column == 0) or (row == LIMIT_BOARD and column == 1) or (
                    BUILD_BOARD[row][column] == PLAYER) or (BUILD_BOARD[row][column] == ABYSS) or (
                           BUILD_BOARD[row][column] == MONSTER)):
                row = random.randint(0, LIMIT_BOARD)
                column = random.randint(0, LIMIT_BOARD)
            if i == loops:
                BUILD_BOARD[row][column] = MONSTER
            else:
                BUILD_BOARD[row][column] = ABYSS
        else:
            while ((BUILD_BOARD[row][column] == PLAYER) or (BUILD_BOARD[row][column] == ABYSS) or canot_positing(row,
                                                                                                                 column,
                                                                                                                 BUILD_BOARD,
                                                                                                                 LIMIT_BOARD)):
                row = random.randint(0, LIMIT_BOARD)
                column = random.randint(0, LIMIT_BOARD)
            BUILD_BOARD[row][column] += GOLD


def summom_stenchs_and_breezes(BUILD_BOARD, LIMIT_BOARD, SIZE_BOARD):
    positions = []

    for i in range(SIZE_BOARD):
        for j in range(SIZE_BOARD):
            if MONSTER in BUILD_BOARD[i][j]:
                positions.append(str(i) + ";" + str(j))
            elif BUILD_BOARD[i][j] == ABYSS:
                positions.append(str(i) + " " + str(j))
    for i in positions:
        valor = ""
        position = []
        if ";" in i:
            valor = STENCH
            position = i.split(";")
        elif " " in i:
            valor = BREEZE
            position = i.split(" ")
        row = int(position[0])
        column = int(position[1])
        checks = [[row + 1, column], [row - 1, column], [row, column + 1], [row, column - 1]]
        for i in checks:
            if (can_put(i[0], i[1], LIMIT_BOARD) and BUILD_BOARD[i[0]][i[1]] != ABYSS and valor not in
                    BUILD_BOARD[i[0]][i[1]]):
                BUILD_BOARD[i[0]][i[1]] += valor


def remapping_keys():
    clear_display()
    commands = ["w", "s", "a", "d", "u", "j", "h", "k"]
    descritiones = ["move up", "move down", "move left", "move right", "shoot up", "shoot down", "shoot left",
                    "shoot right"]

    print("The default keys to play game are: WASD to move player and UHJK to shoot.")
    choose = input("You wanter remap the keys? [Y] to Yes or [N] to Not: ")
    if choose == "Y" or choose == "N":
        choose = choose.lower()
    while choose != "y" and choose != "n":
        clear_display()
        print("Incorrect command!")
        choose = input("You wanter remap the keys? [Y] to Yes or [N] to Not or [F] to Exit: ")
        if choose == "F" or choose == "f":
            sys.exit()
        if choose == "Y" or choose == "N":
            choose = choose.lower()
    if choose == "y":
        for i in range(len(commands)):
            commands[i] = input("Enter your command to " + str(descritiones[i]) + ": ").lower()
    return commands


def play_sound(path, type0):
    pygame.mixer.init(44100)
    music = pygame.mixer.music
    music.load(path)
    music.play()
    if type0 == "monster" or type0 == "abyss" or type0 == "kill" or type0 == "not_hit":
        while pygame.mixer.music.get_busy():
            show_flash(type0)
            time.sleep(1)


def show_flash(type0):
    if type0 == "monster":
        clear_display()
        print("Wait while the monster devour you.")
        time.sleep(0.3)
        clear_display()
        print("Wait while the monster devour you..")
        time.sleep(0.3)
        clear_display()
        print("Wait while the monster devour you...")
        time.sleep(0.3)
    elif type0 == "abyss":
        clear_display()
        print("You're falling.")
        time.sleep(0.3)
        clear_display()
        print("You're falling..")
        time.sleep(0.3)
        clear_display()
        print("You're falling...")
        time.sleep(0.3)


def show_board(BUILD_BOARD, SIZE_BOARD, scores):
    clear_display()
    print("Board Parts: ")
    print("X - player | 1 - monster | x - dead_monster | 2 - stench | 3 - abyss | 4 - breeze | 5 - gold")
    print('\n' + "Scores: " + str(scores) + '\n')
    for i in range(SIZE_BOARD):
        text = ""
        for j in range(SIZE_BOARD):
            if len(str(BUILD_BOARD[i][j])) == 2:
                drop = str(BUILD_BOARD[i][j])
                text = text + "  " + drop[0] + " " + drop[1] + "  " + " | "
            elif len(str(BUILD_BOARD[i][j])) == 3:
                drop = str(BUILD_BOARD[i][j])
                text = text + " " + drop[0] + " " + drop[1] + " " + drop[2] + " " + " | "
            elif len(str(BUILD_BOARD[i][j])) == 4:
                drop = str(BUILD_BOARD[i][j])
                text = text + drop[0] + " " + drop[1] + " " + drop[2] + " " + drop[3] + " | "
            elif len(str(BUILD_BOARD[i][j])) == 1:
                text = text + "   " + str(BUILD_BOARD[i][j]) + "   " + " | "
            elif len(str(BUILD_BOARD[i][j])) == 0:
                text = text + "   -   " + " | "
        print(text)
        print("")


def play_game(BUILD_BOARD, SIZE_BOARD, LIMIT_BOARD, nickname, level, commands):
    RUN_BOARD = []

    for i in range(SIZE_BOARD):
        row = [EMPTY] * SIZE_BOARD
        RUN_BOARD.append(row)

    scores = 0
    row_player = LIMIT_BOARD
    column_player = 0

    RUN_BOARD[row_player][column_player] = PLAYER

    clear_display()
    path_sound = choose_zoeira()

    show_board(RUN_BOARD, SIZE_BOARD, scores)

    while True or True:
        command = msvcrt.getch()
        while command[0] == 0:
            command = msvcrt.getch()
        command = chr(command[0])
        if command == commands[0] or command == commands[1] or command == commands[2] or command == commands[3]:
            if check_wall(row_player, column_player, LIMIT_BOARD, command, commands):
                scores -= 1
                new_positions_player = move_player(row_player, column_player, RUN_BOARD, command, commands).split(" ")
                row_player = int(new_positions_player[0])
                column_player = int(new_positions_player[1])

                if GOLD in BUILD_BOARD[row_player][column_player]:
                    if pick_gold(row_player, column_player, BUILD_BOARD, RUN_BOARD, SIZE_BOARD, scores):
                        play_sound(
                            os.getcwd() + '/' + path_sound + '/withgold.mp3',
                            "gold")
                        scores += 1000

                if (game_over(row_player, column_player, BUILD_BOARD, SIZE_BOARD) == "abyss" or game_over(row_player,
                                                                                                          column_player,
                                                                                                          BUILD_BOARD,
                                                                                                          SIZE_BOARD) == "monster"):
                    if game_over(row_player, column_player, BUILD_BOARD, SIZE_BOARD) == "monster":
                        play_sound(
                            os.getcwd() + '/' + path_sound + '/withmonster.mp3',
                            "monster")
                    else:
                        play_sound(
                            os.getcwd() + '/' + path_sound + '/withabyss.mp3',
                            "abyss")
                    scores -= 10000
                    put_scores(nickname, scores, level)
                    repositioning_player(row_player, column_player, BUILD_BOARD, SIZE_BOARD)
                    show_board(BUILD_BOARD, SIZE_BOARD, scores)
                    if game_over(row_player, column_player, BUILD_BOARD, SIZE_BOARD) == "monster":
                        print("You were devoured by the monster.")
                    else:
                        print("You fell into an abyss.")
                    print("")
                    show_top5(level)
                    sys.exit()

                sensations = feel_sensations(row_player, column_player, BUILD_BOARD, SIZE_BOARD)

                show_board(RUN_BOARD, SIZE_BOARD, scores)

                if bool(sensations[0]):
                    if len(sensations) > 1:
                        print(sensations[1])
                        if sensations[1] == "The player is facing stenches.":
                            play_sound(
                                os.getcwd() + '/' + path_sound + '/withstench.mp3',
                                "stench")
                        elif sensations[1] == "The player is facing breezes.":
                            play_sound(
                                os.getcwd() + '/' + path_sound + '/withbreeze.mp3',
                                "breeze")
                        time.sleep(1.0)
        elif command == commands[4] or command == commands[5] or command == commands[6] or command == commands[7]:
            play_sound(os.getcwd() + '/' + path_sound + '/hit.mp3',
                       "hit")
            repositioning_player(row_player, column_player, BUILD_BOARD, SIZE_BOARD)
            kill_monster(row_player, column_player, BUILD_BOARD, RUN_BOARD, SIZE_BOARD, command, commands, scores)
            for i in range(SIZE_BOARD):
                for j in range(SIZE_BOARD):
                    if "x" in BUILD_BOARD[i][j]:
                        scores += 10000
                        put_scores(nickname, scores, level)
                        repositioning_player(row_player, column_player, BUILD_BOARD, SIZE_BOARD)
                        show_board(BUILD_BOARD, SIZE_BOARD, scores)
                        print("Congratulations! You killed the monster.")
                        print("")
                        show_top5(level)
                        play_sound(
                            os.getcwd() + '/' + path_sound + '/monsterdead.mp3',
                            "kill")
                        sys.exit()
            repositioning_player(row_player, column_player, BUILD_BOARD, SIZE_BOARD)
            show_board(BUILD_BOARD, SIZE_BOARD, scores)
            print("His arrow did not hit the monster. You lost!")
            play_sound(
                os.getcwd() + '/' + path_sound + '/monsteralive.mp3',
                "not_hit")
            sys.exit()


def choose_zoeira():
    zoeira = input("You want play game in mode zoeira? [Y] to yes or [N] to not: ").lower()
    while zoeira != "y" and zoeira != "n":
        print("Incorrect command!")
        zoeira = input("You want play game in mode zoeira? [Y] to yes or [N] to not or [F] to exit: ").lower()
        if zoeira == "f":
            break
    if zoeira == "y":
        return "zoeira"
    else:
        return "default"


def put_scores(nickname, scores, level):
    if exists("scores.txt") == False:
        create = open("scores.txt", "w")
        create.close()
    write_file = open("scores.txt", "a")
    write_file.write(str(nickname) + " " + str(scores) + " " + str(level) + " " + '\n')
    write_file.close()


def show_top5(level):
    contents = []
    points = []
    nicknames = []
    file = open("scores.txt", "r")
    for i in file:
        i = i.split(" ")
        if i[2] == str(level):
            points.append(i[1])
            contents.append(i[0] + " " + i[1])
    file.close()
    points.sort(key=int, reverse=True)
    if len(points) != 0:
        print("Top Rated: ")
        print("")
        if len(points) >= 5:
            for i in range(5):
                for j in contents:
                    if points[i] in j:
                        j = j.split(" ")
                        nicknames.append(j[0])
                        break
                print(str(i + 1) + ": " + nicknames[i] + " ~ " + points[i])
        else:
            for i in range(len(points)):
                for j in contents:
                    if points[i] in j:
                        j = j.split(" ")
                        nicknames.append(j[0])
                        break
                print(str(i + 1) + ": " + nicknames[i] + " ~ " + points[i])


def move_player(row, column, RUN_BOARD, command, commands):
    RUN_BOARD[row][column] = EMPTY
    if command == commands[0]:
        RUN_BOARD[row - 1][column] = PLAYER
        return str(row - 1) + " " + str(column)
    elif command == commands[1]:
        RUN_BOARD[row + 1][column] = PLAYER
        return str(row + 1) + " " + str(column)
    elif command == commands[2]:
        RUN_BOARD[row][column - 1] = PLAYER
        return str(row) + " " + str(column - 1)
    else:
        RUN_BOARD[row][column + 1] = PLAYER
        return str(row) + " " + str(column + 1)


def repositioning_player(row_player, column_player, BUILD_BOARD, SIZE_BOARD):
    for i in range(SIZE_BOARD):
        for j in range(SIZE_BOARD):
            if BUILD_BOARD[i][j] == PLAYER:
                BUILD_BOARD[i][j] = EMPTY
                BUILD_BOARD[row_player][column_player] += PLAYER
                break


def kill_monster(row_player, column_player, BUILD_BOARD, RUN_BOARD, SIZE_BOARD, command, commands, scores):
    checks = [[commands[4], row_player, -1, "row_player"], [commands[5], row_player, SIZE_BOARD, "row_player"],
              [commands[6], column_player, -1, "column_player"],
              [commands[7], column_player, SIZE_BOARD, "column_player"]]
    for i in checks:
        if command in i:
            index1 = 0
            index2 = 0
            while i[1] != i[2]:
                if "row_player" in i:
                    index1 = i[1]
                    index2 = column_player
                else:
                    index1 = row_player
                    index2 = i[1]
                RUN_BOARD[index1][index2] = BUILD_BOARD[index1][index2]
                show_board(RUN_BOARD, SIZE_BOARD, scores)
                time.sleep(0.5)
                if MONSTER in BUILD_BOARD[index1][index2]:
                    BUILD_BOARD[index1][index2] = BUILD_BOARD[index1][index2].replace(MONSTER, DEAD_MONSTER)
                    RUN_BOARD[index1][index2] = RUN_BOARD[index1][index2].replace(MONSTER, DEAD_MONSTER)
                    show_board(RUN_BOARD, SIZE_BOARD, scores)
                    time.sleep(0.5)
                    break
                if i[2] == SIZE_BOARD:
                    i[1] += 1
                else:
                    i[1] -= 1


def check_wall(row_player, column_player, LIMIT_BOARD, command, commands):
    return (row_player != 0 and command == commands[0]) or (row_player != LIMIT_BOARD and command == commands[1]) or (
            column_player != 0 and command == commands[2]) or (
                   column_player != LIMIT_BOARD and command == commands[3])


def pick_gold(row_player, column_player, BUILD_BOARD, RUN_BOARD, SIZE_BOARD, scores):
    RUN_BOARD[row_player][column_player] += BUILD_BOARD[row_player][column_player]
    show_board(RUN_BOARD, SIZE_BOARD, scores)
    choose = input("You want pick gold? [Y] to Yes and [N] to Not: ")
    if choose == "Y" or choose == "N":
        choose = choose.lower()
    while choose != "y" and choose != "n":
        print("Unrecognized command!")
        choose = input("You want pick gold? [y] to Yes and [n] to Not: ")
    if choose == "y":
        BUILD_BOARD[row_player][column_player] = BUILD_BOARD[row_player][column_player].replace(GOLD, EMPTY)
        RUN_BOARD[row_player][column_player] = RUN_BOARD[row_player][column_player].replace(GOLD, EMPTY)
        show_board(RUN_BOARD, SIZE_BOARD, scores)
        return True
    elif choose == "n":
        return False


def game_over(row_player, column_player, BUILD_BOARD, SIZE_BOARD):
    check = []
    for i in range(SIZE_BOARD):
        for j in range(SIZE_BOARD):
            if MONSTER in BUILD_BOARD[i][j]:
                if i == row_player and j == column_player:
                    check.append(1)
            elif BUILD_BOARD[i][j] == ABYSS:
                if i == row_player and j == column_player:
                    check.append(2)
    if 1 in check:
        return "monster"
    elif 2 in check:
        return "abyss"
    else:
        return ""


def feel_sensations(row_player, column_player, BUILD_BOARD, SIZE_BOARD):
    check = []
    tcheck = 0
    return_check = []
    for i in range(SIZE_BOARD):
        for j in range(SIZE_BOARD):
            if row_player == i and column_player == j:
                if STENCH in BUILD_BOARD[i][j] and BREEZE in BUILD_BOARD[i][j]:
                    check.append(1)
                    tcheck = 1
                elif STENCH in BUILD_BOARD[i][j]:
                    check.append(1)
                    tcheck = 2
                elif BREEZE in BUILD_BOARD[i][j]:
                    check.append(1)
                    tcheck = 3
    if 1 in check:
        return_check.append(True)
        if tcheck == 1:
            return_check.append("The player is facing breezes and stenches.")
        elif tcheck == 2:
            return_check.append("The player is facing stenches.")
        elif tcheck == 3:
            return_check.append("The player is facing breezes.")
    else:
        return_check.append(False)
    return return_check


def login():
    if not exists('nicknames.txt'):
        create = open("nicknames.txt", "w")
        create.close()
    choose_input = input("You want create new account? [Y] or [N]: ")
    if choose_input == "Y" or choose_input == "N":
        choose_input = choose_input.lower()
    while choose_input != "y" and choose_input != "n":
        clear_display()
        print("Unrecognized command!")
        choose_input = input("You want create new account? [Y] or [N] or [F] Exit Selection: ").lower()
        if choose_input == "f":
            sys.exit()
    if choose_input == "y":
        clear_display()
        create_nickname = input("Enter with the nickname wanted: ")
        read_file = open("nicknames.txt", "r")
        for i in read_file:
            i = i.split(" ")
            if i[0] == create_nickname:
                while create_nickname == i[0]:
                    create_nickname = input("The nickname exists! Choose other: ")
        read_file.close()
        create_password = input("Create your password: ")
        write_file = open("nicknames.txt", "a")
        content = create_nickname + " " + create_password
        write_file.write(content + " " + '\n')
        write_file.close()
    clear_display()
    nickname = input("Enter with your nickname: ")
    password = input("Enter with your password: ")

    read_file_check = open("nicknames.txt", "r")
    check_credentials = 0
    for i in read_file_check:
        row = i.split(" ")
        if (row[0] == nickname) and (row[1] == password):
            check_credentials = 1
    if check_credentials == 1:
        build_game(nickname, remapping_keys())
    else:
        print("Incorret nickname or password!")
        sys.exit()
    read_file_check.close()


clear_display()
message_init()
login()
