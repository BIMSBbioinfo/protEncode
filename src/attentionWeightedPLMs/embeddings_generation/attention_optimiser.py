import numpy as np
from scipy.optimize import minimize

def total_loss(params, vectors, target_loss=0):
    alpha, beta = params
    total_loss_value = 0
    for vector in vectors:
        vector_sum = np.sum(vector)
        vector_std = np.std(vector)
        total_loss_value += -(alpha * vector_sum - beta * vector_std)
    penalty_loss = (total_loss_value - target_loss)**2
    return penalty_loss

def refined_loss_function(vector, alpha, beta):
    vector_sum = np.sum(vector)
    vector_std = np.std(vector)
    return -(alpha * vector_sum - beta * vector_std)

def optimiseAttention(vectors, num_returned, output_dir, initial_params=[10, 1], target_loss=0):
    result = minimize(total_loss, initial_params, args=(vectors, target_loss))
    optimal_alpha, optimal_beta = result.x
    print(f"Optimal alpha: {optimal_alpha}, Optimal beta: {optimal_beta}")
    losses = [refined_loss_function(vector, optimal_alpha, optimal_beta) for vector in vectors]
    top_indices = np.argsort(losses)[:num_returned]
    print(f"\nTop {num_returned} vectors with the lowest loss:")
    for i in top_indices:
        print(f"Vector {i} with loss {losses[i]}: {vectors[i]}")
    return top_indices