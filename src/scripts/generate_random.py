import numpy as np
import os
import sys


def generate_embeddings(num_vectors: int, dim: int, min_val: float, max_val: float, output_path: str, seed: int) -> None:
    """
    Generate random float32 embeddings.
    """

    np.random.seed(seed)

    embeddings = np.random.uniform(
        low=min_val,
        high=max_val,
        size=(num_vectors, dim)
    ).astype(np.float32)

    save_embeddings_csv(embeddings, output_path)
    print(f"Saved CSV to: {output_path}")


def save_embeddings_csv(embeddings, output_path):
    """
    Save embeddings to CSV with one vector per line.
    """

    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    with open(output_path, "w") as f:
        for row in embeddings:
            # Convert each float to string and join with commas
            line = ",".join(f"{x:.7g}" for x in row)
            f.write(line + "\n")


if __name__ == "__main__":
    if len(sys.argv) != 7:
        print("Usage: python generate_random.py <num_vectors> <dim> <min_val> <max_val> <output_path> <seed>")
        sys.exit(1)

    num_vectors = sys.argv[1]
    dim = sys.argv[2]
    min_val = sys.argv[3]
    max_val = sys.argv[4]
    output_path = sys.argv[5]
    seed = sys.argv[6]

    generate_embeddings(num_vectors, dim, min_val, max_val, output_path, seed)
