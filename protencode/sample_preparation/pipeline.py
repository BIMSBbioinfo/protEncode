import os
import pandas as pd
import numpy as np

from protencode.sample_preparation import (
    binary_encoding,
    multimut_encoding,
    esmattention_encoding,
)

def run_sample_preparation(
    output_dir: str,
    top_n: int = 10,
    do_binary: bool = False,
    do_multi: bool = False,
    do_esm: bool = False,
):
    """
    Run the sample preparation pipeline.

    Parameters
    ----------
    output_dir : str
        Directory where outputs from sequence_preparation are stored.
    top_n : int, default=10
        Number of top embeddings to use for ESM attention matrix.
    do_binary : bool
        Generate the binary encoding matrix.
    do_multi : bool
        Generate the multi-mutation encoding matrix.
    do_esm : bool
        Generate the ESM top-N attention matrix.
    """
    # ---- Load input data
    import os, pandas as pd, numpy as np
    from protencode.sample_preparation import (
        binary_encoding,
        multimut_encoding,
        esmattention_encoding,
    )
    top10_embd_path = os.path.join(
        output_dir, "output_800_t12_35m", "selected_top_unweighted_embeddings.npy"
    )
    pooled_embd_path = os.path.join(
        output_dir, "output_800_t12_35m", "pooled_embeddings.npy"
    )
    samples_path = os.path.join(output_dir, "sample2sequences.tsv")
    if not os.path.exists(samples_path):
        raise FileNotFoundError(f"Missing sample2sequences.tsv in {output_dir}")
    Samples = pd.read_csv(samples_path, sep="\t")
    Top10Embd = np.load(top10_embd_path) if os.path.exists(top10_embd_path) else None
    ESM2Data = np.load(pooled_embd_path) if os.path.exists(pooled_embd_path) else None
    # ---- Decide which encodings to run
    if not (do_binary or do_multi or do_esm):
        do_binary, do_multi, do_esm = True, True, True
    results = {}
    if do_binary:
        results["binary"] = binary_encoding.createBinaryMatrix(Samples, output_dir)
        print(f"[INFO] Binary matrix shape: {results['binary'].shape}")
    if do_multi:
        results["multi"] = multimut_encoding.createMultiMutationMatrix(Samples, output_dir)
        print(f"[INFO] Multi-mutation matrix shape: {results['multi'].shape}")
    if do_esm:
        if Top10Embd is None:
            raise FileNotFoundError("Missing Top10 embeddings .npy file for ESM matrix")
        results["esm_top"] = esmattention_encoding.create_top_matrix(
            Samples, Top10Embd, output_dir, top_n=top_n
        )
        print(f"[INFO] ESM top{top_n} matrix shape: {results['esm_top'].shape}")
    print("[INFO] Sample preparation complete ✅")
    return results