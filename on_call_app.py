import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.title("📅 Who's On Call")

SCHEDULE_FOLDER = "schedules"

# Get today's date
today = datetime.today().date()

# Let user choose a date (default: today)
selected_date = st.date_input("Pick a date", today)

# Infer schedule filename from date
month_name = selected_date.strftime('%B')   # e.g., "July"
filename = f"Schedule_{month_name}.csv"
file_path = os.path.join(SCHEDULE_FOLDER, filename)

# Try to load the appropriate book
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')

    # Filter the row for the selected date
    row = df[df['Date'].dt.date == selected_date]

    # Define relevant columns to search for names
    name_columns = df.columns[2:]

    def find_first_name(row):
        for col in name_columns:
            cell = row[col]
            if isinstance(cell, str) and cell.strip():
                return cell.strip()
        return "No name found"

    if not row.empty:
        first_name = find_first_name(row.iloc[0])

        # Display automatic and manual result
        if selected_date == today:
            st.success(f"👨‍⚕️ On-call today ({today.strftime('%A, %d %B')}): **{first_name}**")
        else:
            st.info(f"📆 On-call for {selected_date.strftime('%A, %d %B %Y')}: **{first_name}**")
    else:
        st.warning("⚠️ No entry found for that date in this book.")
else:
    st.error(f"📁 No schedule found for {month_name}. Looking for `{filename}` in the `schedules/` folder.")
