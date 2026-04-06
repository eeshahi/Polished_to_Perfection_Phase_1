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

# count how many inventory items are low on stock
def get_low_stock_count():
    count = 0
    for item in inventory:
        if item["quantity"] <= item["low_stock_limit"]:
            count += 1
    return count


updated_users = False
for user in users:
    if ensure_user_reward_fields(user): #USED AI to help us with this part becuase we were getting errors
        updated_users = True

if updated_users:
    save_users()

# Logged-In Pages
# -----------------------------
# once logged in, show the correct role-based pages
else:
    if st.session_state["role"] == "Customer":  #page for the customers
        user_appts = get_user_appointments()
        upcoming_count = 0
        old_count = 0
        canceled_count = 0

        # calculate counts for customer dashboard KPI cards
        for appt in user_appts:
            if appt.get("status") == "Canceled":
                canceled_count += 1
            elif appt.get("status") == "Completed":
                old_count += 1
            elif is_past_appointment(appt):
                old_count += 1
            else:
                upcoming_count += 1

# grab reward data from the logged-in user
        reward_points = st.session_state["user"].get("reward_points", 0)
        reward_history = st.session_state["user"].get("reward_history", [])

    # customer dashboard page    #KPI cards
        if st.session_state["page"] == "dashboard":
            col1, col2, col3 = st.columns([2, 3, 2])
            with col2:
                st.header("Polished to Perfection - Customer Dashboard")
            st.divider()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                with st.container(border=True):
                    st.markdown("#### Upcoming")
                    st.markdown(f"## {upcoming_count}")
            with col2:
                with st.container(border            # KPI cards
                =True):
                    st.markdown("#### Old")
                    st.markdown(f"## {old_count}")
            with col3:
                with st.container(border=True):
                    st.markdown("#### Canceled")
                    st.markdown(f"## {canceled_count}")
            with col4:
                with st.container(border=True):
                    st.markdown("#### Reward Points")
                    st.markdown(f"## {reward_points}")


            st.divider()
            col1, col2 = st.columns([4, 2])
            with col1:
                with st.container(border=True):
                    st.markdown("### Quick Overview")
                    if len(user_appts) > 0:
                        for appt in user_appts:
                            st.markdown(f"**{appt['service']}** | {appt['date']} at {appt['time']} | {appt.get('status', 'Scheduled')}")
                    else:
                        st.info("No appointments found.")
            with col2:
                with st.container(border=True):
                    st.markdown("### Rewards Program")
                    st.write("Earn 10 points for every completed appointment.")
                    st.write("Redeem points for salon rewards.")
                    st.write(f"Your current points: {reward_points}")

        # booking page

        elif st.session_state["page"] == "book_appointment":
            st.header("Book Appointment")
            st.divider()

            col1, col2, col3 = st.columns([1, 3, 1])
            with col2:
                with st.container(border=True):
                    nail_service = st.selectbox("Service", list(service_prices.keys()), key="service_select")
                    employee = st.selectbox("Employee Name", employee_names, key="employee_select")
                    selected_date = st.date_input("Date", key="date_select")

# find already booked times for this employee/date

                    booked_times = []
                    for appt in appointments:
                        if appt["employee"] == employee and appt["date"] == str(selected_date) and appt.get("status") != "Canceled":
                            booked_times.append(appt["time"])

                    # only show available times
                    available_times = []
                    for appt_time in all_times:
                        if appt_time not in booked_times:
                            available_times.append(appt_time)

                    if len(available_times) > 0:
                        selected_time = st.selectbox("Time", available_times, key="time_select")
                    else:
                        selected_time = None
                        st.warning("No available times for this employee on this date.")

                    st.markdown(f"**Price:** ${service_prices[nail_service]}")

                    if st.button("Book Appointment", key="book_appointment_submit_btn", type="primary", use_container_width=True):
                        if selected_date < date.today(): #help of ai to help with this line 
                            st.error("You cannot book an appointment in the past.")
                        elif not selected_time:
                            st.error("Please choose a date with an available time.")
                        elif not has_inventory_for_service(nail_service):
                            st.error("Not enough inventory available to book this appointment.")
                        else:
                            subtract_success = False
                            with st.spinner("Recording..."):
                                new_appt = {
                                    "id": get_next_appointment_id(),
                                    "service": nail_service,
                                    "price": service_prices[nail_service],
                                    "date": str(selected_date),
                                    "time": selected_time,
                                    "employee": employee,
                                    "client": st.session_state["user"]["full_name"],
                                    "client_email": st.session_state["user"]["email"],
                                    "status": "Scheduled",
                                    "created_at": str(datetime.now()),
                                    "canceled_at": ""
                                }

                                subtract_success = update_inventory_for_service(nail_service, "subtract")
                                if subtract_success:
                                    appointments.append(new_appt)
                                    save_appointments()
                                    save_inventory()

                            if not subtract_success:
                                st.error("Inventory could not be updated for this appointment.")
                            else:
                                st.success("Appointment booked successfully.")
                                st.session_state["page"] = "my_appointments"
                                st.rerun()




