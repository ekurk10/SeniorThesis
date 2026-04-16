import struct
from collections import defaultdict
import time
import sys
from system_clock import get_clock_speed_ghz

"""
Takes in a 1-dimensional input.
"""

def float_to_bits(f):
    return struct.unpack('>I', struct.pack('>f', f))[0]


def bits_to_float(b):
    return struct.unpack('>f', struct.pack('>I', b))[0]


def compute_bins(values, num_bins):
    """
    Assign each value to a bin.
    """

    vmin = min(values)
    vmax = max(values)

    # Avoid division by zero
    if vmax == vmin:
        bin_numbers = [0] * len(values)
        bins = {0: values.copy()}
        return bin_numbers, bins

    bin_width = (vmax - vmin) / num_bins

    bin_numbers = []
    bins = defaultdict(list)

    for v in values:
        b = int((v - vmin) / bin_width)
        if b == num_bins:  # edge case for max value
            b -= 1

        bin_numbers.append(b)
        bins[b].append(v)

    return bin_numbers, bins


def encode(values, num_bins=256):
    """
    Convert bins into a 1-dimensional array.
    """
    bin_numbers, bins = compute_bins(values, num_bins)

    # Flatten bins in order
    bin_values = []
    for b in range(num_bins):
        if b in bins:
            bin_values.append(bins[b])
        else:
            bin_values.append([])

    return bin_numbers, bin_values


def decode(bin_numbers, bin_values):
    """
    Reconstruct original order.
    """
    # Track read position per bin
    bin_ptrs = [0] * len(bin_values)

    output = []

    for b in bin_numbers:
        v = bin_values[b][bin_ptrs[b]]
        bin_ptrs[b] += 1
        output.append(v)

    return output


def read_csv_floats(path):
    with open(path, 'r') as f:
        return [float(line.strip()) for line in f if line.strip()]


def write_bin_numbers(path, data):
    with open(path, 'w') as f:
        for x in data:
            f.write(f"{x}\n")


def write_bins(path, bin_values):
    with open(path, 'w') as f:
        for b in bin_values:
            for v in b:
                f.write(f"{v}\n")


def read_bins(path):
    bin_values = []
    with open(path, 'r') as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        size = int(lines[i].strip())
        i += 1
        vals = []
        for _ in range(size):
            vals.append(float(lines[i].strip()))
            i += 1
        bin_values.append(vals)

    return bin_values


if __name__ == "__main__":
    if len(sys.argv) != 5:
        print("Usage:")
        print("  encode: python bin_sort.py <input.csv> <output_bin_numbers.csv> <output_bins.csv> <num_bins>")
        sys.exit(1)

    input_path = sys.argv[1]
    bin_numbers_path = sys.argv[2]
    bins_path = sys.argv[3]
    num_bins = int(sys.argv[4])

    values = read_csv_floats(input_path)
    total_values = len(values)

    # Measure encode time
    start_time = time.perf_counter()
    bin_numbers, bin_values = encode(values, num_bins=num_bins)
    encode_time = (time.perf_counter() - start_time) * 1e9

    # Measure decode time
    start_time = time.perf_counter()
    decoded_values = decode(bin_numbers, bin_values)
    decode_time = (time.perf_counter() - start_time) * 1e9

    write_bin_numbers(bin_numbers_path, bin_numbers)
    write_bins(bins_path, bin_values)

    # Calculate metrics
    clock_speed = get_clock_speed_ghz()
    encode_cycles_per_value = (encode_time * clock_speed) / total_values
    decode_cycles_per_value = (decode_time * clock_speed) / total_values

    print(f"Encoded data written to {bin_numbers_path} and {bins_path}")
    print(f"System clock speed: {clock_speed:.2f} GHz")
    print(f"Total values: {total_values}")
    print(f"Encode time: {encode_time:.2f} ns, Cycles per value: {encode_cycles_per_value:.2f}")
    print(f"Decode time: {decode_time:.2f} ns, Cycles per value: {decode_cycles_per_value:.2f}")
