"""
Ward occupancy and infection wave analysis.

This module contains two main functions:
- calculate_ward_occupancy: compute daily occupancy from admissions and discharges
- analyze_infection_wave: identify the day of maximum increase and whether the peak has passed

A simple occupancy chart is included to generate a visually appealing graph.
"""

from typing import List, Dict


def calculate_ward_occupancy(admissions: List[int], discharges: List[int]) -> List[int]:
    """Return the number of patients on the ward for each day.

    The ward starts with zero patients.
    """
    if len(admissions) != 7 or len(discharges) != 7:
        raise ValueError("Both admissions and discharges lists must contain exactly 7 values.")

    occupancy: List[int] = []
    current_patients = 0
    for day, (admission, discharge) in enumerate(zip(admissions, discharges), start=1):
        current_patients += admission - discharge
        occupancy.append(current_patients)
        if current_patients < 0:
            raise ValueError(f"Occupancy cannot be negative on day {day}.")

    return occupancy


def plot_ward_occupancy(occupancy: List[int]) -> None:
    """Generate a line chart for ward occupancy over seven days."""
    try:
        import matplotlib.pyplot as plt
    except ImportError as exc:
        raise ImportError(
            "matplotlib is required to plot ward occupancy. "
            "Install it with 'pip install matplotlib'."
        ) from exc

    days = list(range(1, len(occupancy) + 1))
    plt.figure(figsize=(10, 6))
    plt.plot(days, occupancy, marker='o', linewidth=2, color='#1f77b4')
    plt.fill_between(days, occupancy, color='#1f77b4', alpha=0.15)
    plt.title('Hospital Ward Occupancy Over 7 Days', fontsize=16)
    plt.xlabel('Day', fontsize=12)
    plt.ylabel('Number of Patients', fontsize=12)
    plt.xticks(days)
    plt.grid(alpha=0.35)
    plt.tight_layout()
    plt.show()


def analyze_infection_wave(occupancy: List[int]) -> Dict[str, object]:
    """Return the day of greatest occupancy increase and whether the peak has passed."""
    if len(occupancy) != 7:
        raise ValueError("Occupancy data must contain exactly 7 daily values.")

    increases = [occupancy[0]]
    increases += [occupancy[i] - occupancy[i - 1] for i in range(1, len(occupancy))]

    max_increase = max(increases)
    max_increase_day = increases.index(max_increase) + 1

    peak_passed = max_increase_day < len(occupancy)
    status_message = (
        "The maximum daily increase has been reached and the infection wave peak has passed."
        if peak_passed
        else "The maximum daily increase occurs on the final day, so the infection wave peak is not yet reached."
    )

    return {
        'max_increase_day': max_increase_day,
        'max_increase_value': max_increase,
        'peak_passed': peak_passed,
        'status_message': status_message,
    }


if __name__ == '__main__':
    sample_admissions = [5, 8, 6, 12, 7, 9, 4]
    sample_discharges = [0, 2, 3, 5, 4, 6, 8]

    occupancy = calculate_ward_occupancy(sample_admissions, sample_discharges)
    print('Daily ward occupancy:', occupancy)

    analysis = analyze_infection_wave(occupancy)
    print(
        f"Greatest increase on day {analysis['max_increase_day']} with "
        f"{analysis['max_increase_value']} additional patients."
    )
    print(analysis['status_message'])

    plot_ward_occupancy(occupancy)
