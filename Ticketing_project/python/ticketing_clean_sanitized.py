import argparse
import os
from pathlib import Path

import numpy as np
import pandas as pd

# --------------------
# Paths (relative / env-driven)
# --------------------
DEFAULT_IN = Path(os.getenv("RAW_TICKETS_CSV", "data/customer_support_tickets.csv"))
DEFAULT_OUT = Path(os.getenv("CLEAN_TICKETS_CSV", "data/tickets_clean.csv"))

def main(raw_path: Path, out_path: Path) -> None:
    df = pd.read_csv(raw_path)

    # --- Drop PII / customer-centric fields ---
    drop_cols = ["Customer Name", "Customer Email", "Customer Age", "Customer Gender"]
    existing_drop_cols = [c for c in drop_cols if c in df.columns]
    if existing_drop_cols:
        df = df.drop(columns=existing_drop_cols)

    # --- Rename columns to snake_case ---
    colmap = {
        "Ticket ID": "ticket_id",
        "Product Purchased": "product",
        "Date of Purchase": "purchase_date",
        "Ticket Type": "ticket_type",
        "Ticket Subject": "ticket_subject",
        "Ticket Description": "ticket_description",
        "Ticket Status": "status",
        "Resolution": "resolution_text",
        "Ticket Priority": "priority",
        "Ticket Channel": "channel",
        "First Response Time": "first_response_at",
        "Time to Resolution": "resolved_at",
        "Customer Satisfaction Rating": "satisfaction",
    }
    df = df.rename(columns=colmap)

    # --- Standardize categories ---
    if "status" in df.columns:
        df["status"] = (
            df["status"].astype(str)
            .str.strip()
            .str.lower()
            .replace({"pending customer response": "pending", "inprogress": "in progress", "resolved": "closed"})
            .str.title()
        )

    if "priority" in df.columns:
        p = df["priority"].astype(str).str.strip().str.title()
        valid = {"Low", "Medium", "High", "Critical"}
        df["priority"] = p.where(p.isin(valid), "Medium")

    # --- Parse timestamps (UTC) ---
    for col in ["purchase_date", "first_response_at", "resolved_at"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce", utc=True)

    # --- Compute durations & SLA flags ---
    is_closed = df.get("status", pd.Series([], dtype=str)).astype(str).str.lower().eq("closed")
    has_time_data = df.get("first_response_at", pd.Series([], dtype="datetime64[ns, UTC]")).notna() & \
                    df.get("resolved_at", pd.Series([], dtype="datetime64[ns, UTC]")).notna()

    df["handling_hours_after_first_response"] = np.where(
        is_closed & has_time_data,
        (df["resolved_at"] - df["first_response_at"]).dt.total_seconds() / 3600.0,
        np.nan,
    )

    SLA_TARGET_HOURS = {"Critical": 4, "High": 24, "Medium": 48, "Low": 72}
    df["sla_target_hours"] = df.get("priority", pd.Series([], dtype=str)).map(lambda p: SLA_TARGET_HOURS.get(p, 48))

    df["sla_breached"] = (
        is_closed
        & df["handling_hours_after_first_response"].notna()
        & (df["handling_hours_after_first_response"] > df["sla_target_hours"])
    ).astype(int)

    # Negative durations => NaN
    if "handling_hours_after_first_response" in df.columns:
        df["handling_hours_after_first_response"] = np.where(
            df["handling_hours_after_first_response"] < 0, np.nan, df["handling_hours_after_first_response"]
        )

    # --- Reorder columns for SQL schema ---
    keep = [
        "ticket_id",
        "ticket_type",
        "channel",
        "priority",
        "status",
        "first_response_at",
        "resolved_at",
        "handling_hours_after_first_response",
        "sla_target_hours",
        "sla_breached",
        "satisfaction",
        "product",
        "purchase_date",
        "ticket_subject",
        "ticket_description",
        "resolution_text",
    ]
    existing = [c for c in keep if c in df.columns]
    df = df[existing]

    # --- Ensure ticket_id present & not null ---
    if "ticket_id" in df.columns:
        # drop null/empty ticket_id rows to avoid DB errors and leaked bad records
        before = len(df)
        df = df[df["ticket_id"].astype(str).str.strip() != ""]
        df = df[df["ticket_id"].notna()]
        # enforce integer where possible (coerce errors to NaN then drop)
        df["ticket_id"] = pd.to_numeric(df["ticket_id"], errors="coerce")
        df = df[df["ticket_id"].notna()]
        df["ticket_id"] = df["ticket_id"].astype("int64")
        after = len(df)
        if after < before:
            print(f" Dropped {before - after} rows with missing/invalid ticket_id")

    # --- Format datetimes as naive strings for CSV (DB will parse) ---
    for col in ["first_response_at", "resolved_at", "purchase_date"]:
        if col in df.columns:
            s = df[col].dt.tz_convert(None).dt.strftime("%Y-%m-%d %H:%M:%S")
            df[col] = s.where(~df[col].isna(), "")

    # --- Write output ---
    out_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_path, index=False, encoding="utf-8")


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="Clean customer support tickets CSV (no PII).")
    ap.add_argument("--in", dest="raw_path", default=str(DEFAULT_IN), help="Path to raw tickets CSV")
    ap.add_argument("--out", dest="out_path", default=str(DEFAULT_OUT), help="Path to output cleaned CSV")
    args = ap.parse_args()
    main(Path(args.raw_path), Path(args.out_path))