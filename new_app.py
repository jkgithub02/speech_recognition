import streamlit as st
import vosk
import pyaudio
import json
import numpy as np
import noisereduce as nr

def recognize_speech():
    """Performs speech recognition using Vosk and displays the recognized text in Streamlit."""
    # Obtain the model
    model = vosk.Model(lang="pt")

    # Create the recognizer with a sample rate of 16000 Hz
    rec = vosk.KaldiRecognizer(model, 16000)

    # Enable microphone stream
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8192)

    # Start streaming and recognize speech
    while st.session_state.running:
        data = stream.read(4096)  # Read in chunks of 4096 bytes
        
        # Convert data to numpy array for noise reduction
        audio_data = np.frombuffer(data, dtype=np.int16)
        
        # Apply noise reduction
        reduced_noise_data = nr.reduce_noise(y=audio_data, sr=16000)

        # Convert reduced noise data back to bytes
        reduced_noise_data_bytes = reduced_noise_data.tobytes()
        
        # Feed the processed data into recognizer
        if rec.AcceptWaveform(reduced_noise_data_bytes):
            result = json.loads(rec.Result())
            recognized_text = result['text'].lower()

            # Apply filtering based on confidence if present
            if result.get('confidence', 1.0) >= 0.7:
                if any(keyword in recognized_text for keyword in ["obrigado", "casa", "noite", "amor"]):
                    # Update the passcode based on recognized keywords
                    if "obrigado" in recognized_text:
                        st.session_state.passcode[0] = "0"
                        st.write("<span style='color: green;'>Keyword detected: 'Obrigado'</span>", unsafe_allow_html=True)
                    elif "casa" in recognized_text:
                        st.session_state.passcode[1] = "1"
                        st.write("<span style='color: blue;'>Keyword detected: 'Kaza'</span>", unsafe_allow_html=True)
                    elif "noite" in recognized_text:
                        st.session_state.passcode[2] = "1"
                        st.write("<span style='color: purple;'>Keyword detected: 'Noite'</span>", unsafe_allow_html=True)
                    elif "amor" in recognized_text:
                        st.session_state.passcode[3] = "9"
                        st.write("<span style='color: teal;'>Keyword detected: 'Amor'</span>", unsafe_allow_html=True)

                    # Update passcode and progress bar
                    passcode_box.markdown(
                        f"<div style='font-size: 24px; font-weight: bold; color: #4682B4;'>Password: {''.join(st.session_state.passcode)}</div>",
                        unsafe_allow_html=True
                    )
                    #progress_bar.progress(st.session_state.passcode.count("_") / 4)
                else:
                    st.write(f"<span style='color: red;'>Detected text: {recognized_text}</span>", unsafe_allow_html=True)
            else:
                st.write(f"<span style='color: orange;'>Low confidence recognition ignored.</span>", unsafe_allow_html=True)

    # Stop and close the stream
    stream.stop_stream()
    stream.close()
    p.terminate()

# Initialize Streamlit app
st.set_page_config(page_title="Kristang Speech Recognition", layout="centered", initial_sidebar_state="collapsed")
st.title("Kristang Speech Recognition")
st.markdown("<hr style='border: 1px solid #4682B4;'>", unsafe_allow_html=True)

st.markdown(
    """
    <h3 style='font-size: 24px; font-weight: bold; color: #4682B4;'>Tutorial:</h3>
    <p style='font-size: 15px; color: #808080;'>
    1. Click 'Start Recognition' to start the session.<br>
    2. Kristang words will unlock digits to the passcode.<br>
    3. If no keywords are detected, the full sentence will still be shown.<br>
    4. Unlock the full passcode to reveal the treasure!
    </p>
    """, unsafe_allow_html=True
)
st.markdown("<p style='font-size: 13px; color: #808080;'>Press 'Stop' to stop the session.</p>", unsafe_allow_html=True)

# Session state variables
if 'running' not in st.session_state:
    st.session_state.running = False
if 'passcode' not in st.session_state:
    st.session_state.passcode = ["_", "_", "_", "_"]

# Display passcode and progress bar
passcode_box = st.empty()
passcode_box.markdown(
    f"<div style='font-size: 24px; font-weight: bold; color: #4682B4;'>Passcode: {''.join(st.session_state.passcode)}</div>",
    unsafe_allow_html=True
)

#progress_bar = st.progress(st.session_state.passcode.count("_") / 4)

st.markdown("<hr style='border: 1px solid #4682B4;'>", unsafe_allow_html=True)

# Start button
if st.button("Start Recognition", key="start"):
    st.session_state.running = True
    recognize_speech()


# Additional UI customizations
st.markdown(
    """
    <style>
    div.stButton > button:first-child {
        background-color: #4682B4;
        color: white;
        border-radius: 8px;
        padding: 10px 20px;
    }
    div.stButton > button:hover {
        background-color: #5a9bd5;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True
)
