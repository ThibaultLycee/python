import matplotlib.pyplot as plt
import math


abscisse = [i for i in range(181)]
ord1 = [(90 - i) / 90 for i in range(181)]
ord2 = [math.cos(i*2*math.pi/360) for i in range(181)]

plt.plot(abscisse, ord1, 'r-')
plt.plot(abscisse, ord2, 'b-')
plt.show()