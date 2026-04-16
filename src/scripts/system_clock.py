"""
Get CPU frequency for various systems.
"""

import platform
import subprocess
import re

LINUX_FILE = "/proc/cpuinfo"
MAC_COMMAND = ["sysctl", "-n", "hw.cpufrequency"]
WINDOWS_COMMAND = ["wmic", "cpu", "get", "MaxClockSpeed", "/value"]
DEFAULT_CLOCK_SPEED_GHZ = 3.0
clock_speed = None


def get_clock_speed_ghz():
    """
    Get system clock speed in GHz.
    """
    global clock_speed
    
    if clock_speed is not None:
        return clock_speed
    
    system = platform.system().lower()
    
    if "linux" in system:
        clock_speed = get_linux_clock_speed()
    elif "darwin" in system:  # macOS
        clock_speed = get_mac_clock_speed()
    elif "windows" in system:
        clock_speed = get_windows_clock_speed()
    
    if clock_speed is None or clock_speed <= 0:
        clock_speed = DEFAULT_CLOCK_SPEED_GHZ
    
    return clock_speed


def get_linux_clock_speed():
    try:
        with open(LINUX_FILE, "r") as f:
            for line in f:
                if line.startswith("cpu MHz"):
                    match = re.search(r":\s*([\d.]+)", line)
                    if match:
                        mhz = float(match.group(1))
                        return mhz / 1000.0
    except Exception as e:
        print(f"Get Linux CPU frequency failed:  {e}", file=__import__('sys').stderr)
    return None


def get_mac_clock_speed():
    try:
        result = subprocess.run(MAC_COMMAND, 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0 and result.stdout.strip():
            hz = float(result.stdout.strip())
            return hz / 1e9  # Convert Hz to GHz
    except Exception as e:
        print(f"Get macOS CPU frequency failed: {e}", file=__import__('sys').stderr)
    return None


def get_windows_clock_speed():
    """Extract CPU frequency from Windows using wmic"""
    try:
        result = subprocess.run(WINDOWS_COMMAND,
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            for line in result.stdout.split("\n"):
                if "MaxClockSpeed" in line:
                    match = re.search(r"=(\d+)", line)
                    if match:
                        mhz = float(match.group(1))
                        return mhz / 1000.0  # Convert MHz to GHz
    except Exception as e:
        print(f"Get Windows CPU frequency failed: {e}", file=__import__('sys').stderr)
    return None
