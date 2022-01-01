import matplotlib.pyplot as plt

import random as rd
import math

array_size = 2 ** 7

def linear_interpolation(input_values, plot_nombre, axes):
    precedent = 0
    dist_precedent = 0
    output_values = [None for i in input_values]
    for val, i in zip(input_values, range(len(input_values))):
        if not (val == None):
            precedent = val
            output_values[i] = val
            dist_precedent = 0
        else:
            dist_precedent += 1
            next_val, dist = calculate_distance(input_values, i)
            calculated = (precedent * dist + next_val * dist_precedent) / (dist + dist_precedent)
            output_values[i] = calculated
    axes[plot_nombre].plot(list(range(len(output_values))), output_values)
    axes[plot_nombre].set_title(f"Plot nbre {plot_nombre}")
    return output_values

def calculate_distance(input_list, start):
    for val, dist in zip(input_list[start:], range(len(input_list[start:]))):
        if val != None: return val, dist
    return 0, 0

def perlin():

    plot_nbre = 1

    seed_array = [rd.random() for i in range(array_size)]
    current_array = seed_array
    next_array = [None for i in range(array_size)]

    fig, axes = plt.subplots(3 + int(math.log2(array_size)))
    axes[0].plot(list(range(array_size)), seed_array, "bo")
    axes[0].set_title("Seed array")

    sample = 2
    weight = 1
    weight_sum = 0
    for i in range(int(math.log2(array_size))):
        weight_sum += weight
        for x in range(sample):
            index = int((x * (array_size / sample)) % array_size)
            next_array[index] = current_array[index] + seed_array[index] * weight
        next_array[-1] = next_array[0]
        current_array = linear_interpolation(next_array, plot_nbre, axes)
        plot_nbre += 1
        sample *= 2
        weight /= 2
        next_array = [None for i in range(array_size)]
    weight_sum += weight
    print(weight_sum)

    axes[-2].plot(list(range(array_size)), current_array, "r-")
    axes[-2].set_title("Before averaging")
    for i in range(len(current_array)):
        current_array[i] /= weight_sum

    axes[-1].plot(list(range(array_size)), current_array, "r-")
    axes[-1].set_title("Final result")
    plt.show()

perlin()