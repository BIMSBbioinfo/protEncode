import os
import subprocess

def get_gpu_info():
    """
    Runs the `nvidia-smi` command to fetch GPU usage information.
    :return: Output of nvidia-smi in CSV format (index, memory.total, memory.used), or None if an error occurs.
    """
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=index,memory.total,memory.used', '--format=csv,noheader,nounits'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        output = result.stdout.decode('utf-8').strip()
        if result.returncode != 0:
            print(f"Error querying GPU information: {result.stderr.decode('utf-8')}")
            return None
        return output
    except FileNotFoundError:
        print("nvidia-smi command not found. Make sure NVIDIA drivers and CUDA are properly installed.")
        return None

def parse_gpu_info(output):
    """
    Parses the output from nvidia-smi to extract GPU index, total memory, used memory, and free memory.
    :param output: The raw output from nvidia-smi in CSV format.
    :return: A list of dictionaries with GPU information.
    """
    gpu_info = []
    for line in output.split('\n'):
        gpu_idx, total_mem, used_mem = map(int, line.split(','))
        free_mem = total_mem - used_mem
        gpu_info.append({
            'gpu_idx': gpu_idx,
            'total_mem': total_mem,
            'used_mem': used_mem,
            'free_mem': free_mem
        })
    return gpu_info

def select_best_gpus(gpu_info, num_gpus=1):
    """
    Selects the GPUs with the most available memory.
    :param gpu_info: List of dictionaries containing GPU information.
    :param num_gpus: Number of GPUs to select.
    :return: List of indices of the GPUs with the most free memory.
    """
    # Sort GPUs by available memory in descending order and take the top `num_gpus`
    sorted_gpus = sorted(gpu_info, key=lambda x: x['free_mem'], reverse=True)
    best_gpus = [gpu['gpu_idx'] for gpu in sorted_gpus[:num_gpus]]
    return best_gpus

def set_cuda_visible_devices(gpu_indices):
    """
    Sets the CUDA_VISIBLE_DEVICES environment variable to limit processes to chosen GPUs.
    :param gpu_indices: List of GPU indices to set.
    """
    os.environ["CUDA_VISIBLE_DEVICES"] = ','.join(map(str, gpu_indices))
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "expandable_segments:True"
    print(f"CUDA_VISIBLE_DEVICES set to GPUs {', '.join(map(str, gpu_indices))}")

def select_and_set_best_gpus():
    """
    Main function to query GPUs, select the best ones, and allow user to confirm or override the choice.
    :return: The indices of the selected GPUs, or None if no GPUs were selected.
    """
    gpu_info_str = get_gpu_info()
    if not gpu_info_str:
        print("Unable to fetch GPU information.")
        return None
    
    gpu_info = parse_gpu_info(gpu_info_str)
    
    print("Available GPUs:")
    for gpu in gpu_info:
        print(f"GPU {gpu['gpu_idx']}: {gpu['free_mem']} MiB free out of {gpu['total_mem']} MiB")
    
    num_gpus = int(input("Enter the number of GPUs you want to use: ").strip())
    best_gpu_indices = select_best_gpus(gpu_info, num_gpus=num_gpus)
    print(f"Automatically selecting GPUs {', '.join(map(str, best_gpu_indices))} with the most available memory.")
    
    # Ask user to confirm or override
    while True:
        user_input = input(f"Do you want to use GPUs {', '.join(map(str, best_gpu_indices))}? (y/n or specify different GPU indices separated by commas): ").strip().lower()
        if user_input == 'y':
            # User is happy with the automatic selection
            set_cuda_visible_devices(best_gpu_indices)
            return best_gpu_indices
        elif user_input == 'n':
            # Ask user to enter other GPU indices
            override_gpus = input("Enter the GPU indices you want to use (comma-separated): ").strip()
            override_gpu_indices = [int(idx) for idx in override_gpus.split(',') if idx.isdigit()]
            if all(idx in [gpu['gpu_idx'] for gpu in gpu_info] for idx in override_gpu_indices):
                print(f"Overriding choice. Setting GPUs {', '.join(map(str, override_gpu_indices))}.")
                set_cuda_visible_devices(override_gpu_indices)
                return override_gpu_indices
            else:
                print(f"Invalid GPU indices. Please enter valid GPU indices from the list: {[gpu['gpu_idx'] for gpu in gpu_info]}")
        else:
            print("Invalid input. Please enter 'y' to confirm or 'n' to override.")