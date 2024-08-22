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

      # Check for the termination keyword
      if "tanque" in recognized_text.lower():
        st.write("Tangki: 1")
      elif "bandeira" in recognized_text.lower():
        st.write("Bandera: 2")
        
      elif "lama" in recognized_text.lower():
        st.write("Lama: 3")
      
      elif "mar" in recognized_text.lower():
        st.write("Mar: 4")
      
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
st.markdown("<h3 style='font-size: 24px; font-weight: bold; color: #4682B4;'>Instructions:</h3>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 13px; color: #808080;'> Click the 'Start Recognition' button to start recording.</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 13px; color: #808080;'> Refresh the browser or press 'Stop' to stop the recording session.</p>", unsafe_allow_html=True)
st.markdown("<p style='font-size: 13px; color: #808080;'> With the Kristang words you have obtained in the hangman game, pronounce them to unlock the passcode..")

# Session state variable to control recognition loop
st.session_state.running = False

# Start recognition button
if st.button("Start Recognition"):
  st.session_state.running = True
  recognize_speech()

# Stop recognition button 
if st.button("Stop Recognition"):
  st.session_state.running = False
