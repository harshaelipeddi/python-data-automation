"""
Loader Module
Loads transformed data to CSV, database (MySQL), or JSON.
"""

import csv
import json
import logging
import mysql.connector
import pandas as pd
from pathlib import Path
from datetime import datetime

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, dest_config: dict):
        self.config = dest_config
        self.dest_type = dest_config["type"]

    def load(self, records: list[dict]):
        """Route to correct loader."""
        if self.dest_type == "csv":
            self._load_csv(records)
        elif self.dest_type == "database":
            self._load_database(records)
        elif self.dest_type == "json":
            self._load_json(records)
        else:
            raise ValueError(f"Unsupported destination type: {self.dest_type}")

    def _load_csv(self, records: list[dict]):
        """Write records to a CSV file."""
        output_dir = Path(self.config.get("output_dir", "data/processed"))
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"output_{timestamp}.csv"

        if not records:
            logger.warning("No records to write.")
            return

        logger.info(f"Writing {len(records)} records to {filepath}")
        df = pd.DataFrame(records)
        df.to_csv(filepath, index=False)
        logger.info(f"CSV written: {filepath}")

    def _load_database(self, records: list[dict]):
        """Insert records into a MySQL table."""
        if not records:
            logger.warning("No records to insert.")
            return

        db_cfg = self.config["database"]
        table = self.config["table"]

        conn = mysql.connector.connect(
            host=db_cfg["host"],
            port=db_cfg.get("port", 3306),
            user=db_cfg["user"],
            password=db_cfg["password"],
            database=db_cfg["database"],
        )
        cursor = conn.cursor()

        columns = list(records[0].keys())
        placeholders = ", ".join(["%s"] * len(columns))
        col_names = ", ".join([f"`{c}`" for c in columns])
        query = f"INSERT INTO `{table}` ({col_names}) VALUES ({placeholders})"

        rows = [tuple(r[c] for c in columns) for r in records]
        cursor.executemany(query, rows)
        conn.commit()

        logger.info(f"Inserted {cursor.rowcount} rows into `{table}`.")
        cursor.close()
        conn.close()

    def _load_json(self, records: list[dict]):
        """Write records to a JSON file."""
        output_dir = Path(self.config.get("output_dir", "data/processed"))
        output_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filepath = output_dir / f"output_{timestamp}.json"

        logger.info(f"Writing {len(records)} records to {filepath}")
        with open(filepath, "w") as f:
            json.dump(records, f, indent=2, default=str)
        logger.info(f"JSON written: {filepath}")
