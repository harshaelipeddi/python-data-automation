"""
Unit Tests for DataTransformer
"""

import pytest
from src.transformer import DataTransformer

SAMPLE_CONFIG = {
    "version": "1.0.0",
    "rename_columns": {"First Name": "first_name", "Email Address": "email"},
    "type_casts": {"salary": "float"},
    "required_fields": ["first_name", "email"],
}


@pytest.fixture
def transformer():
    return DataTransformer(SAMPLE_CONFIG)


def test_rename_columns(transformer):
    record = {"First Name": "Alice", "Email Address": "alice@example.com"}
    result = transformer._rename_columns(record)
    assert "first_name" in result
    assert "email" in result
    assert "First Name" not in result


def test_clean_strings(transformer):
    record = {"first_name": "  Alice  ", "email": "alice@example.com"}
    result = transformer._clean_strings(record)
    assert result["first_name"] == "Alice"


def test_cast_types(transformer):
    record = {"salary": "75000.50"}
    result = transformer._cast_types(record)
    assert isinstance(result["salary"], float)
    assert result["salary"] == 75000.50


def test_drop_nulls_raises_on_missing_required(transformer):
    record = {"first_name": "", "email": ""}
    with pytest.raises(ValueError):
        transformer._drop_nulls(record)


def test_add_metadata(transformer):
    record = {"first_name": "Alice"}
    result = transformer._add_metadata(record)
    assert "_etl_processed_at" in result
    assert "_etl_version" in result


def test_full_transform(transformer):
    records = [
        {
            "First Name": "Alice",
            "Email Address": "alice@example.com",
            "salary": "75000",
        }
    ]
    result = transformer.transform(records)
    assert len(result) == 1
    assert result[0]["first_name"] == "Alice"
    assert result[0]["salary"] == 75000.0
