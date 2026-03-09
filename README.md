# PDF Flight Schedule Parser & Bid Optimizer

A Python tool that converts flight schedule PDFs into structured datasets and identifies optimal flight options based on user-defined preferences.

This project demonstrates document parsing, data extraction, and rule-based optimization to transform unstructured scheduling data into actionable insights.

---

## Project Overview

Many scheduling systems distribute information in PDF format, which makes automated analysis difficult.  
This project extracts relevant information from schedule PDFs and converts it into a structured dataset that can be programmatically analyzed.

The processed data can then be filtered or scored based on user preferences (for example: preferred days off, schedule gaps, or trip patterns) to help identify optimal options.

---

## Features

- Extracts structured data from flight schedule PDFs
- Converts schedule information into a clean tabular dataset
- Enables filtering based on user-defined preferences
- Identifies optimal flight options for bidding
- Modular pipeline for parsing, transformation, and analysis

---

## Workflow

The typical workflow is:

1. Input schedule PDFs
2. Parse and extract relevant schedule information
3. Convert extracted data into a structured dataset
4. Apply preference-based filtering or scoring
5. Output a list of recommended flight options

---

## Installation

Clone the repository:

```
git clone https://github.com/shelly-gsr/pdf-flight-schedule-parser.git
cd pdf-flight-schedule-parser
```

--- 

## Example Output

Example structured dataset:

| Flight | Origin | Destination | Departure | Arrival |
| ------ | ------ | ----------- | --------- | ------- |
| 102    | YYC    | YVR         | 08:00     | 09:20   |
| 215    | YYC    | YYZ         | 13:30     | 19:10   |

Example recommended flights:

```
Flight 215 - Preferred schedule match
Flight 102 - Good alignment with requested days off
```

---

## Possible Improvements

Future extensions could include:
- Automatic schedule visualization
- More advanced optimization rules
- Integration with calendar APIs
- Support for multiple schedule formats
- Interactive dashboard for schedule exploration