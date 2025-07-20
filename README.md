# Kristang Speech Recognition Treasure Hunt

A gamified two-part application that combines word games and speech recognition to unlock a treasure chest passcode. This project uses Streamlit to create interactive web applications for learning and recognizing Kristang (a Portuguese-based creole language), part of Stories of the Praya Lane exhibition held in Malacca, September 2024.

## 🎮 Game Overview

This treasure hunt consists of two connected applications:

1. **Hangman Game** ([`hangman_app.py`](hangman_app.py)) - Discover the Kristang words
2. **Speech Recognition** ([`speech_app.py`](speech_app.py)) - Speak the words to unlock the treasure

### Game Flow
1. Play hangman to learn 4 Kristang words: **amor** (love), **obrigadu** (thank you), **kaza** (house), **noite** (night)
2. Use the discovered words in the speech recognition app
3. Speaking each word correctly unlocks one digit of a 4-digit passcode
4. Complete the passcode to unlock the treasure chest! 🏆

## 🚀 Quick Start

### Option 1: Using Dev Container (Recommended)
1. Open in VS Code with Dev Containers extension
2. Select "Reopen in Container"
3. The app will automatically start at `http://localhost:8501`

### Option 2: Manual Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Run the hangman game first
streamlit run hangman_app.py

# Then run the speech recognition
streamlit run speech_app.py
```

## 📋 Requirements

- Python 3.11+
- Streamlit
- Vosk (Portuguese speech recognition model)
- PyAudio (microphone access)

See [`requirements.txt`](requirements.txt) for complete dependency list.

## 🎯 How to Play

### Step 1: Hangman Game
- Guess letters to reveal 4 hidden Kristang words
- You have 6 lives to discover all words
- **Hint**: Kristang is derived from Portuguese!

### Step 2: Speech Recognition
- Click "Start Recognition" to begin listening
- Pronounce the Kristang words you learned:
  - **obrigadu** → unlocks digit `0`
  - **bandera** → unlocks digit `1` 
  - **noite** → unlocks digit `1`
  - **mar** → unlocks digit `9`
- Complete passcode: `0119` 🔓

## 🌍 About Kristang

Kristang is a Portuguese-based creole language spoken by the Kristang people, primarily in Malaysia and Singapore. This application helps preserve and teach this unique language through interactive gaming.

## 🛠️ Technical Details

- **Frontend**: Streamlit web applications
- **Speech Recognition**: Vosk with Portuguese language model
- **Audio Processing**: PyAudio for real-time microphone input
- **Deployment**: Configured for GitHub Codespaces with dev containers

## 📝 Files

- `hangman_app.py` - Word discovery game
- `speech_app.py` - Speech recognition challenge  
- `requirements.txt` - Python dependencies
- `.devcontainer/` - Container configuration for easy deployment

---

*Part of a gamified language learning event focusing on