import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
import os

st.title("📅 Who's On Call")

SCHEDULE_FOLDER = "schedules"

# Get current time
now = datetime.now()
today = now.date()

# Adjust logic based on 8 AM cutoff
effective_date = today
if now.hour < 8:
    effective_date = today - timedelta(days=1)

# Let user pick a date (default to effective date)
selected_date = st.date_input("Pick a date", effective_date)

# Determine the month and file to load
month_name = selected_date.strftime('%B')   # e.g. "July"
filename = f"Schedule_{month_name}.csv"
file_path = os.path.join(SCHEDULE_FOLDER, filename)

# Try to load the correct schedule file
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')

    # Find the row for selected date
    row = df[df['Date'].dt.date == selected_date]

    # Columns where names are listed
    name_columns = df.columns[2:]

    def find_first_name(row):
        for col in name_columns:
            val = row[col]
            if isinstance(val, str) and val.strip():
                return val.strip()
        return "No name found"

    if not row.empty:
        first_name = find_first_name(row.iloc[0])
        if selected_date == effective_date:
            st.success(f"👨‍⚕️ On-call now ({selected_date.strftime('%A, %d %B')}): **{first_name}**")
        else:
            st.info(f"📆 On-call for {selected_date.strftime('%A, %d %B %Y')}: **{first_name}**")
    else:
        st.warning("⚠️ No data found for that date in this book.")
else:
    st.error(f"📁 Schedule file not found: `{filename}` inside `/schedules/`")
