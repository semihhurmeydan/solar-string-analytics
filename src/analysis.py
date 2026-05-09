import pandas as pd
import numpy as np

def calculate_performance_metrics(df):
    """Calculate key performance metrics"""
    # Performance Ratio (simplified)
    df['expected_power'] = df['irradiance_wm2'] * 0.25  # Rough estimate: 250W per m² at STC
    df['performance_ratio'] = df['power_kw'] / df['expected_power'].replace(0, np.nan)
    
    # Normalize by temperature
    df['temp_factor'] = 1 - 0.004 * (df['temperature_c'] - 25)
    df['normalized_power'] = df['power_kw'] / df['temp_factor']
    
    print("✅ Performance metrics calculated")
    return df


def detect_underperformance(df, threshold=0.85):
    """Detect underperforming strings"""
    # Calculate average PR per string
    string_pr = df.groupby('string_id')['performance_ratio'].mean()
    
    # Flag underperformers
    underperformers = string_pr[string_pr < threshold].index.tolist()
    
    df['is_underperforming'] = df['string_id'].isin(underperformers)
    
    print(f"Found {len(underperformers)} underperforming strings (PR < {threshold})")
    return df, underperformers


def detect_clipping(df, power_threshold=0.95):
    """Detect clipping behavior"""
    df['is_clipping'] = df['power_kw'] > (df['expected_power'] * power_threshold)
    clipping_strings = df[df['is_clipping']].groupby('string_id').size()
    
    print("Clipping detected in strings:")
    print(clipping_strings[clipping_strings > 10])
    return df


def generate_string_summary(df):
    """Create summary table for maintenance"""
    summary = df.groupby('string_id').agg({
        'power_kw': 'mean',
        'performance_ratio': 'mean',
        'is_underperforming': 'max',
        'is_clipping': 'sum'
    }).round(3)
    
    summary = summary.rename(columns={
        'power_kw': 'avg_power_kw',
        'performance_ratio': 'avg_pr',
        'is_clipping': 'clipping_events'
    })
    
    summary = summary.sort_values('avg_pr')
    print("\n🔥 Maintenance Priority List (worst first):")
    print(summary.head(10))
    
    return summary


def main():
    """Run full analysis"""
    print("🔍 Starting Performance Analysis...\n")
    
    # Load processed data
    df = pd.read_parquet('data/processed/per_string_data.parquet')
    
    df = calculate_performance_metrics(df)
    df, underperformers = detect_underperformance(df)
    df = detect_clipping(df)
    summary = generate_string_summary(df)
    
    # Save results
    summary.to_csv('reports/string_performance_summary.csv')
    print("\n✅ Analysis completed! Summary saved to reports/string_performance_summary.csv")
    
    return df, summary


if __name__ == "__main__":
    main()