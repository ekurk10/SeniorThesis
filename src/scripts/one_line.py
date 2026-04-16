import csv
import sys


def one_line(input_file: str, output_file: str) -> None:
    """
    Serialize CSV file with vectors to a single dimension.
    Takes in a 2-dimensional input.
    """

    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        csv_reader = csv.reader(infile)
        csv_writer = csv.writer(outfile)
        
        for row in csv_reader:
            for value in row:
                csv_writer.writerow([float(value)])

    print(f"Successfully written individual floats to {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python one_line.py <input_file> <output_csv>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_csv = sys.argv[2]

    one_line(input_file, output_csv)
