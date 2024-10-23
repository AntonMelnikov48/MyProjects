def start():    
    y1 = [' ', ' ', ' ']
    y2 = [' ', ' ', ' ']
    y3 = [' ', ' ', ' ']

    cnt = 1
    condition = True
    play = True
    def playing_field():
        print('  ', 'a', 'b', 'c')
        print(' ', '——————')
        print('1|', *y1)
        print('2|', *y2)
        print('3|', *y3)

    def changing(x, y, sym):
        
        if x == 'a':
            x = 0
        elif x == "b":
            x = 1
        elif x == "c":
            x = 2
        
        if y == 1:
            y1[x] = sym
            
        elif y == 2:
            y2[x] = sym
            
        elif y == 3:
            y3[x] = sym
        playing_field()  



    import random

    print('Добро пожаловать в игру "Х & O"')  
    players = []
    name_1 = input('Игрок №1, введите имя: ')
    name_2 = input('Игрок №2, введите имя: ')
    players.append(name_1)
    players.append(name_2)

    player_1 = random.choice(players)
    print(player_1, '- X')
    del players[players.index(player_1)]
    player_2 = players[0]
    print(player_2, '- O')
    input('Нажмите <-ENTER->, чтобы начать игру...')
    print("НАЧАЛИ!")

    playing_field()
    closed_cells = []
    def motion():
        if cnt % 2 == 0:
            x_o = "O"
            print("Ходит", player_2, "(O)")
        else:
            x_o = "X"
            print("Ходит", player_1, "(X)")
        
        
        while condition == True:
            choice = input("Введите ячейку (Например: a1, b2, d3, ...): ")
            if choice in closed_cells:
                print("Эта ячейка занята!")
            else:    
                if (len(choice)==2) and (choice[0] in "abc") and (choice[1] in '123')  :
                    closed_cells.append(choice)
                    break    
                else:
                    print("Введена не корректная ячейка, попробуйте снова")

        changing(choice[0], int(choice[1]), x_o)


    while play == True:
        motion()
        cnt+=1
        if (y1[0] == y1[1] == y1[2] == "X") or (y2[0] == y2[1] == y2[2] == "X") or (y3[0] == y3[1] == y3[2] == "X") or (y1[0] == y2[0] == y3[0] == "X") or (y1[1] == y2[1] == y3[1] == "X") or (y1[2] == y2[2] == y3[2] == "X") or (y1[0] == y2[1] == y3[2] == "X") or (y1[2] == y2[1] == y3[0] == "X"):
            print('Игра окончена!')
            print("Поздравляю, ", player_1, ", Вы выиграли!", sep='' )
            break
        elif (y1[0] == y1[1] == y1[2] == "O") or (y2[0] == y2[1] == y2[2] == "O") or (y3[0] == y3[1] == y3[2] == "O") or (y1[0] == y2[0] == y3[0] == "O") or (y1[1] == y2[1] == y3[1] == "O") or (y1[2] == y2[2] == y3[2] == "O") or (y1[0] == y2[1] == y3[2] == "O") or (y1[2] == y2[1] == y3[0] == "O"):
            print('Игра окончена!')
            print("Поздравляю, ", player_2, ", Вы выиграли!", sep='' )
            break
        elif cnt == 9:
            print('Победила дружба :)')
            break

start()

while True:  
    question = input("Хотите сыграть ещё раз? ('y' - ДА | 'n' - НЕТ): ")    
    if question == 'y':
        input('Нажмите <-ENTER->, чтобы начать новую игру...')
        start()
    elif question == 'n':
        print('Спасибо за игру и до новых встреч!')
        input('Нажмите <-ENTER->, чтобы выйти из игры...')
        break