import os
import numpy as np
import matplotlib.pyplot as plt


def run_sir_simulation(N=10000, infected0=1, beta=0.3, gamma=0.05, time_steps=1000):
    susceptible = N - infected0
    infected = infected0
    recovered = 0

    S_history = [susceptible]
    I_history = [infected]
    R_history = [recovered]

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

        S_history.append(susceptible)
        I_history.append(infected)
        R_history.append(recovered)

    return np.array(S_history), np.array(I_history), np.array(R_history)


if __name__ == "__main__":
    N = 10000
    beta = 0.3
    gamma = 0.05
    time_steps = 1000

    S_history, I_history, R_history = run_sir_simulation(
        N=N, infected0=1, beta=beta, gamma=gamma, time_steps=time_steps
    )

    time = np.arange(len(S_history))

    plt.figure(figsize=(6, 4), dpi=150)
    plt.plot(time, S_history, label="Susceptible", color="tab:blue")
    plt.plot(time, I_history, label="Infected", color="tab:red")
    plt.plot(time, R_history, label="Recovered", color="tab:green")
    plt.xlabel("Time step")
    plt.ylabel("Number of people")
    plt.title("Stochastic SIR model")
    plt.legend()
    plt.tight_layout()

    output_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(output_dir, "SIR_plot.png")
    plt.savefig(output_path)
    plt.close()
    print(f"Saved SIR plot to {output_path}")
