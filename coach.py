import cv2
import mediapipe as mp
import math
import streamlit as st
import numpy as np
from PIL import Image
import time

# Initialize MediaPipe Pose solution
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

def calculate_angle(a, b, c):
    """
    Calculate the angle between three points.
    """
    try:
        a = np.array([a[0] - b[0], a[1] - b[1]])
        c = np.array([c[0] - b[0], c[1] - b[1]])
        
        dot_product = np.dot(a, c)
        magnitude_a = np.linalg.norm(a)
        magnitude_c = np.linalg.norm(c)
        
        # Avoid division by zero
        if magnitude_a == 0 or magnitude_c == 0:
            return 0
            
        cos_angle = np.clip(dot_product / (magnitude_a * magnitude_c), -1.0, 1.0)
        angle = np.arccos(cos_angle)
        return np.degrees(angle)
    except Exception as e:
        st.error(f"Error calculating angle: {str(e)}")
        return 0

def video_stream():
    """
    Handle the video stream and exercise tracking.
    """
    # Create stop button
    stop_button = st.button('Stop')
    
    # Initialize exercise counters and states
    curl_count = 0
    squat_count = 0
    in_curl = False
    in_squat = False
    
    # Create placeholder for video feed
    video_placeholder = st.empty()
    
    # Initialize status text containers
    curl_status = st.empty()
    squat_status = st.empty()
    
    try:
        # Initialize webcam
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            st.error("Cannot access webcam. Please check your camera connection.")
            return
            
        # Initialize MediaPipe Pose
        with mp_pose.Pose(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as pose:
            
            while cap.isOpened() and not stop_button:
                # Control frame rate
                time.sleep(0.03)  # Limit to roughly 30 FPS
                
                # Read frame
                ret, frame = cap.read()
                if not ret:
                    st.error("Failed to read frame from webcam")
                    break
                
                # Convert frame to RGB
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # Process the frame
                results = pose.process(frame_rgb)
                
                if results.pose_landmarks:
                    # Draw pose landmarks
                    mp_drawing.draw_landmarks(
                        frame,
                        results.pose_landmarks,
                        mp_pose.POSE_CONNECTIONS,
                        mp_drawing_styles.get_default_pose_landmarks_style())
                    
                    try:
                        # Get landmarks
                        landmarks = results.pose_landmarks.landmark
                        
                        # Required landmarks for exercises
                        required_landmarks = [
                            mp_pose.PoseLandmark.RIGHT_SHOULDER,
                            mp_pose.PoseLandmark.RIGHT_ELBOW,
                            mp_pose.PoseLandmark.RIGHT_WRIST,
                            mp_pose.PoseLandmark.LEFT_HIP,
                            mp_pose.PoseLandmark.LEFT_KNEE,
                            mp_pose.PoseLandmark.LEFT_ANKLE
                        ]
                        
                        if all(landmarks[lm.value].visibility > 0.5 for lm in required_landmarks):
                            # Process curl
                            shoulder = [landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].x,
                                      landmarks[mp_pose.PoseLandmark.RIGHT_SHOULDER.value].y]
                            elbow = [landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_ELBOW.value].y]
                            wrist = [landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].x,
                                   landmarks[mp_pose.PoseLandmark.RIGHT_WRIST.value].y]
                            
                            curl_angle = calculate_angle(shoulder, elbow, wrist)
                            
                            # Process squat
                            hip = [landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_HIP.value].y]
                            knee = [landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].x,
                                  landmarks[mp_pose.PoseLandmark.LEFT_KNEE.value].y]
                            ankle = [landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].x,
                                   landmarks[mp_pose.PoseLandmark.LEFT_ANKLE.value].y]
                            
                            squat_angle = calculate_angle(hip, knee, ankle)
                            
                            # Count curls
                            if curl_angle > 160:
                                in_curl = False
                            elif curl_angle < 50 and not in_curl:
                                curl_count += 1
                                in_curl = True
                            
                            # Count squats
                            if squat_angle > 160:
                                in_squat = False
                            elif squat_angle < 90 and not in_squat:
                                squat_count += 1
                                in_squat = True
                            
                            # Draw angles and feedback
                            # Curl feedback
                            if curl_angle < 50:
                                cv2.putText(frame, "Perfect Curl!", (50, 150),
                                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            else:
                                cv2.putText(frame, "Bend your elbow more", (50, 150),
                                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            
                            # Squat feedback
                            if squat_angle < 90:
                                cv2.putText(frame, "Perfect Squat Depth!", (50, 200),
                                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            else:
                                cv2.putText(frame, "Go lower", (50, 200),
                                          cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                            
                            # Display angles
                            cv2.putText(frame, f"Curl angle: {int(curl_angle)}", 
                                      (int(elbow[0] * frame.shape[1]), int(elbow[1] * frame.shape[0])),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                            cv2.putText(frame, f"Squat angle: {int(squat_angle)}", 
                                      (int(knee[0] * frame.shape[1]), int(knee[1] * frame.shape[0])),
                                      cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                        
                        else:
                            cv2.putText(frame, "Please ensure full body is visible", (50, 50),
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                    
                    except Exception as e:
                        st.error(f"Error processing landmarks: {str(e)}")
                
                # Display exercise counts
                cv2.putText(frame, f"Curls: {curl_count}", (50, 50),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                cv2.putText(frame, f"Squats: {squat_count}", (50, 100),
                           cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                
                # Convert frame for Streamlit display
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame_rgb)
                video_placeholder.image(img, caption="Exercise Tracker", use_container_width=True)
                
                # Update status
                curl_status.text(f"Total Curls: {curl_count}")
                squat_status.text(f"Total Squats: {squat_count}")
                
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        
    finally:
        # Clean up
        if 'cap' in locals():
            cap.release()

def app():
    """
    Main Streamlit application.
    """
    st.title("NavJeevan - AI Wellness Coach")
    st.write("This application tracks your bicep curls and squats in real-time.")
    st.write("Make sure your full body is visible in the camera frame.")
    
    # Instructions
    with st.expander("How to use"):
        st.write("""
        1. Click 'Start' to begin exercise tracking
        2. Stand back so your full body is visible
        3. For bicep curls:
           - Keep your upper arm steady
           - Curl your forearm up towards your shoulder
           - Lower back down fully
        4. For squats:
           - Keep your feet shoulder-width apart
           - Lower your body until thighs are parallel to ground
           - Push back up to standing position
        5. Click 'Stop' when finished
        """)
    
    # Start button
    if st.button('Start', key='start_video'):
        video_stream()

if __name__ == "__main__":
    app()