import pandas as pd

def createBinaryMatrix(Samples, output_dir):
    print("Creating binary frame...")
    Samples['samples'] = Samples['sample_id'].str.split(';')
    expanded_df = Samples.explode('samples', ignore_index=True)
    expanded_df['binary_variant'] = expanded_df['variant'].apply(lambda x: 0 if x == 'WT' else 1)
    binary_matrix_df = expanded_df.pivot_table(index='samples', columns='geneName', 
                                                values='binary_variant', aggfunc='first').fillna(0)
    binary_matrix_df.columns.name = None
    binary_matrix_df = binary_matrix_df.reset_index()
    print(f"Saving to {output_dir}.")
    binary_matrix_df.to_csv(f"{output_dir}/sampleFrames/binaryEncoding.csv", index=None)
    return binary_matrix_df