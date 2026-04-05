# st.write("Ask Penny about appointments, booking, cancellations, services, rewards, and nail tech information.")

#             if st.button("Clear Chat", key="clear_customer_chat"):
#                 st.session_state["messages"] = []
#                 st.rerun()

#             for message in st.session_state["messages"]:
#                 with st.chat_message(message["role"]):
#                     st.write(message["content"])

#             prompt = st.chat_input(
#                 "Ask Penny the Polish Pro, our AI salon assistant, something...",
#                 key="customer_chat_input"
#             )

#             if prompt:
#                 st.session_state["messages"].append({"role": "user", "content": prompt})

#                 prompt_lower = prompt.lower()

#                 user_appts_for_chat = [
#                     a for a in appointments
#                     if "client_email" in a and a["client_email"] == st.session_state["user"]["email"]
#                 ]

#                 if "appointment" in prompt_lower and "have" in prompt_lower:
#                     if user_appts_for_chat:
#                         response = "You currently have these appointments:\n"
#                         for appt in user_appts_for_chat:
#                             response += f"- {appt['date']} at {appt['time']} for {appt['service']} with {appt['employee']}\n"
#                     else:
#                         response = "You do not have any appointments booked right now."

#                 elif "cancel" in prompt_lower:
#                     response = "To cancel an appointment, go to the My Appointments section and select your appointment in the Upcoming tab."

#                 elif "service" in prompt_lower:
#                     response = "Available services are Basic Manicure, Gel Manicure, Classic Pedicure, Acrylic Full Set, and Nail Art Design."

#                 elif "status" in prompt_lower:
#                     if user_appts_for_chat:
#                         response = "Here are your current appointment statuses:\n"
#                         for appt in user_appts_for_chat:
#                             response += f"- {appt['service']} on {appt['date']} is {appt.get('status', 'Scheduled')}\n"
#                     else:
#                         response = "You do not have any appointment statuses to check right now."

#                 elif "employee" in prompt_lower or "tech" in prompt_lower:
#                     response = "Current nail techs are Marissa, Jackie, and Eesha."

#                 elif "book" in prompt_lower or "schedule" in prompt_lower:
#                     response = "To book an appointment, go to the Book Appointment section, choose a service, employee, date, and time, then click Book Appointment."

#                 elif "reward" in prompt_lower or "points" in prompt_lower:
#                     response = f"You currently have {reward_points} reward points. Go to the Rewards page to redeem them."

#                 else:
#                     response = "I can help with appointments, booking, cancellations, services, statuses, rewards, and nail tech information."

#                 st.session_state["messages"].append({"role": "assistant", "content": response})
#                 st.rerun()