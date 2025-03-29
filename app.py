# app.py

import streamlit as st
from pathlib import Path
import json
# Import page_setup from common.py
from src.common.common import page_setup
# Import pyopenms if needed
# import pyopenms

# --- Page Configuration (MUST BE FIRST STREAMLIT COMMAND) ---
# Load settings temporarily just for set_page_config
# We'll load them properly again inside page_setup
try:
    with open("settings.json", "r") as f_settings:
        app_settings = json.load(f_settings)
    st.set_page_config(
        page_title=app_settings.get("app-name", "Streamlit App"), # Use .get for safety
        page_icon="assets/openms_transparent_bg_logo.svg",
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )
except FileNotFoundError:
    # Fallback configuration if settings.json is missing
    st.set_page_config(
        page_title="Streamlit App",
        page_icon="assets/openms_transparent_bg_logo.svg", # Ensure this asset exists
        layout="wide",
        initial_sidebar_state="auto",
        menu_items=None,
    )
except Exception as e:
    # Generic fallback
    print(f"Error loading settings for page_config: {e}")
    st.set_page_config(layout="wide")


# --- Setup Phase ---
# Now call page_setup. It will handle the rest:
# loading settings properly into session_state, workspace, sidebar, captcha, etc.
# It should NO LONGER call st.set_page_config() itself.
params = page_setup()
# Execution STOPS inside page_setup (in captcha_control) if captcha is needed.


# --- Main App Logic ---
# This part only runs if page_setup completed.
if __name__ == '__main__':
    # Check if settings were loaded correctly by page_setup
    if "settings" not in st.session_state:
         st.error("Failed to load application settings properly.")
         st.stop()

    # Define all your application pages using the loaded settings
    all_pages = {
        str(st.session_state.settings["app-name"]) : [
            st.Page(Path("content", "quickstart.py"), title="Quickstart", icon="👋"),
            st.Page(Path("content", "documentation.py"), title="Documentation", icon="📖"),
        ],
        "TOPP Workflow Framework": [
            st.Page(Path("content", "topp_workflow_file_upload.py"), title="File Upload", icon="📁"),
            st.Page(Path("content", "topp_workflow_parameter.py"), title="Configure", icon="⚙️"),
            st.Page(Path("content", "topp_workflow_execution.py"), title="Run", icon="🚀"),
            st.Page(Path("content", "topp_workflow_results.py"), title="Results", icon="📊"),
        ],
        "pyOpenMS Workflow" : [
            st.Page(Path("content", "file_upload.py"), title="File Upload", icon="📂"),
            st.Page(Path("content", "raw_data_viewer.py"), title="View MS data", icon="👀"),
            st.Page(Path("content", "run_example_workflow.py"), title="Run Workflow", icon="⚙️"),
            st.Page(Path("content", "download_section.py"), title="Download Results", icon="⬇️"),
        ],
        "Others Topics": [
            st.Page(Path("content", "simple_workflow.py"), title="Simple Workflow", icon="⚙️"),
            st.Page(Path("content", "run_subprocess.py"), title="Run Subprocess", icon="🖥️"),
        ]
    }

    # Pass the defined pages to st.navigation and run the selected page
    pg = st.navigation(all_pages)
    pg.run()