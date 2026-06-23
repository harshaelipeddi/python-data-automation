"""
Utility Functions
Shared helpers for logging, config loading, and file handling.
"""

import logging
import os
import yaml
from pathlib import Path


def load_config(config_path: str) -> dict:
    """Load YAML configuration file."""
    path = Path(config_path)
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {config_path}")
    with open(path, "r") as f:
        config = yaml.safe_load(f)
    return config


def setup_logging(log_config: dict):
    """Configure logging with file and console handlers."""
    log_dir = Path(log_config.get("log_dir", "data/logs"))
    log_dir.mkdir(parents=True, exist_ok=True)

    log_file = log_dir / log_config.get("log_file", "etl.log")
    level = getattr(logging, log_config.get("level", "INFO").upper(), logging.INFO)

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler(),
        ],
    )


def ensure_dirs(*paths):
    """Create directories if they don't exist."""
    for path in paths:
        Path(path).mkdir(parents=True, exist_ok=True)
