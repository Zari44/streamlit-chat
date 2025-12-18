import logging
from pathlib import Path


def setup_logging(log_file: str = None, log_level: int = logging.INFO):
    """
    Configure logging for the application.

    Args:
        log_file: Path to log file. If None, uses 'app.log' in the project root.
        log_level: Logging level (default: logging.INFO)
    """
    if log_file is None:
        # Default to app.log in project root (goatbot directory)
        project_root = Path(__file__).parent.parent
        log_file = str(project_root / "app.log")

    # Ensure log directory exists
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    # Use force=True to allow reconfiguration (Python 3.8+)
    # This allows different components to configure logging as needed
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
        force=True,
    )


def get_logger(name: str = None):
    """
    Get a logger instance.

    Args:
        name: Logger name. If None, uses the calling module's __name__

    Returns:
        logging.Logger instance
    """
    if name is None:
        import inspect

        # Get the name of the calling module
        frame = inspect.currentframe().f_back
        name = frame.f_globals.get("__name__", "unknown")

    return logging.getLogger(name)


# Note: Logging should be configured explicitly by calling setup_logging()
# This allows each component (streamlit-chat, backend) to configure it as needed.
# If LOG_FILE environment variable is set, you can call setup_logging(log_file=os.getenv("LOG_FILE"))
