import streamlit as st
import json
from pathlib import Path
from datetime import datetime, date
import uuid

# Naming the website
st.set_page_config(page_title="Polished to Perfection", layout="wide", initial_sidebar_state="expanded")

# Session State
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "user" not in st.session_state:
    st.session_state["user"] = None
if "role" not in st.session_state:
    st.session_state["role"] = None
if "page" not in st.session_state:
    st.session_state["page"] = "dashboard"
if "selected_appointment_id" not in st.session_state:
    st.session_state["selected_appointment_id"] = None
if "restock_item_id" not in st.session_state:
    st.session_state["restock_item_id"] = None
if "appointment_status_filter" not in st.session_state:
    st.session_state["appointment_status_filter"] = "All"
if "customer_history_filter" not in st.session_state:
    st.session_state["customer_history_filter"] = "All"
if "messages" not in st.session_state:
    st.session_state["messages"] = []

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


#Marissa code added (Appointment Page)
        elif st.session_state["page"] == "my_appointments":
            st.header("My Appointments")
            st.divider()

            history_search = st.text_input("Search by service", key="customer_history_search")
            history_filter = st.selectbox(
                "Status",
                ["All", "Upcoming", "Old", "Canceled"],
                key="customer_history_filter_box"
            )
            st.session_state["customer_history_filter"] = history_filter

            upcoming_tab, old_tab, canceled_tab = st.tabs(["Upcoming", "Old", "Canceled"])

            with upcoming_tab:
                upcoming_appointments = []
                for appt in user_appts:
                    matches_search = history_search.lower() in appt["service"].lower()
                    is_upcoming = appt.get("status") not in ["Canceled", "Completed"] and not is_past_appointment(appt)
                    matches_filter = st.session_state["customer_history_filter"] in ["All", "Upcoming"]
                    if matches_search and is_upcoming and matches_filter:
                        upcoming_appointments.append(appt)

                col1, col2 = st.columns([4, 2])
                with col1:
                    with st.container(border=True):
                        st.markdown("### Appointment List")
                        if len(upcoming_appointments) > 0:
                            appointment_table = []
                            for appt in upcoming_appointments:
                                appointment_table.append({
                                    "Service": appt["service"],
                                    "Date": appt["date"],
                                    "Time": appt["time"],
                                    "Employee": appt["employee"],
                                    "Status": appt.get("status", "Scheduled")
                                })

                            st.dataframe(appointment_table, use_container_width=True)

                            selected_upcoming_appt = st.selectbox(
                                "Select Appointment",
                                upcoming_appointments,
                                format_func=lambda x: f"{x['service']} | {x['date']} {x['time']} | {x['employee']}", ## used AI to help create this line of code 
                                key="customer_upcoming_selectbox"
                            )

                            if selected_upcoming_appt:
                                st.session_state["selected_appointment_id"] = selected_upcoming_appt["id"]
                        else:
                            st.info("No upcoming appointments found.")

                with col2:
                    with st.container(border=True):
                        st.markdown("### Appointment Details")
                        selected_appt = None
                        for appt in upcoming_appointments:
                            if appt["id"] == st.session_state["selected_appointment_id"]:
                                selected_appt = appt
                                break

                        if selected_appt:
                            st.markdown(f"**Service:** {selected_appt['service']}")
                            st.markdown(f"**Price:** ${selected_appt['price']}")
                            st.markdown(f"**Date:** {selected_appt['date']}")
                            st.markdown(f"**Time:** {selected_appt['time']}")
                            st.markdown(f"**Employee:** {selected_appt['employee']}")
                            st.markdown(f"**Status:** {selected_appt.get('status', 'Scheduled')}")

                            if is_past_appointment(selected_appt):
                                st.warning("This appointment has already passed and can no longer be canceled.")
                            else:
                                if st.button("Cancel Appointment", key=f"cancel_appointment_{selected_appt['id']}", type="primary", use_container_width=True):
                                    with st.spinner("Recording..."):
                                        for appt in appointments:
                                            if appt["id"] == selected_appt["id"]:
                                                appt["status"] = "Canceled"
                                                appt["canceled_at"] = str(datetime.now())
                                                update_inventory_for_service(appt["service"], "add")
                                                break
                                        save_appointments()
                                        save_inventory()
                                    st.success("Appointment canceled successfully.")
                                    st.session_state["selected_appointment_id"] = None
                                    st.rerun()
                        else:
                            st.info("Select an appointment to view details.")

            with old_tab:
                old_appointments = []
                for appt in user_appts:
                    matches_search = history_search.lower() in appt["service"].lower()
                    is_old = appt.get("status") == "Completed" or (is_past_appointment(appt) and appt.get("status") != "Canceled")
                    matches_filter = st.session_state["customer_history_filter"] in ["All", "Old"]
                    if matches_search and is_old and matches_filter:
                        old_appointments.append(appt)

                if len(old_appointments) > 0:
                    old_table = []
                    for appt in old_appointments:
                        display_status = appt.get("status", "Scheduled")
                        if display_status == "Scheduled" and is_past_appointment(appt):
                            display_status = "Completed"
                        old_table.append({
                            "Service": appt["service"],
                            "Date": appt["date"],
                            "Time": appt["time"],
                            "Employee": appt["employee"],
                            "Status": display_status,
                            "Price": appt["price"]
                        })
                    st.dataframe(old_table, use_container_width=True)
                else:
                    st.info("No old appointments found.")

            with canceled_tab:
                canceled_appointments = []
                for appt in user_appts:
                    matches_search = history_search.lower() in appt["service"].lower()
                    is_canceled = appt.get("status") == "Canceled"
                    matches_filter = st.session_state["customer_history_filter"] in ["All", "Canceled"]
                    if matches_search and is_canceled and matches_filter:
                        canceled_appointments.append(appt)

                if len(canceled_appointments) > 0:
                    canceled_table = []
                    for appt in canceled_appointments:
                        canceled_table.append({
                            "Service": appt["service"],
                            "Date": appt["date"],
                            "Time": appt["time"],
                            "Employee": appt["employee"],
                            "Status": appt.get("status", "Canceled")
                        })
                    st.dataframe(canceled_table, use_container_width=True)
                else:
                    st.info("No canceled appointments found.")

# Reward code from JACKIE 

        elif st.session_state["page"] == "rewards":
            st.header("Rewards Program")
            st.divider()

            redeem_tab, history_tab = st.tabs(["Redeem Reward", "Reward History"])

            with redeem_tab:
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    with st.container(border=True):
                        st.markdown("### Available Rewards")
                        st.write(f"Current Points: {reward_points}")
                        st.divider()

                        for reward in reward_options:
                            with st.container(border=True):
                                st.markdown(f"**Reward:** {reward['name']}")
                                st.markdown(f"**Points Required:** {reward['points']}")

                                if reward_points >= reward["points"]:
                                    if st.button(f"Redeem {reward['name']}", key=f"redeem_{reward['name']}", type="primary", use_container_width=True):
                                        redeemed = False
                                        with st.spinner("Recording..."):
                                            redeemed = redeem_reward_for_customer(
                                                st.session_state["user"]["id"],
                                                reward["name"],
                                                reward["points"]
                                            )
                                        if redeemed:
                                            st.success(f"{reward['name']} redeemed successfully.")
                                            st.rerun()
                                else:
                                    st.warning("Not enough points for this reward.")

            with history_tab:
                col1, col2, col3 = st.columns([1, 3, 1])
                with col2:
                    with st.container(border=True):
                        st.markdown("### Reward History")
                        if len(reward_history) > 0:
                            for reward_item in reward_history:
                                with st.container(border=True):
                                    st.markdown(f"**Reward:** {reward_item['reward_name']}")
                                    st.markdown(f"**Points Used:** {reward_item['points_used']}")
                                    st.markdown(f"**Redeemed At:** {reward_item['redeemed_at']}")
                                    st.markdown(f"**Status:** {reward_item['status']}")
                        else:
                            st.info("No rewards redeemed yet.")

#Penny Chat (Chatbox from Jackie Add)
        elif st.session_state["page"] == "penny_chat":
            st.header("Penny the Polish Pro")
            st.divider()

            st.write("Ask Penny about appointments, booking, cancellations, services, rewards, and nail tech information.")

            if st.button("Clear Chat", key="clear_customer_chat"):
                st.session_state["messages"] = []
                st.rerun()

            for message in st.session_state["messages"]:
                with st.chat_message(message["role"]):
                    st.write(message["content"])

            prompt = st.chat_input(
                "Ask Penny the Polish Pro, our AI salon assistant, something...",
                key="customer_chat_input"
            )

            if prompt:
                st.session_state["messages"].append({"role": "user", "content": prompt})

                prompt_lower = prompt.lower()

                user_appts_for_chat = [
                    a for a in appointments
                    if "client_email" in a and a["client_email"] == st.session_state["user"]["email"]
                ]

                if "appointment" in prompt_lower and "have" in prompt_lower:
                    if user_appts_for_chat:
                        response = "You currently have these appointments:\n"
                        for appt in user_appts_for_chat:
                            response += f"- {appt['date']} at {appt['time']} for {appt['service']} with {appt['employee']}\n"
                    else:
                        response = "You do not have any appointments booked right now."

                elif "cancel" in prompt_lower:
                    response = "To cancel an appointment, go to the My Appointments section and select your appointment in the Upcoming tab."

                elif "service" in prompt_lower:
                    response = "Available services are Basic Manicure, Gel Manicure, Classic Pedicure, Acrylic Full Set, and Nail Art Design."

                elif "status" in prompt_lower:
                    if user_appts_for_chat:
                        response = "Here are your current appointment statuses:\n"
                        for appt in user_appts_for_chat:
                            response += f"- {appt['service']} on {appt['date']} is {appt.get('status', 'Scheduled')}\n"
                    else:
                        response = "You do not have any appointment statuses to check right now."

                elif "employee" in prompt_lower or "tech" in prompt_lower:
                    response = "Current nail techs are Marissa, Jackie, and Eesha."

                elif "book" in prompt_lower or "schedule" in prompt_lower:
                    response = "To book an appointment, go to the Book Appointment section, choose a service, employee, date, and time, then click Book Appointment."

                elif "reward" in prompt_lower or "points" in prompt_lower:
                    response = f"You currently have {reward_points} reward points. Go to the Rewards page to redeem them."

                else:
                    response = "I can help with appointments, booking, cancellations, services, statuses, rewards, and nail tech information."

                st.session_state["messages"].append({"role": "assistant", "content": response})
                st.rerun()

    elif st.session_state["role"] == "Employee":
        employee_appts = get_employee_appointments()
        todays_appointments = 0
        scheduled_appointments = 0
        completed_appointments = 0

        for appt in employee_appts:
            if appt["date"] == str(date.today()) and appt.get("status") != "Canceled":
                todays_appointments += 1
            if appt.get("status") == "Scheduled":
                scheduled_appointments += 1
            if appt.get("status") == "Completed":
                completed_appointments += 1

#last code from Jackie/Marissa worked on it together
        low_stock_count = get_low_stock_count()

        if st.session_state["page"] == "dashboard":
            col1, col2, col3 = st.columns([2, 3, 2])
            with col2:
                st.header("Polished to Perfection - Employee Dashboard")
            st.divider()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                with st.container(border=True):
                    st.markdown("#### Today's Appointments")
                    st.markdown(f"## {todays_appointments}")
            with col2:
                with st.container(border=True):
                    st.markdown("#### Scheduled")
                    st.markdown(f"## {scheduled_appointments}")
            with col3:
                with st.container(border=True):
                    st.markdown("#### Completed")
                    st.markdown(f"## {completed_appointments}")
            with col4:
                with st.container(border=True):
                    st.markdown("#### Low Stock")
                    st.markdown(f"## {low_stock_count}")

            st.divider()
            col1, col2 = st.columns([4, 2])
            with col1:
                with st.container(border=True):
                    st.markdown("### Assigned Appointments")
                    if len(employee_appts) > 0:
                        for appt in employee_appts:
                            st.markdown(f"**{appt['client']}** | {appt['service']} | {appt['date']} at {appt['time']} | {appt.get('status', 'Scheduled')}")
                    else:
                        st.info("No appointments assigned yet.")
            with col2:
                with st.container(border=True):
                    st.markdown("### Inventory Alerts")
                    if low_stock_count > 0:
                        for item in inventory:
                            if item["quantity"] <= item["low_stock_limit"]:
                                st.warning(f"{item['item_name']} is low on stock")
                    else:
                        st.success("No low stock items right now.")

        elif st.session_state["page"] == "manage_appointments":
            st.header("Manage Appointments")
            st.divider()

            col1, col2 = st.columns([4, 2])
            with col1:
                with st.container(border=True):
                    search_name = st.text_input("Search by client name", key="appt_search_name")

                with st.container(border=True):
                    status_filter = st.selectbox(
                        "Status",
                        ["All", "Scheduled", "Completed", "Canceled"],
                        key="appointment_status_filter_box"
                    )
                st.session_state["appointment_status_filter"] = status_filter

                filtered_appts = []
                for appt in employee_appts:
                    matches_search = search_name.lower() in appt.get("client", "").lower()
                    matches_status = (
                        st.session_state["appointment_status_filter"] == "All"
                        or appt.get("status", "Scheduled") == st.session_state["appointment_status_filter"]
                    )
                    if matches_search and matches_status:
                        filtered_appts.append(appt)

                with st.container(border=True):
                    st.markdown("### Appointment List")
                    if len(filtered_appts) > 0:
                        appointment_table = []
                        for appt in filtered_appts:
                            appointment_table.append({
                                "Client": appt.get("client", "Unknown"),
                                "Service": appt["service"],
                                "Date": appt["date"],
                                "Time": appt["time"],
                                "Status": appt.get("status", "Scheduled")
                            })

                        st.dataframe(appointment_table, use_container_width=True)

                        selected_appt_from_box = st.selectbox(
                            "Select Appointment",
                            filtered_appts,
                            format_func=lambda x: f"{x.get('client', 'Unknown')} | {x['service']} | {x['date']} {x['time']}",
                            key="manage_appt_selectbox"
                        )

                        if selected_appt_from_box:
                            st.session_state["selected_appointment_id"] = selected_appt_from_box["id"]
                    else:
                        st.info("No appointments assigned to you yet.")

            with col2:
                with st.container(border=True):
                    st.markdown("### Appointment Details")
                    selected_appt = None
                    for appt in employee_appts:
                        if appt["id"] == st.session_state["selected_appointment_id"]:
                            selected_appt = appt
                            break

                    if selected_appt:
                        st.markdown(f"**Client:** {selected_appt.get('client', 'Unknown')}")
                        st.markdown(f"**Client Email:** {selected_appt.get('client_email', 'N/A')}")
                        st.markdown(f"**Service:** {selected_appt['service']}")
                        st.markdown(f"**Price:** ${selected_appt['price']}")
                        st.markdown(f"**Date:** {selected_appt['date']}")
                        st.markdown(f"**Time:** {selected_appt['time']}")
                        st.markdown(f"**Status:** {selected_appt.get('status', 'Scheduled')}")

                        status_options = ["Scheduled", "Completed", "Canceled"]
                        current_status = selected_appt.get("status", "Scheduled")
                        current_status_index = status_options.index(current_status) if current_status in status_options else 0

                        selected_status = st.radio(
                            "Update Status",
                            status_options,
                            index=current_status_index,
                            key=f"status_radio_{selected_appt['id']}"
                        )

                        if st.button("Record Decision", key=f"save_status_{selected_appt['id']}", type="primary", use_container_width=True):
                            with st.spinner("Recording the decision..."):
                                for appt in appointments:
                                    if appt["id"] == selected_appt["id"]:
                                        old_status = appt.get("status", "Scheduled")

                                        if old_status != "Canceled" and selected_status == "Canceled":
                                            update_inventory_for_service(appt["service"], "add")
                                            appt["canceled_at"] = str(datetime.now())

                                        if old_status != "Completed" and selected_status == "Completed":
                                            add_reward_points_to_customer(appt["client_email"], 10)

                                        appt["status"] = selected_status
                                        break
                                save_appointments()
                                save_inventory()
                            st.success("Information recorded.")
                            st.rerun()
                    else:
                        st.info("Select an appointment to view details.")

        elif st.session_state["page"] == "inventory":
            st.header("Salon Inventory")
            st.divider()

            col1, col2 = st.columns([4, 2])
            with col1:
                with st.container(border=True):
                    inventory_table = []
                    for item in inventory:
                        inventory_table.append({
                            "Item": item["item_name"],
                            "Category": item["category"],
                            "Quantity": item["quantity"],
                            "Low Stock Limit": item["low_stock_limit"]
                        })

                    if len(inventory_table) > 0:
                        st.dataframe(inventory_table, use_container_width=True)

                        selected_inventory_item = st.selectbox(
                            "Select Inventory Item",
                            inventory,
                            format_func=lambda x: f"{x['item_name']} | Qty: {x['quantity']}",
                            key="inventory_selectbox"
                        )

                        if selected_inventory_item:
                            st.session_state["restock_item_id"] = selected_inventory_item["id"]
                    else:
                        st.info("No inventory items available.")

            with col2:
                with st.container(border=True):
                    st.markdown("### Restock Item")
                    selected_item = None
                    for item in inventory:
                        if item["id"] == st.session_state["restock_item_id"]:
                            selected_item = item
                            break

                    if selected_item:
                        st.markdown(f"**Item:** {selected_item['item_name']}")
                        st.markdown(f"**Current Quantity:** {selected_item['quantity']}")
                        st.markdown(f"**Supplier:** {selected_item['supplier']}")
                        restock_amount = st.number_input("Amount to Add", min_value=1, step=1, key="restock_amount_input")

                        if st.button("Save Restock", key=f"save_restock_{selected_item['id']}", type="primary", use_container_width=True):
                            with st.spinner("Recording..."):
                                selected_item["quantity"] += restock_amount
                                save_inventory()
                            st.success("Inventory updated successfully.")
                            st.session_state["restock_item_id"] = None
                            st.rerun()
                    else:
                        st.info("Select an inventory item to restock.")

        elif st.session_state["page"] == "low_stock":
            st.header("Low Stock Alerts")
            st.divider()

            low_stock_items = []
            for item in inventory:
                if item["quantity"] <= item["low_stock_limit"]:
                    low_stock_items.append(item)

            if len(low_stock_items) > 0:
                for item in low_stock_items:
                    with st.container(border=True):
                        st.markdown(f"**Item:** {item['item_name']}")
                        st.markdown(f"**Quantity:** {item['quantity']}")
                        st.markdown(f"**Low Stock Limit:** {item['low_stock_limit']}")
                        st.markdown(f"**Supplier:** {item['supplier']}")
                        st.warning(f"{item['item_name']} needs to be restocked soon.")
            else:
                st.success("There are no low stock items right now.")
