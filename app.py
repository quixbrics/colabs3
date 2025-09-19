import os
import streamlit as st
import random
import openai
import requests
from bs4 import BeautifulSoup

# --- Constants ---
PLOTGEN_URL = "https://writingexercises.co.uk/plotgenerator.php"
DROPDOWNS = {
    "character": "CHARACTERS",
    "setting": "SETTINGS",
    "situation": "SITUATIONS",
    "theme": "THEMES"
}

# --- Title & Description ---
st.set_page_config(page_title="Colabs 3 Concept Development and Naff Idea Generator", layout="centered")
st.title("Colabs 3 Concept Development and Naff Idea Generator")
st.markdown("""
This tool helps students generate creative writing loglines, cinematic opening scenes, and visual shot lists. Start with a random plot starter, then use AI to develop your story step by step!
""")

# --- Helper Functions ---
def get_api_key():
    return os.environ.get("AZURE_OPENAI_API_KEY")

def call_openai(messages=None, engine="o4-mini-colabs"):
    # Azure OpenAI settings
    api_key = get_api_key()
    if not api_key:
        return None, "Azure OpenAI API key not found. Please set AZURE_OPENAI_API_KEY in your environment."
    try:
        client = openai.AzureOpenAI(
            api_key=api_key,
            api_version="2025-01-01-preview",
            azure_endpoint="https://55147-mfqqttt7-eastus2.cognitiveservices.azure.com/"
        )
        # Use a very simple prompt for debugging
        if messages is None:
            messages = [{"role": "user", "content": "write me a logline for this story"}]
        response = client.chat.completions.create(
            model=engine,
            messages=messages,
            temperature=1,
            max_completion_tokens=1024
        )
        print("DEBUG API RESPONSE:", response)  # Debugging line
        # Defensive: check if choices and message exist
        if hasattr(response, 'choices') and response.choices and hasattr(response.choices[0], 'message'):
            return response.choices[0].message.content.strip(), None
        else:
            return None, "API returned no choices or message. Check model configuration."
    except Exception as e:
        return None, f"API error: {str(e)}"

# --- Plot Generator ---
st.header("Plot Generator (External Tool)")
import streamlit.components.v1 as components
components.iframe("https://writingexercises.co.uk/plotgenerator.php", height=900)

# --- Plot Summary Entry ---
st.header("Plot Summary")
plot_summary = st.text_area("Paste your plot summary here", value="", height=120)

# --- Generate Logline ---
st.header("Step 1: Generate Logline")
if st.button("Generate Logline"):
    messages = [{"role": "user", "content": f"write me a logline for this story: {plot_summary}"}]
    logline, error = call_openai(messages)
    if error:
        st.error(error)
    else:
        st.session_state.logline = logline
        st.session_state.editable_logline = logline
        st.success("Logline generated!")

# Editable logline box
if "editable_logline" in st.session_state:
    st.markdown("**Edit your logline before generating the opening scene:**")
    st.session_state.editable_logline = st.text_area("Logline", value=st.session_state.editable_logline, height=80)

# --- Generate Opening Scene ---
st.header("Step 2: Generate Opening Scene")
if st.button("Generate Opening Scene"):
    logline = st.session_state.get("editable_logline", "")
    if not logline:
        st.error("Please generate a logline first.")
    else:
        messages = [
            {"role": "system", "content": "You are a screenwriter assistant. Based on the logline, write a short summary of a cinematic opening scene that sets the tone and introduces the story."},
            {"role": "user", "content": logline}
        ]
        scene, error = call_openai(messages)
        if error:
            st.error(error)
        else:
            st.session_state.scene = scene
            st.success("Opening scene generated!")

if "scene" in st.session_state:
    st.markdown(f"**Opening Scene:**\n{st.session_state.scene}")

# --- Generate Justification ---
st.header("Step 3: Justification")
if st.button("Generate Justification"):
    scene = st.session_state.get("scene", "")
    if not scene:
        st.error("Please generate an opening scene first.")
    else:
        messages = [
            {"role": "system", "content": "You are a film studies expert. Justify the creative choices made in the following opening scene, referring to concepts in cinematic language and filmic storytelling. Keep the explanation simple and under 500 words."},
            {"role": "user", "content": scene}
        ]
        justification, error = call_openai(messages)
        if error:
            st.error(error)
        else:
            st.session_state.justification = justification
            st.success("Justification generated!")

if "justification" in st.session_state:
    st.markdown(f"**Justification:**\n{st.session_state.justification}")

st.markdown("---")
st.caption("No login required. All data is stored locally in your browser session. Powered by OpenAI.")
