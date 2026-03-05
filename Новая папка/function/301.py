list = list(map(int,  input().split()))
a = "Not valid"
x = []
def func(list , x , a):
    for i in range(len(list)):
        if list[i] % 2 == 0:
            x.append(i)
        else:
            return(a)
            break
if  len(list) == len(x):
     print("Valid")
else:
    print(func(list, x , a))