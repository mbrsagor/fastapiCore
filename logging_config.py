import logging

def setup_logger():
    logging.basicConfig(
        level=logging.INFO,  # Default logging level
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler("app.log"),  # Save logs to a file
            logging.StreamHandler()          # Also log to console
        ]
    )

    logger = logging.getLogger("fastapi_app")
    return logger

