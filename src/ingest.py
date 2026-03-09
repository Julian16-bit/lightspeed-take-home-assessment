import pandas as pd
from dateutil import parser
import re

class IngestFeedback:

    def __init__(self, source, file_path):
        self.source = source
        self.file_path = file_path

    def read_source_file(self):
        return pd.read_csv(self.file_path)

    def standardize_columns(self, df):
        mapping = {
                "review_text": "content",
                "description": "content",
                "feedback_text": "content",
                "rating": "raw_score",
                "score": "raw_score",
                "created_at": "date",
                "survey_date": "date"
            }
        
        df = df.rename(columns=mapping)

        df["source_type"] = self.source
        standard_cols = ["merchant_id", "source_type", "content", "raw_score", "date"]

        return df.reindex(columns=standard_cols)
    
    def standardize_dates(self, df):
        date_formats = {
            "nps_survey": "%d-%m-%Y",
            "app_store": "%Y-%m-%d",
            "support": "%Y-%m-%d"
        }
        initial_format = date_formats.get(self.source)

        df["date"] = pd.to_datetime(df["date"], format=initial_format, errors="coerce")
        df = df.dropna(subset=["date"])
        df["date"] = df["date"].dt.strftime("%Y-%m-%d")
        return df

    def clean_merchant_ids(self, df):
        def normalize_merchant_ids(merchant_id):
            if pd.isna(merchant_id):
                return None
            
            merchant_id = str(merchant_id).strip().upper()
            merchant_id = re.sub(r"[^A-Z0-9]", "", merchant_id)

            return merchant_id
        
        df["merchant_id"] = df["merchant_id"].apply(normalize_merchant_ids)
        df = df.dropna(subset=["merchant_id"])

        return df
    
    def normalize_scores(self, df):
        if self.source == "app_store":
            df["raw_score"] = df["raw_score"]*2
        return df

def full_ingestion():
    sources = [
        IngestFeedback("app_store", "data/app_reviews.csv"),
        IngestFeedback("support", "data/support_tickets.csv"),
        IngestFeedback("nps_survey", "data/nps_surveys.csv")
    ]

    processed_dfs = []

    for source in sources:
        raw_df = source.read_source_file()
        if not raw_df.empty:
            print(f"{source.source} Initial rows: {len(raw_df)}")

            standard_df = source.standardize_columns(raw_df)
            print(f"{source.source} after standardizing columns: {len(standard_df)}")

            clean_dates_df = source.standardize_dates(standard_df)
            dropped_dates = len(standard_df) - len(clean_dates_df)
            print(f"{source.source} after date cleaning: {len(clean_dates_df)} (dropped {dropped_dates} rows)")

            clean_null_df = source.clean_merchant_ids(clean_dates_df)
            dropped_nulls = len(clean_dates_df) - len(clean_null_df)
            print(f"{source.source} after removing null IDs: {len(clean_null_df)} (dropped {dropped_nulls} rows)")

            normalized_df = source.normalize_scores(clean_null_df)

            processed_dfs.append(normalized_df)
    
    unified_df = pd.concat(processed_dfs, ignore_index=True)
    return unified_df

if __name__ == "__main__":
    df = full_ingestion()
    pd.set_option('display.max_rows', None)
    df.to_csv("output.csv")
    print(df)