# Requirements:
# pip install "camelot-py[cv]"

# Imports:
import camelot
import pandas as pd

# Step 1: Read the tables within the PDF file
lattice_tables = camelot.read_pdf("00_data/01_input/employee_schedules.pdf", pages='3', flavor="stream", split_text=True)

for table in lattice_tables:
    # Print the table to see its structure
    print(table.df)

# Step 2: Convert the list of DataFrames to a single DataFrame
# Note: This assumes that all tables have the same structure. If they don't, you may need to handle them separately
employee_schedules_df = table.df

# Step 3: Save to CSV
employee_schedules_df.to_csv("00_data/02_output/employee_schedules.csv", index=False)