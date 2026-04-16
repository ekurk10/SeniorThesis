package com.benchmarks;

import java.io.IOException;

/**
 * Doubles are used as values for compatability with Chimp and Gorilla
 * Usage: java -jar unified-benchmark-jar-with-dependencies.jar <dataset-path> <sampled-dataset-path>
 */
public class BenchmarkRunner {

    public static void main(String[] args) throws IOException {
        if (args.length < 1) {
            System.err.println("Usage: java -jar unified-benchmark.jar <dataset-path> <sampled-dataset-path>");
            System.exit(1);
        }

        // Parse arguments
        String datasetPath = args[0];
        String sampledDatasetPath = args[1];
        String fileType = DatasetReader.detectFileType(datasetPath);

        System.out.println(CompressionMetrics.getHeader());

        try {
            // Parse data as doubles for Chimp and Gorilla
            double[] fullData;
            if ("csv".equals(fileType)) {
                fullData = DatasetReader.readDoublesFromCsv(datasetPath);
            } else {
                fullData = DatasetReader.readDoublesFromBinary(datasetPath);
            }

            String sampledFileType = DatasetReader.detectFileType(sampledDatasetPath);
            double[] sampledData;
            if ("csv".equals(sampledFileType)) {
                sampledData = DatasetReader.readDoublesFromCsv(sampledDatasetPath);
            } else {
                sampledData = DatasetReader.readDoublesFromBinary(sampledDatasetPath);
            }

            // Obtain and print metrics
            CompressionMetrics chimpMetrics = ChimpBenchmark.benchmarkDoublesHybrid(fullData, sampledData);
            System.out.println(chimpMetrics);

            CompressionMetrics gorillaMetrics = GorillaBenchmark.benchmarkDoublesHybrid(fullData, sampledData);
            System.out.println(gorillaMetrics);
        } catch (IOException e) {
            System.err.println("Error: " + e.getMessage());
            e.printStackTrace();
            System.exit(1);
        }
    }
}
