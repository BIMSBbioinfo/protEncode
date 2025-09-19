import pandas as pd
import matplotlib.pyplot as plt

def DownstreamReduce(mutseq_mutated, positional_threshold, output_dir):
    early_mutations = mutseq_mutated[mutseq_mutated['pos'] < positional_threshold]
    print(f"{(len(early_mutations)/len(mutseq_mutated))*100:.1f}% mutations retained below positional threshold.")
    gene_counts = early_mutations['geneName'].value_counts()
    cumulative_counts = gene_counts.cumsum()
    positions = [100, 200, 500, 1000, 5000]
    colours = ['red', 'green', 'blue', 'purple', 'orange']
    threshold_counts = [cumulative_counts.iloc[pos - 1] if pos <= len(cumulative_counts) else None for pos in positions]
    fig, axes = plt.subplots(1, 2, figsize=(20, 6))
    axes[0].plot(cumulative_counts.values, linestyle='-', color='skyblue', label='Cumulative Count')
    axes[0].set_yscale('log')
    axes[0].set_title('Cumulative Count of Gene Names (Log Scale)')
    axes[0].set_xlabel('Gene Name Index')
    axes[0].set_ylabel('Cumulative Count (Log Scale)')
    for pos, colour, count in zip(positions, colours, threshold_counts):
        if count is not None:
            axes[0].axvline(x=pos - 0.5, color=colour, linestyle='--', label=f'First {pos} genes: {count}')
    axes[0].legend(loc='lower right')
    gene_counts.plot(kind='bar', color='skyblue', ax=axes[1])
    axes[1].set_title('Counts of Each Gene Name')
    axes[1].set_xlabel('Gene Name')
    axes[1].set_ylabel('Count')
    axes[1].set_xticks([])
    for pos, colour, count in zip(positions, colours, threshold_counts):
        if count is not None:
            axes[1].axvline(x=pos - 0.5, color=colour, linestyle='--', label=f'First {pos} genes: {count}')
    axes[1].legend(loc='upper right')
    plt.tight_layout()
    plt.show()
    top_gene_number = input("Please select number of top genes to take forward.")
    print(f"Returning {top_gene_number} top genes.")
    top_genes = gene_counts.head(int(top_gene_number)).index.tolist()
    topearly_mutseq = early_mutations[early_mutations['geneName'].isin(top_genes)]
    print(f"Saving to {output_dir}.")
    topearly_mutseq.to_csv(f"{output_dir}/topearly_mutseq.csv")
    return topearly_mutseq