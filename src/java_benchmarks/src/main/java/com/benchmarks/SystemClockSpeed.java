package com.benchmarks;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileReader;
import java.io.InputStreamReader;

/*
 * Detect system clock speed.
 */
public class SystemClockSpeed {
    
    private static final String LINUX_FILE = "/proc/cpuinfo";
    private static final String MAC_COMMAND = "sysctl -n hw.cpufrequency";
    private static final String[] WINDOWS_COMMAND = new String[]{"wmic", "cpu", "get", "MaxClockSpeed", "/value"};

    private static final double DEFAULT_CLOCK_SPEED_GHZ = 3.0;
    private static Double clockSpeed = null;
    
    /*
     * Get the system clock speed in GHz for various systems.
     */
    public static double getClockSpeedGHz() {
        if (clockSpeed != null) {
            return clockSpeed;
        }
        
        String os = System.getProperty("os.name").toLowerCase();
        
        if (os.contains("linux")) {
            clockSpeed = getLinuxClockSpeed();
        } else if (os.contains("mac")) {
            clockSpeed = getMacClockSpeed();
        } else if (os.contains("win")) {
            clockSpeed = getWindowsClockSpeed();
        }
        
        if (clockSpeed == null || clockSpeed <= 0) {
            clockSpeed = DEFAULT_CLOCK_SPEED_GHZ;
        }
        
        return clockSpeed;
    }
    
    /*
     * CPU frequency in Linux is at /proc/cpuinfo
     */
    private static Double getLinuxClockSpeed() {
        try (BufferedReader br = new BufferedReader(new FileReader(LINUX_FILE))) {
            String line;
            while ((line = br.readLine()) != null) {
                if (line.startsWith("cpu MHz")) {
                    String[] parts = line.split(":");
                    if (parts.length > 1) {
                        double mhz = Double.parseDouble(parts[1].trim());
                        return mhz / 1000.0; // Convert to GHz
                    }
                }
            }
        } catch (Exception e) {
            System.err.println("Get Linux CPU frequency failed: " + e.getMessage());
        }
        return null;
    }
    
    /*
     * Get CPU frequency from macOS using sysctl
     */
    private static Double getMacClockSpeed() {
        try {
            Process process = Runtime.getRuntime().exec(MAC_COMMAND);
            try (BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line = br.readLine();
                if (line != null && !line.isEmpty()) {
                    long hz = Long.parseLong(line.trim());
                    return hz / 1e9;
                }
            }
            process.waitFor();
        } catch (Exception e) {
            System.err.println("Get macOS CPU frequency failed: " + e.getMessage());
        }
        return null;
    }
    
    /*
     * Get CPU frequency from Windows using WMI
     */
    private static Double getWindowsClockSpeed() {
        try {
            Process process = Runtime.getRuntime().exec(WINDOWS_COMMAND);
            try (BufferedReader br = new BufferedReader(new InputStreamReader(process.getInputStream()))) {
                String line;
                while ((line = br.readLine()) != null) {
                    if (line.startsWith("MaxClockSpeed")) {
                        String[] parts = line.split("=");
                        if (parts.length > 1) {
                            double mhz = Double.parseDouble(parts[1].trim());
                            return mhz / 1000.0;
                        }
                    }
                }
            }
            process.waitFor();
        } catch (Exception e) {
            System.err.println("Get Windows CPU frequency failed: " + e.getMessage());
        }
        return null;
    }
}
