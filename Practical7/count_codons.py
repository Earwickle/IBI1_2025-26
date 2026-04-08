import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
from collections import defaultdict
from pathlib import Path


def parse_fasta(filename):
    """Parse a FASTA file and yield gene name, sequence tuples."""
    with open(filename, 'r') as f:
        gene_name = None
        sequence = []
        
        for line in f:
            line = line.strip()
            if line.startswith('>'):
                if gene_name is not None:
                    yield gene_name, ''.join(sequence)
                header_parts = line[1:].split()
                gene_name = header_parts[0]
                sequence = []
            else:
                sequence.append(line)
        
        if gene_name is not None:
            yield gene_name, ''.join(sequence)


def find_longest_orf_with_stop(sequence, stop_codon):
    """
    Find the longest ORF ending with the specified stop codon.
    Returns a list of codons (including the stop codon) or None.
    """
    atg_index = sequence.find('ATG')
    
    if atg_index == -1:
        return None
    
    longest_orf = None
    
    # Look for all instances of the stop codon in-frame from ATG
    i = atg_index
    while i + 3 <= len(sequence):
        codon = sequence[i:i+3]
        
        if codon == stop_codon:
            # Found a stop codon, extract the ORF
            orf = []
            j = atg_index
            while j <= i:
                orf.append(sequence[j:j+3])
                j += 3
            
            # Keep the longest ORF
            if longest_orf is None or len(orf) > len(longest_orf):
                longest_orf = orf
        
        i += 3
    
    return longest_orf


def count_codons_for_stop(input_file, stop_codon):
    """
    Count all in-frame codons upstream of the specified stop codon.
    Returns a dictionary of codon counts.
    """
    codon_counts = defaultdict(int)
    genes_processed = 0
    genes_with_stop = 0
    
    print(f"\nAnalyzing genes with stop codon: {stop_codon}")
    print("=" * 50)
    
    for gene_name, sequence in parse_fasta(input_file):
        genes_processed += 1
        
        orf = find_longest_orf_with_stop(sequence, stop_codon)
        
        if orf:
            genes_with_stop += 1
            # Count all codons including the stop codon
            for codon in orf:
                codon_counts[codon] += 1
    
    print(f"Total genes processed: {genes_processed}")
    print(f"Genes with {stop_codon} stop codon: {genes_with_stop}")
    print(f"Total codons counted: {sum(codon_counts.values())}")
    
    return codon_counts


def create_pie_chart(codon_counts, stop_codon, output_file):
    """
    Create and save a pie chart of codon distribution.
    Shows top 15 codons, with remaining codons grouped as 'Other'.
    Uses ocean-themed color palette.
    """
    if not codon_counts:
        print(f"No data to create pie chart for {stop_codon}")
        return
    
    # Sort by count and get top 15
    sorted_by_count = sorted(codon_counts.items(), key=lambda x: x[1], reverse=True)
    top_15 = sorted_by_count[:15]
    others = sorted_by_count[15:]
    
    # Prepare data for pie chart
    labels = [codon for codon, _ in top_15]
    counts = [count for _, count in top_15]
    
    # Add "Other" category if there are remaining codons
    if others:
        other_count = sum(count for _, count in others)
        labels.append('Other')
        counts.append(other_count)
    
    # Ocean-themed color palette (Haiyangqingfeng style)
    ocean_colors = [
        '#BFEDF2',  # Light cyan
        '#51999F',  # Teal
        '#4D8BA4',  # Steel blue
        '#7BC0CD',  # Light blue
        '#DBCB92',  # Light gold
        '#ECB66C',  # Warm gold
        '#EAA958',  # Orange-gold
        '#ED8D7D',  # Coral
        '#548AA3',  # Deep blue
        '#A3D5E1',  # Sky blue
        '#B8D4DC',  # Light steel
        '#C5B99A',  # Beige
        '#D4A574',  # Light tan
        '#DA9465',  # Peach
        '#DF7E6B',  # Coral orange
        '#999999'   # Gray for "Other"
    ]
    
    # Ensure we have enough colors
    while len(ocean_colors) < len(labels):
        ocean_colors.extend(ocean_colors)
    
    colors = ocean_colors[:len(labels)]
    
    # Create figure
    fig, ax = plt.subplots(figsize=(14, 10))
    
    # Create pie chart
    wedges, texts, autotexts = ax.pie(counts, 
                                       labels=labels, 
                                       autopct='%1.2f%%',
                                       colors=colors, 
                                       startangle=90,
                                       textprops={'fontsize': 12, 'weight': 'bold'})
    
    # Format percentage text
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(11)
        autotext.set_weight('bold')
    
    # Add title
    ax.set_title(f'Codon Distribution in Genes with Stop Codon {stop_codon}\n'
                 f'Total codons: {sum(counts):,}',
                 fontsize=16, fontweight='bold', pad=20)
    
    # Create legend with counts
    legend_labels = []
    for i, (codon, count) in enumerate(top_15):
        percentage = (count / sum(counts)) * 100
        legend_labels.append(f'{codon}: {count:,} ({percentage:.2f}%)')
    
    if others:
        other_count = counts[-1]
        percentage = (other_count / sum(counts)) * 100
        legend_labels.append(f'Other ({len(others)} codons): {other_count:,} ({percentage:.2f}%)')
    
    ax.legend(legend_labels, 
              loc='upper center', 
              bbox_to_anchor=(0.5, -0.08),
              ncol=2,
              fontsize=10,
              frameon=True,
              fancybox=True,
              shadow=True)
    
    plt.tight_layout()
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\nPie chart saved to: {output_file}")
    plt.close()


def print_codon_statistics(codon_counts):
    """Print detailed statistics about codon frequencies."""
    print("\nCodon Frequency Table:")
    print("-" * 40)
    print(f"{'Codon':<10} {'Count':<10} {'Percentage':<10}")
    print("-" * 40)
    
    total = sum(codon_counts.values())
    for codon in sorted(codon_counts.keys()):
        count = codon_counts[codon]
        percentage = (count / total) * 100
        print(f"{codon:<10} {count:<10} {percentage:>6.2f}%")
    
    print("-" * 40)
    print(f"{'TOTAL':<10} {total:<10} {100.00:>6.2f}%")


def main():
    script_dir = Path(__file__).resolve().parent
    input_file = script_dir / 'Saccharomyces_cerevisiae.R64-1-1.cdna.all.fa'
    valid_stops = {'TAA', 'TAG', 'TGA'}
    
    print("=" * 50)
    print("Codon Frequency Analysis Tool")
    print("=" * 50)
    print(f"\nAvailable stop codons: {', '.join(valid_stops)}")
    
    # Get user input
    while True:
        stop_codon = input("\nEnter a stop codon (TAA, TAG, or TGA): ").upper().strip()
        if stop_codon in valid_stops:
            break
        else:
            print(f"Invalid input. Please enter one of: {', '.join(valid_stops)}")
    
    # Count codons
    codon_counts = count_codons_for_stop(input_file, stop_codon)
    
    if not codon_counts:
        print(f"\nNo genes found with stop codon {stop_codon}")
        return
    
    # Print statistics
    print_codon_statistics(codon_counts)
    
    # Create and save pie chart in the script directory
    output_chart = script_dir / f'codon_distribution_{stop_codon}.png'
    create_pie_chart(codon_counts, stop_codon, output_chart)
    
    print("\n" + "=" * 50)
    print("Analysis complete!")
    print("=" * 50)


if __name__ == '__main__':
    main()
