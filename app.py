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
      recognized_text = result['text']

      keyword_digits = {
        "tanque": 1,
        "bandeira": 2,
        "lama": 3,
        "mar": 4
    }

    # Revealed digits
    revealed_digits = []
    # Check if the full password is revealed
    if len(password) == len(set(keyword_digits.values())):
      st.markdown("<p style='font-size: 13px; color: #808080;'> The complete passcode is: {password}</p>", unsafe_allow_html=True)
      
    # Check for keywords and reveal digits
    if recognized_text.lower() in keyword_digits:
        revealed_digits.append(keyword_digits[recognized_text.lower()])
        password = "".join(map(str, revealed_digits))
        st.markdown(f"<p style='font-size: 13px; color: #808080;'> Password revealed so far: {password}</p>", unsafe_allow_html=True)
    else:
      # Display recognized text in Streamlit
      st.write("Detected text: " , recognized_text)

      


  # Stop and close the stream
  stream.stop_stream()
  stream.close()

  # Terminate the PyAudio object
  p.terminate()

# Initialize Streamlit app
st.title("Speech Recognition")
st.markdown("---")
st.markdown("<p style='font-size: 13px; color: #808080;'> Click the 'Start Recognition' button to start recording.</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 13px; color: #808080;'> Refresh the browser or press 'Stop' to stop the recording session.</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 13px; color: #808080;'> With the Kristang words you have obtained in the hangman game, pronounce them to unlock the passcode..</p>",unsafe_allow_html=True)

# Session state variable to control recognition loop
st.session_state.running = False

# Start recognition button
if st.button("Start Recognition"):
  st.session_state.running = True
  recognize_speech()

# Stop recognition button 
if st.button("Stop Recognition"):
  st.session_state.running = False
