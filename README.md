# Real-Time Data Engineering Pipeline

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python)
![MSSQL](https://img.shields.io/badge/Microsoft%20SQL%20Server-Data%20Warehouse-red?style=flat&logo=microsoft-sql-server)
![Docker](https://img.shields.io/badge/Docker-Containerized%20DB-2496ED?style=flat&logo=docker)
![Power BI](https://img.shields.io/badge/Power%20BI-Dashboard-F2C811?style=flat&logo=power-bi)
![Telegram](https://img.shields.io/badge/Telegram-Bot%20API-2CA5E0?style=flat&logo=telegram)

## Overview

This repository is a hands-on data engineering portfolio built from scratch. It demonstrates the full data lifecycle: ingesting raw data from multiple sources, transforming and storing it in a relational data warehouse, automating the pipeline, and visualizing the output — running on a containerized local infrastructure secured with role-based database access control.

The project is structured in two modules that work independently but share the same SQL Server data warehouse.

---

## Architecture

```
[Source: CSV / Binance API]
         |
         v
[Python ETL Scripts]  ──── Error Handling (try-except)
         |                 Data Validation & Transformation
         v
[Docker Container]
[MS SQL Server : 1433]  ──── Fact Tables, Views, Stored Procedures
         |                   Role-Based Access Control (RBAC)
         |                   Dedicated ETL User (least privilege)
         ├──> [Power BI Dashboard]     (Visualization)
         └──> [Telegram Bot Alerts]    (Real-time Notifications)

[Windows Task Scheduler]  ──── Automated daily execution via .bat script
```

---

## Modules

### Module 1 — Batch ETL Pipeline (`etl_pro.py`)

Processes static corporate employee data from CSV files and loads it into SQL Server.

**What it does:**
- Reads raw CSV data dynamically
- Applies business rule validation (age restrictions, salary corrections)
- Calculates derived metrics (e.g., bonus fields)
- Loads clean data into MS SQL Server using SQLAlchemy + PyODBC
- Handles failures gracefully with `try-except` blocks
- Writes structured logs to `etl_gunlugu.txt` for monitoring

**Automation:** Configured with Windows Task Scheduler via `run_pipeline.bat` to run on a defined schedule without manual intervention.

---

### Module 2 — Real-Time Streaming & Alert System (`canli_veri.py`)

Connects to the Binance public API to collect live BTC/USDT price data and stores it in SQL Server for historical analysis.

**What it does:**
- Fetches live JSON data from Binance API at set intervals
- Appends each data point to the `Kripto_Fiyatlari` table in SQL Server
- Evaluates incoming prices against a configurable threshold
- Sends instant push notifications to a mobile device via Telegram Bot API when the threshold is breached
- API credentials are stored securely using `.env` (never committed to version control)

---

## Infrastructure & Security

### Docker — Containerized SQL Server

The SQL Server database runs inside a Docker container, isolating the database engine from the host system and ensuring a reproducible, portable environment.

- SQL Server is exposed on **port 1433** and mapped to the host for local application connectivity
- The container is configured via `docker-compose.yml` with persistent volume mounting to preserve data across restarts

### Role-Based Access Control (RBAC)

Instead of using the default `sa` (system administrator) account for application connections, a dedicated low-privilege SQL user was created following the **principle of least privilege**:

```sql
-- Create a dedicated ETL user
CREATE LOGIN etl_user WITH PASSWORD = 'your_password';
CREATE USER etl_user FOR LOGIN etl_user;

-- Grant only the necessary permissions (read + write on specific tables)
ALTER ROLE db_datawriter ADD MEMBER etl_user;
ALTER ROLE db_datareader ADD MEMBER etl_user;
```

This ensures that even if the application credentials are compromised, the blast radius is limited to data read/write operations only — no schema changes, no administrative access.

---

## Power BI Dashboard

The `Kripto_Fiyatlari` table is connected directly to Power BI Desktop via SQL Server connector. The dashboard displays real-time price movement as data is streamed into the warehouse.

![Power BI Dashboard](assets/powerbi_dashboard.png)

> *Dashboard shows BTC/USDT price over time, sourced live from SQL Server.*

---

## Project Structure

```
├── etl_pro.py              # Batch ETL pipeline for employee data
├── canli_veri.py           # Real-time API streaming + Telegram alerts
├── telegram.py             # Standalone Telegram bot test module
├── run_pipeline.bat        # Automation script for Task Scheduler
├── docker-compose.yml      # Docker configuration for SQL Server container
├── etl_gunlugu.txt         # Auto-generated execution log
├── yeni_personel.csv       # Sample source data for ETL module
├── requirements.txt        # Python dependencies
├── .env                    # API credentials (not committed — see .gitignore)
├── .gitignore              # Excludes .env and sensitive files
├── assets/
│   └── powerbi_dashboard.png   # Dashboard screenshot
└── README.md
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.10+ |
| Data Manipulation | Pandas |
| Database Connectivity | SQLAlchemy, PyODBC |
| HTTP / API | Requests |
| Scheduling | Windows Task Scheduler |
| Database | Microsoft SQL Server (Docker, port 1433) |
| Containerization | Docker |
| Visualization | Power BI Desktop |
| Notifications | Telegram Bot API |
| Security | python-dotenv (.env), RBAC (least privilege SQL user) |
| Version Control | Git, GitHub |

---

## Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/ensar-sencan/Real-Time-Data-Engineering-Pipeline.git
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Start the SQL Server container:
   ```bash
   docker-compose up -d
   ```

4. Create a `.env` file in the project root:
   ```
   TELEGRAM_TOKEN=your_bot_token_here
   TELEGRAM_CHAT_ID=your_chat_id_here
   ```

5. Update the SQL Server connection string in `etl_pro.py` and `canli_veri.py`.

6. Run the ETL pipeline:
   ```bash
   python etl_pro.py
   ```

7. Run the streaming bot:
   ```bash
   python canli_veri.py
   ```

---

## Author

**Ensar Sencan**  
Computer Engineering Student | Aspiring Data Engineer  
[LinkedIn](https://linkedin.com/in/ensar-sencan) · [GitHub](https://github.com/ensar-sencan)
