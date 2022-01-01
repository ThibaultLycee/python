for a, b in zip('abcdefghijklmnopqrstuvwxyz', range(1, 27)):
    print(f'\'{a}\': \'\\{hex(b)[1:]}\'')
