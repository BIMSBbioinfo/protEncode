import pandas as pd

def mergeReport(all_mutations, uniprot_data, on_column='geneName', how='inner'):
    """
    Merges two dataframes and generates a detailed report on the merge process.
    
    Args:
        all_mutations (pd.DataFrame): DataFrame containing mutation data.
        uniprot_data (pd.DataFrame): DataFrame containing UniProt data.
        on_column (str): Column name to merge on (default: 'geneName').
        how (str): Merge method (default: 'inner').
    
    Returns:
        pd.DataFrame: Merged DataFrame.
    """
    print("Starting the merge process...")
    merged_df = all_mutations.merge(uniprot_data, on=on_column, how=how)
    print(f"Merge complete! Number of rows in merged dataset: {len(merged_df)}")
    print(f"Rows in all_mutations: {len(all_mutations)}")
    print(f"Rows in uniprot_data: {len(uniprot_data)}\n")
    # Check for duplicates in the merge column
    print("Checking for duplicates in the merge columns...")
    duplicates_all_mutations = all_mutations[on_column].duplicated().sum()
    duplicates_uniprot_data = uniprot_data[on_column].duplicated().sum()
    print(f"Duplicate {on_column} entries in all_mutations: {duplicates_all_mutations}")
    print(f"Duplicate {on_column} entries in uniprot_data: {duplicates_uniprot_data}\n")
    # Check unmatched records
    unmatched_in_all_mutations = all_mutations[~all_mutations[on_column].isin(uniprot_data[on_column])]
    unmatched_in_uniprot_data = uniprot_data[~uniprot_data[on_column].isin(all_mutations[on_column])]
    print("Checking for unmatched records...")
    print(f"Unmatched records in all_mutations: {len(unmatched_in_all_mutations)}")
    print(f"Unmatched records in uniprot_data: {len(unmatched_in_uniprot_data)}\n")
    # Check for mismatches or inconsistencies in geneName between the datasets or duplicates.
    mismatched_records = merged_df[~merged_df['geneName'].isin(uniprot_data['geneName'])]
    duplicates_in_merge = merged_df.duplicated().sum()
    print("Checking fatal merge errors...")
    print(f"Mismatched records: {len(mismatched_records)}")
    print(f"Duplicate rows in merged dataset: {duplicates_in_merge}\n")
    # Return merged dataframe
    print("Merge and report complete!")
    return merged_df