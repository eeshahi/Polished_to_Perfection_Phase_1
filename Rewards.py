# Reward code
        # elif st.session_state["page"] == "rewards":
        #     st.header("Rewards Program")
        #     st.divider()

        #     redeem_tab, history_tab = st.tabs(["Redeem Reward", "Reward History"])

        #     with redeem_tab:
        #         col1, col2, col3 = st.columns([1, 3, 1])
        #         with col2:
        #             with st.container(border=True):
        #                 st.markdown("### Available Rewards")
        #                 st.write(f"Current Points: {reward_points}")
        #                 st.divider()

        #                 for reward in reward_options:
        #                     with st.container(border=True):
        #                         st.markdown(f"**Reward:** {reward['name']}")
        #                         st.markdown(f"**Points Required:** {reward['points']}")

        #                         if reward_points >= reward["points"]:
        #                             if st.button(f"Redeem {reward['name']}", key=f"redeem_{reward['name']}", type="primary", use_container_width=True):
        #                                 redeemed = False
        #                                 with st.spinner("Recording..."):
        #                                     redeemed = redeem_reward_for_customer(
        #                                         st.session_state["user"]["id"],
        #                                         reward["name"],
        #                                         reward["points"]
        #                                     )
        #                                 if redeemed:
        #                                     st.success(f"{reward['name']} redeemed successfully.")
        #                                     st.rerun()
        #                         else:
        #                             st.warning("Not enough points for this reward.")

        #     with history_tab:
        #         col1, col2, col3 = st.columns([1, 3, 1])
        #         with col2:
        #             with st.container(border=True):
        #                 st.markdown("### Reward History")
        #                 if len(reward_history) > 0:
        #                     for reward_item in reward_history:
        #                         with st.container(border=True):
        #                             st.markdown(f"**Reward:** {reward_item['reward_name']}")
        #                             st.markdown(f"**Points Used:** {reward_item['points_used']}")
        #                             st.markdown(f"**Redeemed At:** {reward_item['redeemed_at']}")
        #                             st.markdown(f"**Status:** {reward_item['status']}")
        #                 else:
        #                     st.info("No rewards redeemed yet.")
