# Enterprise Data Engineering Pipeline & Real-Time Ingestion System

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![MSSQL](https://img.shields.io/badge/Microsoft%20SQL%20Server-Data%20Warehouse-red?style=flat&logo=microsoft-sql-server)
![Power BI](https://img.shields.io/badge/Power%20BI-Business%20Intelligence-F2C811?style=flat&logo=power-bi)

## Project Description

This repository hosts a hybrid data engineering solution designed to simulate real-world data processing scenarios. The system integrates **Batch Processing** for corporate data and **Stream Processing** for financial market data, utilizing a centralized Microsoft SQL Server Data Warehouse.

The primary objective of this project is to demonstrate the implementation of robust, fault-tolerant ETL (Extract, Transform, Load) pipelines and automated data workflows without relying on enterprise-grade tools, showcasing raw coding proficiency in Python and SQL.

## System Architecture

The project consists of two main independent modules:

### 1. Batch ETL Module (`etl_pro.py`)
This module handles static data files (CSV/Excel) representing corporate employee records.
* **Extraction:** Reads raw data sources dynamically.
* **Transformation:** Applies data cleaning, type casting, and business logic validation (e.g., age restrictions, bonus calculations).
* **Loading:** Uses SQLAlchemy and PyODBC for high-performance data insertion into MS SQL Server.
* **Error Handling:** Implements a comprehensive `try-except` mechanism to manage operational failures (File Not Found, DB Connection Timeout) and logs incidents to a local file.

### 2. Real-Time Streaming Module (`canli_veri.py`)
This module connects to external APIs to fetch and store live financial data.
* **Data Source:** Binance Public API (BTC/USDT).
* **Ingestion:** Fetches JSON data at set intervals (simulating streaming).
* **Storage:** Appends real-time data to the SQL Server for historical analysis.
* **Visualization:** Designed to feed a live Power BI Dashboard.

### 3. Automation (`run_pipeline.bat`)
* Contains Windows Batch scripts configured with **Task Scheduler** to execute the pipelines automatically at specific time intervals, ensuring data freshness without manual intervention.

## Technical Stack

* **Programming Language:** Python 3.x
* **Libraries:** Pandas, Requests, SQLAlchemy, PyODBC
* **Database:** Microsoft SQL Server (Express Edition)
* **Visualization:** Microsoft Power BI Desktop
* **Version Control:** Git & GitHub
* **OS Integration:** Windows Task Scheduler / Batch Scripting

## Installation and Usage

1.  **Clone the Repository**
    ```bash
    git clone [https://github.com/ensar-sencan/Try_Except-ETL-Pipeline-MSSQL.git](https://github.com/ensar-sencan/Try_Except-ETL-Pipeline-MSSQL.git)
    ```

2.  **Install Dependencies**
    ```bash
    pip install pandas sqlalchemy pyodbc requests
    ```

3.  **Database Configuration**
    Update the connection string in `etl_pro.py` and `canli_veri.py` to match your local SQL Server instance:
    ```python
    Server = r'.\SQLEXPRESS' 
    Database = 'YourDatabaseName'
    ```

4.  **Execution**
    * Run `etl_pro.py` for batch processing.
    * Run `canli_veri.py` for starting the data stream.
    * Use `run_pipeline.bat` to test the automation logic.

## Project Structure

```text
├── etl_pro.py          # Main ETL script for employee data
├── canli_veri.py       # API streaming script for crypto data
├── run_pipeline.bat    # Automation script for Task Scheduler
├── etl_gunlugu.txt     # System log file (Generated automatically)
├── requirements.txt    # Python dependencies
└── README.md           # Project documentation
