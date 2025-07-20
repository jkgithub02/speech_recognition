import streamlit as st
import vosk
import pyaudio
import json

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
        if rec.AcceptWaveform(data):  # Accept waveform of input voice
            # Parse the JSON result and get the recognized text
            result = json.loads(rec.Result())
            recognized_text = result['text'].lower()
            if any(keyword in recognized_text for keyword in ["obrigado", "bandeira", "noite", "mar"]):
              # Update the passcode based on recognized keywords
              if "obrigado" in recognized_text:
                st.session_state.passcode[0] = "0"
                st.write("Keyword detected: 'Obrigadu'")
              elif "bandeira" in recognized_text:
                st.session_state.passcode[1] = "1"
                st.write("Keyword detected: 'Bandera'")
              elif "noite" in recognized_text:
                st.session_state.passcode[2] = "1"
                st.write("Keyword detected: 'Noite'")
              elif "mar" in recognized_text:
                st.session_state.passcode[3] = "9"
                st.write("Keyword detected: 'Mar'")

              # Update the displayed passcode with the text 'Password'
              passcode_box.markdown(
                f"<div style='font-size: 24px; font-weight: bold; color: #4682B4;'>Password: {''.join(st.session_state.passcode)}</div>",
                unsafe_allow_html=True)
                
            else:
              # Display recognized text if none of the keywords are detected
              st.write("Detected text:", recognized_text)


    # Stop and close the stream
    stream.stop_stream()
    stream.close()

    # Terminate the PyAudio object
    p.terminate()

# Initialize Streamlit app
st.title("Speech Recognition")
st.markdown("---")
st.markdown("<h3 style='font-size: 24px; font-weight: bold; color: #4682B4;'>Tutorial:</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 15px; color: #808080;'>1. This program detects Kristang speech.<br>2. Click the 'Start Recognition' button to start the recording session.<br>3. Each Kristang word you have solved is assigned one digit to the passcode.<br>4. If other words than the keywords are detected, they will be also be shown.<br>5. Pronounce the Kristang keywords correctly to obtain the full passcode and unlock the treasure!</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 13px; color: #808080;'>Refresh the browser or press 'Stop' to stop the recording session.</p>", unsafe_allow_html=True)

# Session state variables
if 'running' not in st.session_state:
    st.session_state.running = False
if 'passcode' not in st.session_state:
    st.session_state.passcode = ["_", "_", "_", "_"]  # Placeholder for passcode digits

# Display the passcode box
passcode_box = st.empty()
passcode_box.markdown(
    f"<div style='font-size: 24px; font-weight: bold; color: #4682B4;'>Passcode: {''.join(st.session_state.passcode)}</div>",
    unsafe_allow_html=True
)

st.markdown("---")

# Start recognition button
if st.button("Start Recognition"):
    st.session_state.running = True
    recognize_speech()

