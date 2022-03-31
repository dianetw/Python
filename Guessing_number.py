#
# Author: Diane
# Create on: 2022/3/31
#

import random

ans = random.choice(range(1, 100+1))

game = True
hint = ["Higher", "Lower"]
while game:
    n = int(input("Please enter a number in range 1 to 100:"))

    if n < 1 or n > 100:
        print("\n============================")
        print("Number must in range 1 to 100")
        print("============================\n")

    if n > ans:
        print(f"Hint: {hint[1]}")
    elif n < ans:
        print(f"Hint: {hint[0]}")
    else:
        print(f"Congratulations! The correct number is: {ans}")
        game = False
