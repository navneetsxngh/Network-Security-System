import logging
import os
from datetime import datetime

# Optional: Create a timestamped log file
# LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Log file name
LOG_FILE = "networksecurity.log"

# Get the root directory of the project
ROOT_DIR = os.getcwd()

# Define logs directory
LOG_DIR = os.path.join(ROOT_DIR, "logs")

# Create the logs directory if it doesn't exist
os.makedirs(LOG_DIR, exist_ok=True)

# Full path to the log file
LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Test log
logging.info("Logging has been successfully configured.")

print(f"Log file created at: {LOG_FILE_PATH}")