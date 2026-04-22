import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm


def run_sir_with_vaccination(N, vaccinated_percent, beta=0.3, gamma=0.05, time_steps=1000):
    vaccinated = min(int(round(N * vaccinated_percent / 100)), N - 1)
    susceptible = N - vaccinated - 1
    infected = 1
    recovered = vaccinated

    I_history = [infected]

    for _ in range(time_steps):
        p_infection = beta * infected / N if infected > 0 else 0.0

        if susceptible > 0 and p_infection > 0:
            new_infections = np.sum(
                np.random.choice([0, 1], size=susceptible, p=[1 - p_infection, p_infection])
            )
        else:
            new_infections = 0

        if infected > 0:
            new_recoveries = np.sum(
                np.random.choice([0, 1], size=infected, p=[1 - gamma, gamma])
            )
        else:
            new_recoveries = 0

        new_infections = min(new_infections, susceptible)
        new_recoveries = min(new_recoveries, infected)

        susceptible -= new_infections
        infected += new_infections - new_recoveries
        recovered += new_recoveries

        I_history.append(infected)

    return np.array(I_history)


if __name__ == "__main__":
    N = 10000
    beta = 0.3
    gamma = 0.05
    time_steps = 1000
    vaccination_levels = list(range(0, 101, 10))

    time = np.arange(time_steps + 1)
    plt.figure(figsize=(8, 5), dpi=150)

    for i, level in enumerate(vaccination_levels):
        infected_curve = run_sir_with_vaccination(
            N=N, vaccinated_percent=level, beta=beta, gamma=gamma, time_steps=time_steps
        )
        color = plt.cm.viridis(i / (len(vaccination_levels) - 1)) # type: ignore
        plt.plot(time, infected_curve, label=f"{level}% vaccinated", color=color)

    plt.xlabel("Time step")
    plt.ylabel("Number of infected people")
    plt.title("SIR model with vaccination levels")
    plt.legend(loc="upper right", fontsize="small", ncol=2)
    plt.tight_layout()

    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "SIR_vaccination_plot.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved vaccination SIR plot to {output_path}")
