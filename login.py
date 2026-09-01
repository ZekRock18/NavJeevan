import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Set up Google Sheets authentication
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', 
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("navjeevan-service-account.json", scope)
    client = gspread.authorize(creds)
    return client.open("navjeevan_database").sheet1

# Google Sheets authentication and sheet access
sheet = authenticate_google_sheets()

# Registration function
def register_user():
    st.title("Register")

    # Collect user input
    email = st.text_input("Email")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Register"):
        # Check if email already exists in the Google Sheet
        records = sheet.get_all_records()
        for record in records:
            if record['Email'] == email:
                st.error("Email already registered!")
                return

        # If email is unique, add the user to the sheet
        sheet.append_row([email, username, password])
        st.success("Registration Successful!")

# Login function
def login_user():
    st.title("Sign In")

    # Collect user input
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if st.button("Sign In"):
        # Check if email and password match any entry in Google Sheets
        records = sheet.get_all_records()
        for record in records:
            if record['Email'] == email and record['Password'] == password:
                # Set session state to logged in
                st.session_state.logged_in = True
                st.session_state.email = email
                st.session_state.username = record['Username']
                st.success(f"Welcome back, {record['Username']}!")
                return

        st.error("Invalid email or password")

# Main function to toggle between register and login
def app():
    # If the user is logged in, skip the login page and go to the home page
    if "logged_in" in st.session_state and st.session_state.logged_in:
        st.write(f"Welcome back, {st.session_state.username}!")
        st.sidebar.success("You are logged in.")
        # Here you can redirect to other pages or show options as needed.
    else:
        # Add a sidebar to choose between Register and Login
        choice = st.sidebar.selectbox("Choose an option", ["Sign In", "Register"])

        if choice == "Sign In":
            login_user()
        elif choice == "Register":
            register_user()
