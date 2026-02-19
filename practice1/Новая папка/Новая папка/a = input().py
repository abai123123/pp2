first = list(map(int, input().split()))
second = list(map(int, input().split()))
numbers = []
num = []
a = second[first[1] - 1]
b = second[first[2] - 1]
for i in range(first[1] , first[2] - 1):
    num.append(second[i])
reversed_num = num[::-1]
for i in range (len(num)):
    print(reversed_num[i] , end = " ")


for i in range(first[1] - 1):
    numbers.append(second[i])
for i in range (len(numbers)):
    print(numbers[i], end = " ")