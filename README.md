# Senior Thesis
Entire source code for the senior thesis. Instructions for getting started are included.

## Requirements
- A version of Python3
- Java 11
- Latest g++ version
- Latest cmake version
- Latest maven version

## Setup and Compiling Dependencies
In the src directory run `bash setup.sh`

## Running a Benchmark
`python benchmark_runner.py --dataset ./datasets/input.csv --output ./results/results.csv`

## Scripts
Parsing scripts are included that were used for the datasets.
The remaining scripts are used to encode CSV vector data.
All scripts expect a 2-dimensional input except for bin_sort.py which expects a 1-dimensional input
where the vectors are already in a 1-dimensional format.

## Datasets
The datasets used in the evaluation can be found here:
- GloVe: https://nlp.stanford.edu/projects/glove/
- FastText: https://fasttext.cc/docs/en/english-vectors.html
- SIFT: http://corpus-texmex.irisa.fr/

Use generate_random.py with seed 100 to generate the Random 32 dataset used or other random datasets.

## Credits
The original ALP repository is found at https://github.com/cwida/ALP \
The original Chimp repository with Gorilla is found at https://github.com/panagiotisl/chimp \
The Gorilla repository Chimp uses is found at https://github.com/burmanm/gorilla-tsc
