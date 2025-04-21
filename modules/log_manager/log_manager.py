# log_manager.py
import logging
import os
import sys
import codecs

def get_logger(name: str = __name__) -> logging.Logger:
    """
    Get a logger instance with both file and console handlers that properly handle Unicode characters.
    
    Args:
        name (str): The name of the logger, typically __name__
        
    Returns:
        logging.Logger: Configured logger instance
    """
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file_path = os.path.join(log_dir, "app.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Prevent duplicate handlers when re-importing
    if not logger.handlers:
        try:
            # File handler with UTF-8 encoding
            file_handler = logging.FileHandler(log_file_path, encoding='utf-8')
            file_handler.setFormatter(logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
            ))

            # Console handler with appropriate encoding
            if sys.platform == 'win32':
                # On Windows, use UTF-8 encoding for console output
                sys.stdout.reconfigure(encoding='utf-8')
                sys.stderr.reconfigure(encoding='utf-8')
                console_handler = logging.StreamHandler(codecs.getwriter('utf-8')(sys.stdout.buffer))
            else:
                # On Unix-like systems, use standard console handler
                console_handler = logging.StreamHandler()
                
            console_handler.setFormatter(logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
            ))

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)
            
        except Exception as e:
            # Fallback logging configuration if the main one fails
            fallback_handler = logging.StreamHandler()
            fallback_handler.setFormatter(logging.Formatter(
                "%(asctime)s [%(levelname)s] %(name)s - %(message)s"
            ))
            logger.addHandler(fallback_handler)
            logger.error(f"Error setting up logger handlers: {str(e)}")

    return logger
