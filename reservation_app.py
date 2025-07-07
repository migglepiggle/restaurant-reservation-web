import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- Setup ---
st.set_page_config(page_title="Reservation Manager", layout="wide")

# --- File paths ---
MENU_FILE = "menu.csv"
RES_FILE = "reservations.csv"

# --- Load or create CSVs ---
def load_menu():
    if not os.path.exists(MENU_FILE):
        pd.DataFrame(columns=["Item", "Price"]).to_csv(MENU_FILE, index=False)
    return pd.read_csv(MENU_FILE)

def load_reservations():
    if not os.path.exists(RES_FILE):
        pd.DataFrame(columns=["Name", "Guests", "Date", "Time"]).to_csv(RES_FILE, index=False)
    return pd.read_csv(RES_FILE)

def save_menu(df):
    df.to_csv(MENU_FILE, index=False)

def save_reservations(df):
    df.to_csv(RES_FILE, index=False)

# --- UI Layout ---
st.title("🍴 Menu & Reservation Manager")

# === Sidebar: Menu Editor ===
st.sidebar.header("📋 Edit Menu")

menu_df = load_menu()
new_item = st.sidebar.text_input("New Item")
new_price = st.sidebar.number_input("Price ($)", min_value=0.0, format="%.2f")
if st.sidebar.button("➕ Add to Menu"):
    if new_item and new_price:
        menu_df = pd.concat([menu_df, pd.DataFrame([[new_item, new_price]], columns=["Item", "Price"])], ignore_index=True)
        save_menu(menu_df)
        st.sidebar.success(f"Added {new_item}!")

# === Main Panel: Menu Display ===
st.subheader("📃 Current Menu")
if not menu_df.empty:
    st.dataframe(menu_df, use_container_width=True)
else:
    st.info("Menu is empty. Add items from the sidebar.")

# === Reservation Booking ===
st.subheader("🪑 Make a Reservation")
res_df = load_reservations()
with st.form("res_form"):
    name = st.text_input("Name")
    guests = st.number_input("Number of Guests", min_value=1, max_value=20, step=1)
    date = st.date_input("Date")
    time = st.time_input("Time")
    submit = st.form_submit_button("Book Table")

    if submit:
        if name:
            new_res = pd.DataFrame([[name, guests, date.strftime("%Y-%m-%d"), time.strftime("%H:%M")]],
                                   columns=["Name", "Guests", "Date", "Time"])
            res_df = pd.concat([res_df, new_res], ignore_index=True)
            save_reservations(res_df)
            st.success(f"Reservation booked for {name}!")
        else:
            st.error("Name is required.")

# === View/Cancel Reservations ===
st.subheader("📅 Current Reservations")

if not res_df.empty:
    selected_name = st.selectbox("Select a name to cancel reservation", options=res_df["Name"].unique())
    if st.button("❌ Cancel Reservation"):
        res_df = res_df[res_df["Name"] != selected_name]
        save_reservations(res_df)
        st.success(f"Reservation for {selected_name} cancelled.")
    st.dataframe(res_df, use_container_width=True)
else:
    st.info("No reservations yet.")
