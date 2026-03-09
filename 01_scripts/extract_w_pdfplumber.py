# Requirements:
# pip install pdfplumber

# Imports:
import pdfplumber
import pandas as pd

tables = []

# Step 1: Read the tables within the PDF file
with pdfplumber.open("00_data/01_input/employee_schedules.pdf") as pdf:
    for page in pdf.pages:
        tables_on_page = page.extract_tables({
            "vertical_strategy": "text",
            "horizontal_strategy": "text"
        })

        if tables_on_page:
            for table in tables_on_page:
                if table:
                    tables.append({
                        'page' : pdf.pages.index(page),
                        'data' : table
                    })

# Step 2: Convert the list of DataFrames to a single DataFrame
# Note: This assumes that all tables have the same structure. If they don't, you may need to handle them separately
for table in tables:
    # Print the table to see its structure
    print('Page:', table['page'])
    print(pd.DataFrame(table['data']))

employee_schedules_df  = pd.DataFrame(tables[0]['data'])

# Step 3: Save to CSV
employee_schedules_df.to_csv("00_data/02_output/employee_schedules_pdf_plumber.csv", index=False)