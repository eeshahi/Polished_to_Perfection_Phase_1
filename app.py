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

# refresh the logged-in user data because it may change 
def refresh_logged_in_user():
    if st.session_state["user"] is not None:
        for user in users:
            if user["id"] == st.session_state["user"]["id"]:
                st.session_state["user"] = user
                break


#making sure each of the rewards have fields and they work
def ensure_user_reward_fields(user):
    updated = False
    if "reward_points" not in user:
        user["reward_points"] = 0
        updated = True
    if "reward_history" not in user:
        user["reward_history"] = []
        updated = True
    return updated

#finding the next appointment id
def get_next_appointment_id():
    if len(appointments) == 0:
        return 1
    max_id = 0
    for appt in appointments:
        if appt["id"] > max_id:
            max_id = appt["id"]
    return max_id + 1

# find one inventory item by its item name
def get_item_by_name(item_name):
    for item in inventory:
        if item["item_name"] == item_name:
            return item
    return None

# check whether all needed inventory exists for a service
def has_inventory_for_service(service_name):
    required_items = service_inventory_map[service_name]
    for required_item in required_items:
        item = get_item_by_name(required_item)
        if item is None or item["quantity"] < 1:
            return False
    return True

# add or subtract inventory when appointments are booked or canceled
def update_inventory_for_service(service_name, action):
    required_items = service_inventory_map[service_name]

    if action == "subtract":
        for required_item in required_items:
            item = get_item_by_name(required_item)
            if item is None or item["quantity"] < 1:
                return False

        for required_item in required_items:
            item = get_item_by_name(required_item)
            item["quantity"] -= 1
        return True

    if action == "add":
        for required_item in required_items:
            item = get_item_by_name(required_item)
            if item:
                item["quantity"] += 1
        return True

    return False

# get only the appointments that belong to the logged-in customer
def get_user_appointments():
    user_appts = []
    for appt in appointments:
        if appt.get("client_email") == st.session_state["user"]["email"]:
            user_appts.append(appt)
    return user_appts

## get only the appointments assigned to the logged-in employee
def get_employee_appointments():
    employee_appts = []
    for appt in appointments:
        if appt.get("employee") == st.session_state["user"]["full_name"]:
            employee_appts.append(appt)
    return employee_appts

# check if an appointment time is already in the past
def is_past_appointment(appt):
    appointment_datetime = datetime.strptime(
        f"{appt['date']} {appt['time']}",
        "%Y-%m-%d %I:%M %p" #used ai to help run this line of code
    )
    return appointment_datetime < datetime.now()

# add reward points to a customer after a completed appointment
def add_reward_points_to_customer(customer_email, points_to_add):
    for user in users:
        if user["email"] == customer_email:
            ensure_user_reward_fields(user)
            user["reward_points"] += points_to_add
            break
    save_users()
    refresh_logged_in_user()

# redeem a reward if the customer has enough points
def redeem_reward_for_customer(user_id, reward_name, reward_cost):
    for user in users:
        if user["id"] == user_id:
            ensure_user_reward_fields(user)
            if user["reward_points"] >= reward_cost:
                user["reward_points"] -= reward_cost
                user["reward_history"].append({
                    "reward_name": reward_name,
                    "points_used": reward_cost,
                    "redeemed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "Available"
                })
                save_users()
                refresh_logged_in_user()
                return True
    return False



    