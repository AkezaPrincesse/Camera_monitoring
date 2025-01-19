import os
import time
import subprocess
import shutil

# Define the folders
watch_folder = "C:\\Users\\ernes\\OneDrive\\Documents\\Monitor"
uploaded_folder = "C:\\Users\\ernes\\OneDrive\\Documents\\Uploaded"
# Ensure the uploaded folder exists
os.makedirs(uploaded_folder, exist_ok=True)

# Define the upload URL
upload_url = "https://projects.benax.rw/f/o/t/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b660f7efa9d39741a93ed0356c/iot_testing_202501/upload.php"

def upload_image(file_path):
    """
    Upload an image using the curl command.
    """
    try:
        result = subprocess.run(
            ["curl", "-X", "POST", "-F", f"imageFile=@{file_path}", upload_url],
            check=True,
            capture_output=True,
            text=True,
        )
        # Check for success in the output
        if "success" in result.stdout.lower():
            print(f"Uploaded {file_path}: {result.stdout}")
            return True
        else:
            print(f"Failed to upload {file_path}: {result.stdout}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"Failed to upload {file_path}: {e.stderr}")
        return False

def monitor_folder():
    """
    Monitor the folder for new images and handle uploads.
    """
    while True:
        # List files in the watch folder
        files = [f for f in os.listdir(watch_folder) if os.path.isfile(os.path.join(watch_folder, f))]

        for file in files:
            file_path = os.path.join(watch_folder, file)

            # Wait for 30 seconds
            time.sleep(30)

            # Upload the file
            if upload_image(file_path):
                # Move the uploaded file to the uploaded folder
                shutil.move(file_path, os.path.join(uploaded_folder, file))
                print(f"Moved {file} to {uploaded_folder}")

        # Check for new files every 5 seconds
        time.sleep(5)

if __name__ == "__main__":
    try:
        print("Monitoring folder for new files...")
        monitor_folder()
    except KeyboardInterrupt:
        print("\nStopped monitoring.")
