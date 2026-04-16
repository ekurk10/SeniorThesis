#!/bin/bash
# Setup script for benchmarking ALP, Chimp, and Gorilla

set -e  # Exit on error

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "Checking prerequisites..."

commands=("java" "mvn" "cmake" "g++")
for cmd in "${commands[@]}"; do
    if ! command -v "$cmd" &> /dev/null; then
        echo "ERROR: $cmd is not installed"
        exit 1
    fi
done

java_version=$(java -version 2>&1 | grep -oE '[0-9]+' | head -1)
if [ "$java_version" -lt 11 ]; then
    echo "ERROR: Java 11 or higher required (found version $java_version)"
    exit 1
fi

# Build Chimp from source
echo "Building Chimp..."
if [ ! -f "$PROJECT_ROOT/chimp/target/chimp-1.0.0.jar" ]; then
    cd "$PROJECT_ROOT/chimp"
    mvn clean package -DskipTests -q
    cd "$SCRIPT_DIR"
    echo "Chimp built successfully"
else
    echo "Chimp already built"
fi
echo ""

# Build Java benchmarks
echo "Building Java files..."
cd "$SCRIPT_DIR/java_benchmarks"
mvn clean package -DskipTests -q
echo "Java benchmark built successfully"
cd "$SCRIPT_DIR"
echo ""

# Build ALP
echo "Building ALP..."
if [ ! -f "$PROJECT_ROOT/ALP/build/benchmarks/bench_your_dataset" ]; then
    echo "  Building ALP..."
    cd "$PROJECT_ROOT/ALP"
    cmake -DCMAKE_C_COMPILER=clang -DCMAKE_CXX_COMPILER=clang++ -DALP_BUILD_BENCHMARKING=ON -DALP_ENABLE_VERBOSE_OUTPUT=ON -DCMAKE_BUILD_TYPE=Release -S . -B build
    cmake --build build
    echo "ALP built successfully"
    cd "$SCRIPT_DIR"
else
    echo "ALP already built"
fi
echo ""

# Create directory structure
echo "Creating directories..."
mkdir -p "$SCRIPT_DIR/datasets"
mkdir -p "$SCRIPT_DIR/results"
echo "Directories created"
echo ""

echo "Setup Complete!"
