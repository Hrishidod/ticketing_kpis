Ticketing KPI Dashboard

  This project provides an end-to-end pipeline for analyzing customer support tickets and visualizing key performance indicators (KPIs) in Power BI.
  It integrates data cleaning, relational database storage, SQL-based KPI definitions, and interactive dashboards.

Overview

The workflow includes:

- Raw data ingestion from CSV (customer_support_tickets.csv)

- Data cleaning and anonymization using Python (ticketing_clean_sanitized.py)

- Loading cleaned data into MySQL (schema.sql, load_to_mysql_sanitized.py, views.sql)

- KPI visualization in Power BI (ticketing_kpis.pbit)

- The result is a fully automated reporting system for tracking support performance, SLA compliance, and customer satisfaction.

Key Features

- Removal of personally identifiable information (PII) to ensure data privacy

- Standardization of categories (ticket status, priority levels, channels)

- SLA monitoring with automatic breach detection

- Duration and performance metrics computed in preprocessing

- Reusable SQL schema and views for KPI calculations

- Interactive dashboard with drill-down capabilities in Power BI

Tech Stack

- Python for data preprocessing and loading

- Pandas and NumPy for data manipulation

- MySQL for structured storage, schema enforcement, and view-based KPIs

- Power BI for visualization

- Optional environment variables for flexible configuration

KPIs Explained

The dashboard provides insights into the following areas:

- Backlog and Aging

  - Number of open vs. closed tickets

  - Distribution of ticket aging in time buckets (0–24h, 24–48h, 49–72h, over 72h)

- First Response Time (FRT)

  - Average number of hours until the first response

  - Breach rates by channel and by priority

- Resolution Performance and SLA Compliance

  - Average handling duration after the first response

  - SLA breach rates by ticket type, channel, and priority

  - Weekly SLA breach trends

- Customer Satisfaction (CSAT)

  - Average satisfaction scores by priority

  - Closed tickets with valid customer satisfaction ratings

- Weekly Trends

  - Responded and closed tickets by week

  - SLA breach percentages over time

Setup

 - Detailed installation and usage instructions are available in docs/setup_instructions.md. This includes setting up the Python environment, preparing the dataset, configuring MySQL, and connecting Power BI.

<img width="1881" height="808" alt="kpis_3" src="https://github.com/user-attachments/assets/08e5401b-3882-4826-890d-aa45b6b1711a" />
<img width="1883" height="368" alt="kpis_2" src="https://github.com/user-attachments/assets/6a534c47-1b9f-4973-8e72-14ffca36832c" />
<img width="1882" height="267" alt="kpis_1" src="https://github.com/user-attachments/assets/6ff33824-8bdd-4397-b8cd-fc694c474964" />
Some screenshots of the dashboard
