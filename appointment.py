import streamlit as st
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import datetime
import sendgrid
from sendgrid.helpers.mail import Mail, Email, To, Content
from twilio.rest import Client
import os
from dotenv import load_dotenv

load_dotenv()

# Google Calendar API Setup
SERVICE_ACCOUNT_FILE = "navjeevan-service-account.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]
JITSI_BASE_URL = "https://meet.jit.si"

# Twilio Setup
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = '+12313837782'
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

# SendGrid Setup
SENDGRID_API_KEY = os.getenv('SENDGRID_API_KEY')
sg = sendgrid.SendGridAPIClient(api_key=SENDGRID_API_KEY)

# Doctor schedules
doctor_schedules = {
    "Dermatologist": {"start_time": "14:00", "end_time": "19:00"},
    "Cardiologist": {"start_time": "10:00", "end_time": "15:00"},
    "Pediatrician": {"start_time": "09:00", "end_time": "13:00"}
}

# Generate time slots
def generate_time_slots(start_time, end_time, interval=30):
    slots = []
    start = datetime.datetime.strptime(start_time, "%H:%M")
    end = datetime.datetime.strptime(end_time, "%H:%M")
    while start < end:
        slots.append(start.strftime("%H:%M"))
        start += datetime.timedelta(minutes=interval)
    return slots

def create_google_calendar_event(doctor, date, time_slot):
    try:
        credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
        service = build("calendar", "v3", credentials=credentials)
        
        event_start = f"{date}T{time_slot}:00+05:30"  # Added timezone offset
        event_end = (datetime.datetime.fromisoformat(event_start) + datetime.timedelta(minutes=30)).isoformat()
        
        event = {
            "summary": f"Appointment with {doctor}",
            "description": f"Your appointment with {doctor}.",
            "start": {"dateTime": event_start, "timeZone": "Asia/Kolkata"},
            "end": {"dateTime": event_end, "timeZone": "Asia/Kolkata"},
            "visibility": "public",
            "reminders": {
                "useDefault": False,
                "overrides": [
                    {"method": "email", "minutes": 24 * 60},
                    {"method": "popup", "minutes": 30}
                ]
            }
        }
        
        event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()
        return event["htmlLink"]
    except Exception as e:
        st.error(f"Calendar Error: {str(e)}")
        return None

# Send email using SendGrid
def send_email(to_email, doctor, date, time_slot, jitsi_link, calendar_link):
    subject = f"Appointment Confirmation with {doctor}"
    body = f"""
    Hello,

    Your appointment with {doctor} is confirmed for {date} at {time_slot}.
    Join the video call here: {jitsi_link}
    
    To add this event to your Google Calendar, click here: {calendar_link}
    
    Thank you for scheduling with us!
    """
    
    # Create the email message properly
    message = Mail(
        from_email=Email("prakhargupta.pg123@gmail.com"),
        to_emails=to_email,  # Changed from To(to_email) to just to_email
        subject=subject,
        plain_text_content=body
    )
    
    try:
        response = sg.send(message)
        return response.status_code, response.body
    except Exception as e:
        st.error(f"Failed to send email: {str(e)}")
        return None, str(e)


def send_sms(to_phone, doctor, date, time_slot, jitsi_link):
    # Format phone number to E.164 format
    formatted_phone = "+91" + to_phone.replace(" ", "").replace("-", "")[-10:]
    
    try:
        message = client.messages.create(
            body=f"Appointment with {doctor} on {date} at {time_slot}. Join the call here: {jitsi_link}",
            from_=TWILIO_PHONE_NUMBER,
            to=formatted_phone
        )
        return message.sid
    except Exception as e:
        st.error(f"Failed to send SMS: {str(e)}")
        return None
# Streamlit App Interface
def app():
    st.title("Doctor Appointment Scheduler")

    # Get user's email and phone number
    user_email = st.text_input("Enter Your Email ID", "")
    phone_number = st.text_input("Enter Your Phone Number", "")

    if user_email and phone_number:
        # Select doctor
        doctor = st.selectbox("Select a Doctor", list(doctor_schedules.keys()))
        date = st.date_input("Select a Date", min_value=datetime.date.today())

        if doctor and date:
            schedule = doctor_schedules[doctor]
            st.write(f"Available slots for {doctor}: {schedule['start_time']} to {schedule['end_time']}")
            
            time_slots = generate_time_slots(schedule['start_time'], schedule['end_time'])
            selected_slot = st.selectbox("Select a Time Slot", time_slots)

            if st.button("Schedule Appointment"):
                # Generate Jitsi link
                jitsi_link = f"{JITSI_BASE_URL}/{doctor.replace(' ', '')}_{selected_slot.replace(':', '')}"
                
                # Add to Google Calendar
                calendar_link = create_google_calendar_event(doctor, date, selected_slot)
                
                # Send email and SMS
                send_email(user_email, doctor, date, selected_slot, jitsi_link, calendar_link)
                send_sms(phone_number, doctor, date, selected_slot, jitsi_link)
                
                st.success(f"Appointment Scheduled with {doctor} at {selected_slot}")
                st.write(f"Join the video call: [Click Here]({jitsi_link})")
                st.write(f"View your Google Calendar event: [Click Here]({calendar_link})")

# Run the app

