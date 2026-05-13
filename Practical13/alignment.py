import sys
from pathlib import Path
from typing import Tuple, Dict

BLOSUM62_TEXT = '''   A  R  N  D  C  Q  E  G  H  I  L  K  M  F  P  S  T  W  Y  V
A  4 -1 -2 -2  0 -1 -1  0 -2 -1 -1 -1 -1 -2 -1  1  0 -3 -2  0
R -1  5  0 -2 -3  1  0 -2  0 -3 -2  2 -1 -3 -2 -1 -1 -3 -2 -3
N -2  0  6  1 -3  0  0  0  1 -3 -3  0 -2 -3 -2  1  0 -4 -2 -3
D -2 -2  1  6 -3  0  2 -1 -1 -3 -4 -1 -3 -3 -1  0 -1 -4 -3 -3
C  0 -3 -3 -3  9 -3 -4 -3 -3 -1 -1 -3 -1 -2 -3 -1 -1 -2 -2 -1
Q -1  1  0  0 -3  5  2 -2  0 -3 -2  1  0 -3 -1  0 -1 -2 -1 -2
E -1  0  0  2 -4  2  5 -2  0 -3 -3  1 -2 -3 -1  0 -1 -3 -2 -2
G  0 -2  0 -1 -3 -2 -2  6 -2 -4 -4 -2 -3 -3 -2  0 -2 -2 -3 -3
H -2  0  1 -1 -3  0  0 -2  8 -3 -3 -1 -2 -1 -2 -1 -2 -2  2 -3
I -1 -3 -3 -3 -1 -3 -3 -4 -3  4  2 -3  1  0 -3 -2 -1 -3 -1  3
L -1 -2 -3 -4 -1 -2 -3 -4 -3  2  4 -2  2  0 -3 -2 -1 -2 -1  1
K -1  2  0 -1 -3  1  1 -2 -1 -3 -2  5 -1 -3 -1  0 -1 -3 -2 -2
M -1 -1 -2 -3 -1  0 -2 -3 -2  1  2 -1  5  0 -2 -1 -1 -1 -1  1
F -2 -3 -3 -3 -2 -3 -3 -3 -1  0  0 -3  0  6 -4 -2 -2  1  3 -1
P -1 -2 -2 -1 -3 -1 -1 -2 -2 -3 -3 -1 -2 -4  7 -1 -1 -4 -3 -2
S  1 -1  1  0 -1  0  0  0 -1 -2 -2  0 -1 -2 -1  4  1 -3 -2 -2
T  0 -1  0 -1 -1 -1 -1 -2 -2 -1 -1 -1 -1 -2 -1  1  5 -2 -2  0
W -3 -3 -4 -4 -2 -2 -3 -2 -2 -3 -2 -3 -1  1 -4 -3 -2 11  2 -3
Y -2 -2 -2 -3 -2 -1 -2 -3  2 -1 -1 -2 -1  3 -3 -2 -2  2  7 -1
V  0 -3 -3 -3 -1 -2 -2 -3 -3  3  1 -2  1 -1 -2 -2  0 -3 -1  4
'''


def parse_blosum(text: str) -> Dict[str, Dict[str, int]]:
    lines = [l.strip() for l in text.strip().splitlines() if l.strip()]
    headers = lines[0].split()
    matrix = {}
    for row in lines[1:]:
        parts = row.split()
        row_aa = parts[0]
        scores = list(map(int, parts[1:]))
        matrix[row_aa] = {col_aa: score for col_aa, score in zip(headers, scores)}
    return matrix


def read_fasta(path: Path) -> Tuple[str, str]:
    header = ''
    seq_lines = []
    with path.open('r') as fh:
        for line in fh:
            line = line.rstrip('\n')
            if not line:
                continue
            if line.startswith('>'):
                if not header:
                    header = line[1:].strip()
                else:
                    # multiple records - stop at first
                    break
            else:
                seq_lines.append(line.strip())
    seq = ''.join(seq_lines).upper()
    return header or path.name, seq


def compare_seqs(s1: str, s2: str, blosum: Dict[str, Dict[str, int]]) -> Tuple[int, float, int]:
    n = min(len(s1), len(s2))
    score = 0
    identical = 0
    for i in range(n):
        a = s1[i]
        b = s2[i]
        if a == b:
            identical += 1
        if a in blosum and b in blosum[a]:
            score += blosum[a][b]
        else:
            # unknown residue: penalize slightly
            score -= 1
    pct_id = (identical / n * 100) if n > 0 else 0.0
    return score, pct_id, n


def run_pairwise(file1: Path, file2: Path, blosum: Dict[str, Dict[str, int]]):
    h1, s1 = read_fasta(file1)
    h2, s2 = read_fasta(file2)
    score, pct_id, comp_len = compare_seqs(s1, s2, blosum)
    print('---')
    print(f'File1: {file1.name} ({h1})')
    print(f'File2: {file2.name} ({h2})')
    print(f'Compared length: {comp_len}')
    print(f'Alignment score (BLOSUM62): {score}')
    print(f'Percentage identity: {pct_id:.2f}%')
    print(f'{file1.name} length: {len(s1)}, {file2.name} length: {len(s2)}')
    print('')


def main():
    blosum = parse_blosum(BLOSUM62_TEXT)
    p = Path(__file__).parent
    # default fasta files in this folder
    fasta_candidates = [p / 'P56178.fasta', p / 'P70396.fasta', p / 'random protein sequence.fasta']
    fasta_existing = [f for f in fasta_candidates if f.exists()]

    if len(sys.argv) == 3:
        f1 = Path(sys.argv[1])
        f2 = Path(sys.argv[2])
        if not f1.exists() or not f2.exists():
            print('One of the provided files does not exist.')
            sys.exit(1)
        run_pairwise(f1, f2, blosum)
        return

    if len(fasta_existing) >= 2:
        # run all pairwise combinations among existing files
        from itertools import combinations
        for a, b in combinations(fasta_existing, 2):
            run_pairwise(a, b, blosum)
    else:
        print('Not enough FASTA files found in Practical13 to run comparisons.')


if __name__ == '__main__':
    main()
