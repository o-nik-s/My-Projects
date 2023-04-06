import pandas as pd
import random
from pygame import mixer
from calculate import calculate_p
from recognize import check_text


from_language, to_language = 'en', 'ru'

name = "English words.csv"

error_point = 0.75
error_random = 3


def choice_word(data, error_list:list):
    if random.randint(1, error_random) == error_random and len(error_list)>0:
        word = error_list[random.randint(0, len(error_list)-1)]
    else:
        rnd = random.randint(0, data.iloc[-1, :].sumP)
        word = data[data.sumP<=rnd].iloc[-1, :][0]
    print(word)
    return word


def main():

    data = pd.read_csv(name, sep=';', index_col=False)
    data = calculate_p(data)
    
    mixer.init()
    
    reslt_dict = dict()
    error_list = list()

    mx_similarity = 1
    while mx_similarity>=0:
        word = choice_word(data, error_list)
        mx_similarity = check_text(word, from_language, to_language)
        if mx_similarity<error_point: error_list.append(word)
        print("Сходство:", mx_similarity)


if __name__ == '__main__':
    main()