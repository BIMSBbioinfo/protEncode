import os
import requests
from datetime import datetime
from tqdm import tqdm

def downloadUniprotFasta(
    organism_id,
    output_dir,
    contact_email="",
    update=False,
    verbose=True,
    base_url="https://rest.uniprot.org/uniprotkb/stream",
    format="fasta",
    chunk_size=1024
):
    """
    Download FASTA sequences for a specified organism from UniProt and save to a local file.

    Parameters:
    -----------
    organism_id : str or int
        The UniProt organism ID (taxonomy ID) for which to download the FASTA sequences.
    output_dir : str
        Directory where the FASTA file will be saved.
    contact_email : str, optional
        Contact email address to be included in the User-Agent header (default is an empty string).
    update : bool, optional
        If True, force re-download of the file even if it already exists locally (default is False).
    verbose : bool, optional
        If True, print detailed progress and status messages (default is True).
    base_url : str, optional
        Base URL for the UniProt REST API (default is "https://rest.uniprot.org/uniprotkb/stream").
    format : str, optional
        File format to retrieve from UniProt (default is "fasta").

    Returns:
    --------
    str
        Path to the downloaded FASTA file or a message indicating no update was needed.

    Raises:
    -------
    RuntimeError
        If the download fails due to an error in the request.
    """
    print(f"Starting download process for organism ID: {organism_id}")
    os.makedirs(output_dir, exist_ok=True)
    output_file = os.path.join(output_dir, f"{organism_id}.fasta")
    if verbose:
        print(f"Output directory: {output_dir}")
        print(f"Output file: {output_file}")
    query_url = f"{base_url}?query=organism_id:{organism_id}&format={format}"
    if verbose:
        print(f"Constructed query URL: {query_url}")
    headers = {
        "User-Agent": f"Python-requests {contact_email}" if contact_email else "Python-requests",
    }
    if os.path.exists(output_file) and not update:
        last_modified_time = datetime.utcfromtimestamp(os.path.getmtime(output_file)).strftime("%a, %d %b %Y %H:%M:%S GMT")
        headers["If-Modified-Since"] = last_modified_time
        if verbose:
            print(f"Existing file found. Last modified: {last_modified_time}")
            print("Checking if the data is up-to-date...")
    response = requests.get(query_url, headers=headers)
    if response.status_code == 200:
        if verbose:
            print("New data available. Downloading...")
        total_size = int(response.headers.get("Content-Length", 0))
        with open(output_file, "wb") as f, tqdm(
            total=total_size,
            unit="B",
            unit_scale=True,
            desc=f"Downloading {organism_id}"
        ) as pbar:
            for chunk in response.iter_content(chunk_size=chunk_size):
                f.write(chunk)
                pbar.update(len(chunk))
        results = response.headers.get("X-Total-Results", "unknown")
        release = response.headers.get("X-UniProt-Release", "unknown")
        release_date = response.headers.get("X-UniProt-Release-Date", "unknown")
        if verbose:
            print(
                f"Downloaded FASTAs for organism ID: {organism_id} from UniProt release {release} "
                f"({release_date}). Total results: {results}"
            )
            print(f"File saved to: {output_file}")
        return output_file
    elif response.status_code == 304:
        if verbose:
            print(f"Data for taxon {organism_id} is up-to-date. No new download needed.")
        return f"Data for taxon {organism_id} is up-to-date. No new download needed."
    else:
        error_message = (
            f"Failed to download data. Status: {response.status_code}, URL: {query_url}\n"
            f"Reason: {response.text}"
        )
        if verbose:
            print("An error occurred during the download process.")
            print(error_message)
        raise RuntimeError(error_message)