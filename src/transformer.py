"""
Transformer Module
Cleans, validates, and transforms raw data records.
"""

import logging
import re
from datetime import datetime

logger = logging.getLogger(__name__)


class DataTransformer:
    def __init__(self, transform_config: dict):
        self.config = transform_config

    def transform(self, records: list[dict]) -> list[dict]:
        """Run all transformation steps on the data."""
        logger.info(f"Transforming {len(records)} records...")

        transformed = []
        skipped = 0

        for i, record in enumerate(records):
            try:
                record = self._rename_columns(record)
                record = self._clean_strings(record)
                record = self._cast_types(record)
                record = self._drop_nulls(record)
                record = self._add_metadata(record)
                transformed.append(record)
            except Exception as e:
                logger.warning(f"Skipping record {i} due to error: {e}")
                skipped += 1

        logger.info(f"Transformation complete. {len(transformed)} passed, {skipped} skipped.")
        return transformed

    def _rename_columns(self, record: dict) -> dict:
        """Rename columns based on config mapping."""
        mapping = self.config.get("rename_columns", {})
        return {mapping.get(k, k): v for k, v in record.items()}

    def _clean_strings(self, record: dict) -> dict:
        """Strip whitespace and normalize string fields."""
        cleaned = {}
        for k, v in record.items():
            if isinstance(v, str):
                v = v.strip()
                v = re.sub(r'\s+', ' ', v)  # Collapse extra spaces
            cleaned[k] = v
        return cleaned

    def _cast_types(self, record: dict) -> dict:
        """Cast fields to expected types from config."""
        type_map = self.config.get("type_casts", {})
        for field, target_type in type_map.items():
            if field in record and record[field] is not None:
                try:
                    if target_type == "int":
                        record[field] = int(record[field])
                    elif target_type == "float":
                        record[field] = float(record[field])
                    elif target_type == "str":
                        record[field] = str(record[field])
                    elif target_type == "date":
                        record[field] = datetime.strptime(record[field], "%Y-%m-%d").date()
                except (ValueError, TypeError) as e:
                    logger.warning(f"Could not cast field '{field}' to {target_type}: {e}")
        return record

    def _drop_nulls(self, record: dict) -> dict:
        """Remove fields with None or empty string values."""
        required = self.config.get("required_fields", [])
        for field in required:
            if not record.get(field):
                raise ValueError(f"Required field '{field}' is missing or empty.")
        return record

    def _add_metadata(self, record: dict) -> dict:
        """Append pipeline metadata to each record."""
        record["_etl_processed_at"] = datetime.utcnow().isoformat()
        record["_etl_version"] = self.config.get("version", "1.0.0")
        return record
