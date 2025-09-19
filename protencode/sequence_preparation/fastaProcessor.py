from Bio import SeqIO
import re
from tqdm import tqdm
import pandas as pd

def uniprotFastaSwissProtProcessor(fasta_file, output_dir, show_progress=True):
    """
    Parses a UniProt FASTA file to extract SwissProt entries with gene names and sequences.
    
    Args:
        fasta_file (str): Path to the FASTA file.
        show_progress (bool): Whether to show a progress bar (default: True).
        
    Returns:
        tuple: A tuple containing:
            - uniprot_data (list): A list of dictionaries with 'uniprotAccession', 'geneName', and 'sequence'.
            - count (int): The total number of SwissProt records.
    """
    uniprot_data = []
    count = 0
    if show_progress:
        total_records = sum(1 for _ in SeqIO.parse(fasta_file, "fasta"))
    with open(fasta_file, "r") as file:
        iterator = SeqIO.parse(file, "fasta")
        if show_progress:
            iterator = tqdm(iterator, total=total_records, desc="Processing records")
        for record in iterator:
            header = record.description
            if header.startswith("sp|"):
                count += 1
                uniprot_accession = re.sub(r"^sp\|(.+?)\|.+$", r"\1", header)
                gene_name_match = re.search(r" GN=(.+?) ", header)
                gene_name = gene_name_match.group(1) if gene_name_match else None
                if gene_name is not None:
                    uniprot_data.append({
                        'uniprotAccession': uniprot_accession,
                        'geneName': gene_name,
                        'wildtypeSequence': str(record.seq)
                    })
    uniprot_df = pd.DataFrame(uniprot_data)
    uniprot_df.to_csv(f"{output_dir}/uniprot_data.csv", index=False)
    print(f"\nThere are {count} SwissProt records.")
    print(f"Returning dataframe with {len(uniprot_data)} entries (containing both a gene name and a sequence).")
    return uniprot_df