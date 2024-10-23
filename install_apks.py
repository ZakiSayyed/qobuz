# PACKAGE_NAMES = ["com.qobuz.music", "com.scheler.superproxy"]  # List of package names to check
import subprocess
import os
import time

# Constants
APK_PATHS = {
    "com.qobuz.music": "qobuz.apk",  # Change to the path of your first APK file
    "com.scheler.superproxy": "super_proxy.apk"   # Change to the path of your second APK file
}
PACKAGE_NAMES = list(APK_PATHS.keys())  # List of package names to check
LOG_FILE = "install_log.txt"

def run_adb_command(command):
    """Run an ADB command and return the output."""
    try:
        result = subprocess.run(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return result.stdout.decode('utf-8'), result.stderr.decode('utf-8')
    except Exception as e:
        return "", str(e)

def get_connected_devices():
    """Get a list of connected devices using ADB."""
    output, error = run_adb_command("adb devices")
    if error:
        print(f"Error retrieving devices: {error}")
        return []

    lines = output.splitlines()
    devices = [line.split()[0] for line in lines if "device" in line and not line.startswith("List of devices")]
    return devices

def check_app_installed(device_id, package_names):
    """Check if any of the apps is installed on the device."""
    output, _ = run_adb_command(f"adb -s {device_id} shell pm list packages")
    installed_packages = []

    for package_name in package_names:
        # Check if the package_name is in the output
        if package_name in output:
            installed_packages.append(package_name)

    return installed_packages


def install_app(device_id, apk_path):
    """Stream install the APK to the device."""
    output, error = run_adb_command(f"adb -s {device_id} install {apk_path}")
    return output, error

def main_install_apk():
    # Create or clear the log file
    with open(LOG_FILE, 'w') as log_file:
        log_file.write("Installation Log\n")
        log_file.write("="*50 + "\n\n")

    devices = get_connected_devices()

    if not devices:
        print("No devices connected.")
        with open(LOG_FILE, 'a') as log_file:
            log_file.write("No devices connected.\n")
        return

    for device in devices:
        print(f"Checking device: {device}")

        with open(LOG_FILE, 'a') as log_file:
            log_file.write(f"Device ID: {device}\n")
            log_file.write("-" * 50 + "\n")

        # Check if the app is already installed
        installed_apps = check_app_installed(device, PACKAGE_NAMES)

        # Install apps based on installed packages
        for package_name in PACKAGE_NAMES:
            if package_name in installed_apps:
                print(f"{package_name} is already installed on device {device}.")
                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(f"{package_name} is already installed.\n")
            else:
                # Apps are not installed, proceed with installation
                print(f"{package_name} is not installed on device {device}. Installing...")
                with open(LOG_FILE, 'a') as log_file:
                    log_file.write(f"{package_name} is not installed. Installing...\n")

                start_time = time.time()
                apk_path = APK_PATHS[package_name]  # Get the corresponding APK path
                output, error = install_app(device, apk_path)
                end_time = time.time()

                if error:
                    print(f"Installation failed on device {device} for {package_name}. Error: {error}")
                    with open(LOG_FILE, 'a') as log_file:
                        log_file.write(f"Installation failed for {package_name}. Error: {error}\n")
                else:
                    print(f"Installation successful on device {device} for {package_name}.")
                    with open(LOG_FILE, 'a') as log_file:
                        log_file.write(f"Installation successful for {package_name}.\n")
                        log_file.write(f"Time taken: {end_time - start_time:.2f} seconds\n")

        with open(LOG_FILE, 'a') as log_file:
            log_file.write("\n")  # New line for separation between devices

    print("Installation process completed. Check the log file for details.")

# if __name__ == "__main__":
#     main()
