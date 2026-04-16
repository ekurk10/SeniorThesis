#!/usr/bin/env python3
"""
Run benchmarks for ALP, Chimp, and Gorilla on datasets.
For Chimp and Gorilla a decompression is performed on a sample of the original dataset.

Usage:
    python benchmark_runner.py --dataset <path> --output <output_csv> [--data-type double|float]
    
Example:
    python benchmark_runner.py --dataset ./datasets/test.csv --output ./results/benchmark_results_total.csv
"""

import argparse
import csv
import subprocess
import sys
from pathlib import Path
from typing import Dict, List, Optional
import tempfile


# Paths relative to project src
ALP_BUILD_DIR = "build"
ALP_BENCH_EXECUTABLE = "benchmarks/bench_your_dataset"
ALP_DATASET = "your_own_dataset.csv"
ALP_DATASET_RESULT = "your_own_dataset_result.csv"
JAR_PATH = "target/chimp-gorilla-benchmark-runner-shaded.jar"


# Helper functions to get paths
def get_alp_path() -> Path:
    current = Path(__file__).resolve().parent
    return current.parent / "ALP"


def get_java_root() -> Path:
    current = Path(__file__).resolve().parent
    return current / "java_benchmarks"


# Helper functions to parse results
def parse_alp_results(result_file: Path, data_type: str) -> Optional[Dict]:
    with open(result_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            total_values = int(row.get('vectors_count', 0)) * 1024
            compression_ratio = float(row.get('size(bits_per_value)', row.get('size', 0)))
            
            if 'total_compressed_bits' in row and row['total_compressed_bits']:
                total_compressed_bits = int(float(row.get('total_compressed_bits', 0)))
            else:
                total_compressed_bits = int(compression_ratio * total_values)
            
            return {
                'algorithm': 'alp',
                'data_type': row.get('data_type', data_type),
                'compression_ratio_bits_per_value': compression_ratio,
                'total_compressed_bits': total_compressed_bits,
                'decompression_speed_cycles_per_value': float(row.get('decompression_speed(cycles_per_value)', 0)),
                'compression_speed_cycles_per_value': float(row.get('compression_speed(cycles_per_value)', 0)),
                'total_values': total_values,
            }


def parse_java_results(stdout: str) -> List[Dict]:
    results = []
    lines = stdout.strip().split('\n')
    if not lines:
        return results
    
    for line in lines[1:]:
        if not line.strip():
            continue
        
        values = line.split(',')
        if len(values) >= 7:
            compression_ratio = float(values[2])
            compression_speed = float(values[3])
            decompression_speed = float(values[4])
            total_values = int(values[5])
            total_compressed_bits = int(compression_ratio * total_values)
            
            result = {
                'algorithm': values[0].strip(),
                'data_type': values[1].strip(),
                'compression_ratio_bits_per_value': compression_ratio,
                'total_compressed_bits': total_compressed_bits,
                'compression_speed_cycles_per_value': compression_speed,
                'decompression_speed_cycles_per_value': decompression_speed,
                'total_values': total_values,
            }
            results.append(result)

    return results


class BenchmarkRunner:    
    def __init__(self, dataset_path: str, output_path: str, data_type: str = "float"):
        """
        Initialize the benchmark runner.
        Stores instance variables to reuse in other functions instead of passing parameters
        """

        self.dataset_path = Path(dataset_path).resolve()
        self.output_path = Path(output_path)
        self.data_type = data_type

        # Ensure dataset and output paths exist
        if not self.dataset_path.exists():
            raise FileNotFoundError(f"Dataset not found: {self.dataset_path}")
        self.output_path.parent.mkdir(parents=True, exist_ok=True)


    def run_all_benchmarks(self) -> None:
        """Run all benchmarks and save results."""
        results = []
        
        # Run ALP
        alp_result = self.run_alp_benchmark()
        if alp_result:
            results.append(alp_result)
        else:
            print("ALP benchmark failed or produced no results")
        
        # Run Chimp and Gorilla
        java_results = self.run_chimp_gorilla_benchmark()
        results.extend(java_results)
        
        # Save results
        self.save_results(results)


    def run_alp_benchmark(self) -> Optional[Dict]:
        """Run ALP benchmark on the dataset."""
        
        print(f"Running ALP on {self.dataset_path}")

        try:
            alp_bench_root = get_alp_path()
            alp_build_dir = alp_bench_root / ALP_BUILD_DIR
            alp_bench_executable = alp_build_dir / ALP_BENCH_EXECUTABLE
            alp_bench_dir = alp_bench_root / "benchmarks"
            
            # Write dataset path and argument details into ALP benchmark setup
            spec_file = alp_bench_dir / ALP_DATASET
            file_type = "csv" if self.dataset_path.suffix.lower() in ['.csv', '.gz'] else "binary"
            
            with open(spec_file, 'w') as f:
                f.write("id,column_name,data_type,file_path,file_type\n")
                f.write(f"0,data,{self.data_type},{self.dataset_path},{file_type}\n")
                        
            result = subprocess.run(
                [str(alp_bench_executable)],
                cwd=str(alp_build_dir),
                capture_output=True,
                text=True,
                timeout=300
            )
            
            # Report any error
            if result.returncode != 0:
                print(f"ALP Benchmark failed with return code {result.returncode}")
                if result.stdout:
                    print(f"[ALP] stdout: {result.stdout[:300]}")
                if result.stderr:
                    print(f"[ALP] stderr: {result.stderr[:300]}")
                return None
            
            # Parse ALP results from result file
            alp_result_path = alp_bench_dir / ALP_DATASET_RESULT
            return parse_alp_results(alp_result_path, self.data_type)

        except Exception as e:
            print(f"ALP experienced this error: {e}")


    def run_chimp_gorilla_benchmark(self) -> List[Dict]:
        """Run Chimp and Gorilla on the dataset."""
        
        print(f"Starting Chimp and Gorilla on {self.dataset_path}")
        
        results = []
        sampled_path = None

        try:
            # Create sampled dataset for decompression
            sampled_path = self.create_sample_dataset()
            
            # Obtain JAR
            java_root = get_java_root()
            jar = java_root / JAR_PATH
            if not jar.exists():
                print(f"JAR not found at {jar}. Please build the Java project.")
                return results
            
            print(f"Running Chimp and Gorilla on {self.dataset_path}")

            result = subprocess.run(
                ["java", "-Xmx8g", "-jar", str(jar), str(self.dataset_path), str(sampled_path)],
                capture_output=True,
                text=True,
                timeout=1800
            )

            # Report any error
            if result.returncode != 0:
                print(f"[Chimp/Gorilla] Benchmark failed with return code {result.returncode}")
                if result.stderr:
                    print(f"[Chimp/Gorilla] stderr: {result.stderr[:500]}")
                return results
            
            results = parse_java_results(result.stdout)
            
        except Exception as e:
            print(f"Chimp or Gorilla experienced this error: {e}")
        
        return results


    def create_sample_dataset(self) -> str:
        """Create a sample of the dataset for Chimp and Gorilla decompression."""
        SAMPLE_SIZE = 100000
        
        # Read all of the original data
        data = []
        with open(self.dataset_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    try:
                        data.append(float(line))
                    except ValueError:
                        pass  # Skip header or non-numeric lines
        
        total_values = len(data)
        print(f"INFO: Total dataset size is {total_values} values")
        
        # If dataset is small just use it
        if total_values <= SAMPLE_SIZE:
            print(f"Dataset is small so no sampling needs to occur")
            return str(self.dataset_path)
        
        # Sample evenly across dataset
        step = total_values // SAMPLE_SIZE
        sampled_data = data[::step][:SAMPLE_SIZE]
        
        # Write sample to a temp file
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as tmp:
            for val in sampled_data:
                tmp.write(f"{val}\n")
            print(f"Sampled dataset created")
            return tmp.name

    
    def save_results(self, results: List[Dict]) -> None:
        """Save benchmark results to CSV."""
        if not results:
            return
        
        fieldnames = [
            'algorithm',
            'data_type',
            'compression_ratio_bits_per_value',
            'total_compressed_bits',
            'compression_speed_cycles_per_value',
            'decompression_speed_cycles_per_value',
            'total_values',
        ]
        
        with open(self.output_path, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for result in results:
                row = {fn: result.get(fn, '') for fn in fieldnames}
                writer.writerow(row)
        
        print(f"\nResults saved to {self.output_path} for your reference")
        print("\nBenchmark Results:")
        for result in results:
            print(f"Algorithm: {result['algorithm'].upper()}")
            print(f"  Data Type: {result['data_type']}")
            print(f"  Compression Ratio: {result['compression_ratio_bits_per_value']:.2f} bits/value")
            print(f"  Total Compressed Size: {result['total_compressed_bits']:,} bits ({result['total_compressed_bits'] / 8 / 1024 / 1024:.2f} MB)")
            print(f"  Total Values: {result['total_values']:,}")
            print(f"  Compression Speed: {result['compression_speed_cycles_per_value']:.2f} cycles/value")
            print(f"  Decompression Speed: {result['decompression_speed_cycles_per_value']:.2f} cycles/value")
            print()


def main():
    parser = argparse.ArgumentParser(
        description='Benchmark dataset on ALP, Chimp, and Gorilla'
    )
    parser.add_argument(
        '--dataset',
        required=True,
        help='Path to dataset file (CSV or binary)'
    )
    parser.add_argument(
        '--output',
        required=True,
        help='Path for output CSV results'
    )
    parser.add_argument(
        '--data-type',
        choices=['double', 'float'],
        default='float',
        help='Data type in dataset'
    )
    
    args = parser.parse_args()
    
    try:
        runner = BenchmarkRunner(args.dataset, args.output, args.data_type)
        runner.run_all_benchmarks()
    except Exception as e:
        print(f"[ERROR] {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
