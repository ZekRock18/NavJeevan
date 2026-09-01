import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime, timedelta
import pandas as pd

load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Set up Google Sheets authentication
def authenticate_google_sheets():
    scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets', 
             "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name("navjeevan-service-account.json", scope)
    client = gspread.authorize(creds)
    return client.open("navjeevan_database")

# Get user profile data
def get_user_profile(email):
    sheet = authenticate_google_sheets().sheet1
    try:
        records = sheet.get_all_records()
        for record in records:
            if record['Email'] == email:
                return record
        return None
    except Exception as e:
        st.error(f"Error fetching profile: {str(e)}")
        return None

# Save daily tracking data
def save_daily_tracking(email, tracking_data):
    workbook = authenticate_google_sheets()
    tracking_sheet = workbook.worksheet("DailyTracking")  # Create this sheet in your spreadsheet
    
    try:
        tracking_data['Email'] = email
        tracking_data['Date'] = datetime.now().strftime('%Y-%m-%d')
        tracking_sheet.append_row([
            tracking_data['Date'],
            email,
            tracking_data['sleep_hours'],
            tracking_data['water_intake'],
            tracking_data['exercise_minutes'],
            tracking_data['mood'],
            tracking_data['stress_level'],
            tracking_data['meal_quality'],
            tracking_data['notes']
        ])
        return True
    except Exception as e:
        st.error(f"Error saving tracking data: {str(e)}")
        return False

def process_data(profile_data, tracking_data):
    # Create a comprehensive prompt using both profile and tracking data
    prompt = f"""Given the following patient information and daily tracking data, provide a personalized health recommendation:

    Profile Information:
    Height: {profile_data.get('Height', 'N/A')} cm
    Weight: {profile_data.get('Weight', 'N/A')} kg
    Blood Group: {profile_data.get('Blood Group', 'N/A')}
    Medical Conditions: {profile_data.get('Disease', 'None')}
    Allergies: {profile_data.get('Allergies', 'None')}
    Previous Surgeries: {profile_data.get('Previous Surgeries', 'None')}
    Current Medications: {profile_data.get('Current Medications', 'None')}
    
    Today's Tracking Data:
    Sleep Duration: {tracking_data.get('sleep_hours', 'N/A')} hours
    Water Intake: {tracking_data.get('water_intake', 'N/A')} glasses
    Exercise Duration: {tracking_data.get('exercise_minutes', 'N/A')} minutes
    Mood: {tracking_data.get('mood', 'N/A')}
    Stress Level: {tracking_data.get('stress_level', 'N/A')}/5
    Meal Quality: {tracking_data.get('meal_quality', 'N/A')}/5
    Additional Notes: {tracking_data.get('notes', '')}

    Please provide a comprehensive health recommendation including:
    1. Sleep quality assessment and suggestions
    2. Hydration status and recommendations
    3. Exercise routine evaluation going through patients previous surgeries and current medications
    4. Mental wellness insights
    5. Dietary suggestions based on meal quality
    6. Specific considerations based on medical conditions
    7. Short-term and long-term health goals
    """
    
    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            model="llama3-8b-8192",
            temperature=0.7,
            max_tokens=1000
        )
        return chat_completion.choices[0].message.content
    except Exception as e:
        st.error(f"Error generating recommendation: {str(e)}")
        return None

def app():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.error("Please log in to access health tracking and recommendations.")
        return
    
    st.title("Health Tracking & Recommendations")
    
    # Get user profile data
    profile_data = get_user_profile(st.session_state.email)
    if not profile_data:
        st.error("Unable to fetch your profile data. Please ensure your profile is complete.")
        return
    
    # Create tabs for different sections
    tab1, tab2 = st.tabs(["📊 Daily Tracking", "💡 View Recommendations"])
    
    with tab1:
        st.subheader("Daily Health Tracking")
        with st.form("daily_tracking_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                sleep_hours = st.number_input("Hours of Sleep:", 
                                            min_value=0.0, 
                                            max_value=24.0, 
                                            value=7.0,
                                            step=0.5)
                
                water_intake = st.number_input("Water Intake (glasses):", 
                                             min_value=0, 
                                             max_value=20, 
                                             value=8)
                
                exercise_minutes = st.number_input("Exercise Duration (minutes):", 
                                                 min_value=0, 
                                                 max_value=300, 
                                                 value=30)
            
            with col2:
                mood = st.selectbox("Today's Mood:", 
                                  options=["Excellent", "Good", "Neutral", "Poor", "Very Poor"])
                
                stress_level = st.slider("Stress Level (1-5):", 
                                       min_value=1, 
                                       max_value=5, 
                                       value=3)
                
                meal_quality = st.slider("Overall Meal Quality (1-5):", 
                                       min_value=1, 
                                       max_value=5, 
                                       value=3)
            
            notes = st.text_area("Additional Notes:", 
                               placeholder="Any specific health concerns, symptoms, or achievements today?")
            
            submitted = st.form_submit_button("Save Daily Tracking")
            
            if submitted:
                tracking_data = {
                    'sleep_hours': sleep_hours,
                    'water_intake': water_intake,
                    'exercise_minutes': exercise_minutes,
                    'mood': mood,
                    'stress_level': stress_level,
                    'meal_quality': meal_quality,
                    'notes': notes
                }
                
                if save_daily_tracking(st.session_state.email, tracking_data):
                    st.success("Daily tracking data saved successfully!")
                    
                    # Generate and display recommendation
                    with st.spinner("Generating personalized recommendation..."):
                        recommendation = process_data(profile_data, tracking_data)
                        if recommendation:
                            st.info("Based on your profile and today's data:")
                            st.write(recommendation)
    
    with tab2:
        st.subheader("Health Insights & Recommendations")
        if st.button("Generate New Recommendation"):
            # Get the latest tracking data (you'll need to implement this)
            tracking_data = {
                'sleep_hours': sleep_hours if 'sleep_hours' in locals() else 0,
                'water_intake': water_intake if 'water_intake' in locals() else 0,
                'exercise_minutes': exercise_minutes if 'exercise_minutes' in locals() else 0,
                'mood': mood if 'mood' in locals() else 'Not specified',
                'stress_level': stress_level if 'stress_level' in locals() else 3,
                'meal_quality': meal_quality if 'meal_quality' in locals() else 3,
                'notes': notes if 'notes' in locals() else ''
            }
            
            with st.spinner("Generating personalized recommendation..."):
                recommendation = process_data(profile_data, tracking_data)
                if recommendation:
                    st.info("Your Personalized Health Recommendations:")
                    st.write(recommendation)
        
        # Display tracking history
        st.subheader("Your Tracking History")
        try:
            tracking_sheet = authenticate_google_sheets().worksheet("DailyTracking")
            tracking_records = tracking_sheet.get_all_records()
            user_records = [r for r in tracking_records if r['Email'] == st.session_state.email]
            if user_records:
                df = pd.DataFrame(user_records)
                st.line_chart(df[['Sleep Hours', 'Water Intake', 'Exercise Minutes']])
            else:
                st.info("No tracking history available yet. Start tracking your daily health metrics!")
        except Exception as e:
            st.error(f"Error loading tracking history: {str(e)}")

    # Add a disclaimer
    st.caption("Disclaimer: This tool provides general recommendations based on your data and should not replace professional medical advice.")

if __name__ == "__main__":
    app()