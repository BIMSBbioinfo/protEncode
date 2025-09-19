import pandas as pd
import numpy as np
import os

def sampleJoin(Samples, Top10Embd):
    Top10DF = pd.DataFrame(Top10Embd, columns=[f'Top{i}' for i in range(1, Top10Embd.shape[1] + 1)])
    SamplesCombined = pd.concat([Samples, Top10DF], axis=1)
    SamplesCombined['samples'] = SamplesCombined['sample_id'].str.split(';')
    SamplesExpanded = SamplesCombined.explode('samples', ignore_index=True)
    return SamplesExpanded

def create_top_matrix(Samples, Top10Embd, output_dir, top_n):
    expanded_df = sampleJoin(Samples, Top10Embd)
    melted_df = expanded_df.melt(id_vars=['samples', 'geneName'], 
                                 value_vars=[f'Top{i}' for i in range(1, top_n+1)],
                                 var_name='Top', value_name='Score')
    melted_df['gene_Top'] = melted_df['geneName'] + '.' + melted_df['Top']
    matrix_df = melted_df.pivot_table(index='samples', columns='gene_Top', values='Score', aggfunc='first')
    # Ensure the sampleFrames directory exists
    save_dir = os.path.join(output_dir, "sampleFrames")
    os.makedirs(save_dir, exist_ok=True)
    out_path = os.path.join(save_dir, "esmTop10Encoding.csv")
    print(f"Saving to {out_path}.")
    matrix_df_reset = matrix_df.reset_index()
    matrix_df_reset.to_csv(out_path, index=False)
    return matrix_df