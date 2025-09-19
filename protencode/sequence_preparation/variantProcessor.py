import pandas as pd
import os
from tqdm import tqdm

def processVariantFile(
    file_path,
    variant_type='Missense_Mutation',
    classification_column='Variant_Classification',
    columns_to_keep=None,
    column_mappings=None,
    separator='\t'
):
    """
    Process a variant annotation file (e.g., MAF or VCF) to extract and standardise mutation information.

    Parameters:
    -----------
    file_path : str
        Path to the variant annotation file.
    variant_type : str, optional
        The specific type of variant to filter (default is 'Missense_Mutation').
    classification_column : str, optional
        The column name in the input file that specifies variant classification (default is 'Variant_Classification').
    columns_to_keep : list, optional
        List of column names to retain in the output (default is ['Tumor_Sample_Barcode', 'Hugo_Symbol', 'HGVSp_Short']).
    column_mappings : dict, optional
        Dictionary mapping original column names to new names for standardisation (default is 
        {'Tumor_Sample_Barcode': 'sample_id', 'Hugo_Symbol': 'geneName', 'HGVSp_Short': 'variant'}).
    separator : str, optional
        Delimiter used in the input file (default is '\t' for tab-separated files).

    Returns:
    --------
    pd.DataFrame
        A DataFrame containing filtered and standardised mutation information, with duplicates removed.
    """ 
    if columns_to_keep is None:
        columns_to_keep = ['Tumor_Sample_Barcode', 'Hugo_Symbol', 'HGVSp_Short']
    if column_mappings is None:
        column_mappings = {
            'Tumor_Sample_Barcode': 'sample_id',
            'Hugo_Symbol': 'geneName',
            'HGVSp_Short': 'variant'
        } 
    mut = pd.read_csv(file_path, sep=separator, low_memory=False)
    mut = mut[mut[classification_column] == variant_type]
    mut = mut[columns_to_keep]
    mut.columns = [column_mappings.get(col, col) for col in mut.columns]
    return mut.drop_duplicates()

def multiProcessVariantFiles(
    data_dir,
    file_list,
    output_dir,
    **kwargs
):
    """
    Process multiple variant annotation files and combine the results into a single DataFrame.

    Parameters:
    -----------
    data_dir : str
        The directory containing the variant files.
    file_list : list of str
        A list of filenames to process within the specified directory.

    Returns:
    --------
    pd.DataFrame
        A concatenated DataFrame containing the processed data from all files.
    """
    processed_files = [processVariantFile(os.path.join(data_dir, file), **kwargs) for file in tqdm(file_list, desc="Processing variant files")]
    all_processed_files = pd.concat(processed_files, ignore_index=True)
    print(f"Saving processed files to {output_dir}.")
    all_processed_files.to_csv(f"{output_dir}/all_mutations.csv", index=False)
    print(f"Returning processed files with {len(all_processed_files.index)} rows and {len(all_processed_files.columns)} columns.")
    return all_processed_files