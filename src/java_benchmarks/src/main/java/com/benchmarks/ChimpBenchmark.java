package com.benchmarks;

import gr.aueb.delorean.chimp.Chimp;
import gr.aueb.delorean.chimp.ChimpDecompressor;

/*
 * Benchmarks Chimp compression and decompression.
 * Metrics are normalized to per value for comparison with ALP.
 */
public class ChimpBenchmark {

    private static final int WARMUP_ITERATIONS = 5;
    private static final int BENCHMARK_ITERATIONS = 10;

    /*
     * Benchmark Chimp
     */
    public static CompressionMetrics benchmarkDoublesHybrid(double[] fullData, double[] sampledData) {
        CompressionMetrics metrics = new CompressionMetrics("chimp", "double");

        // Warmup on full data
        for (int i = 0; i < WARMUP_ITERATIONS; i++) {
            try {
                compressDoubles(fullData);
            } catch (Exception e) {
                e.printStackTrace();
            }
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
    * Applies Chimp compression on a list of values.
    */
    private static byte[] compressDoubles(double[] data) {
        Chimp chimp = new Chimp();
        for (double value : data) {
            chimp.addValue(value);
        }
        chimp.close();
        return chimp.getOut();
    }

    /*
    * Applies Chimp decompression on a list of values.
    */
    private static double[] decompressDoubles(byte[] compressedData) {
        ChimpDecompressor decompressor = new ChimpDecompressor(compressedData);
        java.util.List<Double> values = decompressor.getValues();
        double[] result = new double[values.size()];
        for (int i = 0; i < values.size(); i++) {
            result[i] = values.get(i);
        }
        return result;
    }
}
