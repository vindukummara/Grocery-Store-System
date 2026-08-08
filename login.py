import streamlit as st


def login():

    # -----------------------------
    # Initialize Session State
    # -----------------------------
    if "username" not in st.session_state:
        st.session_state.username = "admin"

    if "password" not in st.session_state:
        st.session_state.password = "admin123"

    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False

    # -----------------------------
    # Login Page
    # -----------------------------
    st.title("🛒 Grocery Store Management System")
    st.subheader("🔐 Admin Login")

    username = st.text_input("Username")
    password = st.text_input(
        "Password",
        type="password"
    )

    if st.button("Login"):

        if (
            username == st.session_state.username
            and password == st.session_state.password
        ):
            st.session_state.logged_in = True

            st.success("✅ Login Successful!")

            st.rerun()

        else:
            st.error("❌ Invalid Username or Password")

    # -----------------------------
    # Forgot Password
    # -----------------------------
    st.markdown("---")

    with st.expander("🔑 Forgot Password?"):

        st.write(
            "Answer the security question to reset your password."
        )

        answer = st.text_input(
            "What is your favourite color?",
            key="security_answer"
        )

        if answer.lower().strip() == "blue":

            new_password = st.text_input(
                "New Password",
                type="password",
                key="new_password"
            )

            confirm_password = st.text_input(
                "Confirm Password",
                type="password",
                key="confirm_password"
            )

            if st.button("Reset Password"):

                if not new_password:
                    st.warning(
                        "⚠️ Please enter a new password."
                    )

                elif new_password != confirm_password:
                    st.error(
                        "❌ Passwords do not match."
                    )

                else:
                    st.session_state.password = new_password

                    st.success(
                        "✅ Password Reset Successfully!"
                    )

                    st.info(
                        "You can now login with your new password."
                    )

        elif answer:
            st.error(
                "❌ Incorrect security answer."
            )