import os
import numpy as np
import matplotlib.pyplot as plt


# Pseudocode:
# 1. Create a 100x100 grid with 0 = susceptible, 1 = infected, 2 = recovered.
# 2. Choose one random cell to be the first infected person.
# 3. For each time step:
#    a. Find all infected cells.
#    b. For each infected cell, check all 8 neighbours.
#    c. If a neighbour is susceptible, infect it with probability beta.
#    d. Allow each infected cell to recover with probability gamma.
#    e. Record the new grid state and optionally save a plot.


def simulate_spatial_sir(size=100, beta=0.3, gamma=0.05, time_steps=100):
    population = np.zeros((size, size), dtype=int)
    outbreak = np.random.choice(range(size), 2)
    population[outbreak[0], outbreak[1]] = 1

    neighbor_offsets = [
        (dy, dx)
        for dy in (-1, 0, 1)
        for dx in (-1, 0, 1)
        if not (dy == 0 and dx == 0)
    ]

    history = {
        "susceptible": [],
        "infected": [],
        "recovered": [],
    }

    snapshot_times = [0, 10, 20, 30, 40, 60, 80, 99]
    snapshot_images = []

    for t in range(time_steps):
        infected_yx = list(zip(*np.where(population == 1)))
        next_population = population.copy()

        for y, x in infected_yx:
            for dy, dx in neighbor_offsets:
                ny, nx = y + dy, x + dx
                if 0 <= ny < size and 0 <= nx < size:
                    if population[ny, nx] == 0 and np.random.random() < beta:
                        next_population[ny, nx] = 1

        for y, x in infected_yx:
            if np.random.random() < gamma:
                next_population[y, x] = 2

        population = next_population

        susceptible = np.sum(population == 0)
        infected = np.sum(population == 1)
        recovered = np.sum(population == 2)

        history["susceptible"].append(susceptible)
        history["infected"].append(infected)
        history["recovered"].append(recovered)

        if t in snapshot_times:
            snapshot_images.append((t, population.copy()))

    return population, history, outbreak, snapshot_images


def save_snapshots(snapshot_images, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for t, image in snapshot_images:
        filename = os.path.join(output_dir, f"spatial_SIR_t{t:03d}.png")
        plt.figure(figsize=(6, 5), dpi=150)
        plt.imshow(image, cmap="viridis", interpolation="nearest")
        plt.title(f"Spatial SIR at time step {t}")
        plt.xlabel("X")
        plt.ylabel("Y")
        plt.colorbar(ticks=[0, 1, 2], label="State")
        plt.clim(-0.5, 2.5)
        plt.tight_layout()
        plt.savefig(filename)
        plt.close()
        print(f"Saved snapshot {filename}")


if __name__ == "__main__":
    np.random.seed()
    size = 100
    beta = 0.3
    gamma = 0.05
    time_steps = 100

    population, history, outbreak, snapshots = simulate_spatial_sir(
        size=size, beta=beta, gamma=gamma, time_steps=time_steps
    )

    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spatial_SIR_snapshots")
    save_snapshots(snapshots, output_dir)

    plt.figure(figsize=(7, 4), dpi=150)
    plt.plot(history["susceptible"], label="Susceptible", color="tab:blue")
    plt.plot(history["infected"], label="Infected", color="tab:red")
    plt.plot(history["recovered"], label="Recovered", color="tab:green")
    plt.xlabel("Time step")
    plt.ylabel("Cell count")
    plt.title("Spatial SIR counts over time")
    plt.legend()
    plt.tight_layout()

    counts_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spatial_SIR_counts.png")
    plt.savefig(counts_path)
    plt.close()
    print(f"Saved count plot to {counts_path}")
    print(f"Outbreak started at cell {tuple(outbreak)}")
