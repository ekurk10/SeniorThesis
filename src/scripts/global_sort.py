import csv
import time
import sys
from system_clock import get_clock_speed_ghz


def sort_values(input_file: str, output_file: str) -> None:
    """
    Sort all floats from the CSV file.
    Takes in a 2-dimensional input.
    """

    with open(input_file, "r") as infile:
        reader = csv.reader(infile)
        data = [list(map(float, row)) for row in reader]

    # Flatten the 2D list into a 1D list of floats
    all_floats = [float(x) for row in data for x in row]
    total_values = len(all_floats)

    # Measure sort time
    start_time = time.perf_counter()
    sorted_floats = sorted(all_floats)
    sort_time = (time.perf_counter() - start_time) * 1e9  # Convert to nanoseconds

    # Create a mapping to reverse the sort
    sorted_with_indices = sorted(enumerate(all_floats), key=lambda x: x[1])
    unsort_indices = [0] * total_values
    for new_idx, (original_idx, _) in enumerate(sorted_with_indices):
        unsort_indices[original_idx] = new_idx

    # Measure unsort time
    start_time = time.perf_counter()
    unsorted_floats = [0] * total_values
    for original_idx, sorted_idx in enumerate(unsort_indices):
        unsorted_floats[original_idx] = sorted_floats[sorted_idx]
    unsort_time = (time.perf_counter() - start_time) * 1e9  # Convert to nanoseconds

    # Reshape the sorted list back into vectors
    n_cols = len(data[0])
    sorted_data = [sorted_floats[i:i + n_cols] for i in range(0, len(sorted_floats), n_cols)]

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
        print("Usage: python global_sort.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]

    sort_values(input_file, output_csv)
