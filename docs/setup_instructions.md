Setup Instructions

Follow these steps to run the project end-to-end.

1. Clone the Repository

2. Python Environment

Create a virtual environment and install dependencies:

python3 -m venv venv
source venv/bin/activate # (Linux/macOS)
venv\Scripts\activate # (Windows)

pip install -r requirements.txt

3. Prepare Data

Place raw CSV under data/customer_support_tickets.csv.

Run the cleaning script:

python python/ticketing_clean_sanitized.py --in data/customer_support_tickets.csv --out data/tickets_clean.csv

This removes PII, standardizes categories, computes SLA metrics, and outputs tickets_clean.csv.

4. Setup MySQL Database

Start MySQL server

Create database:

CREATE DATABASE ticketing_db;
USE ticketing_db;

Apply schema:

mysql -u root -p ticketing_db < sql/schema.sql

Load cleaned data:

python python/load_to_mysql_sanitized.py --csv data/tickets_clean.csv

Apply KPI views:

mysql -u root -p ticketing_db < sql/views.sql

5. Power BI Dashboard

Open powerbi/ticketing_kpis.pbit in Power BI Desktop

Configure the MySQL connection (DB_HOST, DB_USER, DB_PASSWORD, DB_NAME)

Refresh data to load KPIs

6. Environment Variables

Optional: create .env under env/ for safe DB configs:

DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=yourpassword
DB_NAME=ticketing_db
