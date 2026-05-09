import pandas as pd
import numpy as np

np.random.seed(42)

# Generate timestamps (7 days, hourly)
dates = pd.date_range(start='2025-01-01', end='2025-01-07', freq='h')
n_rows = len(dates)

# Create SCADA data
data = {
    'timestamp': dates.repeat(12),
    'inverter_id': np.tile([f'INV_{i:02d}' for i in range(1,5)], n_rows*3),
    'string_id': np.tile([f'STR_{i:02d}' for i in range(1,13)], n_rows),
    'power_kw': np.random.normal(25, 8, n_rows*12).clip(0, 45),
    'voltage_v': np.random.normal(650, 50, n_rows*12).clip(500, 800),
    'current_a': np.random.normal(38, 6, n_rows*12).clip(0, 50),
    'irradiance_wm2': np.random.normal(600, 300, n_rows*12).clip(0, 1100),
    'temperature_c': np.random.normal(25, 8, n_rows*12).clip(5, 45),
}

df_scada = pd.DataFrame(data)

# Add some realistic problems for testing
df_scada.loc[df_scada['string_id'].isin(['STR_03', 'STR_04']), 'power_kw'] *= 0.78   # Underperforming
df_scada.loc[df_scada['string_id'] == 'STR_07', 'power_kw'] *= 0.15                 # Almost failed

# Save files
df_scada.to_csv('data/raw/raw_scada.csv', index=False)

# Create Wiring Plan
wiring = {
    'string_id': [f'STR_{i:02d}' for i in range(1,13)],
    'inverter_id': ['INV_01']*3 + ['INV_02']*3 + ['INV_03']*3 + ['INV_04']*3,
    'string_length': [24]*12,
    'orientation': ['South']*12,
    'tilt_deg': [35]*12
}

df_wiring = pd.DataFrame(wiring)
df_wiring.to_csv('data/raw/wiring_plan.csv', index=False)

print("✅ Synthetic data created successfully!")
print(f"SCADA data: {len(df_scada):,} rows")
print(f"Wiring plan: {len(df_wiring)} strings")
print("Files saved in data/raw/")