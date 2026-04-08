#Predict protein mass from an amino acid sequence

RESIDUE_MASSES = {
    'G': 57.02,
    'A': 71.04,
    'S': 87.03,
    'P': 97.05,
    'V': 99.07,
    'T': 101.05,
    'C': 103.01,
    'I': 113.08,
    'L': 113.08,
    'N': 114.04,
    'D': 115.03,
    'Q': 128.06,
    'K': 128.09,
    'E': 129.04,
    'M': 131.04,
    'H': 137.06,
    'F': 147.07,
    'R': 156.10,
    'Y': 163.06,
    'W': 186.08,
}


def protein_mass(sequence):
    #Return the total mass of a protein sequence in atomic mass units (amu).
    total_mass = 0.0
    for residue in sequence:
        residue = residue.upper()
        if residue not in RESIDUE_MASSES:
            raise ValueError(f"Unknown amino acid symbol: '{residue}'")
        total_mass += RESIDUE_MASSES[residue]
    return total_mass


if __name__ == '__main__':
    example_sequence = 'ACDEFGHIKLMNPQRSTVWY'
    print('Example sequence:', example_sequence)
    print('Predicted mass (amu):', protein_mass(example_sequence))
