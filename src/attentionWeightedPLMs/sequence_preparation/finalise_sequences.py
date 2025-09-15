import numpy as np
import pandas as pd
from tqdm import tqdm

def sequence_sample_count(lengene_mutseq):
    unique_wildtype = lengene_mutseq["wildtypeSequence"].nunique()
    unique_mutant = lengene_mutseq["mutantSequence"].nunique()
    number_overall = unique_wildtype + unique_mutant
    numberoverall = list(range(1, number_overall + 1))
    unique_samples = lengene_mutseq['sample_id'].unique()
    print("There are {} unique wildtype sequences and {} unique mutant sequences.".format(unique_wildtype, unique_mutant))
    print("There are {} unique samples.".format(len(unique_samples)))
    return unique_samples

def generate_sequence_mappings(output_dir, lengene_mutseq, unique_samples, starting_sequence_count=0):
    sequence_results = []
    sample2seq_results = []
    sequence_count = starting_sequence_count
    for gene_name in tqdm(lengene_mutseq["geneName"].unique(), desc="Generating sequence mappings"):
        gene_df = lengene_mutseq[lengene_mutseq["geneName"] == gene_name]
        # Must have exactly one wildtype sequence
        if len(gene_df["wildtypeSequence"].unique()) != 1:
            print(f"⚠️ Warning: Gene {gene_name} skipped (wildtype sequence not unique).")
            continue
        WT_sequence = gene_df["wildtypeSequence"].unique()[0]
        mutant_sequences = gene_df["mutantSequence"].unique()
        all_sequences = np.insert(mutant_sequences, 0, WT_sequence)
        # Assign sequence IDs
        sequence_count_new = sequence_count + len(all_sequences)
        sequence_ids = list(range(sequence_count + 1, sequence_count_new + 1))
        sequence_file = pd.DataFrame(all_sequences, columns=["sequence"])
        sequence_file["sequence_id"] = [
            f"Seq{sequence_ids[i]}_{gene_name}{j+1}" for i, j in enumerate(range(len(all_sequences)))
        ]
        sequence_results.append(sequence_file)
        # Map sequence → ID
        sequence_mapping = dict(zip(sequence_file["sequence"], sequence_file["sequence_id"]))
        # Mutant mapping
        Sample2Sequence = (
            gene_df.groupby(["mutantSequence", "geneName", "variant"])["sample_id"]
            .apply(lambda x: ";".join(x))
            .reset_index()
        )
        Sample2Sequence["sequence_id"] = Sample2Sequence["mutantSequence"].map(sequence_mapping)
        # Handle missing samples (assign to WT)
        missing_sample_ids = set(unique_samples) - set(gene_df["sample_id"])
        missing_samples_one = ";".join(missing_sample_ids)
        WT_sequence_id = sequence_file.loc[sequence_file["sequence"] == WT_sequence, "sequence_id"].iloc[0]
        WT_data = {
            "mutantSequence": WT_sequence,
            "geneName": gene_name,
            "variant": ["WT"],
            "sample_id": missing_samples_one,
            "sequence_id": WT_sequence_id,
        }
        WT_frame = pd.DataFrame(WT_data)
        # Combine
        FullFrame = pd.concat([WT_frame, Sample2Sequence], ignore_index=True)
        sample2seq_results.append(FullFrame)
        sequence_count = sequence_count_new
    # Concatenate results across all genes
    final_sequence_file = pd.concat(sequence_results, ignore_index=True)
    final_sample2sequence = pd.concat(sample2seq_results, ignore_index=True)
    final_sequence_file.to_csv(f"{output_dir}/sequences.txt", sep='\t', index=None)
    final_sample2sequence.to_csv(f"{output_dir}/sample2sequences.tsv", sep='\t', index=None)
    return final_sequence_file, final_sample2sequence