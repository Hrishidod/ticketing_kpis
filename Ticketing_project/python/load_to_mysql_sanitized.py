import argparse
import os
from pathlib import Path

import pandas as pd
import mysql.connector

# --------------------
# Config via Env / CLI
# --------------------
DEFAULT_CSV = Path(os.getenv("CLEAN_TICKETS_CSV", "data/tickets_clean.csv"))

def get_db_cfg():
    return dict(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),
        database=os.getenv("DB_NAME", "ticketing_db"),
        # ssl_disabled by default; add SSL options here if needed
    )

# --------------------
# Helpers (safe casts)
# --------------------
def as_dt(v):
    if v is None or v == "" or (isinstance(v, float) and pd.isna(v)):
        return None
    return pd.to_datetime(v, errors="coerce").to_pydatetime()

def as_str(v):
    if v is None or (isinstance(v, float) and pd.isna(v)) or v == "":
        return None
    return str(v)

def as_int(v):
    if v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip() == "":
        return None
    try:
        return int(float(v))
    except Exception:
        return None

def as_float(v):
    if v is None or (isinstance(v, float) and pd.isna(v)) or str(v).strip() == "":
        return None
    try:
        return float(v)
    except Exception:
        return None

def validate_row(row):
    # Ensure ticket_id exists; skip otherwise to avoid DB integrity errors
    return as_int(row.get("ticket_id")) is not None

def main(csv_path: Path) -> None:
    df = pd.read_csv(csv_path, dtype=str)

    # Cast numeric columns where present
    for col in ["handling_hours_after_first_response", "sla_target_hours", "satisfaction", "sla_breached"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Filter invalid rows early
    before = len(df)
    df = df[df.apply(validate_row, axis=1)]
    after = len(df)
    if after < before:
        print(f"Skipping {before - after} rows due to missing/invalid ticket_id")

    cfg = get_db_cfg()
    conn = mysql.connector.connect(**cfg)
    cur = conn.cursor()

    sql = '''
    INSERT INTO Tickets (
      ticket_id, ticket_type, channel, priority, status,
      first_response_at, resolved_at,
      handling_hours_after_first_response, sla_target_hours, sla_breached,
      satisfaction, product, purchase_date,
      ticket_subject, ticket_description, resolution_text
    ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    '''

    rows = []
    for _, r in df.iterrows():
        rows.append((
            as_int(r.get("ticket_id")),
            as_str(r.get("ticket_type")),
            as_str(r.get("channel")),
            as_str(r.get("priority")),
            as_str(r.get("status")),
            as_dt(r.get("first_response_at")),
            as_dt(r.get("resolved_at")),
            as_float(r.get("handling_hours_after_first_response")),
            as_float(r.get("sla_target_hours")),
            0 if pd.isna(r.get("sla_breached")) else int(float(r.get("sla_breached"))),
            as_int(r.get("satisfaction")),
            as_str(r.get("product")),
            as_dt(r.get("purchase_date")),
            as_str(r.get("ticket_subject")),
            as_str(r.get("ticket_description")),
            as_str(r.get("resolution_text")),
        ))

    cur.executemany(sql, rows)
    conn.commit()
    print(f" Loaded {len(rows)} rows into {cfg['database']}.Tickets")

    cur.close()
    conn.close()

if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Load cleaned tickets CSV into MySQL")
    ap.add_argument("--csv", default=str(DEFAULT_CSV), help="Path to tickets_clean.csv")
    args = ap.parse_args()
    main(Path(args.csv))