import csv
import time
import sys
from system_clock import get_clock_speed_ghz


def sort_rows(input_file: str, output_file: str) -> None:
    """
    Sort dimensions of each vector embedding from CSV file.
    """

    # Read and process each row individually
    with open(input_file, "r") as infile:
        reader = csv.reader(infile)
        data = [list(map(float, row)) for row in reader]

    total_values = sum(len(row) for row in data)

    # Measure sort time
    start_time = time.perf_counter()
    sorted_data = [sorted(row) for row in data]
    sort_time = (time.perf_counter() - start_time) * 1e9  # Convert to nanoseconds

    # Create a mapping to reverse the sort for each row
    unsort_indices = []
    for row in data:
        sorted_with_idx = sorted(enumerate(row), key=lambda x: x[1])
        row_unsort_indices = [0] * len(row)
        for new_idx, (original_idx, _) in enumerate(sorted_with_idx):
            row_unsort_indices[original_idx] = new_idx
        unsort_indices.append(row_unsort_indices)

    # Measure unsort time
    start_time = time.perf_counter()
    unsorted_data = []
    for sorted_row, row_unsort_idx in zip(sorted_data, unsort_indices):
        unsorted_row = [0] * len(sorted_row)
        for original_idx, sorted_idx in enumerate(row_unsort_idx):
            unsorted_row[original_idx] = sorted_row[sorted_idx]
        unsorted_data.append(unsorted_row)
    unsort_time = (time.perf_counter() - start_time) * 1e9  # Convert to nanoseconds

    # Write the sorted data to a new CSV
    with open(output_file, "w", newline="") as outfile:
        writer = csv.writer(outfile)
        writer.writerows(sorted_data)

    # Calculate metrics
    clock_speed = get_clock_speed_ghz()
    sort_cycles_per_value = (sort_time * clock_speed) / total_values
    unsort_cycles_per_value = (unsort_time * clock_speed) / total_values

    print(f"Sorted data written to {output_file}")
    print(f"System clock speed: {clock_speed:.2f} GHz")
    print(f"Total values: {total_values}")
    print(f"Sort time: {sort_time:.2f} ns, Cycles per value: {sort_cycles_per_value:.2f}")
    print(f"Unsort time: {unsort_time:.2f} ns, Cycles per value: {unsort_cycles_per_value:.2f}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python row_sort.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]

    sort_rows(input_file, output_csv)
