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
    # Ensure the sampleFrames directory exists
    save_dir = os.path.join(output_dir, "sampleFrames")
    os.makedirs(save_dir, exist_ok=True)
    out_path = os.path.join(save_dir, "binaryEncoding.csv")
    print(f"Saving to {out_path}.")
    binary_matrix_df.to_csv(out_path, index=None)
    return binary_matrix_df