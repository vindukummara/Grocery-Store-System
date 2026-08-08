import streamlit as st


def logout():

    st.title("🚪 Logout")

    st.warning("Are you sure you want to logout?")

    col1, col2 = st.columns(2)

    # -----------------------------
    # Confirm Logout
    # -----------------------------
    with col1:

        if st.button("✅ Yes, Logout"):

            st.session_state.logged_in = False

            # Clear login-related session data
            for key in [
                "username",
                "password",
                "security_answer",
                "new_password",
                "confirm_password"
            ]:
                if key in st.session_state:
                    del st.session_state[key]

            st.success("✅ You have been logged out successfully.")

            st.rerun()

    # -----------------------------
    # Cancel Logout
    # -----------------------------
    with col2:

        if st.button("❌ Cancel"):

            st.info("Logout cancelled.")