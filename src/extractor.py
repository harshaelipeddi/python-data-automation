"""
Extractor Module
Supports extraction from CSV files, databases (MySQL), and REST APIs.
"""

import csv
import json
import logging
import mysql.connector
import requests
import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)


class DataExtractor:
    def __init__(self, source_config: dict):
        self.config = source_config
        self.source_type = source_config["type"]

    def extract(self) -> list[dict]:
        """Route to the correct extractor based on source type."""
        if self.source_type == "csv":
            return self._extract_csv()
        elif self.source_type == "database":
            return self._extract_database()
        elif self.source_type == "api":
            return self._extract_api()
        else:
            raise ValueError(f"Unsupported source type: {self.source_type}")

    def _extract_csv(self) -> list[dict]:
        """Extract data from a CSV file."""
        filepath = Path(self.config["filepath"])
        if not filepath.exists():
            raise FileNotFoundError(f"CSV file not found: {filepath}")

        logger.info(f"Reading CSV: {filepath}")
        df = pd.read_csv(filepath)
        records = df.to_dict(orient="records")
        logger.info(f"Read {len(records)} rows from CSV.")
        return records

    def _extract_database(self) -> list[dict]:
        """Extract data from a MySQL database."""
        db_cfg = self.config["database"]
        logger.info(f"Connecting to database: {db_cfg['host']}/{db_cfg['database']}")

        conn = mysql.connector.connect(
            host=db_cfg["host"],
            port=db_cfg.get("port", 3306),
            user=db_cfg["user"],
            password=db_cfg["password"],
            database=db_cfg["database"],
        )
        cursor = conn.cursor(dictionary=True)
        query = self.config.get("query", f"SELECT * FROM {self.config.get('table', 'data')}")
        logger.info(f"Executing query: {query}")
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        conn.close()
        logger.info(f"Fetched {len(records)} rows from database.")
        return records

    def _extract_api(self) -> list[dict]:
        """Extract data from a REST API endpoint."""
        url = self.config["url"]
        headers = self.config.get("headers", {})
        params = self.config.get("params", {})

        logger.info(f"Calling API: {url}")
        response = requests.get(url, headers=headers, params=params, timeout=30)
        response.raise_for_status()

        data = response.json()
        # Support both list responses and nested responses
        if isinstance(data, list):
            records = data
        else:
            records = data.get(self.config.get("data_key", "data"), [data])

        logger.info(f"Retrieved {len(records)} records from API.")
        return records
