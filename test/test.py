import re
g = input()
match = re.findall("\b\[0-9]+[0-9]\b" , g)
for i in range(len(match)):
    print(match[i] , "\n")