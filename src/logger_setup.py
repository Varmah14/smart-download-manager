import logging


# src/logger_setup.py (optional if you want a separate file)
def setup_logger():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("logs.txt"),  # Log to file
            logging.StreamHandler(),  # Log to console
        ],
    )
