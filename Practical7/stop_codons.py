from pathlib import Path


def parse_fasta(filename):
    """Parse a FASTA file and yield gene name, sequence tuples."""
    with open(filename, 'r') as f:
        gene_name = None
        sequence = []
        
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                # If we have a previous sequence, yield it
                if gene_name is not None:
                    yield gene_name, ''.join(sequence)
                # Parse new header to get gene name
                # Format: >YBR024W_mRNA cdna chromosome:...
                header_parts = line[1:].split()
                gene_name = header_parts[0]  # Extract gene identifier
                sequence = []
            else:
                sequence.append(line)
        
        # Don't forget the last sequence
        if gene_name is not None:
            yield gene_name, ''.join(sequence)


def find_stop_codons_in_frame(sequence):
    """
    Find in-frame stop codons in a sequence.
    In-frame means the stop codon is part of the same reading frame as ATG.
    Returns a sorted list of stop codons found, or None if no ATG or no stops found.
    """
    stop_codons = {'TAA', 'TAG', 'TGA'}
    found_stops = set()
    
    # Find ATG (start codon)
    atg_index = sequence.find('ATG')
    
    if atg_index == -1:
        # No start codon found
        return None
    
    # Look for stop codons in-frame from the ATG
    # Starting from ATG, read codons in frame (every 3 nucleotides)
    i = atg_index
    while i + 3 <= len(sequence):
        codon = sequence[i:i+3]
        if codon in stop_codons:
            found_stops.add(codon)
        i += 3
    
    return sorted(list(found_stops)) if found_stops else None


def main():
    script_dir = Path(__file__).resolve().parent
    input_file = script_dir / 'Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa'
    output_file = script_dir / 'stop_genes.fa'
    
    genes_with_stops = []
    
    print(f"Reading sequences from {input_file}...")
    
    for gene_name, sequence in parse_fasta(input_file):
        stop_codons = find_stop_codons_in_frame(sequence)
        
        if stop_codons:
            genes_with_stops.append((gene_name, sequence, stop_codons))
    
    # Write output
    print(f"Writing results to {output_file}...")
    with open(output_file, 'w') as f:
        for gene_name, sequence, stop_codons in genes_with_stops:
            # Header: gene name and stop codons found
            stops_str = ', '.join(stop_codons)
            f.write(f'>{gene_name} {stops_str}\n')
            
            # Write sequence in 60-character lines (FASTA standard)
            for i in range(0, len(sequence), 60):
                f.write(sequence[i:i+60] + '\n')
    
    print(f"\nResults:")
    print(f"Found {len(genes_with_stops)} genes with in-frame stop codons")
    print(f"Output written to {output_file}")
    
    # Print summary of stop codon usage
    stop_usage = {}
    for gene_name, sequence, stop_codons in genes_with_stops:
        for stop in stop_codons:
            stop_usage[stop] = stop_usage.get(stop, 0) + 1
    
    print("\nStop codon usage summary:")
    for stop in sorted(stop_usage.keys()):
        print(f"  {stop}: {stop_usage[stop]} genes")


if __name__ == '__main__':
    main()
