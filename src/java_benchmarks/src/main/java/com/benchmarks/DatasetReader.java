package com.benchmarks;

import java.io.*;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.ArrayList;
import java.util.List;

/**
 * Read datasets in CSV or binary format.
 */
public class DatasetReader {

    /**
     * Read doubles from a CSV file.
     */
    public static double[] readDoublesFromCsv(String filePath) throws IOException {
        List<Double> values = new ArrayList<>();
        
        try (BufferedReader reader = new BufferedReader(new FileReader(filePath))) {
            String line;
            // Skip header if present
            boolean firstLine = true;
            while ((line = reader.readLine()) != null) {
                if (firstLine) {
                    firstLine = false;
                    try {
                        Double.parseDouble(line.trim());
                    } catch (NumberFormatException e) {
                        firstLine = false;
                        continue;
                    }
                }
                
                line = line.trim();
                if (!line.isEmpty()) {
                    try {
                        values.add(Double.parseDouble(line));
                    } catch (NumberFormatException e) {
                        // Skip non-numeric lines
                    }
                }
            }
        }
        
        double[] result = new double[values.size()];
        for (int i = 0; i < values.size(); i++) {
            result[i] = values.get(i);
        }
        return result;
    }

    /*
     * Read doubles from a binary file (little-endian doubles).
     */
    public static double[] readDoublesFromBinary(String filePath) throws IOException {
        byte[] bytes = readAllBytes(filePath);
        ByteBuffer buffer = ByteBuffer.wrap(bytes).order(ByteOrder.LITTLE_ENDIAN);
        
        double[] result = new double[bytes.length / 8];
        for (int i = 0; i < result.length; i++) {
            result[i] = buffer.getDouble();
        }
        return result;
    }

    /*
     * Read all bytes from a file
     */
    private static byte[] readAllBytes(String filePath) throws IOException {
        File file = new File(filePath);
        byte[] bytes = new byte[(int) file.length()];
        try (FileInputStream fis = new FileInputStream(file)) {
            fis.read(bytes);
        }
        return bytes;
    }

    /*
     * Detect file type based on extension.
     */
    public static String detectFileType(String filePath) {
        if (filePath.endsWith(".csv") || filePath.endsWith(".csv.gz")) {
            return "csv";
        } else if (filePath.endsWith(".bin") || filePath.endsWith(".binary")) {
            return "binary";
        }
        return "unknown";
    }
}
