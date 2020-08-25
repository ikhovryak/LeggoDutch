import nltk
nltk.download('wordnet')
from nltk.corpus import wordnet as wn
import re

def if_food(word):

    syns = wn.synsets(str(word), pos = wn.NOUN)

    for syn in syns:
        if any(c in syn.lexname() for c in ('food', 'breakfast', 'dinner', 'lunch', 'brunch', 'meal')):
            print(syn)
            return 1

    return 0

def line_food(line: list):

    for box in line:

        words = box.split(' ')
        
        for word in words:
            if '/' in word:
                words.extend(re.split(r'\/', word))
        # splash = re.split(r'\/', word) for word in words if '/' in word
        # if splash:
        #     words = words.extend(splash)
        print(words, '---', line)

        for word in words:
            if if_food(word):
                return True

    return False

if __name__ == "__main__":

    print(line_food(['34-35 Green Street']))