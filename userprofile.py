import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
from datetime import datetime

# Set up Google Sheets authentication
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', 
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("navjeevan-service-account.json", scope)
    client = gspread.authorize(creds)
    return client.open("navjeevan_database").sheet1

# Initialize Google Sheets
sheet = authenticate_google_sheets()

def update_patient_details(email, name, gender, age, birth_date, disease, allergies, blood_group, 
                         height, weight, emergency_contact, previous_surgeries, current_medications,
                         family_history, insurance_details, recent_lab_tests, blood_test_results,
                         imaging_reports, other_test_results, lab_report_dates):
    try:
        records = sheet.get_all_records()
        row_index = None
        
        # Find the row index for the email
        for idx, record in enumerate(records):
            if record['Email'] == email:
                row_index = idx + 2  # Adding 2 to account for header row and 0-based index
                break
        
        if row_index:
            # Update all cells in a single request
            sheet.update(f'D{row_index}:V{row_index}', 
                        [[name, gender, str(age), str(birth_date), disease, allergies,
                          blood_group, str(height), str(weight), emergency_contact,
                          previous_surgeries, current_medications, family_history,
                          insurance_details, recent_lab_tests, blood_test_results,
                          imaging_reports, other_test_results, lab_report_dates]])
            
            st.success("Details updated successfully!")
            return True
        else:
            st.error("Profile not found!")
            return False
    except Exception as e:
        st.error(f"Error updating details: {str(e)}")
        return False

def get_patient_details(email):
    """Fetch existing patient details"""
    try:
        records = sheet.get_all_records()
        for record in records:
            if record['Email'] == email:
                return record
        return None
    except Exception as e:
        st.error(f"Error fetching details: {str(e)}")
        return None

def app():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in to access your profile.")
        return
    
    st.title("My Profile")
    st.info(f"Logged in as: {st.session_state.email}")
    
    existing_details = get_patient_details(st.session_state.email)
    
    tab1, tab2 = st.tabs(["📋 Personal Information", "🔬 Lab Reports"])
    
    with tab1:
        with st.form("personal_info_form"):
            st.subheader("Basic Information")
            col1, col2 = st.columns(2)
            
            with col1:
                name = st.text_input("Full Name", value=existing_details.get('Name', '') if existing_details else '')
                gender = st.selectbox("Gender", options=["Male", "Female", "Other"],
                                    index=["Male", "Female", "Other"].index(existing_details.get('Gender', 'Male')) 
                                    if existing_details and existing_details.get('Gender') in ["Male", "Female", "Other"]
                                    else 0)
                age = st.number_input("Age", min_value=1, max_value=120,
                                    value=int(existing_details.get('Age', 25)) if existing_details and existing_details.get('Age') else 25)
                birth_date = st.date_input("Birth Date", value=datetime.now().date())
            
            with col2:
                blood_group = st.selectbox("Blood Group", 
                                         options=["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                         index=0)
                height = st.number_input("Height (cm)", min_value=50, max_value=250,
                                       value=int(existing_details.get('Height', 170)) if existing_details and existing_details.get('Height') else 170)
                weight = st.number_input("Weight (kg)", min_value=20, max_value=200,
                                       value=int(existing_details.get('Weight', 70)) if existing_details and existing_details.get('Weight') else 70)
                emergency_contact = st.text_input("Emergency Contact (Name & Phone)",
                                                value=existing_details.get('Emergency Contact', '') if existing_details else '')

            st.subheader("Medical Information")
            col3, col4 = st.columns(2)
            
            with col3:
                disease = st.text_area("Current Medical Conditions", 
                                     value=existing_details.get('Disease', '') if existing_details else '')
                allergies = st.text_area("Known Allergies",
                                       value=existing_details.get('Allergies', '') if existing_details else '')
                current_medications = st.text_area("Current Medications",
                                                 value=existing_details.get('Current Medications', '') if existing_details else '')
            
            with col4:
                previous_surgeries = st.text_area("Previous Surgeries",
                                                value=existing_details.get('Previous Surgeries', '') if existing_details else '')
                family_history = st.text_area("Family Medical History",
                                            value=existing_details.get('Family History', '') if existing_details else '')
                insurance_details = st.text_area("Insurance Details",
                                               value=existing_details.get('Insurance Details', '') if existing_details else '')
            
            submitted = st.form_submit_button("Save Personal Information")
            if submitted:
                if not name or not gender or not age:
                    st.error("Please fill in all required fields (Name, Gender, and Age)")
                    return
                
                # Get existing lab details or empty strings if none exist
                update_patient_details(
                    st.session_state.email,
                    name, gender, age, birth_date, disease, allergies, blood_group,
                    height, weight, emergency_contact, previous_surgeries,
                    current_medications, family_history, insurance_details,
                    existing_details.get('Recent Lab Tests', ''),
                    existing_details.get('Blood Test Results', ''),
                    existing_details.get('Imaging Reports', ''),
                    existing_details.get('Other Test Results', ''),
                    existing_details.get('Lab Report Dates', '')
                )
    
    with tab2:
        with st.form("lab_reports_form"):
            st.subheader("Laboratory Reports")
            
            recent_lab_tests = st.text_area("Recent Laboratory Tests",
                                          value=existing_details.get('Recent Lab Tests', '') if existing_details else '',
                                          help="List all recent laboratory tests performed")
            
            col5, col6 = st.columns(2)
            
            with col5:
                blood_test_results = st.text_area("Blood Test Results",
                                                value=existing_details.get('Blood Test Results', '') if existing_details else '',
                                                help="Include details like CBC, lipid profile, blood sugar, etc.")
                imaging_reports = st.text_area("Imaging Reports",
                                             value=existing_details.get('Imaging Reports', '') if existing_details else '',
                                             help="Include dates and findings of X-rays, CT scans, MRI, etc.")
            
            with col6:
                other_test_results = st.text_area("Other Test Results",
                                                value=existing_details.get('Other Test Results', '') if existing_details else '',
                                                help="Include any other diagnostic test results")
                lab_report_dates = st.text_area("Test Dates and Follow-ups",
                                              value=existing_details.get('Lab Report Dates', '') if existing_details else '',
                                              help="Include dates of tests and scheduled follow-ups")
            
            lab_submitted = st.form_submit_button("Save Lab Reports")
            if lab_submitted:
                update_patient_details(
                    st.session_state.email,
                    existing_details.get('Name', ''), existing_details.get('Gender', ''),
                    existing_details.get('Age', ''), existing_details.get('Birth Date', ''),
                    existing_details.get('Disease', ''), existing_details.get('Allergies', ''),
                    existing_details.get('Blood Group', ''), existing_details.get('Height', ''),
                    existing_details.get('Weight', ''), existing_details.get('Emergency Contact', ''),
                    existing_details.get('Previous Surgeries', ''),
                    existing_details.get('Current Medications', ''),
                    existing_details.get('Family History', ''),
                    existing_details.get('Insurance Details', ''),
                    recent_lab_tests, blood_test_results, imaging_reports,
                    other_test_results, lab_report_dates
                )

    # Display current profile information
    if existing_details:
        with st.expander("📑 View Current Profile", expanded=False):
            st.write("### 👤 Personal Details")
            col7, col8 = st.columns(2)
            
            with col7:
                st.write(f"**Name:** {existing_details.get('Name', 'Not provided')}")
                st.write(f"**Gender:** {existing_details.get('Gender', 'Not provided')}")
                st.write(f"**Age:** {existing_details.get('Age', 'Not provided')}")
                st.write(f"**Birth Date:** {existing_details.get('Birth Date', 'Not provided')}")
                st.write(f"**Blood Group:** {existing_details.get('Blood Group', 'Not provided')}")
                st.write(f"**Height:** {existing_details.get('Height', 'Not provided')} cm")
                st.write(f"**Weight:** {existing_details.get('Weight', 'Not provided')} kg")
            
            with col8:
                st.write(f"**Emergency Contact:** {existing_details.get('Emergency Contact', 'Not provided')}")
                st.write(f"**Medical Conditions:** {existing_details.get('Disease', 'Not provided')}")
                st.write(f"**Allergies:** {existing_details.get('Allergies', 'Not provided')}")
                st.write(f"**Current Medications:** {existing_details.get('Current Medications', 'Not provided')}")
                st.write(f"**Insurance Details:** {existing_details.get('Insurance Details', 'Not provided')}")
            
            st.write("### 🔬 Laboratory Reports")
            st.write(f"**Recent Tests:** {existing_details.get('Recent Lab Tests', 'Not provided')}")
            st.write(f"**Blood Test Results:** {existing_details.get('Blood Test Results', 'Not provided')}")
            st.write(f"**Imaging Reports:** {existing_details.get('Imaging Reports', 'Not provided')}")
            st.write(f"**Other Test Results:** {existing_details.get('Other Test Results', 'Not provided')}")
            st.write(f"**Test Dates:** {existing_details.get('Lab Report Dates', 'Not provided')}")