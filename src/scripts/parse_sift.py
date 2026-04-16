import struct
import csv
import sys


def parse_sift(input_file: str, output_csv: str) -> None:
    """
    Parse .fvecs file into CSV.
    """

    with open(input_file, 'rb') as f, open(output_csv, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)

        while True:
            # Read dimension (int32, little endian)
            dim_bytes = f.read(4)
            if not dim_bytes:
                # EOF reached
                break

            d = struct.unpack('<i', dim_bytes)[0]

            # Read vector components
            vec_bytes = f.read(d * 4)

            # Unpack vector
            vec = struct.unpack(f"<{d}{'f'}", vec_bytes)

            # Write to CSV
            writer.writerow(vec)

    print(f"Finished writing to {output_csv}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python parse_sift.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]

    parse_sift(input_file, output_csv)
