def environ(a, b, c):
    return abs(a-b) < c

for i in range(2, 10000):
    print(169/i)
    print(275/i)
    if environ(169/i, 275/i, 2):
        print(i)
        break
    print('==========')