import re

block = "A12 -- -- 05 06 -- -- 31 -- TMP -- -- 13 15 -- A07 --"

# Step 1: Find all groups that include numbers and might be around dashes
segments = re.findall(r'(?:[A-Z]?\d{2}(?:\s\d{2})*|(?:\d{2}\s?)+)(?=\s*--)', block)

# Step 2: From those segments, pull out the actual 2-digit numbers
start_dates = []
for seg in segments:
    nums = re.findall(r'\d{2}', seg)
    if nums:
        start_dates.extend(nums)

print(start_dates)