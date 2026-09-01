import os
import torch
import streamlit as st
from torchvision import transforms, models
from PIL import Image

# Set paths
DATA_DIR = os.path.join(os.path.dirname(__file__), "img")  # Update to your test image directory
MODEL_PATH = os.path.join(os.path.dirname(__file__), "models", "hair_classification.pth")  # Update to your trained model path

# Define classes for hair classification
CLASSES = ["Stage1", "Stage2", "Stage3"]  # Ensure these match your training dataset classes

def load_model(model_path):
    """
    Load the pre-trained model and optimize for CPU usage.
    """
    try:
        # Load ResNet-18 architecture
        model = models.resnet18(weights=None)
        model.fc = torch.nn.Linear(model.fc.in_features, len(CLASSES))  # Adjust output layer

        # Load trained weights
        state_dict = torch.load(model_path, map_location="cpu")
        model.load_state_dict(state_dict)

        # Optimize the model for CPU
        model.eval()  # Set the model to evaluation mode
        return model.to(memory_format=torch.channels_last)
    except Exception as e:
        st.error(f"Error loading model: {e}")
        raise


def preprocess_image(image_path):
    """
    Preprocess an input image for the model.
    """
    try:
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])

        img = Image.open(image_path).convert("RGB")
        return transform(img).unsqueeze(0)  # Add batch dimension
    except Exception as e:
        st.error(f"Error preprocessing image {image_path}: {e}")
        raise


def predict_hair_stage(model, image_tensor):
    """
    Predict the hair classification stage.
    """
    try:
        with torch.no_grad():
            # Convert image tensor to channels-last format
            image_tensor = image_tensor.to(memory_format=torch.channels_last)

            # Perform inference
            output = model(image_tensor)
            probabilities = torch.softmax(output, dim=1)
            _, predicted_class = probabilities.max(1)
            return predicted_class.item(), probabilities[0].tolist()
    except Exception as e:
        st.error(f"Error during prediction: {e}")
        raise


def app():
    # Set up Streamlit app layout
    st.title("Hair Fall Classification")
    st.markdown("This app classifies hair fall stages based on input images.")
    
    # Upload an image for classification
    uploaded_image = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
    
    if uploaded_image is not None:
        try:
            # Display the uploaded image
            image = Image.open(uploaded_image)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Preprocess the uploaded image
            image_tensor = preprocess_image(uploaded_image)
            
            # Load the model
            model = load_model(MODEL_PATH)
            
            # Predict the hair classification stage
            predicted_class, probabilities = predict_hair_stage(model, image_tensor)
            
            # Display the results
            st.write(f"Predicted Hair Fall Stage: {CLASSES[predicted_class]}")
            st.write(f"Probabilities: {probabilities}")
            
            if probabilities[predicted_class] > 0.8:
                st.success(f"High confidence in this prediction: {CLASSES[predicted_class]}")
            else:
                st.warning("Prediction confidence is low. Please check the image quality.")
            
        except Exception as e:
            st.error(f"Error processing the image: {e}")
    
    else:
        st.info("Please upload an image to classify the hair fall stage.")


