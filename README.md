# sales-analytics-system
Sales Analytics System

Project Overview

This project implements a Sales Data Analytics System for an e-commerce company using Python.
The system reads and cleans raw sales data, performs analytical computations, integrates with an external API (DummyJSON), enriches transaction records, and generates a comprehensive business report.

The implementation demonstrates Python fundamentals including file I/O, data cleaning, validation, data structures, API integration, error handling, and report generation.

Repository Structure
sales-analytics-system/
│
├── README.md
├── main.py
├── requirements.txt
│
├── utils/
│   ├── file_handler.py
│   ├── data_processor.py
│   ├── api_handler.py
│   └── report_generator.py
│
├── data/
│   ├── sales_data.txt
│   └── enriched_sales_data.txt
│
├── output/
│   └── sales_report.txt

Technologies Used

Python 3.13
Standard Python libraries (os, datetime, collections)
requests library for API integration

Dataset Description

File: sales_data.txt
Format: Pipe-delimited (|)
Encoding: Non-UTF-8 (handled programmatically)

Issues handled:

Commas in product names
Commas in numeric values
Missing / extra fields
Invalid quantities or prices
Invalid ID formats
Data Cleaning Rules
Invalid records are removed if:
Quantity ≤ 0
UnitPrice ≤ 0
Missing CustomerID or Region
TransactionID does not start with T

After cleaning:
Total records parsed: ~80
Valid records retained: ~70
Invalid records removed: ~10

Module Breakdown

Part 1: File Handling & Validation (file_handler.py)

Reads sales data with encoding fallback (utf-8, latin-1, cp1252)
Cleans raw data and parses it into structured dictionaries
Validates transactions and applies optional filters
Displays validation summary and available filter options

Part 2: Data Processing & Analysis (data_processor.py)

Provides analytical insights including:
Total revenue calculation
Region-wise sales analysis
Top-selling products
Customer purchase analysis
Daily sales trends
Peak sales day identification
Low-performing product detection

Part 3: API Integration (api_handler.py)

Fetches product data from the DummyJSON API
Creates a product mapping dictionary
Enriches sales transactions with API metadata
Saves enriched data to data/enriched_sales_data.txt

⚠️ API Limitation Note

The assignment requires fetching products using:
https://dummyjson.com/products?limit=100


Since sales ProductIDs range from P101–P110 and the API fetch is restricted to the first 100 products, enrichment results in 0 successful matches.
This behavior is expected and handled gracefully, as per assignment instructions.

API connection errors are handled safely, and the system continues execution without crashing.

Part 4: Report Generation (report_generator.py)

Generates a comprehensive formatted report saved to:
output/sales_report.txt


The report includes:

Header & metadata
Overall sales summary
Region-wise performance
Top 5 products
Top 5 customers
Daily sales trend
Product performance analysis
API enrichment summary

How to Run the Project
1. Install Dependencies
pip install -r requirements.txt

2. Run the Application

From the project root:

python main.py

Sample Console Output (Excerpt)
========================================
SALES ANALYTICS SYSTEM
========================================

[1/10] Reading sales data...
✓ Successfully read 80 transactions

[5/10] Analyzing sales data...
✓ Analysis complete

[6/10] Fetching product data from API...
✓ Successfully fetched 100 products from API

[9/10] Generating report...
✓ Sales report generated: output/sales_report.txt

[10/10] Process Complete!
========================================

Output Files

data/enriched_sales_data.txt → Enriched transaction data
output/sales_report.txt → Final analytical report

Error Handling & Robustness

Handles file encoding issues
Handles malformed data safely
Handles API failures without crashing
Ensures report generation even if API enrichment fails

Conclusion

This project delivers a complete, modular, and robust sales analytics pipeline.
All assignment requirements have been implemented as specified, with clear separation of concerns and defensive programming practices.