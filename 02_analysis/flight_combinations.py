# How To Run:
# source .venv/bin/activate

# Imports:
import pandas as pd
import numpy as np
import itertools
import pandas as pd

# Sample datasets
# sample_1 has 1 day pairings
# sample_2 has 3 day pairings
# sample_3 has 1, 3 or 4 day pairings

# Step 1: Split by the horizontal line
df = pd.read_csv("00_data/02_output/flight_schedules_october.csv")

# Define credit range
min_credit = 75
max_credit = 80

# Store valid combinations
valid_combinations = []

# Store valid combinations
valid_combinations = []

# Generate combinations
for r in range(1, len(df) + 1):
    for combo in itertools.combinations(df.itertuples(index=False), r):
        # Sort by start date to check sequencing
        sorted_combo = sorted(combo, key=lambda x: x.start_date)
        is_valid = True
        for i in range(len(sorted_combo) - 1):
            current_end = sorted_combo[i].end_date
            next_start = sorted_combo[i + 1].start_date
            if next_start < current_end + 2:
                is_valid = False
                break

        if is_valid:
            total_credit = sum(trip.credit for trip in sorted_combo)
            if min_credit <= total_credit <= max_credit:
                valid_combinations.append([trip.unique_trip_code for trip in sorted_combo])

# Display results
for comb in valid_combinations:
    print(comb)