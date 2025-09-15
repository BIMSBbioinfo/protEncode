import argparse
from attentionWeightedPLMs.sequence_preparation.pipeline import run_sequence_preparation
# later: also import from embeddings_generation, sample_preparation

def embeddings_main(args):
    print("Embeddings pipeline not wired yet")

def sample_main(args):
    print("Sample pipeline not wired yet")

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
        prog="attention-plm",
        description="Command line interface for attentionWeightedPLMs"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)
    # --- embeddings placeholder
    parser_embeddings = subparsers.add_parser("embeddings", help="Run embeddings generation")
    parser_embeddings.set_defaults(func=embeddings_main)
    # --- sample placeholder
    parser_sample = subparsers.add_parser("sample", help="Run sample preparation")
    parser_sample.set_defaults(func=sample_main)
    # --- sequence preparation (your Option A pipeline)
    parser_sequence = subparsers.add_parser("sequence", help="Run sequence preparation pipeline")
    parser_sequence.add_argument("--data", required=True, help="Directory with .maf files")
    parser_sequence.add_argument("--output", required=True, help="Output directory")
    parser_sequence.add_argument("--organism", default="9606", help="NCBI taxonomy ID (default: 9606)")
    parser_sequence.add_argument("--email", default="", help="Contact email for UniProt downloads")
    parser_sequence.add_argument("--update", action="store_true", help="Force UniProt FASTA update")
    parser_sequence.add_argument("--min-length", type=int, default=200, help="Minimum gene length filter")
    parser_sequence.set_defaults(func=sequence_main)
    # Parse and dispatch
    args = parser.parse_args()
    args.func(args)

if __name__ == "__main__":
    main()