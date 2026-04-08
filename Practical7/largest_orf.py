# Find the largest Open Reading Frame (ORF) in an mRNA sequence
seq = 'AAGAUACAUGCAAGUGGUGUGUCUGUUCUGAGAGGGCCUAAAAG'

start_codon = 'AUG'
stop_codons = {'UAA', 'UAG', 'UGA'}
max_orf_length = 0
max_orf_seq = ''

for i in range(len(seq) - 2):
    # Look for start codon
    if seq[i:i+3] == start_codon:
        # Scan in-frame for stop codon
        for j in range(i+3, len(seq)-2, 3):
            codon = seq[j:j+3]
            if codon in stop_codons:
                orf_length = j + 3 - i
                if orf_length > max_orf_length:
                    max_orf_length = orf_length
                    max_orf_seq = seq[i:j+3]
                break

print(f"The largest ORF is {max_orf_length} nucleotides long.")
if max_orf_seq:
    print(f"ORF sequence: {max_orf_seq}")
else:
    print("No ORF found.")
