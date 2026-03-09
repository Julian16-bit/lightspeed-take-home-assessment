import pandas as pd
from src.ingest import full_ingestion
from src.llm_functions import create_ai_generated_fields

def main():
    print("Starting data ingestion...")
    df = full_ingestion()
    print(f"Ingestion complete. Total rows: {len(df)}")

    print("Generating AI fields...")
    df_with_ai = create_ai_generated_fields(df)
    print("AI field generation complete.")

    output_file = "output_with_generated_fields.csv"
    df_with_ai.to_csv(output_file, index=False)
    print(f"Output saved to {output_file}")

if __name__ == "__main__":
    main()
