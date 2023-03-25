# Imports
import math
import matplotlib.pyplot as plt
import numpy as np
import random
import seaborn as sns
from tqdm import tqdm

# Import internal modules
from game import Game
from graph import graph

# ===================================================

# Varying games randomly

# ===================================================

# Generate data
day_n = np.arange(1, 200)

variables = np.linspace(0, 1, 100)
d_pops = []
h_pops = []
ratioss = []

for i in tqdm(variables):
    a = Game(1000, random.random(), 1000, random.random()*10)

    d_pop = []
    h_pop = []
    ratios = []

    for n in day_n:
        d_pop.append(a.doves)
        h_pop.append(a.hawks)
        ratios.append(a.doves/max(0.0001, a.doves + a.hawks))
        a.day()
    
    d_pops.append(d_pop)
    h_pops.append(h_pop)
    ratioss.append(ratios)

# Graph
graph(variables, day_n, d_pops, h_pops, ratioss, variable_name="Initial Parameters")

# ===================================================

# Varying starting proportions

# ===================================================

# Generate data
day_n = np.arange(1, 200)

variables = np.linspace(0, 1, 100)
d_pops = []
h_pops = []
ratioss = []

for i in tqdm(variables):
    a = Game(1000, i, 1000, 0.5)

    d_pop = []
    h_pop = []
    ratios = []

    for n in day_n:
        d_pop.append(a.doves)
        h_pop.append(a.hawks)
        ratios.append(a.doves/max(0.0001, a.doves + a.hawks))
        a.day()
    
    d_pops.append(d_pop)
    h_pops.append(h_pop)
    ratioss.append(ratios)

# Graph
graph(variables, day_n, d_pops, h_pops, ratioss, variable_name="Starting Proportions")

# ===================================================

# Varying growth rates

# ===================================================

# Generate data
day_n = np.arange(1, 200)

d_pops = []
h_pops = []
ratioss = []

variables = np.linspace(0, 10, 100)

for i in tqdm(variables):
    a = Game(1000, 0.75, 1000, i)

    d_pop = []
    h_pop = []
    ratios = []

    for n in day_n:
        d_pop.append(a.doves)
        h_pop.append(a.hawks)
        ratios.append(a.doves/max(0.0001, a.doves + a.hawks))
        a.day()
    
    d_pops.append(d_pop)
    h_pops.append(h_pop)
    ratioss.append(ratios)

# Graph
graph(variables, day_n, d_pops, h_pops, ratioss, variable_name="Growth Rates")

# ===================================================

# Varying both starting proportions and growth rates

# ===================================================

# Generate data
proportions = np.linspace(0, 1, 30)
growth_rates = np.linspace(0, 3, 90)

averages = np.zeros((30, 90))

n_iters = 30

for i, proportion in tqdm(enumerate(proportions)):
    for j, growth_rate in enumerate(growth_rates):
        current_sum = 0
        for k in range(n_iters):
            a = Game(1000, proportion, 1000, growth_rate)
            for _ in range(100):
                a.day()
            
            s = 0
            for _ in range(100):
                a.day()
                s += a.hawks

            if s/100 > 100:
                current_sum += 1
        averages[i][j] = current_sum/n_iters

# Label helper function
def format_labels(labels):
    return [f"{label:.3f}" for label in labels]

# Graph
n_xticks = 20
n_yticks = 20

xticks = np.linspace(0, len(growth_rates), n_xticks)
xticklabels = growth_rates[0] + ((growth_rates[-1] - growth_rates[0])/len(growth_rates))*xticks

yticks = np.linspace(0, len(proportions), n_yticks)
yticklabels = proportions[0] + ((proportions[-1] - proportions[0])/len(proportions))*yticks

plot = sns.heatmap(averages, cbar_kws={'label': '\nCommunity Establishment Rate'})

plt.xticks(rotation=90)
plt.yticks(rotation=0)

plot.set_xticks(xticks, format_labels(xticklabels))
plot.set_yticks(yticks, format_labels(yticklabels))

plt.title("2-Bird Community Establishment over Community Parameters\n", size=14)
plt.xlabel("\nGrowth Rates", size=12)
plt.ylabel("Starting Proportion Doves\n", size=12)

plt.show()
w