import os
from . import variantProcessor, uniProtFasta
from .finalise_sequences import generate_sequence_mappings, sequence_sample_count

def run_sequence_preparation(data_dir, output_dir, organism_id="9606", contact_email="", update=False, max_len=200):
    # Step 1: process variant files
    maf_files = [f for f in os.listdir(data_dir) if f.endswith(".maf")]
    print(f"[1/9] Processing {len(maf_files)} variant files…")
    all_mutations = variantProcessor.multiProcessVariantFiles(data_dir, maf_files, output_dir)
    # Step 2: download UniProt FASTA
    print("[2/9] Downloading UniProt FASTA…")
    result = uniProtFasta.downloadUniprotFasta(
        organism_id, output_dir, contact_email, update, verbose=True
    )
    # Step 3: process FASTA
    print("[3/9] Processing FASTA…")
    fasta_file = f"{output_dir}/{organism_id}.fasta"
    uniprot_data = fastaProcessor.uniprotFastaSwissProtProcessor(fasta_file, output_dir)
    # Step 4: merge mutation sequences
    print("[4/9] Merging mutation sequences…")
    all_mutations = pd.read_csv(f"{output_dir}/all_mutations.csv")
    uniprot_data = pd.read_csv(f"{output_dir}/uniprot_data.csv")
    mut_seq_merge = mutationSequenceMerge.mergeReport(all_mutations, uniprot_data)
    # Step 5: extract variation info
    print("[5/9] Extracting variation info…")
    mutseq_variantextract, unmatched_variants = extractVarationInfo.processVariantParts(mut_seq_merge)
    # Step 6: filter genes by length
    print(f"[6/9] Filtering genes shorter than {min_length}…")
    mutseq_widthfilt = geneLengthFilter.filterGenesLength(mutseq_variantextract)
    mutseq_dropmultires = (
    mutseq_widthfilt.sort_values(by=['geneName', 'sample_id', 'uniprotAccession', 'pos', 'mutAA'])
       .drop_duplicates(subset=['geneName', 'sample_id', 'uniprotAccession', 'pos'])
    )
    # Step 7: generate mutations
    print("[7/9] Generating mutations…")
    log_file = f"{data_dir}/mutation_validation_errors.log"
    mutseq_mutated = mutationGenerator.processMutationsProgress(mutseq_dropmultires, log_file, output_dir)
    # Step 8: downstream processing
    print(f"[8/9] Limiting mutation length to {max_len}.")
    lengene_mutseq = downstreamProcess.DownstreamReduce(mutseq_mutated, max_len, output_dir)
    # Step 9: finalise sequences
    print("[9/9] Finalising sequences and saving…")
    unique_samples = sequence_sample_count(lengene_mutseq)
    sequence_df, sample2seq_df = generate_sequence_mappings(lengene_mutseq, unique_samples)
    print("Sequence preparation pipeline completed.")
    return sequence_df, sample2seq_df