import torch.nn.functional as F
import torch
import numpy as np

def ESM2Attention(attentions_tensor, stacked_embeddings, output_dir):
    attention_avg = attentions_tensor.mean(dim=0)
    attention_weights = attention_avg.mean(dim=1)
    attention_weights = F.softmax(attention_weights, dim=-1)
    weighted_sum = torch.bmm(attention_weights, stacked_embeddings)
    pooled_embeddings = weighted_sum.mean(dim=1)
    WPE_np = pooled_embeddings.numpy()
    print(f"Saving weighted pooled embeddings to {output_dir}")
    np.save(f"{output_dir}/esm2_weighted_pooledembeddings_maxlen200.npy", WPE_np)
    return WPE_np.transpose()