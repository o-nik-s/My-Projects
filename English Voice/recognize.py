import speech_recognition as sr
import difflib
import translators as ts
import translators.server as tss
from play_sound import play_word, play_words
# from recognize import recognize, translate, max_similarity


stop_words = ["стоп", "хватит", "надоело", "закончим", "закончить"]
repeat_words = ["повтори", "еще раз"]
correct_point = 0.95


def recognize():
    r = sr.Recognizer() 
    mic = sr.Microphone()
    with sr.Microphone() as source:
        print("Say translation!")
        audio = r.listen(source)
    voice = r.recognize_google(audio,  language='ru-RU', show_all=True)
    if len(voice)>0: recognize_lst = [el['transcript'] for el in voice['alternative']]
    else: recognize_lst = []
    print('Распознано:', recognize_lst)
    return recognize_lst

    
def translate(text:str, from_language:str, to_language:str):
    translate_set = list()
    translator_list = ['google', 'bing', 'deepl']
    for translator in translator_list:
        try: translate_set.append(ts.translate_text(text, translator=translator, from_language=from_language, to_language=to_language).lower())
        except: pass
    translate_set = set(translate_set)
    for transl in translate_set: 
        if len(transl.split())>1: translate_set | set(transl.split())
    print("Перевод:", set(translate_set))
    return set(translate_set)


def similarity(s1, s2):
        normalized1 = s1.lower()
        normalized2 = s2.lower()
        matcher = difflib.SequenceMatcher(None, normalized1, normalized2)
        return matcher.ratio()


def max_similarity(recognize_lst:list, translate_list:list):
    mx_similarity = 0
    for rec in recognize_lst:
        for transl in translate_list:
            mx_similarity = max(mx_similarity, similarity(rec, transl))
    return mx_similarity


def play_and_recognize(text:str, from_language:str):
    play_word(text, from_language)
    return recognize()    


def check_text(text:str, from_language:str, to_language:str):
    recognize_lst = play_and_recognize(text, from_language)
    while len(recognize_lst)==0: recognize_lst = play_and_recognize(text, from_language)
    while max_similarity(recognize_lst, repeat_words)>=correct_point: recognize_lst = play_and_recognize(text, from_language)
    if max_similarity(recognize_lst, stop_words)>correct_point: return -1
    translate_list = translate(text, from_language, to_language)
    mx_similarity = max_similarity(recognize_lst, translate_list)
    if mx_similarity>=correct_point and len(translate_list): pass # Здесь надо говорить: так же какие слова
    elif mx_similarity<correct_point: play_words(translate_list, to_language)
    return mx_similarity