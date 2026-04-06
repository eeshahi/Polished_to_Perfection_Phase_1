# Stock code

    #  low_stock_count = get_low_stock_count()

        # if st.session_state["page"] == "dashboard":
        #     col1, col2, col3 = st.columns([2, 3, 2])
        #     with col2:
        #         st.header("Polished to Perfection - Employee Dashboard")
        #     st.divider()

        #     col1, col2, col3, col4 = st.columns(4)
        #     with col1:
        #         with st.container(border=True):
    #                 st.markdown("#### Today's Appointments")
    #                 st.markdown(f"## {todays_appointments}")
    #         with col2:
    #             with st.container(border=True):
    #                 st.markdown("#### Scheduled")
    #                 st.markdown(f"## {scheduled_appointments}")
    #         with col3:
    #             with st.container(border=True):
    #                 st.markdown("#### Completed")
    #                 st.markdown(f"## {completed_appointments}")
    #         with col4:
    #             with st.container(border=True):
    #                 st.markdown("#### Low Stock")
    #                 st.markdown(f"## {low_stock_count}")

    #         st.divider()
    #         col1, col2 = st.columns([4, 2])
    #         with col1:
    #             with st.container(border=True):
    #                 st.markdown("### Assigned Appointments")
    #                 if len(employee_appts) > 0:
    #                     for appt in employee_appts:
    #                         st.markdown(f"**{appt['client']}** | {appt['service']} | {appt['date']} at {appt['time']} | {appt.get('status', 'Scheduled')}")
    #                 else:
    #                     st.info("No appointments assigned yet.")
    #         with col2:
    #             with st.container(border=True):
    #                 st.markdown("### Inventory Alerts")
    #                 if low_stock_count > 0:
    #                     for item in inventory:
    #                         if item["quantity"] <= item["low_stock_limit"]:
    #                             st.warning(f"{item['item_name']} is low on stock")
    #                 else:
    #                     st.success("No low stock items right now.")

    #     elif st.session_state["page"] == "manage_appointments":
    #         st.header("Manage Appointments")
    #         st.divider()

    #         col1, col2 = st.columns([4, 2])
    #         with col1:
    #             with st.container(border=True):
    #                 search_name = st.text_input("Search by client name", key="appt_search_name")

    #             with st.container(border=True):
    #                 status_filter = st.selectbox(
    #                     "Status",
    #                     ["All", "Scheduled", "Completed", "Canceled"],
    #                     key="appointment_status_filter_box"
    #                 )
    #             st.session_state["appointment_status_filter"] = status_filter

    #             filtered_appts = []
    #             for appt in employee_appts:
    #                 matches_search = search_name.lower() in appt.get("client", "").lower()
    #                 matches_status = (
    #                     st.session_state["appointment_status_filter"] == "All"
    #                     or appt.get("status", "Scheduled") == st.session_state["appointment_status_filter"]
    #                 )
    #                 if matches_search and matches_status:
    #                     filtered_appts.append(appt)

    #             with st.container(border=True):
    #                 st.markdown("### Appointment List")
    #                 if len(filtered_appts) > 0:
    #                     appointment_table = []
    #                     for appt in filtered_appts:
    #                         appointment_table.append({
    #                             "Client": appt.get("client", "Unknown"),
    #                             "Service": appt["service"],
    #                             "Date": appt["date"],
    #                             "Time": appt["time"],
    #                             "Status": appt.get("status", "Scheduled")
    #                         })

    #                     st.dataframe(appointment_table, use_container_width=True)

    #                     selected_appt_from_box = st.selectbox(
    #                         "Select Appointment",
    #                         filtered_appts,
    #                         format_func=lambda x: f"{x.get('client', 'Unknown')} | {x['service']} | {x['date']} {x['time']}",
    #                         key="manage_appt_selectbox"
    #                     )

    #                     if selected_appt_from_box:
    #                         st.session_state["selected_appointment_id"] = selected_appt_from_box["id"]
    #                 else:
    #                     st.info("No appointments assigned to you yet.")

    #         with col2:
    #             with st.container(border=True):
    #                 st.markdown("### Appointment Details")
    #                 selected_appt = None
    #                 for appt in employee_appts:
    #                     if appt["id"] == st.session_state["selected_appointment_id"]:
    #                         selected_appt = appt
    #                         break

    #                 if selected_appt:
    #                     st.markdown(f"**Client:** {selected_appt.get('client', 'Unknown')}")
    #                     st.markdown(f"**Client Email:** {selected_appt.get('client_email', 'N/A')}")
    #                     st.markdown(f"**Service:** {selected_appt['service']}")
    #                     st.markdown(f"**Price:** ${selected_appt['price']}")
    #                     st.markdown(f"**Date:** {selected_appt['date']}")
    #                     st.markdown(f"**Time:** {selected_appt['time']}")
    #                     st.markdown(f"**Status:** {selected_appt.get('status', 'Scheduled')}")

    #                     status_options = ["Scheduled", "Completed", "Canceled"]
    #                     current_status = selected_appt.get("status", "Scheduled")
    #                     current_status_index = status_options.index(current_status) if current_status in status_options else 0

    #                     selected_status = st.radio(
    #                         "Update Status",
    #                         status_options,
    #                         index=current_status_index,
    #                         key=f"status_radio_{selected_appt['id']}"
    #                     )

    #                     if st.button("Record Decision", key=f"save_status_{selected_appt['id']}", type="primary", use_container_width=True):
    #                         with st.spinner("Recording the decision..."):
    #                             for appt in appointments:
    #                                 if appt["id"] == selected_appt["id"]:
    #                                     old_status = appt.get("status", "Scheduled")

    #                                     if old_status != "Canceled" and selected_status == "Canceled":
    #                                         update_inventory_for_service(appt["service"], "add")
    #                                         appt["canceled_at"] = str(datetime.now())

    #                                     if old_status != "Completed" and selected_status == "Completed":
    #                                         add_reward_points_to_customer(appt["client_email"], 10)

    #                                     appt["status"] = selected_status
    #                                     break
    #                             save_appointments()
    #                             save_inventory()
    #                         st.success("Information recorded.")
    #                         st.rerun()
    #                 else:
    #                     st.info("Select an appointment to view details.")

    #     elif st.session_state["page"] == "inventory":
    #         st.header("Salon Inventory")
    #         st.divider()

    #         col1, col2 = st.columns([4, 2])
    #         with col1:
    #             with st.container(border=True):
    #                 inventory_table = []
    #                 for item in inventory:
    #                     inventory_table.append({
    #                         "Item": item["item_name"],
    #                         "Category": item["category"],
    #                         "Quantity": item["quantity"],
    #                         "Low Stock Limit": item["low_stock_limit"]
    #                     })

    #                 if len(inventory_table) > 0:
    #                     st.dataframe(inventory_table, use_container_width=True)

    #                     selected_inventory_item = st.selectbox(
    #                         "Select Inventory Item",
    #                         inventory,
    #                         format_func=lambda x: f"{x['item_name']} | Qty: {x['quantity']}",
    #                         key="inventory_selectbox"
    #                     )

    #                     if selected_inventory_item:
    #                         st.session_state["restock_item_id"] = selected_inventory_item["id"]
    #                 else:
    #                     st.info("No inventory items available.")

    #         with col2:
    #             with st.container(border=True):
    #                 st.markdown("### Restock Item")
    #                 selected_item = None
    #                 for item in inventory:
    #                     if item["id"] == st.session_state["restock_item_id"]:
    #                         selected_item = item
    #                         break

    #                 if selected_item:
    #                     st.markdown(f"**Item:** {selected_item['item_name']}")
    #                     st.markdown(f"**Current Quantity:** {selected_item['quantity']}")
    #                     st.markdown(f"**Supplier:** {selected_item['supplier']}")
    #                     restock_amount = st.number_input("Amount to Add", min_value=1, step=1, key="restock_amount_input")

    #                     if st.button("Save Restock", key=f"save_restock_{selected_item['id']}", type="primary", use_container_width=True):
    #                         with st.spinner("Recording..."):
    #                             selected_item["quantity"] += restock_amount
    #                             save_inventory()
    #                         st.success("Inventory updated successfully.")
    #                         st.session_state["restock_item_id"] = None
    #                         st.rerun()
    #                 else:
    #                     st.info("Select an inventory item to restock.")

    #     elif st.session_state["page"] == "low_stock":
    #         st.header("Low Stock Alerts")
    #         st.divider()

    #         low_stock_items = []
    #         for item in inventory:
    #             if item["quantity"] <= item["low_stock_limit"]:
    #                 low_stock_items.append(item)

    #         if len(low_stock_items) > 0:
    #             for item in low_stock_items:
    #                 with st.container(border=True):
    #                     st.markdown(f"**Item:** {item['item_name']}")
    #                     st.markdown(f"**Quantity:** {item['quantity']}")
    #                     st.markdown(f"**Low Stock Limit:** {item['low_stock_limit']}")
    #                     st.markdown(f"**Supplier:** {item['supplier']}")
    #                     st.warning(f"{item['item_name']} needs to be restocked soon.")
    #         else:
    #             st.success("There are no low stock items right now.")
