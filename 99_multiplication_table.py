#
# Author: Diane
# Create on: 2022/3/21
#

# print multiplication table of 99
nums = range(1, 99+1)
for x in nums:
    for y in nums:
        total = x * y
        print(f"{x} x {y} = {total}")
    print("=" * 15)