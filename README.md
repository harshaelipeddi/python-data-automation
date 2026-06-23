# Python Data Automation - ETL Pipeline

An automated ETL (Extract, Transform, Load) pipeline built with Python to streamline data ingestion and processing workflows.

## Features

- **Extract** from CSV files, MySQL databases, or REST APIs
- **Transform** with column renaming, type casting, null validation, and metadata tagging
- **Load** to CSV, MySQL, or JSON output
- Configurable via a single `config/config.yaml` file
- Structured logging to both console and file
- Unit tested with pytest

## Project Structure

```
python-data-automation/
├── src/
│   ├── etl_pipeline.py    # Main pipeline runner
│   ├── extractor.py       # Extract module (CSV / DB / API)
│   ├── transformer.py     # Transform module (clean, cast, validate)
│   ├── loader.py          # Load module (CSV / DB / JSON)
│   └── utils.py           # Logging and config helpers
├── config/
│   └── config.yaml        # Pipeline configuration
├── data/
│   ├── raw/               # Input data files
│   │   └── sample_input.csv
│   ├── processed/         # Output files (git-ignored)
│   └── logs/              # Log files (git-ignored)
├── tests/
│   └── test_transformer.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Setup

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/python-data-automation.git
cd python-data-automation

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate        # Mac/Linux
venv\Scripts\activate           # Windows

# 3. Install dependencies
pip install -r requirements.txt
```

## Configuration

Edit `config/config.yaml` to set your source, transformations, and destination.

**CSV source example (default):**
```yaml
source:
  type: csv
  filepath: data/raw/sample_input.csv
```

**Database source example:**
```yaml
source:
  type: database
  database:
    host: localhost
    user: root
    password: your_password
    database: your_db
  query: "SELECT * FROM employees"
```

## Running the Pipeline

```bash
python -m src.etl_pipeline
```

## Running Tests

```bash
pytest tests/ -v
```

## Technologies Used

- Python 3.10+
- pandas
- mysql-connector-python
- requests
- PyYAML
- pytest

## Author

Elipeddi Harshavardhan  
[LinkedIn](https://linkedin.com) | harshaelipeddi15@gmail.com
