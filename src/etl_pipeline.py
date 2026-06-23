"""
ETL Pipeline - Main Entry Point
Automates Extract, Transform, Load processes for data pipeline efficiency.
"""

import logging
import time
from datetime import datetime
from src.extractor import DataExtractor
from src.transformer import DataTransformer
from src.loader import DataLoader
from src.utils import setup_logging, load_config

def run_pipeline(config_path: str = "config/config.yaml"):
    """Run the full ETL pipeline."""
    config = load_config(config_path)
    setup_logging(config["logging"])

    logger = logging.getLogger(__name__)
    logger.info("=" * 50)
    logger.info(f"ETL Pipeline started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    logger.info("=" * 50)

    start_time = time.time()

    try:
        # --- EXTRACT ---
        logger.info("[1/3] Starting extraction...")
        extractor = DataExtractor(config["source"])
        raw_data = extractor.extract()
        logger.info(f"Extracted {len(raw_data)} records.")

        # --- TRANSFORM ---
        logger.info("[2/3] Starting transformation...")
        transformer = DataTransformer(config["transform"])
        transformed_data = transformer.transform(raw_data)
        logger.info(f"Transformed {len(transformed_data)} records.")

        # --- LOAD ---
        logger.info("[3/3] Starting load...")
        loader = DataLoader(config["destination"])
        loader.load(transformed_data)
        logger.info("Data loaded successfully.")

    except Exception as e:
        logger.error(f"Pipeline failed: {e}", exc_info=True)
        raise

    elapsed = time.time() - start_time
    logger.info(f"Pipeline completed in {elapsed:.2f} seconds.")


if __name__ == "__main__":
    run_pipeline()
