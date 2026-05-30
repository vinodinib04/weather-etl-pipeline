import logging
from sqlalchemy import create_engine, text
from dotenv import load_dotenv
from urllib.parse import quote_plus
import os

load_dotenv()


def get_engine():
    """Create and return a SQLAlchemy engine for MySQL."""
    password = quote_plus(os.getenv('DB_PASSWORD'))
    db_url = (
        f"mysql+pymysql://{os.getenv('DB_USER')}:{password}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    return create_engine(db_url)


def load(df):
    """Load transformed DataFrame into MySQL with duplicate detection."""
    if df.empty:
        logging.warning("No data to load — DataFrame is empty")
        return

    engine = get_engine()
    inserted = 0
    skipped = 0

    with engine.connect() as conn:
        for _, row in df.iterrows():
            try:
                query = text("""
                    INSERT IGNORE INTO weather_data
                        (city, country, temperature_celsius, feels_like_celsius,
                         humidity, wind_speed, weather_description, recorded_at)
                    VALUES
                        (:city, :country, :temperature_celsius, :feels_like_celsius,
                         :humidity, :wind_speed, :weather_description, :recorded_at)
                """)
                result = conn.execute(query, row.to_dict())
                if result.rowcount > 0:
                    inserted += 1
                else:
                    skipped += 1
            except Exception as e:
                logging.error(f"Load error for {row['city']}: {e}")

        conn.commit()

    logging.info(f"Load complete: {inserted} inserted, {skipped} duplicates skipped")
    print(f"Load complete: {inserted} inserted, {skipped} duplicates skipped")