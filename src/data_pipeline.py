import pandas as pd
import numpy as np
from pathlib import Path

def load_raw_data():
    """Load raw SCADA and wiring data"""
    scada = pd.read_csv('data/raw/raw_scada.csv')
    wiring = pd.read_csv('data/raw/wiring_plan.csv')
    
    # Convert timestamp
    scada['timestamp'] = pd.to_datetime(scada['timestamp'])
    
    print(f"Loaded {len(scada):,} SCADA records and {len(wiring)} strings")
    return scada, wiring


def merge_with_wiring(scada, wiring):
    """Combine SCADA data with wiring plan"""
    df = scada.merge(wiring, on='string_id', how='left')
    print(f"Merged dataset shape: {df.shape}")
    return df


def clean_data(df):
    """Basic data cleaning"""
    # Sort by time and string
    df = df.sort_values(['string_id', 'timestamp']).reset_index(drop=True)
    
    # Fill small missing values if any (new pandas way)
    df = df.ffill().bfill()
    
    print("Data cleaned and sorted")
    return df


def create_per_string_timeseries(df):
    """Create clean per-string time series"""
    # Group by string to verify
    print("\nRecords per string:")
    print(df.groupby('string_id').size().head())
    
    return df


def main():
    """Run the full pipeline"""
    print("🚀 Starting PV String Performance Pipeline...\n")
    
    scada, wiring = load_raw_data()
    df_merged = merge_with_wiring(scada, wiring)
    df_clean = clean_data(df_merged)
    df_final = create_per_string_timeseries(df_clean)
    
    # Save processed data
    output_path = 'data/processed/per_string_data.parquet'
    Path('data/processed').mkdir(exist_ok=True)
    df_final.to_parquet(output_path, index=False)
    
    print(f"\n✅ Pipeline completed! Processed data saved to: {output_path}")
    print(f"Final dataset shape: {df_final.shape}")
    
    return df_final


if __name__ == "__main__":
    main()