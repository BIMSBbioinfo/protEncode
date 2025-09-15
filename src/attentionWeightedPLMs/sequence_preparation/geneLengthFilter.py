import pandas as pd

def filterGenesLength(mutseq_variantextract, wildtype_col='wildtypeSequence', max_width=5000):
    """
    Filters the dataset to include only genes with protein lengths less than the given threshold.
    
    Args:
        mutseq_variantextract (pd.DataFrame): Input DataFrame containing mutation and protein data.
        wildtype_col (str): Column name containing the wildtype sequence. Default is 'wildtypeSequence'.
        max_width (int): Maximum allowable protein width for filtering. Default is 5000.
    
    Returns:
        pd.DataFrame: Filtered DataFrame containing only rows with genes meeting the criteria.
    """
    mutseq_variantextract = mutseq_variantextract.copy()
    mutseq_variantextract.loc[:, 'width'] = mutseq_variantextract[wildtype_col].str.len()
    total_records = len(mutseq_variantextract)
    filtered_data = mutseq_variantextract[
        mutseq_variantextract['width'] < max_width
    ]
    excluded_records_count = total_records - len(filtered_data)
    print(f"Returning dataframe with {total_records} records.")
    print(f"Excluded records with width >= {max_width}: {excluded_records_count}")
    return filtered_data