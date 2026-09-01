import streamlit as st
from streamlit_option_menu import option_menu

import appointment, hosloc, models, recommendation, userprofile, home, login , coach

# Initialize session state variables
if "email" not in st.session_state:
    st.session_state.email = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False  # User is not logged in by default

st.set_page_config(page_title="Healthcare Chatbot", page_icon=":hospital:")

class MultiApp:
    def __init__(self):
        self.apps = []

    def add_app(self, title, function):
        self.apps.append({
            "title": title,
            "function": function
        })    

    def run(self):
        # Sidebar navigation menu
        with st.sidebar:
            app = option_menu(
                menu_title='Navigation', 
                options=['Home', 'Login', 'Profile', 'Health Overview', 'Prediction Models', 'AI Coach', 'Connect with Doctor', 'Hospital Locator'],
                default_index=0,
            )

        # If the user is not logged in and tries to access pages other than Home and Login, redirect to Login
        if not st.session_state.logged_in and app not in ["Home", "Login"]:
            st.error("You need to log in to access this page.")
            login.app()  # Redirect to the login page
            return

        # Page navigation
        if app == "Home":
            home.app()
        elif app == "Login":
            login.app()    
        elif app == "Profile":
            userprofile.app()    
        elif app == "Health Overview":
            recommendation.app()        
        elif app == 'Prediction Models':
            models.app()
        elif app == 'AI Coach':
            coach.app()
        elif app == 'Connect with Doctor':
            appointment.app()    
        elif app == 'Hospital Locator':
            hosloc.app()

# Run the app
multi_app = MultiApp()
multi_app.run()
