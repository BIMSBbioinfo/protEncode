import os
import pandas as pd
from tqdm import tqdm

from protencode.sequence_preparation import (
    variantProcessor,
    uniProtFasta,
    fastaProcessor,
    mutationSequenceMerge,
    extractVarationInfo,
    geneLengthFilter,
    mutationGenerator,
    downstreamProcess,
    finalise_sequences,
)

def run_sequence_preparation(
    data_dir: str,
    output_dir: str,
    organism_id: str = "9606",
    contact_email: str = "",
    update: bool = False,
    min_length: int = 200,
):
    """
    Run the sequence preparation pipeline.

    Parameters
    ----------
    data_dir : str
        Directory containing MAF/CSV files with mutation data.
    output_dir : str
        Directory to write processed files.
    organism_id : str, default="9606"
        NCBI taxonomy ID (default: human).
    contact_email : str, optional
        Email address required for UniProt downloads.
    update : bool, default=False
        Force UniProt FASTA re-download.
    min_length : int, default=200
        Minimum gene length filter.
    """
    os.makedirs(output_dir, exist_ok=True)
    os.makedirs(os.path.join(output_dir, "logs"), exist_ok=True)
    # 1. Collect mutation data
    maf_files = [f for f in os.listdir(data_dir) if f.endswith(".csv")]
    all_mutations = variantProcessor.multiProcessVariantFiles(
        data_dir,
        maf_files,
        output_dir,
        columns_to_keep=["DepMap_ID", "Hugo_Symbol", "Protein_Change"],
        column_mappings={
            "DepMap_ID": "sample_id",
            "Hugo_Symbol": "geneName",
            "Protein_Change": "variant",
        },
        separator=",",
    )
    # 2. Download and parse UniProt FASTA
    try:
        result = uniProtFasta.downloadUniprotFasta(
            organism_id, output_dir, contact_email, update, verbose=True
        )
        print(f"[INFO] UniProt FASTA download result: {result}")
    except RuntimeError as e:
        print(f"[ERROR] UniProt download failed: {e}")
        return
    fasta_file = os.path.join(output_dir, f"{organism_id}.fasta")
    uniprot_data = fastaProcessor.uniprotFastaSwissProtProcessor(fasta_file, output_dir)
    # 3. Merge mutation data with UniProt
    all_mutations = pd.read_csv(os.path.join(output_dir, "all_mutations.csv"))
    uniprot_data = pd.read_csv(os.path.join(output_dir, "uniprot_data.csv"))
    mut_seq_merge = mutationSequenceMerge.mergeReport(all_mutations, uniprot_data)
    # 4. Extract variant info
    mutseq_variantextract, unmatched_variants = extractVarationInfo.processVariantParts(
        mut_seq_merge, variant_column="variant"
    )
    # 5. Apply gene length filter
    mutseq_widthfilt = geneLengthFilter.filterGenesLength(
        mutseq_variantextract, min_length=min_length
    )
    # 6. Drop multi-residues duplicates
    mutseq_dropmultires = (
        mutseq_widthfilt.sort_values(
            by=["geneName", "sample_id", "uniprotAccession", "pos", "mutAA"]
        )
        .drop_duplicates(subset=["geneName", "sample_id", "uniprotAccession", "pos"])
    )
    # 7. Generate mutated sequences
    log_file = os.path.join(output_dir, "logs", "mutation_generator.log")
    mutseq_mutated = mutationGenerator.processMutationsProgress(
        mutseq_dropmultires, log_file, output_dir
    )
    # 8. Downstream filtering
    lengene_mutseq = downstreamProcess.DownstreamReduce(
        mutseq_mutated, 800, output_dir
    )
    # 9. Final sequence mappings
    unique_samples = finalise_sequences.sequence_sample_count(lengene_mutseq)
    final_sequence_file, final_sample2sequence = finalise_sequences.generate_sequence_mappings(
        output_dir, lengene_mutseq, unique_samples, starting_sequence_count=0
    )
    print("[INFO] Sequence preparation pipeline complete ✅")