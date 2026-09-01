# home.py

import streamlit as st

def app():
   # Page configuration
   st.markdown("""
       <style>
       .main {
           padding: 2rem;
       }
       .title {
           text-align: center;
           color: white;  # Changed to white
           padding-bottom: 2rem;
           font-weight: bold;
           font-size: 40px;
       }
       .description {
           text-align: center;
           font-size: 1.2rem;
           color: white;  # Changed to white
           margin-bottom: 2rem;
       }
       .stButton>button {
           background-color: #0066cc;
           color: white;
           padding: 10px 24px;
           border-radius: 5px;
           border: none;
           font-size: 18px;
           width: 150px;
       }
       .stButton>button:hover {
           background-color: #0052a3;
       }
       </style>
   """, unsafe_allow_html=True)

   # Title and welcome message
   st.markdown("<h1 class='title'>Welcome to NavJeevan - Healthcare Access Platform</h1>", unsafe_allow_html=True)
   
   # Hero section with description
   st.markdown("""
       <p class='description'>
       Your comprehensive healthcare companion for better health management and medical assistance
       </p>
   """, unsafe_allow_html=True)

  
   # Create three columns for a balanced layout
   col1, col2, col3 = st.columns(3)

   with col1:
       st.markdown("### 🏥 Patient Care")
       st.write("Access your medical records, schedule appointments, and track your health progress all in one place.")

   with col2:
       st.markdown("### 👨‍⚕️ Expert Consultation")
       st.write("Connect with healthcare professionals, get expert advice, and receive personalized care recommendations.")

   with col3:
       st.markdown("### 📊 Health Analytics")
       st.write("Monitor your health metrics, view detailed analytics, and get insights about your well-being.")

   # Additional features section
   st.markdown("### Key Features")
   
   # Create two columns for features
   col1, col2 = st.columns(2)

   with col1:
       st.markdown("""
       - **Appointment Management**: Easy scheduling and reminders
       - **Medical Records**: Secure storage and access
       - **Health Tracking**: Monitor vital signs and medications
       """)

   with col2:
       st.markdown("""
       - **Hospital Locator**: Find nearest healthcare facilities
       - **Emergency Support**: Quick access to emergency services
       - **Health Tips**: Daily health recommendations
       """)

   # Footer
   st.markdown("<br>", unsafe_allow_html=True)
   st.markdown("---")
   st.markdown(
       "<p style='text-align: center; color: white;'>© 2025 NavJeevan Healthcare Access Platform. All rights reserved.</p>", 
       unsafe_allow_html=True
   )