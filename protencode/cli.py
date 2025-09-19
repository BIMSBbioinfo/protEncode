import argparse
from protencode.sequence_preparation.pipeline import run_sequence_preparation
from protencode.sample_preparation.pipeline import run_sample_preparation
from protencode.utils.download_test_data import download_ccle_mutations
# later: from protencode.embeddings_generation.pipeline import run_embeddings_generation

def testdata_main(args):
    download_ccle_mutations(outdir=args.output, nrows=args.nrows)

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
            "  • sequence   Prepare sequences from mutation files and UniProt\n"
            "  • sample     Generate sample-level encoding matrices (binary, multi, ESM)\n"
            "  • embeddings (coming soon)\n"
            "  • testdata   Download and prepare CCLE test dataset\n\n"
            "👉 For more details on a specific pipeline, run:\n"
            "   protencode <pipeline> --help\n"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- testdata
    parser_testdata = subparsers.add_parser(
        "testdata",
        help="Download and prepare CCLE test dataset",
        description=(
            "Download the CCLE mutations dataset (DepMap 22Q2) and create a lightweight subset "
            "for testing the ProtEncode pipelines.\n\n"
            "This command will:\n"
            "  1. Download CCLE_mutations.csv (~1.6 GB) if not already present.\n"
            "  2. Extract the first N rows (default: 200).\n"
            "  3. Save to <output>/ccle_mutations_test.csv for use in sequence/sample pipelines."
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser_testdata.add_argument(
        "--output",
        default="tests/data",
        help="Directory to save the full and subset CCLE mutations files (default: tests/data).",
    )
    parser_testdata.add_argument(
        "--nrows",
        type=int,
        default=200,
        help="Number of rows to keep in the test file (default: 200).",
    )
    parser_testdata.set_defaults(func=testdata_main)

    # --- sample preparation
    parser_sample = subparsers.add_parser(
        "sample",
        help="Run sample preparation",
        description=(
            "Generate encoding matrices at the sample level.\n\n"
            "By default, runs all encodings. Use flags to select specific ones."
        ),
    )
    parser_sample.add_argument("--output", required=True, help="Output directory (from sequence preparation).")
    parser_sample.add_argument("--top-n", type=int, default=10, help="Number of top embeddings to use for ESM attention.")
    parser_sample.add_argument("--binary", action="store_true", help="Generate binary matrix only.")
    parser_sample.add_argument("--multi", action="store_true", help="Generate multi-mutation matrix only.")
    parser_sample.add_argument("--esm", action="store_true", help="Generate ESM top-N matrix only.")
    parser_sample.set_defaults(func=lambda args: run_sample_preparation(
        output_dir=args.output,
        top_n=args.top_n,
        do_binary=args.binary,
        do_multi=args.multi,
        do_esm=args.esm,
    ))

    # --- sequence preparation
    parser_sequence = subparsers.add_parser(
        "sequence",
        help="Run sequence preparation pipeline",
        description=(
            "Prepare sequences from mutation data and UniProt.\n\n"
            "Steps include:\n"
            "  1. Process mutation files (.maf or .csv)\n"
            "  2. Download UniProt FASTA (if missing)\n"
            "  3. Merge mutation + UniProt data\n"
            "  4. Apply gene length filtering\n"
            "  5. Generate mutated sequences\n"
            "  6. Finalise sequence mappings"
        ),
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser_sequence.add_argument("--data", required=True, help="Directory containing .maf or .csv mutation files.")
    parser_sequence.add_argument("--output", required=True, help="Directory to write processed outputs.")
    parser_sequence.add_argument("--organism", default="9606", help="NCBI taxonomy ID (default: 9606 = human).")
    parser_sequence.add_argument("--email", default="", help="Contact email required for UniProt downloads.")
    parser_sequence.add_argument("--update", action="store_true", help="Force UniProt FASTA re-download.")
    parser_sequence.add_argument("--min-length", type=int, default=200, help="Minimum gene length filter (default: 200).")
    parser_sequence.set_defaults(func=lambda args: run_sequence_preparation(
        data_dir=args.data,
        output_dir=args.output,
        organism_id=args.organism,
        contact_email=args.email,
        update=args.update,
        min_length=args.min_length,
    ))

    # --- embeddings placeholder
    parser_embeddings = subparsers.add_parser(
        "embeddings",
        help="Run embeddings generation (coming soon)",
        description="Generate embeddings for protein sequences (not yet implemented).",
    )
    parser_embeddings.set_defaults(func=lambda args: print("Embeddings pipeline not wired yet."))

    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()