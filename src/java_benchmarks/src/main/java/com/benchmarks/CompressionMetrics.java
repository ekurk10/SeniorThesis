package com.benchmarks;

/*
 * Benchmark metrics to report.
 */
public class CompressionMetrics {
    public String algorithm;
    public String dataType;
    public double compressionRatioBitsPerValue;
    public double compressionSpeedCyclesPerValue;
    public double decompressionSpeedCyclesPerValue;
    public long totalValueCount;
    public long totalTimeNanos;

    public CompressionMetrics(String algorithm, String dataType) {
        this.algorithm = algorithm;
        this.dataType = dataType;
    }

    @Override
    public String toString() {
        return String.format(
            "%s,%s,%.2f,%.2f,%.2f,%d,%d",
            algorithm,
            dataType,
            compressionRatioBitsPerValue,
            compressionSpeedCyclesPerValue,
            decompressionSpeedCyclesPerValue,
            totalValueCount,
            totalTimeNanos
        );
    }

    public static String getHeader() {
        return "algorithm,data_type,compression_ratio_bits_per_value,compression_speed_cycles_per_value,decompression_speed_cycles_per_value,total_values,total_time_nanos";
    }
}
