package com.benchmarks;

import fi.iki.yak.ts.compression.gorilla.*;
import java.nio.ByteBuffer;

/**
 * Benchmarks Gorilla compression and decompression.
 * Gorilla value-only mode is used instead of timestamp compression
 */
public class GorillaBenchmark {

    private static final int WARMUP_ITERATIONS = 5;
    private static final int BENCHMARK_ITERATIONS = 10;

    /*
     * Benchmark Gorilla.
     */
    public static CompressionMetrics benchmarkDoublesHybrid(double[] fullData, double[] sampledData) {
        CompressionMetrics metrics = new CompressionMetrics("gorilla", "double");

        // Warmup on full data
        for (int i = 0; i < WARMUP_ITERATIONS; i++) {
            compressDoubles(fullData);
        }

        // Compression benchmark on dataset
        long compressionTimeNanos = 0;
        byte[] compressedData = null;
        for (int i = 0; i < BENCHMARK_ITERATIONS; i++) {
            long start = System.nanoTime();
            compressedData = compressDoubles(fullData);
            compressionTimeNanos += System.nanoTime() - start;
        }
        compressionTimeNanos /= BENCHMARK_ITERATIONS;

        // Decompression benchmark on sampled dataset
        byte[] sampledCompressedData = null;
        for (int i = 0; i < WARMUP_ITERATIONS; i++) {
            sampledCompressedData = compressDoubles(sampledData);
        }

        long decompressionTimeNanos = 0;
        for (int i = 0; i < BENCHMARK_ITERATIONS; i++) {
            long start = System.nanoTime();
            decompressDoubles(sampledCompressedData);
            decompressionTimeNanos += System.nanoTime() - start;
        }
        decompressionTimeNanos /= BENCHMARK_ITERATIONS;

        // Calculate compression metrics
        compressedData = compressDoubles(fullData);
        metrics.compressionRatioBitsPerValue = (compressedData.length * 8.0) / fullData.length;
        metrics.totalValueCount = fullData.length;

        // Convert nanoseconds to cycles
        double clockSpeed = SystemClockSpeed.getClockSpeedGHz();
        metrics.compressionSpeedCyclesPerValue = (compressionTimeNanos * clockSpeed) / (double) fullData.length;
        metrics.decompressionSpeedCyclesPerValue = (decompressionTimeNanos * clockSpeed) / (double) sampledData.length;
        metrics.totalTimeNanos = compressionTimeNanos + decompressionTimeNanos;

        return metrics;
    }

    /*
    * Applies Gorilla compression on a list of values.
    */
    private static byte[] compressDoubles(double[] data) {
        ByteBufferBitOutput bitOutput = new ByteBufferBitOutput();
        Compressor compressor = new Compressor(bitOutput);

        // Use Gorilla value compression
        for (double value : data) {
            compressor.addValue(value);
        }

        compressor.close();
        
        // Extract bytes properly
        ByteBuffer directBuffer = bitOutput.getByteBuffer();
        int size = directBuffer.position();
        byte[] result = new byte[size];
        
        // Start from the beginning of the buffer
        directBuffer.rewind();
        directBuffer.get(result);
        return result;
    }

    /*
    * Applies Gorilla decompression on a list of values.
    */
    private static double[] decompressDoubles(byte[] compressedData) {
        ByteBufferBitInput bitInput = new ByteBufferBitInput(ByteBuffer.wrap(compressedData));
        Decompressor decompressor = new Decompressor(bitInput);

        java.util.List<Double> values = decompressor.getValues();
        double[] result = new double[values.size()];
        for (int i = 0; i < values.size(); i++) {
            result[i] = values.get(i);
        }
        return result;
    }
}
