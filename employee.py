    # elif st.session_state["role"] == "Employee":
    #     employee_appts = get_employee_appointments()
    #     todays_appointments = 0
    #     scheduled_appointments = 0
    #     completed_appointments = 0

    #     for appt in employee_appts:
    #         if appt["date"] == str(date.today()) and appt.get("status") != "Canceled":
    #             todays_appointments += 1
    #         if appt.get("status") == "Scheduled":
    #             scheduled_appointments += 1
    #         if appt.get("status") == "Completed":
    #             completed_appointments += 1
