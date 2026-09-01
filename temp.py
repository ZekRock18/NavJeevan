import streamlit as st
from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()

# Groq Client initialization
client = Groq(api_key=os.getenv('GROQ_API_KEY'))

# Function to process the data and get recommendation
def process_data(height, weight, blood_pressure, notes):
    # Create a prompt for the LLM
    prompt = f"""Given the following patient information, provide a brief health recommendation:
    Height: {height} cm
    Weight: {weight} kg
    Blood Pressure: {blood_pressure}
    Additional Notes: {notes}
    
    Please provide a concise health recommendation based on these metrics, including:
    1. BMI assessment
    2. Blood pressure evaluation
    3. General health suggestions
    4. Diet plans or restrictions
    5. Exercise recommendations
    """
    
    # Make the API call to Groq
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        model="llama3-8b-8192",  # Using llama2-70b model
        temperature=0.7,
        max_tokens=800
    )
    
    # Extract the recommendation from the response
    return chat_completion.choices[0].message.content

# Streamlit app frontend
def app():
    st.title("Health Recommendation System")
    
    # Add a brief description
    st.write("Enter your health metrics below to receive personalized recommendations.")
    
    # Create two columns for input fields
    col1, col2 = st.columns(2)
    
    with col1:
        height = st.number_input("Height (cm):", min_value=0.0, max_value=300.0, value=170.0)
        weight = st.number_input("Weight (kg):", min_value=0.0, max_value=500.0, value=70.0)
    
    with col2:
        blood_pressure = st.text_input("Blood Pressure (e.g., 120/80):", value="120/80")
        notes = st.text_area("Additional Notes (optional):", height=100)

    # Add a divider
    st.divider()
    
    # Button to process the data and get recommendation
    if st.button("Get Recommendation", type="primary"):
        if height > 0 and weight > 0 and blood_pressure:
            with st.spinner("Generating recommendation..."):
                try:
                    recommendation = process_data(height, weight, blood_pressure, notes)
                    st.success("Recommendation Generated!")
                    st.write(recommendation)
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")
        else:
            st.warning("Please fill in all required fields (Height, Weight, and Blood Pressure).")

    # Add a disclaimer
    st.caption("Disclaimer: This tool provides general recommendations and should not replace professional medical advice.")

if __name__ == "__main__":
    app()