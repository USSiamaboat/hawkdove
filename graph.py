"""
This module separates graphing from the main file. It serves no other purpose.
"""

import matplotlib.pyplot as plt
import numpy as np

def graph(variables, day_n, d_pops, h_pops, ratioss, variable_name="Variable"):
    """
    Generates the graphs describing a set of simulations
    Uses variables defined in the main file
    """

    for i in range(len(variables)):
        plt.plot(day_n, d_pops[i], color="blue", alpha=0.02)
        plt.plot(day_n, h_pops[i], color="red", alpha=0.02)

    plt.plot([0, 0], [0, 0], color="blue", label="doves true")
    plt.plot([0, 0], [0, 0], color="red", label="hawks true")

    plt.plot([0, 200],
        [750*0.75, 750*0.75],
        color="blue",
        label="doves expected",
        linestyle="dashed"
    )
    plt.plot([0, 200],
        [250*0.75, 250*0.75],
        color="red",
        label="hawks expected",
        linestyle="dashed"
    )

    plt.title(f"Population Size over Time with Varying {variable_name}")
    plt.xlabel("Day Number")
    plt.ylabel("Population Count")

    plt.ylim(0, 1000)

    plt.legend(loc="upper right")
    plt.show()


    for i in range(len(variables)):
        plt.plot(day_n, ratioss[i], color="green", alpha=0.02)

    plt.plot([0, 0], [0, 0], color="green", label="true")
    plt.plot([0, 200], [0.75, 0.75], color="green", linestyle="dashed", label="expected")

    plt.title(f"Dove Population Proportion with Varying {variable_name}")
    plt.xlabel("Day Number")
    plt.ylabel("Proportion Population Doves")

    plt.ylim(0, 1)

    plt.legend(loc="lower right")
    plt.show()


    last_100_d_means = []
    last_100_h_means = []
    last_100_r_means = []
    for i in range(len(variables)):
        last_100_d_means.append(np.mean(d_pops[i][-100:]))
        last_100_h_means.append(np.mean(h_pops[i][-100:]))
        last_100_r_means.append(np.mean(ratioss[i][-100:]))

    plt.plot(variables, last_100_d_means, label="doves", color="blue")
    plt.plot(variables, last_100_h_means, label="hawks", color="red")

    plt.title(f"Stable Population Sizes over {variable_name}")
    plt.xlabel(variable_name)
    plt.ylabel("Population")

    plt.ylim(0, 1000)

    plt.legend(loc="upper right")
    plt.show()

    plt.plot(variables, last_100_r_means, color="green")

    plt.title(f"Stable Dove Population Proportion over {variable_name}")
    plt.xlabel(variable_name)
    plt.ylabel("Proportion Population Doves")

    plt.ylim(0, 1)

    plt.show()
