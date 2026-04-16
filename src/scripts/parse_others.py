import csv
import sys


def parse(input_file: str, output_file: str, dimensions: int) -> None:
    """
    Parse .txt file into CSV.
    Note: For FastText remove the first header
    """

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_writer = csv.writer(outfile)
        
        for line in infile:
            # Split each line by spaces
            parts = line.strip().split()
            
            floats = []

            # Traverse backwards to collect last floats
            for part in reversed(parts):
                try:
                    value = float(part)
                    floats.append(value)
                    if len(floats) == dimensions:
                        break
                except:
                    continue

            # Restore to the original order
            floats.reverse()

            # Write the floats to the CSV file
            csv_writer.writerow(floats)

    print(f"Successfully written to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python parse_others.py <input_file> <output_csv> <dimensions>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]
    dimensions = sys.argv[3]

    parse(input_file, output_csv, dimensions)
