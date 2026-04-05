import streamlit as st
import json
from pathlib import Path
from datetime import datetime, date
import uuid

# Naming the website
st.set_page_config(page_title="Polished to Perfection", layout="wide", initial_sidebar_state="expanded")

#Adding the files
# -----------------------------
users_file = Path("users.json")
appt_file = Path("appointments.json")
inventory_file = Path("inventory.json")

#loading the data
# ------------------------------
if users_file.exists():
    with open(users_file, "r") as f:
        users = json.load(f)
else:
    users = []
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)

if appt_file.exists():
    with open(appt_file, "r") as f:
        appointments = json.load(f)
else:
    appointments = []
    with open(appt_file, "w") as f:
        json.dump(appointments, f, indent=4)

if inventory_file.exists():
    with open(inventory_file, "r") as f:
        inventory = json.load(f)
else:
    inventory = []
    with open(inventory_file, "w") as f:
        json.dump(inventory, f, indent=4)
