import csv
import time
import sys
from system_clock import get_clock_speed_ghz


def transpose_vectors(input_file: str, output_file: str) -> None:
    """
    Transpose vector embeddings from CSV file.
    Takes in a 2-dimensional input.
    """

    # Read all rows
    with open(input_file, "r") as infile:
        reader = csv.reader(infile)
        data = [list(map(float, row)) for row in reader]

    total_values = sum(len(row) for row in data)

    # Measure encode time
    start_time = time.perf_counter()
    transposed = list(zip(*data))
    transpose_time = (time.perf_counter() - start_time) * 1e9

    # Measure decode time
    start_time = time.perf_counter()
    untransposed = list(zip(*transposed))
    untranspose_time = (time.perf_counter() - start_time) * 1e9

    # Write transposed data
    with open(output_file, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        for row in transposed:
            writer.writerow(row)

    # Calculate metrics
    clock_speed = get_clock_speed_ghz()
    transpose_cycles_per_value = (transpose_time * clock_speed) / total_values
    untranspose_cycles_per_value = (untranspose_time * clock_speed) / total_values

    print(f"Transposed data written to {output_file}")
    print(f"System clock speed: {clock_speed:.2f} GHz")
    print(f"Total values: {total_values}")
    print(f"Transpose time: {transpose_time:.2f} ns, Cycles per value: {transpose_cycles_per_value:.2f}")
    print(f"Untranspose time: {untranspose_time:.2f} ns, Cycles per value: {untranspose_cycles_per_value:.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python column_order.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]

    transpose_vectors(input_file, output_csv)
