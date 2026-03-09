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
text = extract_text("00_data/01_input/flight_schedules.pdf")
blocks = re.split(r'_{119}', text)

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
    # Scenarios:
    # 1. -- 01 --
    # 2. A12 --
    # 3. -- 21 22 --
    # 4. -- 31

    # 1. A01 -- -- -- -- -- --
    # 2. P-- 06 -- 15 -- -- --
    # 3. R-- 21 22 -- 24 -- --
    # 4. I-- -- -- -- -- 31

    # Step 1: Grab only likely schedule lines (start with letter-dash-dash or space-dash-dash)

    # Option 1: 
    # schedule_lines = re.findall(r'(?:[A-Z]?\d{2}(?:\s\d{2})*|(?:\d{2}\s?)+)(?=\s*--)', block , re.MULTILINE)

    # Option 2:
    #schedule_lines = re.findall(r'(?:(?:[A-Z]?\d{2}(?:\s\d{2})*|(?:\d{2}\s?)+)\s*--|\b\d{1,2}h\d{1,2}\s*--)', block) #not getting -- 31
    
    # Option 3:
    schedule_lines = re.findall(r'(?:(?:[A-Z]?\d{2}(?:\s\d{2})*|(?:\d{2}\s?)+)\s*--|\b\d{1,2}h\d{1,2}\s*--|--\s?\d{2})', block)
    #print(schedule_lines)

    # Step 2: From those segments, pull out the actual 2-digit numbers
    start_dates = []
    for line in schedule_lines:
        # Option 1: Skip anything that looks like (12) or times like 01:30 or 12:15
        # cleaned_line = re.sub(r'\(\d{2}\)\d{1,2}:\d{2}' , '', line)

        # Option 2: Skip full match if it's a known time pattern like "3h14"
        if re.search(r'\b\d{1,2}h\d{2}\b', line):
            continue
        # Skip long digit strings (e.g., phone numbers, codes)
        if re.search(r'\d{5,}', line):
            continue
        # Skip if pattern is: 4 or more digits followed by optional space and then "--"
        if re.search(r'\b\d{4,}\s*-*\b', line):
            continue

        # #print(cleaned_line)
        nums = re.findall(r'\d{2}\b', line) #r'\d{2}'
        for n in nums:
            if n != "00" and int(n) <= 31:
                start_dates.append(n)

    print(start_dates) 

