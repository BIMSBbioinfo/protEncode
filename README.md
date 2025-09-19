# Protein Encoding

Repository relating to generation of encoding of amino acid muations.

ProtEncode provides pipelines for **encoding protein mutations** using multiple schemes:  
- **Sequence preparation** → processes mutation data and UniProt sequences.  
- **Sample preparation** → generates sample-level encoding matrices (binary, multi-mutation, ESM-based).  
- **Embeddings generation** → coming soon.  

The package installs a CLI tool `protencode` for running the pipelines end-to-end.  

---

## 🚀 Installation

### Option 1: Using `conda`/`mamba` (recommended)

```bash
git clone https://github.com/BIMSBbioinfo/protEncode.git
cd protEncode

# Create environment
mamba env create -f environment.yml
conda activate protencode-env
```

This installs all dependencies (Python, PyTorch, transformers, etc.) and ProtEncode itself.  

### Option 2: Using `pip`

```bash
git clone https://github.com/BIMSBbioinfo/protEncode.git
cd protEncode

pip install -e .
```

This installs ProtEncode in *editable mode*, so changes to the source code are immediately reflected.  

---

## 🛠️ Usage

The package installs the command-line tool `protencode`. Run:

```bash
protencode --help
```

You should see available pipelines:

```
usage: protencode [-h] {embeddings,sample,sequence} ...

ProtEncode: encode protein mutations with different embedding schemes.

Available pipelines:
  • sequence   Prepare sequences from MAF files and UniProt
  • sample     Generate sample-level encoding matrices (binary, multi-mutation, ESM)
  • embeddings (coming soon) Generate embeddings for sequences
```

---

## 🔬 Pipelines

### 1️⃣ Sequence preparation

Processes mutation data (MAF/CSV) and UniProt sequences into finalised mutated sequences.

```bash
protencode sequence     --data ./data     --output ./output     --organism 9606     --email you@example.com     --min-length 200     --update
```

**Arguments**:
- `--data` (required) → directory with `.maf` or `.csv` mutation files.  
- `--output` (required) → output directory.  
- `--organism` → NCBI taxonomy ID (default: 9606 = human).  
- `--email` → contact email for UniProt downloads.  
- `--min-length` → minimum gene length filter (default: 200).  
- `--update` → force UniProt FASTA re-download.  

---

### 2️⃣ Sample preparation

Generates encoding matrices at the **sample level**.  

```bash
protencode sample --output ./output
```

By default, **all matrices** are generated.  
You can restrict output with flags:  

- Only binary matrix:
  ```bash
  protencode sample --output ./output --binary
  ```

- Only multi-mutation matrix:
  ```bash
  protencode sample --output ./output --multi
  ```

- Only ESM matrix (top-20 embeddings):
  ```bash
  protencode sample --output ./output --esm --top-n 20
  ```

**Arguments**:
- `--output` (required) → directory with outputs from sequence preparation.  
- `--top-n` → number of top embeddings to use for ESM (default: 10).  
- `--binary` → generate binary matrix.  
- `--multi` → generate multi-mutation matrix.  
- `--esm` → generate ESM attention matrix.  
- If **no flags are given**, all three are generated.  

---

### 3️⃣ Embeddings generation (coming soon)

Placeholder for embeddings pipeline:

```bash
protencode embeddings
```

---

## 📂 Output

- **Sequence preparation**  
  Produces mutated sequences, UniProt data, logs, and sample-to-sequence mappings in the specified `--output` directory.  

- **Sample preparation**  
  Produces encoding matrices saved in the output directory:  
  - `binary_matrix.*`  
  - `multi_matrix.*`  
  - `esm_topN_matrix.*`  

---

## 🐛 Troubleshooting

- **Command not found** → ensure your conda env is activated or pip install ran successfully.  
- **Missing module errors** → make sure `__init__.py` files exist in each subpackage. Reinstall with `pip install -e .`.  
- **Torch/CUDA errors** → check your GPU setup or install the CPU version of PyTorch via pip.  
- **UniProt download fails** → ensure you provide a valid email with `--email`.  

---

## 📜 License

MIT License.  
