import streamlit as st
import requests
import os
from dotenv import load_dotenv
import pandas as pd
import math

# Load environment variables from .env file
load_dotenv()

# Get the Google Maps API key from the environment variable
API_KEY = os.getenv('API_KEY')

# Function to get latitude and longitude from place name using Google Maps Geocoding API
def geocode_place(place_name):
    url = f'https://maps.googleapis.com/maps/api/geocode/json?address={place_name}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        # Get the latitude and longitude from the first result
        lat = data['results'][0]['geometry']['location']['lat']
        lng = data['results'][0]['geometry']['location']['lng']
        return lat, lng
    else:
        st.error("Geocoding failed. Please check the place name and try again.")
        return None, None

# Function to get contact information (phone number) from Google Places API using place_id
def get_contact_info(place_id):
    url = f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    
    if data['status'] == 'OK':
        # Extract phone number if available
        phone_number = data['result'].get('formatted_phone_number', 'N/A')
        return phone_number
    else:
        return 'N/A'

# Function to calculate distance between two coordinates using Haversine formula
def calculate_distance(lat1, lng1, lat2, lng2):
    # Convert degrees to radians
    lat1, lng1, lat2, lng2 = map(math.radians, [lat1, lng1, lat2, lng2])

    # Haversine formula
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    
    # Radius of Earth in kilometers (mean radius)
    R = 6371.0
    distance = R * c
    return distance

# Function to find nearest hospitals using Google Maps Places API
def find_nearest_hospitals(lat, lng):
    url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&radius=5000&type=hospital&key={API_KEY}'
    response = requests.get(url)
    data = response.json()

    hospitals = []
    if 'results' in data:
        for result in data['results']:
            name = result.get('name')
            address = result.get('vicinity')
            rating = result.get('rating', 'N/A')  # Default to 'N/A' if no rating
            user_ratings_total = result.get('user_ratings_total', 'N/A')  # Number of reviews
            place_id = result.get('place_id')  # Place ID for navigating
            hospital_lat = result['geometry']['location']['lat']
            hospital_lng = result['geometry']['location']['lng']
            
            # Get the contact information for the hospital
            phone_number = get_contact_info(place_id)
            
            # Calculate the distance to the hospital
            distance = calculate_distance(lat, lng, hospital_lat, hospital_lng)
            
            hospitals.append({
                'name': name, 
                'address': address, 
                'rating': rating,
                'user_ratings_total': user_ratings_total,
                'phone_number': phone_number,  # Add phone number to the data
                'distance_km': round(distance, 2),  # Add distance in km
                'place_id': place_id
            })
    else:
        st.error("No hospitals found.")
    
    return hospitals

# Streamlit App Interface
def app():
    st.title('Find Nearest Hospitals')

    # Input for place name
    place_name = st.text_input("Enter Your Area/Place Name (e.g., City, Locality)")

    # Button to trigger the search for nearest hospitals
    if st.button("Find Nearest Hospitals"):
        if place_name:
            # Get latitude and longitude from the place name
            lat, lng = geocode_place(place_name)
            
            if lat and lng:
                st.write(f"Latitude: {lat}, Longitude: {lng}")
                
                # Find nearest hospitals
                hospitals = find_nearest_hospitals(lat, lng)
                
                if hospitals:
                    # Create a DataFrame to display hospitals in a table
                    df = pd.DataFrame(hospitals)
                    
                    # Display hospitals in a more interactive way using st.dataframe
                    st.markdown("### Nearby Hospitals:")
                    st.dataframe(df[['name', 'address', 'rating', 'user_ratings_total', 'phone_number', 'distance_km']])

                    # Display clickable links in a systematic format (one below the other)
                    links = ""
                    for index, row in df.iterrows():
                        url = f"https://www.google.com/maps/search/?q={row['name']}+{row['address']}"
                        links += f'<a href="{url}" target="_blank">{row["name"]}</a><br>'  # Line break for each link

                    # Render the links in the Streamlit app
                    st.markdown(f"### Click to navigate to the hospitals:<br>{links}", unsafe_allow_html=True)
                else:
                    st.write("No hospitals found.")
        else:
            st.write("Please enter a place name.")

# Run the app

