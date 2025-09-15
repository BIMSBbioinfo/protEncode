import numpy as np
import torch

def processESM2Embeddings(embds, attentions, output_dir, save_setting=True):
    stacked_embeddings = torch.stack(embds)
    attentions_tensor = torch.stack(attentions, dim=0)
    preX = stacked_embeddings.numpy()
    pooled_embeddings = torch.mean(stacked_embeddings, dim=1)
    X = pooled_embeddings.numpy()
    if save_setting == True:
        np.save(f"{output_dir}/esm2_fullseq_preaveraged_embeddings.npy", preX)
        np.save(f"{output_dir}/esm2_fullseq_averaged_embeddings.npy", X)
    return stacked_embeddings, attentions_tensor, X

def processProtTransEmbeddings(embds, output_dir, save_setting=True):
    stacked_embeddings = torch.stack(embds)
    preX = stacked_embeddings.numpy()
    pooled_embeddings = torch.mean(stacked_embeddings, dim=1)
    X = pooled_embeddings.numpy()
    if save_setting == True:
        np.save(f"{output_dir}/prottrans_fullseq_preaveraged_embeddings.npy", preX)
    return stacked_embeddings, X