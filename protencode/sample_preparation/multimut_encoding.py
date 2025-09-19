import pandas as pd

def createMultiMutationMatrix(Samples, output_dir):
    print("Creating multi-mutation frame...")
    Samples['samples'] = Samples['sample_id'].str.split(';')
    expanded_df = Samples.explode('samples', ignore_index=True)
    expanded_df['mutation_count'] = expanded_df['variant'].apply(lambda x: 0 if x == 'WT' else 1)
    mutation_count_df = expanded_df.groupby(['samples', 'geneName'])['mutation_count'].sum().reset_index()
    mutation_matrix_df = mutation_count_df.pivot_table(index='samples', columns='geneName', 
                                                        values='mutation_count', aggfunc='first').fillna(0)
    mutation_matrix_df.columns.name = None
    mutation_matrix_df = mutation_matrix_df.reset_index()
    print(f"Saving to {output_dir}.")
    mutation_matrix_df.to_csv(f"{output_dir}/sampleFrames/multimutEncoding.csv", index=None)
    return mutation_matrix_df