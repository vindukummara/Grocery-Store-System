import streamlit as st
from database import get_connection


# =====================================================
# CREATE DEFAULT USER
# =====================================================

def create_default_user():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT UserID
        FROM users
        WHERE Username = ?
    """, ("admin",))

    user = cursor.fetchone()

    if user is None:

        cursor.execute("""
            INSERT INTO users
            (
                Username,
                Password,
                SecurityQuestion,
                SecurityAnswer
            )
            VALUES (?, ?, ?, ?)
        """, (
            "admin",
            "admin123",
            "What is your favorite color?",
            "blue"
        ))

        conn.commit()

    conn.close()


# =====================================================
# LOGIN
# =====================================================

def login():

    # Create default admin account
    create_default_user()

    login_tab, forgot_tab = st.tabs(
        ["🔐 Login", "🔑 Forgot Password"]
    )

    # =================================================
    # LOGIN TAB
    # =================================================

    with login_tab:

        st.title("🛒 Grocery Store Login")

        username = st.text_input(
            "Username",
            key="login_username"
        )

        password = st.text_input(
            "Password",
            type="password",
            key="login_password"
        )

        if st.button(
            "Login",
            key="login_button"
        ):

            if not username or not password:

                st.warning(
                    "⚠️ Please enter username and password."
                )

            else:

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT UserID
                    FROM users
                    WHERE Username = ?
                    AND Password = ?
                """, (
                    username,
                    password
                ))

                user = cursor.fetchone()

                conn.close()

                if user:

                    st.session_state.logged_in = True
                    st.session_state.username = username

                    st.success(
                        "✅ Login successful!"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Invalid username or password."
                    )

    # =================================================
    # FORGOT PASSWORD TAB
    # =================================================

    with forgot_tab:

        st.title("🔑 Forgot Password")

        forgot_username = st.text_input(
            "Enter Username",
            key="forgot_username"
        )

        if st.button(
            "Find Account",
            key="find_account"
        ):

            if not forgot_username.strip():

                st.warning(
                    "⚠️ Please enter your username."
                )

            else:

                conn = get_connection()
                cursor = conn.cursor()

                cursor.execute("""
                    SELECT SecurityQuestion
                    FROM users
                    WHERE Username = ?
                """, (
                    forgot_username.strip()
                ))

                result = cursor.fetchone()

                conn.close()

                if result:

                    st.session_state.reset_username = (
                        forgot_username.strip()
                    )

                    st.session_state.security_question = (
                        result[0]
                    )

                    st.success(
                        "✅ Account found."
                    )

                else:

                    st.error(
                        "❌ Username not found."
                    )

        # =================================================
        # RESET PASSWORD
        # =================================================

        if (
            "reset_username" in st.session_state
            and "security_question" in st.session_state
        ):

            st.info(
                "🔐 Security Question: "
                + st.session_state.security_question
            )

            answer = st.text_input(
                "Security Answer",
                key="security_answer"
            )

            new_password = st.text_input(
                "New Password",
                type="password",
                key="new_password"
            )

            confirm_password = st.text_input(
                "Confirm New Password",
                type="password",
                key="confirm_password"
            )

            if st.button(
                "Reset Password",
                key="reset_password"
            ):

                if not answer.strip():

                    st.warning(
                        "⚠️ Please enter the security answer."
                    )

                elif not new_password.strip():

                    st.warning(
                        "⚠️ Please enter a new password."
                    )

                elif new_password != confirm_password:

                    st.error(
                        "❌ Passwords do not match."
                    )

                else:

                    conn = get_connection()
                    cursor = conn.cursor()

                    cursor.execute("""
                        SELECT UserID
                        FROM users
                        WHERE Username = ?
                        AND LOWER(SecurityAnswer) = LOWER(?)
                    """, (
                        st.session_state.reset_username,
                        answer.strip()
                    ))

                    user = cursor.fetchone()

                    if user is None:

                        conn.close()

                        st.error(
                            "❌ Incorrect security answer."
                        )

                    else:

                        cursor.execute("""
                            UPDATE users
                            SET Password = ?
                            WHERE Username = ?
                        """, (
                            new_password,
                            st.session_state.reset_username
                        ))

                        conn.commit()
                        conn.close()

                        st.success(
                            "✅ Password reset successfully!"
                        )

                        st.session_state.pop(
                            "reset_username",
                            None
                        )

                        st.session_state.pop(
                            "security_question",
                            None
                        )

                        st.info(
                            "You can now login with your new password."
                        )