# import streamlit as st
# import json
# from pathlib import Path
# from datetime import datetime, date
# import uuid

# if st.session_state["logged_in"]:
#     refresh_logged_in_user() 

#     with st.sidebar:
#         st.markdown("## Polished to Perfection")
#         st.write(f"Logged in as: {st.session_state['user']['full_name']}")
#         st.write(f"Role: {st.session_state['role']}")
#         st.divider()

#         if st.session_state["role"] == "Customer":
#             if st.button("Customer Dashboard", key="customer_dashboard_btn", type="primary", use_container_width=True):
#                 st.session_state["page"] = "dashboard"
#                 st.rerun()
#             if st.button("Book Appointment", key="book_appointment_btn", use_container_width=True):
#                 st.session_state["page"] = "book_appointment"
#                 st.rerun()
#             if st.button("My Appointments", key="my_appointments_btn", use_container_width=True):
#                 st.session_state["page"] = "my_appointments"
#                 st.rerun()
#             if st.button("Rewards", key="rewards_btn", use_container_width=True):
#                 st.session_state["page"] = "rewards"
#                 st.rerun()
#             if st.button("Penny the Polish Pro", key="penny_chat_btn", use_container_width=True):
#                 st.session_state["page"] = "penny_chat"
#                 st.rerun()

#         elif st.session_state["role"] == "Employee":
#             if st.button("Employee Dashboard", key="employee_dashboard_btn", type="primary", use_container_width=True):
#                 st.session_state["page"] = "dashboard"
#                 st.rerun()
#             if st.button("Manage Appointments", key="manage_appointments_btn", use_container_width=True):
#                 st.session_state["page"] = "manage_appointments"
#                 st.rerun()
#             if st.button("Inventory", key="inventory_btn", use_container_width=True):
#                 st.session_state["page"] = "inventory"
#                 st.rerun()
#             if st.button("Low Stock Alerts", key="low_stock_btn", use_container_width=True):
#                 st.session_state["page"] = "low_stock"
#                 st.rerun()

#         st.divider()
#         if st.button("Logout", key="logout_btn", use_container_width=True):
#             st.session_state["logged_in"] = False
#             st.session_state["user"] = None
#             st.session_state["role"] = None
#             st.session_state["page"] = "dashboard"
#             st.session_state["selected_appointment_id"] = None
#             st.session_state["restock_item_id"] = None
#             st.session_state["messages"] = []
#             st.rerun()

# # -----------------------------
# # Authentication
# # -----------------------------
# if not st.session_state["logged_in"]:
#     st.title("Polished to Perfection")
#     st.caption("Salon Management System")
#     st.divider()

#     register_tab, login_tab = st.tabs(["Register", "Login"])

#     with register_tab:
#         st.subheader("Create Account")
#         reg_email = st.text_input("Email", key="reg_email").strip().lower()
#         reg_name = st.text_input("Full Name", key="reg_name").strip()
#         reg_password = st.text_input("Password", type="password", key="reg_password")
#         reg_role = st.selectbox("Role", ["Customer", "Employee"], key="reg_role")

#         if st.button("Create Account", key="create_account_btn"):
#             if not reg_email or not reg_name or not reg_password:
#                 st.error("Please fill in all fields.")
#             elif "@" not in reg_email or "." not in reg_email:
#                 st.error("Please enter a valid email address.")
#             elif len(reg_password) < 6:
#                 st.error("Password must be at least 6 characters long.")
#             else:
#                 email_exists = False
#                 for user in users:
#                     if user["email"].lower() == reg_email.lower():
#                         email_exists = True
#                         break

#                 if email_exists:
#                     st.error("An account with that email already exists.")
#                 else:
#                     with st.spinner("Recording..."):
#                         new_user = {
#                             "id": str(uuid.uuid4()),
#                             "email": reg_email,
#                             "full_name": reg_name,
#                             "password": reg_password,
#                             "role": reg_role,
#                             "registered_at": str(datetime.now()),
#                             "reward_points": 0,
#                             "reward_history": []
#                         }
#                         users.append(new_user)
#                         save_users()
#                     st.success("Account created successfully. You can now log in.")

#     with login_tab:
#         st.subheader("Login")
#         login_email = st.text_input("Email", key="login_email").strip().lower()
#         login_password = st.text_input("Password", type="password", key="login_password")

#         if st.button("Log In", key="login_btn"):
#             user_found = None
#             for user in users:
#                 if user["email"].lower() == login_email and user["password"] == login_password:
#                     user_found = user
#                     break

#             if user_found:
#                 with st.spinner("Recording..."):
#                     st.session_state["logged_in"] = True
#                     st.session_state["user"] = user_found
#                     st.session_state["role"] = user_found["role"]
#                     st.session_state["page"] = "dashboard"
#                     st.session_state["messages"] = []
#                 st.success("Login successful!")
#                 st.rerun()
#             else:
#                 st.error("Invalid credentials.")
