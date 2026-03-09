# Requirements:
# install Java JDK (ARM64 DMG Installer) https://www.oracle.com/java/technologies/downloads/?er=221886#jdk24-mac
# Set JAVA_HOME to the JDK path (to check the path, run echo $JAVA_HOME)
# pip install tabula-py

# Imports:
import tabula
import pandas as pd

# Step 1: Read the tables within the PDF file
tables = tabula.read_pdf("00_data/01_input/employee_schedules.pdf", pages=1, multiple_tables=True)

print(tables)