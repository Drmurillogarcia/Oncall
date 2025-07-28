import streamlit as st
import pandas as pd
from datetime import datetime
import os

# App title
st.title("📅 Who's On Call")

# Folder with schedule files
SCHEDULE_FOLDER = "Schedules"

# Get list of books (months)
books = [f for f in os.listdir(SCHEDULE_FOLDER) if f.endswith(".csv")]
book_names = [f.replace("Schedule_", "").replace(".csv", "") for f in books]

# Book (month) selection
selected_book = st.selectbox("Select a schedule book (month)", book_names)

# Load the selected book
file_path = os.path.join(SCHEDULE_FOLDER, f"Schedule_{selected_book}.csv")
df = pd.read_csv(file_path)
df['Date'] = pd.to_datetime(df['Date'], format='%d-%b-%y', errors='coerce')

# Select a date
selected_date = st.date_input("Choose a date", datetime.today())

# Filter row for selected date
row = df[df['Date'].dt.date == selected_date]

# Define columns to check for names
name_columns = df.columns[2:]

def find_first_name(row):
    for col in name_columns:
        val = row[col]
        if isinstance(val, str) and val.strip():
            return val.strip()
    return "No name found"

# Display result
if not row.empty:
    first_name = find_first_name(row.iloc[0])
    st.success(f"✅ On {selected_date.strftime('%A, %d %B %Y')} → {first_name}")
else:
    st.warning("⚠️ No data found for that date.")
