import re
import pandas as pd

def processVariantParts(df, variant_column='variant'):
    """
    Processes a DataFrame to extract parts of a variant string and merge them back into the original DataFrame.
    
    Args:
        df (pd.DataFrame): Input DataFrame with a column containing variant strings.
        variant_column (str): Name of the column containing the variants (default: 'variant').
        
    Returns:
        pd.DataFrame: DataFrame with additional columns 'wtAA', 'pos', 'mutAA', and the count of unmatched variants.
    """
    def extract_variant_parts(variant):
        if pd.isna(variant):
            return None
        match = re.match(r"^p\.(.)([0-9]+)(.)$", variant)
        if match:
            return match.groups()
        return None
    df['variant_parts'] = df[variant_column].apply(extract_variant_parts)

    unmatched_variants = df[df['variant_parts'].isna()].reset_index(drop=True)
    print(f"Non-pattern matching variants removed ({len(unmatched_variants)}):")
    print(unmatched_variants[variant_column])

    matched_df = df[df['variant_parts'].notna()].reset_index(drop=True)

    change = pd.DataFrame(
        matched_df['variant_parts'].tolist(), columns=['wtAA', 'pos', 'mutAA']
    )
    change['pos'] = pd.to_numeric(change['pos'], errors='coerce').astype('Int64')
    matched_df = pd.concat([matched_df.drop(columns=['variant_parts']), change], axis=1)
    print(f"Returning extracted variation information merged into dataframe with length {len(matched_df)},")
    print(f"and dataframe of variants which did not match extraction pattern (length: {len(unmatched_variants)})")
    return matched_df, unmatched_variants