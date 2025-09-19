import os
import pandas as pd
import requests

def download_ccle_mutations(outdir="tests/data", nrows=200):
    """
    Download and subset CCLE mutations file for testing.
    Parameters
    ----------
    outdir : str
        Directory to save the test dataset.
    nrows : int
        Number of rows from CCLE_mutations.csv to keep in the test file.
    """
    url = (
        "https://depmap.org/portal/data_page/?tab=allData&releasename=DepMap%20Public%2022Q2&filename=CCLE_mutations.csv"  
        # direct file link for CCLE_mutations.csv (DepMap 22Q2 release)
    )
    os.makedirs(outdir, exist_ok=True)
    full_path = os.path.join(outdir, "CCLE_mutations.csv")
    test_path = os.path.join(outdir, "ccle_mutations_test.csv")
    if not os.path.exists(full_path):
        print(f"[INFO] Downloading CCLE mutations → {full_path}")
        r = requests.get(url, stream=True)
        with open(full_path, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
    else:
        print(f"[INFO] File already exists: {full_path}")
    print(f"[INFO] Reading subset of CCLE_mutations.csv (first {nrows} rows)")
    df = pd.read_csv(full_path, nrows=nrows)
    df.to_csv(test_path, index=False)
    print(f"[INFO] Saved test dataset → {test_path}")

if __name__ == "__main__":
    download_ccle_mutations()