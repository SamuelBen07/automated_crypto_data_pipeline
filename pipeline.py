import logging
import os
import requests
import json
import datetime
from sqlalchemy import create_engine, text
import pandas as pd
from sqlalchemy.types import String, BigInteger, DECIMAL, DateTime
import schedule
import time

# Create required folders
os.makedirs('logs', exist_ok=True)
os.makedirs('raw_data', exist_ok=True)
os.makedirs('processed_data', exist_ok=True)

def extract_data():
    url= "https://api.coingecko.com/api/v3/coins/markets"
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 10,
        "page": 1,
        "sparkline": "false"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        raw_file = f"raw_data/crypto_{timestamp}.json"
        with open(raw_file, "w") as f:
            json.dump(data, f, indent=4)

        logging.info(f"Data extracted successfully: {raw_file}")
        return data 

    except Exception as e:
        logging.error(f"Data extraction failed: {str(e)}")
        return None
    
def transform_data(data):
    try:
        df = pd.DataFrame(data)
        df = df[['id', 'symbol', 'name', 'current_price', 'market_cap', 'total_volume']]
        df['timestamp'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return df
    except Exception as e:
        logging.error(f"Data transformation failed: {str(e)}")
        return None
       
def transform_to_json(data):
    try:
        current_ts_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        transformed_records = []
        for item in data:
            transformed_records.append({
                'id': item.get('id'),
                'symbol': item.get('symbol'),
                'name': item.get('name'),
                'current_price': item.get('current_price'),
                'market_cap': item.get('market_cap'),
                'total_volume': item.get('total_volume'),
                'timestamp': current_ts_str,
            })

        # Save transformed JSON
        ts_file = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        out_file = f"processed_data/crypto_transformed_{ts_file}.json"
        with open(out_file, "w") as f:
            json.dump(transformed_records, f, indent=4)
        logging.info(f"Transformed JSON written: {out_file}")
        return transformed_records
    except Exception as e:
        logging.error(f"JSON transform failed: {str(e)}")
        return None


def create_sqlite_engine():
    engine=create_engine("sqlite:///crypto_data.db")
    return engine

def load_data(df: pd.DataFrame) -> bool:
    """
    Load the tabular DataFrame into SQLite with explicit column types.
    """
    try:
        if df is None or df.empty:
            logging.warning("No rows to load into tabular table.")
            return True

        # Ensure correct dtypes before to_sql
        df = df.copy()
        df["id"] = df["id"].astype(str)
        df["symbol"] = df["symbol"].astype(str)
        df["name"] = df["name"].astype(str)
        df["current_price"] = pd.to_numeric(df["current_price"], errors="coerce")
        df["market_cap"]   = pd.to_numeric(df["market_cap"], errors="coerce").astype("Int64")
        df["total_volume"] = pd.to_numeric(df["total_volume"], errors="coerce").astype("Int64")
        df["timestamp"]    = pd.to_datetime(df["timestamp"], errors="coerce")

        dtype_map = {
            "id": String(64),
            "symbol": String(32),
            "name": String(128),
            "current_price": DECIMAL(20, 8),
            "market_cap": BigInteger(),
            "total_volume": BigInteger(),
            "timestamp": DateTime(),
        }

        table_name = "market_data"
        engine = create_sqlite_engine()

        

        # Create/append with explicit types
        df.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False,
            dtype=dtype_map,
            
        )

        logging.info(f"✅ Loaded {len(df)} rows into SQLite table:{table_name}")
        return True

    except Exception as e:
        logging.error(f"❌ Data load failed: {str(e)}")
        return False


def load_json(json_records) -> bool:
    """
    Load the full JSON payload into a SQLite table.
   
    """
    try:
        if not json_records:
            logging.warning("No JSON records to load.")
            return True

        table_name = "market_data_json"
        engine = create_sqlite_engine()

        #create a dataframe from your list of JSON records
        df = pd.DataFrame(json_records)

        df['payload'] = df.apply(lambda row: json.dumps(row.to_dict()), axis=1)

        df_to_load = df[['timestamp','payload']].copy()
        df_to_load.rename(columns={'timestamp': 'collected_at'},inplace=True)

        df_to_load.to_sql(
            table_name,
            con=engine,
            if_exists="append",
            index=False,
            dtype={"collected_at":DateTime(),"payload":String()}
        )
        logging.info(f"✅ Loaded {len(json_records)} JSON rows into SQLite table:{table_name}")
        return True

        

    except Exception as e:
        logging.error(f"❌ JSON load failed: {str(e)}")
        return False

def run_pipeline():
    logging.info("=============================")
    logging.info("Starting scheduled pipeline run")
    data = extract_data()
    if not data:
        logging.error("Extraction failed; skipping transform/load")
        return False

    json_records = transform_to_json(data)
    df_records = transform_data(data)

    success_json = load_json(json_records) if json_records is not None else False
    success_df = load_data(df_records) if df_records is not None else False

    logging.info(f"Pipeline run finished.JSON Load: {'Success' if success_json else 'Failed'},DF Load: {'Success' if success_df else 'Failed'}")
    logging.info("=============================")

    return success_json and success_df

if __name__ == "__main__":
    logging.basicConfig(
        handlers=[
            logging.FileHandler("logs/pipeline.log"),
            logging.StreamHandler()
        ],
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s"
    )

    schedule.every(1).hour.do(run_pipeline)

    logging.info("Starting scheduled pipeline.First job will run at the scheduled time.")

    run_pipeline()

    while True:
        schedule.run_pending()
        time.sleep(1)
       