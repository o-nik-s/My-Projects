import os, time
from gtts import gTTS
from pygame import mixer

def play_word(text, lang):
    name = f'Words/{lang}/{text}.mp3'
    if not os.path.isfile(name):
        tts = gTTS(text, lang=lang)
        tts.save(name)
    mixer.music.load(name)
    mixer.music.play()
    # mixer.quit()

def play_words(word_lst:set, language:str):
    for word in word_lst: 
        play_word(word, language)
        time.sleep(2)