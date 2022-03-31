#
# Author: Diane
# Create on: 2022/3/30
#

import random

mora_dict = {
    "player": {0: "玩家", 1: "電腦"},
    "mora": {1: "剪刀", 2: "石頭", 3: "布"}
}
tries = 1
winner, win_count, lost_count, draw_count = 0, 0, 0, 0
status = ""
print("猜拳遊戲")
print("請輸入[1]剪刀 [2]石頭 [3]布 [q]退出遊戲")
game = True
while game:
    print(f"第{tries}輪遊戲開始")
    user = input("玩家請出拳[1]剪刀 [2]石頭 [3]布: ")
    if user in ['q', '1', '2', '3']:
        if user == 'q':
            game = False
        else:
            user = int(user)
            computer = random.choice(range(1,3+1))
            print(mora_dict["player"][0],":", mora_dict["mora"][user])
            print(mora_dict["player"][1],":", mora_dict["mora"][computer])
            if ((user > computer) - (user < computer) == 0): # cmp()
                draw_count += 1
                status = "平手"
            elif user > computer or (user == 1 and computer == 3):
                win_count += 1
                status = f"第{tries}輪, 玩家獲勝"
            elif computer > user or (computer == 1 and user == 3):
                lost_count += 1
                status = f"第{tries}輪, 電腦獲勝"
            print(status)
            print(f"目前戰績: 玩家{win_count}勝、電腦{lost_count}勝、平手{draw_count}次")
            if win_count == 3 or lost_count == 3:
                game = False
            tries += 1
            print("*" * 40)
    else:
        print("請輸入1-3猜拳,或者輸入q退出遊戲\n")

if win_count == 3:
    winner = 0
elif lost_count == 3:
    winner = 1
if user != 'q':
    print("遊戲結束, 贏家為", mora_dict["player"][winner]) 
