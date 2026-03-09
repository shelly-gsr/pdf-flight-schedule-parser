# How To Run:
# source .venv/bin/activate

# TO DO:
# 1. add another clause for start_date for 1 liners. Might be a nice to have, its just manual for now to calculate the end date

# Requirements:
# pip install pdfminer.six

# Imports:
import pandas as pd
import numpy as np
import re
from pdfminer.high_level import extract_pages, extract_text

# Sample datasets
# sample_1 has 1 day pairings
# sample_2 has 3 day pairings
# sample_3 has 1, 3 or 4 day pairings

# Step 1: Split by the horizontal line
text = extract_text("00_data/01_input/flight_schedules_october.pdf")
blocks = re.split(r'_{119}', text)
# Debuggging: How many shifts are there?
# print(f"Number of blocks: {len(blocks)}")

# Step 2: Filter out empty or short blocks. Anything less than 100 characters is likely not a valid block.
blocks = [block.strip() for block in blocks if len(block.strip()) > 100]

# Step 3: Loop through each block and parse it
flight_schedules_data = []

for block in blocks:
    # ---- Feature: trip_code ---- #
    match = re.search(r'TRIP\s{2}([A-Z0-9]{5})', block)
    trip_code = match.group(1) if match else None
    # Skip this block if no flight codes found
    if not trip_code:
        continue

    # ---- Feature: start_dates ---- #
    # Step 1: Find all groups that include numbers and might be around dashes
    schedule_lines = re.findall(r'(?:(?:[A-Z]?\d{2}(?:\s\d{2})*|(?:\d{2}\s?)+)\s*--|\b\d{1,2}h\d{1,2}\s*--|--\s?\d{2})', block)

    # Step 2: From those segments, pull out the actual 2-digit numbers
    start_dates = []
    for line in schedule_lines:
        # Skip full match if it's a known time pattern like "3h14"
        if re.search(r'\b\d{1,2}h\d{2}\b', line):
            continue
        # Skip long digit strings (e.g., phone numbers, codes)
        if re.search(r'\d{5,}', line):
            continue
        # Skip if pattern is: 4 or more digits followed by optional space and then "--"
        if re.search(r'\b\d{4,}\s*-*\b', line):
            continue
        # Find all 2-digit numbers in the line
        nums = re.findall(r'\d{2}\b', line) #r'\d{2}'
        for n in nums:
            if n != "00" and int(n) <= 31:
                start_dates.append(n)
    #print(start_dates) #debgging

    # ---- Feature: pairing_length ---- #
    count = len(re.findall(r'FU:', block))
    pairing_length = f"{count}" if count > 0 else None

    # ---- Feature: airports_by_day ---- #      
    airports_by_day = []
    current_segment = []
    # Split the text into lines
    lines = block.splitlines()
    # Variable to keep track of the day
    day_count = 1
    for line in lines:
        # Exclude lines with "DEP" or "ARR"
        if "DEP" in line or "ARR" in line:
            continue

        # Find airport pairs in each line using your regex
        airports = re.findall(r'\b([A-Z]{3})\s([A-Z]{3})\b', line)
        
        if airports:
            # If airports are found, add them to the current segment
            current_segment.extend(airports)
        
        # If we encounter "FU:", end the current segment and start a new one
        if "FU:" in line:
            if current_segment:  # If there's any data in current segment, save it
                airports_by_day.append((f"Day {day_count}", current_segment))
                current_segment = []  # Reset for the new segment
            day_count += 1  # Increment the day count
    # Don't forget to add the last segment if there is one
    if current_segment:
        airports_by_day.append((f"Day {day_count}", current_segment))

    # ---- Feature: flight_count_by_day ---- #
    # Calculate the number of flights per day
    flights_per_day = [len(airport_list) for _, airport_list in airports_by_day]
    # Format the output as "3-2-4"
    flight_count_by_day = '-'.join(map(str, flights_per_day))

    # ---- Feature: flight_time ---- #
    match = re.search(r'TOTAL\s+FLT\s+TIME:\s+(\d{1,2}h\d{2})', block)
    flight_time_str = match.group(1) if match else None
    hours, minutes = flight_time_str.split("h")
    flight_time = float(f"{hours}.{minutes}")

    # ---- Feature: duty_time ---- #
    match = re.search(r'TOTAL\s+DUTY\s+TIME:\s+(\d{1,2}h\d{2})', block)
    duty_time_str = match.group(1) if match else None
    hours, minutes = duty_time_str.split("h")
    duty_time = float(f"{hours}.{minutes}")

    # ---- Feature: credit ---- #
    match = re.search(r'TOTAL\s+CREDIT:\s+(\d{1,2}h\d{2})', block)
    credit_str = match.group(1) if match else None
    hours, minutes = credit_str.split("h")
    credit = float(f"{hours}.{minutes}")

    # ---- Feature: fatigue_unit ---- #
    match = re.search(r'FATIGUE\s+UNIT:\s+(\d{1,2}h\d{2})', block)
    fatigue_unit_str = match.group(1) if match else None
    hours, minutes = fatigue_unit_str.split("h")
    fatigue_unit = float(f"{hours}.{minutes}")

    # ---- Feature: USD meals ---- #
    match = re.search(r'MEALS\s+US:\s+([0-9]+\.[0-9]{2})', block)
    usd_meals = match.group(1) if match else None

    # ---- Feature: CAD meals ---- #
    match = re.search(r'MEALS\s+CAD:\s+([0-9]+\.[0-9]{2})', block)
    cad_meals = match.group(1) if match else None

    # ---- Save the parsed shift info ---- #
    flight_schedules_data.append({
        "trip_code": trip_code,
        "start_date": start_dates,
        "pairing_length": pairing_length,
        "flight_count_by_day": str(flight_count_by_day),
        "airport_by_day": airports_by_day,
        "flight_time": flight_time,
        "duty_time": duty_time,
        "credit": credit,
        "fatigue_unit": fatigue_unit,
        "usd_meals": usd_meals,
        "cad_meals": cad_meals,
        "raw_block": block  # Optional: store full raw block
    })

# Step 4: Convert to DataFrame
flight_schedules_df = pd.DataFrame(flight_schedules_data)

# Step 5: Expand start_dates so that each date is in its own row
# Function to split the lists into separate rows
def split_rows(flight_schedules_df):
    # Explode the 'Values' column, which will create new rows for each value in the list
    return flight_schedules_df.explode('start_date', ignore_index=True)
# Apply the function to the dataframe
flight_schedule_expanded_df = split_rows(flight_schedules_df)

# Step 6: Calculate the "Feature: end_date" using start_date and pairing_length
flight_schedule_expanded_df['end_date'] = flight_schedule_expanded_df.apply(
    lambda row: 0 if pd.isna(row['start_date']) else int(row['start_date']) + int(row['pairing_length']) - 1,
    axis=1)

# Step 7: Make the trip_code's unique e.g. if trip_code C7001 has 4 start_dates, we need to note each like C7001/01, C7001/02, C7001/03, C7001/04
# Count occurrences of each trip_code
flight_counts = flight_schedule_expanded_df['trip_code'].value_counts()
# Identify non-unique flight codes
non_unique = flight_counts[flight_counts > 1].index
# Create the new column with conditional logic
flight_schedule_expanded_df['unique_trip_code'] = flight_schedule_expanded_df.apply(
    lambda row: f"{row['trip_code']}/{row['start_date']}" if row['trip_code'] in non_unique else row['trip_code'],
    axis=1
)

# Step 8: Reorder columns
flight_schedule_expanded_df = flight_schedule_expanded_df[['unique_trip_code', 'start_date', 'end_date', 'pairing_length', 'flight_count_by_day', 
                                                           'airport_by_day', 'flight_time', 'duty_time', 'credit', 'fatigue_unit', 
                                                           'usd_meals', 'cad_meals']]

print(flight_schedule_expanded_df) #debugging

# Step 8: Save to CSV
#flight_schedules_df.to_csv("00_data/02_output/flight_schedules.csv", index=False)
flight_schedule_expanded_df.to_csv("00_data/02_output/flight_schedules_october.csv", index=False)
flight_schedule_expanded_df.to_excel("00_data/02_output/flight_schedule_october.xlsx", index=False)