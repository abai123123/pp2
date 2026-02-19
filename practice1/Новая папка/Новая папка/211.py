a = int(input())
numbers = list(map(int, input().split()))
n = []
for i in range (a):
    c = 0
    for g in range(a):
        if numbers[i] == numbers[g]:
            a += 1
    n.append(a)
print(n)