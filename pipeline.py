import logging
from etl.extract import extract_all
from etl.transform import transform
from etl.load import load
from datetime import datetime

logging.basicConfig(
    filename="pipeline.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


def run_pipeline():
    """Run the full ETL pipeline: extract → transform → load."""
    print(f"\n--- Pipeline started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')} ---")
    logging.info("Pipeline started")

    try:
        # Extract
        print("Extracting weather data...")
        raw_data = extract_all()

        if not raw_data:
            logging.error("Extraction returned no data. Aborting pipeline.")
            print("Extraction failed. Check pipeline.log for details.")
            return

        # Transform
        print("Transforming data...")
        df = transform(raw_data)

        if df.empty:
            logging.error("Transform returned empty DataFrame. Aborting pipeline.")
            print("Transformation failed. Check pipeline.log for details.")
            return

        # Load
        print("Loading into PostgreSQL...")
        load(df)

        print(f"--- Pipeline completed successfully ---\n")
        logging.info("Pipeline completed successfully")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        print(f"Pipeline failed: {e}")


if __name__ == "__main__":
    run_pipeline()