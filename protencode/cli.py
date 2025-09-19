import argparse
from protencode.sequence_preparation.pipeline import run_sequence_preparation
from protencode.sample_preparation.pipeline import run_sample_preparation
# later: from protencode.embeddings_generation.pipeline import run_embeddings_generation

def embeddings_main(args):
    print("Embeddings pipeline not wired yet")

def sample_main(args):
    run_sample_preparation(
        output_dir=args.output,
        top_n=args.top_n,
        do_binary=args.binary,
        do_multi=args.multi,
        do_esm=args.esm,
    )

def sequence_main(args):
    run_sequence_preparation(
        data_dir=args.data,
        output_dir=args.output,
        organism_id=args.organism,
        contact_email=args.email,
        update=args.update,
        min_length=args.min_length,
    )

def main():
    parser = argparse.ArgumentParser(
        prog="protencode",
        description=(
            "ProtEncode: encode protein mutations with different embedding schemes.\n\n"
            "Available pipelines:\n"
            "  • sequence   Prepare sequences from MAF files and UniProt\n"
            "  • sample     Generate sample-level encoding matrices (binary, multi-mutation, ESM)\n"
            "  • embeddings (coming soon) Generate embeddings for sequences\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- embeddings placeholder
    parser_embeddings = subparsers.add_parser(
        "embeddings",
        help="Run embeddings generation (coming soon)",
        description="Generate embeddings for protein sequences (not yet implemented).",
    )
    parser_embeddings.set_defaults(func=embeddings_main)

    # --- sample preparation
    parser_sample = subparsers.add_parser(
        "sample",
        help="Run sample preparation",
        description=(
            "Generate encoding matrices at the sample level.\n\n"
            "By default, runs all encodings. Use flags to select specific ones."
        ),
    )
    parser_sample.add_argument("--output", required=True, help="Output directory from sequence preparation")
    parser_sample.add_argument("--top-n", type=int, default=10, help="Number of top embeddings to use for ESM attention")
    parser_sample.add_argument("--binary", action="store_true", help="Generate binary matrix")
    parser_sample.add_argument("--multi", action="store_true", help="Generate multi-mutation matrix")
    parser_sample.add_argument("--esm", action="store_true", help="Generate ESM top-N attention matrix")
    parser_sample.set_defaults(func=sample_main)

    # --- sequence preparation
    parser_sequence = subparsers.add_parser(
        "sequence",
        help="Run sequence preparation pipeline",
        description=(
            "Prepare sequences from mutation data.\n\n"
            "Steps include:\n"
            "  1. Process MAF/CSV files\n"
            "  2. Download UniProt FASTA\n"
            "  3. Merge mutation and UniProt data\n"
            "  4. Apply gene length filtering\n"
            "  5. Generate mutated sequences\n"
            "  6. Finalise sequence mappings"
        ),
    )
    parser_sequence.add_argument("--data", required=True, help="Directory with .maf or .csv files")
    parser_sequence.add_argument("--output", required=True, help="Output directory")
    parser_sequence.add_argument("--organism", default="9606", help="NCBI taxonomy ID (default: 9606 for human)")
    parser_sequence.add_argument("--email", default="", help="Contact email for UniProt downloads")
    parser_sequence.add_argument("--update", action="store_true", help="Force UniProt FASTA re-download")
    parser_sequence.add_argument("--min-length", type=int, default=200, help="Minimum gene length filter")
    parser_sequence.set_defaults(func=sequence_main)

    # Parse and dispatch
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()