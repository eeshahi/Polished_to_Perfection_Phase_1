        # elif st.session_state["page"] == "my_appointments":
        #     st.header("My Appointments")
        #     st.divider()

        #     history_search = st.text_input("Search by service", key="customer_history_search")
        #     history_filter = st.selectbox(
        #         "Status",
        #         ["All", "Upcoming", "Old", "Canceled"],
        #         key="customer_history_filter_box"
        #     )
        #     st.session_state["customer_history_filter"] = history_filter

        #     upcoming_tab, old_tab, canceled_tab = st.tabs(["Upcoming", "Old", "Canceled"])

        #     with upcoming_tab:
        #         upcoming_appointments = []
        #         for appt in user_appts:
        #             matches_search = history_search.lower() in appt["service"].lower()
        #             is_upcoming = appt.get("status") not in ["Canceled", "Completed"] and not is_past_appointment(appt)
        #             matches_filter = st.session_state["customer_history_filter"] in ["All", "Upcoming"]
        #             if matches_search and is_upcoming and matches_filter:
        #                 upcoming_appointments.append(appt)

        #         col1, col2 = st.columns([4, 2])
        #         with col1:
        #             with st.container(border=True):
        #                 st.markdown("### Appointment List")
        #                 if len(upcoming_appointments) > 0:
        #                     appointment_table = []
        #                     for appt in upcoming_appointments:
        #                         appointment_table.append({
        #                             "Service": appt["service"],
        #                             "Date": appt["date"],
        #                             "Time": appt["time"],
        #                             "Employee": appt["employee"],
        #                             "Status": appt.get("status", "Scheduled")
        #                         })

        #                     st.dataframe(appointment_table, use_container_width=True)

        #                     selected_upcoming_appt = st.selectbox(
        #                         "Select Appointment",
        #                         upcoming_appointments,
        #                         format_func=lambda x: f"{x['service']} | {x['date']} {x['time']} | {x['employee']}", ## used AI to help create this line of code 
        #                         key="customer_upcoming_selectbox"
        #                     )

        #                     if selected_upcoming_appt:
        #                         st.session_state["selected_appointment_id"] = selected_upcoming_appt["id"]
        #                 else:
        #                     st.info("No upcoming appointments found.")

        #         with col2:
        #             with st.container(border=True):
        #                 st.markdown("### Appointment Details")
        #                 selected_appt = None
        #                 for appt in upcoming_appointments:
        #                     if appt["id"] == st.session_state["selected_appointment_id"]:
        #                         selected_appt = appt
        #                         break

        #                 if selected_appt:
        #                     st.markdown(f"**Service:** {selected_appt['service']}")
        #                     st.markdown(f"**Price:** ${selected_appt['price']}")
        #                     st.markdown(f"**Date:** {selected_appt['date']}")
        #                     st.markdown(f"**Time:** {selected_appt['time']}")
        #                     st.markdown(f"**Employee:** {selected_appt['employee']}")
        #                     st.markdown(f"**Status:** {selected_appt.get('status', 'Scheduled')}")

        #                     if is_past_appointment(selected_appt):
        #                         st.warning("This appointment has already passed and can no longer be canceled.")
        #                     else:
        #                         if st.button("Cancel Appointment", key=f"cancel_appointment_{selected_appt['id']}", type="primary", use_container_width=True):
        #                             with st.spinner("Recording..."):
        #                                 for appt in appointments:
        #                                     if appt["id"] == selected_appt["id"]:
        #                                         appt["status"] = "Canceled"
        #                                         appt["canceled_at"] = str(datetime.now())
        #                                         update_inventory_for_service(appt["service"], "add")
        #                                         break
        #                                 save_appointments()
        #                                 save_inventory()
        #                             st.success("Appointment canceled successfully.")
        #                             st.session_state["selected_appointment_id"] = None
        #                             st.rerun()
        #                 else:
        #                     st.info("Select an appointment to view details.")

        #     with old_tab:
        #         old_appointments = []
        #         for appt in user_appts:
        #             matches_search = history_search.lower() in appt["service"].lower()
        #             is_old = appt.get("status") == "Completed" or (is_past_appointment(appt) and appt.get("status") != "Canceled")
        #             matches_filter = st.session_state["customer_history_filter"] in ["All", "Old"]
        #             if matches_search and is_old and matches_filter:
        #                 old_appointments.append(appt)

        #         if len(old_appointments) > 0:
        #             old_table = []
        #             for appt in old_appointments:
        #                 display_status = appt.get("status", "Scheduled")
        #                 if display_status == "Scheduled" and is_past_appointment(appt):
        #                     display_status = "Completed"
        #                 old_table.append({
        #                     "Service": appt["service"],
        #                     "Date": appt["date"],
        #                     "Time": appt["time"],
        #                     "Employee": appt["employee"],
        #                     "Status": display_status,
        #                     "Price": appt["price"]
        #                 })
        #             st.dataframe(old_table, use_container_width=True)
        #         else:
        #             st.info("No old appointments found.")

        #     with canceled_tab:
        #         canceled_appointments = []
        #         for appt in user_appts:
        #             matches_search = history_search.lower() in appt["service"].lower()
        #             is_canceled = appt.get("status") == "Canceled"
        #             matches_filter = st.session_state["customer_history_filter"] in ["All", "Canceled"]
        #             if matches_search and is_canceled and matches_filter:
        #                 canceled_appointments.append(appt)

        #         if len(canceled_appointments) > 0:
        #             canceled_table = []
        #             for appt in canceled_appointments:
        #                 canceled_table.append({
        #                     "Service": appt["service"],
        #                     "Date": appt["date"],
        #                     "Time": appt["time"],
        #                     "Employee": appt["employee"],
        #                     "Status": appt.get("status", "Canceled")
        #                 })
        #             st.dataframe(canceled_table, use_container_width=True)
        #         else:
        #             st.info("No canceled appointments found.")
