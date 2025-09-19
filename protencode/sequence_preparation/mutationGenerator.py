import pandas as pd
from tqdm import tqdm

def generateMutatedSequence(row, log_file, error_counter):
    """
    Generate the mutated protein sequence for a given row with validation.
    Logs validation errors to a file if mismatches occur and increments an error counter.
    
    Args:
        row (pd.Series): A row from the DataFrame containing mutation details.
        log_file (str): Path to the log file for recording validation errors.
        error_counter (dict): Dictionary to count validation errors.

    Returns:
        str: The mutated protein sequence if validation passes, or None if it fails.
    """
    sequence = list(row['wildtypeSequence'])
    position = row['pos'] - 1
    if position >= len(sequence) or sequence[position] != row['wtAA']:
        with open(log_file, "a") as log:
            log.write(f"Validation Error for sample {row['sample_id']}:\n")
            log.write(f"  Position: {row['pos']}\n")
            log.write(f"  Expected wtAA: '{row['wtAA']}'\n")
            log.write(f"  Found: '{sequence[position] if position < len(sequence) else 'Out of bounds'}'\n")
            log.write(f"  Wildtype Sequence: {row['wildtypeSequence']}\n")
            log.write("-" * 50 + "\n")
        error_counter['count'] += 1
        return None
    sequence[position] = row['mutAA']
    return ''.join(sequence)

def processMutationsProgress(df, log_file, output_dir):
    """
    Process all rows in the DataFrame to generate mutated sequences.
    Uses tqdm for a progress bar, logs validation errors to a file, and returns only valid rows.
    
    Args:
        df (pd.DataFrame): The DataFrame containing mutation data.
        log_file (str): Path to the log file for validation errors.
    
    Returns:
        pd.DataFrame: Updated DataFrame with a new 'mutantSequence' column, excluding rows with errors.
    """
    error_counter = {'count': 0}
    tqdm.pandas(desc="Processing sequences")
    df['mutantSequence'] = df.progress_apply(
        lambda row: generateMutatedSequence(row, log_file, error_counter), axis=1
    )
    print(f"\nTotal validation errors: {error_counter['count']}")
    valid_df = df[df['mutantSequence'].notnull()].reset_index(drop=True)
    print(f"Saving processed files to {output_dir}. Error log at {log_file}.")
    valid_df.to_csv(f"{output_dir}/mutationsequence.csv", index=False)
    print(f"Returning processed dataframe with {len(valid_df)} entries.")
    return valid_df