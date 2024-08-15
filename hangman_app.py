import streamlit as st
import random

words = ["mar", "lama", "tangki", "bandera"]

# Initialize or reset session state for new games
if "word_list" not in st.session_state:
    st.session_state.word_list = {word: set(word) for word in words}
    st.session_state.alphabet = set('abcdefghijklmnopqrstuvwxyz')
    st.session_state.used_letters = set()
    st.session_state.lives = 6
    st.session_state.user_letter = ""

# Function to reset the game
def reset_game():
    st.session_state.word_list = {word: set(word) for word in words}
    st.session_state.used_letters = set()
    st.session_state.lives = 6
    st.session_state.user_letter = ""

# Display the current game status
st.title("Kristang Hangman")
st.write("1. 4 Kristang words are hidden, play a game of hangman to discover them and unlock the treasure!\n2. You have 6 lives, type a letter in the text box and double click the button to submit your guess!\n3. A wrong guess will result in one life gone, good luck!\n")

if st.session_state.lives > 0 and any(word_letters for word_letters in st.session_state.word_list.values()):
    st.write(f'You have {st.session_state.lives} lives left.')
    st.write('Used letters:', ' '.join(st.session_state.used_letters))
    
    for word in words:
        word_display = [letter if letter in st.session_state.used_letters else '_' for letter in word]
        st.write(' '.join(word_display))
    
    # Input for guessing a letter
    user_letter = st.text_input("Guess a letter:", max_chars=1).lower()
    if st.button("Submit Guess"):
        if user_letter:
            if user_letter in st.session_state.alphabet - st.session_state.used_letters:
                st.session_state.used_letters.add(user_letter)
                found_letter = False
                
                for word, word_letters in st.session_state.word_list.items():
                    if user_letter in word_letters:
                        word_letters.remove(user_letter)
                        found_letter = True

                if not found_letter:
                    st.session_state.lives -= 1
                    st.write('Letter is not in any word.')

            elif user_letter in st.session_state.used_letters:
                st.write('You have already used that letter.')
            else:
                st.write('That is not a valid letter.')

else:
    if st.session_state.lives == 0:
        st.write('You died, sorry.')
    else:
        st.write('You guessed all the words!', ', '.join(words))
    if st.button("Play Again"):
        reset_game()
