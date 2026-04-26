import pandas as pd
import numpy as np

def facility_usage_analysis(bookings):
    df = pd.DataFrame(bookings)

    if df.empty:
        print("No booking data available")
        return

    print("\n--- Facility Usage ---")
    print(df["facility_id"].value_counts())

    counts = df["facility_id"].value_counts().values
    print("\nAverage Usage:", np.mean(counts))