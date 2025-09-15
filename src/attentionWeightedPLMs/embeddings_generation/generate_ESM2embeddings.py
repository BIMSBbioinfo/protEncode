import os
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
import torch
from transformers import AutoTokenizer, AutoModel
import torch.nn as nn
from tqdm import tqdm

def generateESM2(model_name, sequence_data, batch_size, max_length):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Using device {device}")
    model = nn.DataParallel(model)
    model = model.to(device)
    model.eval()
    pro_seq = sequence_data['sequence'].tolist()
    embds = []
    attentions = []
    for i in tqdm(range(0, len(pro_seq), batch_size), desc="Processing Sequences"):
        batch_seqs = pro_seq[i:i+batch_size]
        inputs = tokenizer(batch_seqs, return_tensors='pt', padding='max_length', max_length=max_length, truncation=True)
        input_ids = inputs['input_ids'].to(device)
        attention_mask = inputs['attention_mask'].to(device)
        with torch.no_grad():
            embeddings = model(input_ids=input_ids, attention_mask=attention_mask, output_attentions=True)
        embds.extend(embeddings.last_hidden_state.cpu())
        if not attentions:
            attentions = [attn.cpu() for attn in embeddings.attentions]
        else:
            cpu_attentions = [attn.cpu() for attn in embeddings.attentions]
            attentions = [torch.cat((attn_layer, cpu_attentions[i]), dim=0) 
                        for i, attn_layer in enumerate(attentions)]
        del input_ids, attention_mask, embeddings
        torch.cuda.empty_cache()
    return embds, attentions