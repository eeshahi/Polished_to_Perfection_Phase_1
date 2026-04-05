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


#Pricing and TOOLS NEEDED
# -----------------------------
service_price ={
    "Basic Manicure": 20,
    "Gel Manicure": 35,
    "Classic Pedicure": 30,
    "Acrylic Full Set": 50,
    "Nail Art Design": 15
}

service_inventory_map ={ 
    "Basic Manicure": ["Cuticle Oil", "Cotton Pads"],
    "Gel Manicure": ["Gel Polish", "Cuticle Oil", "Cotton Pads"],
    "Classic Pedicure": ["Cuticle Oil", "Cotton Pads"],
    "Acrylic Full Set": ["Acrylic Powder", "Nail Files", "Cotton Pads"],
    "Nail Art Design": ["Nail Files", "Cotton Pads"]
}

#Rewards Program and the points
reward_options = [
    {"name": "10% Off Next Service", "points": 50},
    {"name": "Free Nail Art Design", "points": 100},
    {"name": "Free Basic Manicure", "points": 250},
    {"name": "Free Gel Manicure", "points": 400}
]

#employees name for booking availability 
# _______________________________________
employee_names = ["Marissa", "Jackie", "Eesha Shahi"]

#timing of the salon and bookings 
all_times = ["9:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "1:00 PM", "2:00 PM", "3:00 PM", "4:00 PM", "5:00 PM"]

# save the users list back to all the paths 
def save_users():
    with open(users_file, "w") as f:
        json.dump(users, f, indent=4)


def save_appointments():
    with open(appt_file, "w") as f:
        json.dump(appointments, f, indent=4)


def save_inventory():
    with open(inventory_file, "w") as f:
        json.dump(inventory, f, indent=4)

