# models.py
import streamlit as st
import importlib.util
import sys
from pathlib import Path

def import_app_from_file(file_path):
    """
    Import a module from file path dynamically.
    """
    try:
        module_name = Path(file_path).stem
        if module_name not in sys.modules:
            spec = importlib.util.spec_from_file_location(module_name, file_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            return module
        return sys.modules[module_name]
    except Exception as e:
        st.error(f"Error loading module {file_path}: {str(e)}")
        return None

def app():
    st.title("Disease Prediction Models")
    
    # Dictionary mapping display names to script paths
    prediction_apps = {
        "Eye Disease Prediction": "Prediciton models/Eye-Disease-Detection/app.py",
        #"General Disease Prediction": "Prediciton models/disease_prediction/app.py",
        "Heart Disease Prediction": "Prediciton models/Heart_Disease_Predictor/app.py",
        "Hairfall Prediction": "Prediciton models/hair_fall_prediticition/main.py",
        "Skin Disease Prediction": "Prediciton models/skin_disease_prediciton/main.py"
    }
    
    # Create the dropdown for app selection
    selected_app = st.selectbox(
        "Select Disease Prediction Model",
        options=list(prediction_apps.keys()),
        index=None,
        placeholder="Choose a prediction model..."
    )
    
    # Load and run the selected app
    if selected_app:
        script_path = prediction_apps[selected_app]
        
        if Path(script_path).exists():
            # Import the selected app module
            app_module = import_app_from_file(script_path)
            
            if app_module and hasattr(app_module, 'app'):
                # Clear previous content (optional)
                # st.empty()
                
                # Create a visual separator
                st.markdown("---")
                
                # Run the app's main function
                app_module.app()
            else:
                st.error(f"The selected app doesn't have the required 'app' function")
        else:
            st.error(f"App file not found: {script_path}")

