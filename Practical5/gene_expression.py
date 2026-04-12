import matplotlib.pyplot as plt

gene_expression = {
    'TP53': 12.4,
    'EGFR': 15.1,
    'BRCA1': 8.2,
    'PTEN': 5.3,
    'ESR1': 10.7
}

gene_expression['MYC'] = 11.6

print("Gene expression dictionary:")
for gene, value in gene_expression.items():
    print(f"  {gene}: {value}")

genes = list(gene_expression.keys())
values = list(gene_expression.values())

plt.figure(figsize=(8, 5))
plt.bar(genes, values, color='skyblue', edgecolor='black')
plt.title('Gene Expression Levels')
plt.xlabel('Gene')
plt.ylabel('Expression Level')
plt.grid(True, axis='y', linestyle='--', alpha=0.5)

for x, y in zip(genes, values):
    plt.text(genes.index(x), y + 0.2, f'{y:.1f}', ha='center')

plt.tight_layout()
plt.show()

gene_of_interest = 'TP53'  

if gene_of_interest in gene_expression:
    print(f"Expression of {gene_of_interest}: {gene_expression[gene_of_interest]}")
else:
    print(f"Error: {gene_of_interest} not found in the dataset.")

average_expression = sum(gene_expression.values()) / len(gene_expression)
print(f"Average gene expression level (all genes): {average_expression:.2f}")
