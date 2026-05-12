import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm, ListedColormap
from matplotlib.patches import Patch


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

    snapshot_times = [0, 10, 20, 30, 40, 50, 60, 70, 80, 100]
    snapshot_images = []

    susceptible = np.sum(population == 0)
    infected = np.sum(population == 1)
    recovered = np.sum(population == 2)

    history["susceptible"].append(susceptible)
    history["infected"].append(infected)
    history["recovered"].append(recovered)

    if 0 in snapshot_times:
        snapshot_images.append((0, population.copy()))

    for t in range(1, time_steps + 1):
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


def save_snapshots(snapshot_images, output_path):
    state_cmap = ListedColormap(["#edf2f7", "#f4a261", "#2a9d8f"])
    state_norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5], state_cmap.N)
    state_legend = [
        Patch(facecolor="#edf2f7", edgecolor="#4a5568", label="Susceptible (0)"),
        Patch(facecolor="#f4a261", edgecolor="#4a5568", label="Infected (1)"),
        Patch(facecolor="#2a9d8f", edgecolor="black", label="Recovered (2)"),
    ]

    total_snapshots = len(snapshot_images)
    cols = 5
    rows = int(np.ceil(total_snapshots / cols))

    fig, axes = plt.subplots(rows, cols, figsize=(18, 8), dpi=150)
    axes = np.array(axes).reshape(-1)

    for axis, (t, image) in zip(axes, snapshot_images):
        axis.imshow(image, cmap=state_cmap, norm=state_norm, interpolation="nearest")
        axis.set_title(f"t = {t}")
        axis.set_xticks([])
        axis.set_yticks([])

    for axis in axes[total_snapshots:]:
        axis.axis("off")

    fig.suptitle("Spatial SIR snapshots over time", fontsize=16, fontweight="bold")
    fig.legend(
        handles=state_legend,
        loc="lower center",
        ncol=3,
        frameon=False,
        bbox_to_anchor=(0.5, 0.01),
    )

    fig.subplots_adjust(left=0.03, right=0.97, top=0.90, bottom=0.14, wspace=0.05, hspace=0.35)
    fig.savefig(output_path)
    plt.close(fig)
    print(f"Saved combined snapshot figure to {output_path}")


if __name__ == "__main__":
    np.random.seed()
    size = 100
    beta = 0.3
    gamma = 0.05
    time_steps = 100

    population, history, outbreak, snapshots = simulate_spatial_sir(
        size=size, beta=beta, gamma=gamma, time_steps=time_steps
    )

    output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "spatial_SIR_snapshots.png")
    save_snapshots(snapshots, output_path)

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
