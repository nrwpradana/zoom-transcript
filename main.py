import os
import streamlit as st
from dotenv import load_dotenv
import assemblyai as aai
from utils.zoom import ZoomClient

load_dotenv()

# Define the Streamlit app title
st.title("Transcribe Your Zoom Meeting")
st.text("Make Your Meeting Easy")

# Load environment variables
ZOOM_ACCOUNT_ID = st.text_input("Enter Zoom Account ID:")
ZOOM_CLIENT_ID = st.text_input("Enter Zoom Client ID:")
ZOOM_CLIENT_SECRET = st.text_input("Enter Zoom Client Secret:", type="password")
aai.settings.api_key = os.environ.get('077e55247d45442a8072380722f738bd')

# Create a Streamlit button to trigger the transcription process
if st.button("Transcribe Zoom Meeting"):
    # Initialize the Zoom client
    a = ZoomClient(account_id=ZOOM_ACCOUNT_ID, client_id=ZOOM_CLIENT_ID, client_secret=ZOOM_CLIENT_SECRET)

    # Get Zoom recordings
    recs = a.get_recordings()

    if recs['meetings']:
        rec_id = recs['meetings'][0]['id']
        my_url = a.get_download_url(rec_id)

        # Initialize the AssemblyAI transcriber
        transcriber = aai.Transcriber()

        # Perform transcription
        transcript = transcriber.transcribe(my_url)

        # Display the transcript on the Streamlit app
        st.header("Transcript:")
        st.text(transcript.text)

        # Save the transcript to a file
        with open('transcript.txt', 'w') as f:
            f.write(transcript.text)
    else:
        st.warning('No meetings to transcribe.')

# Add an optional file upload feature if you want users to upload their own recordings
uploaded_file = st.file_uploader("Or Upload Zoom Meeting Recording (MP4 or MP3)", type=["mp4", "mp3"])
if uploaded_file:
    # Perform transcription on the uploaded file
    st.header("Transcript for Uploaded Recording:")

    # You'll need to modify this part to transcribe the uploaded file
    # This could involve saving the file temporarily, passing its path to AssemblyAI, and displaying the transcript
    st.text("Transcription of the uploaded file goes here.")
