from aitextgen import aitextgen

from random import shuffle
from nltk.corpus import wordnet as word_net
from syllapy import count

from math import inf

exceptions = ["in", "a", "the"]

ai = aitextgen(model_folder="trained_model")

def generate_haiku(base = ""):
    score, final_haiku = inf, None
    haiku_raw = ai.generate(prompt = base, return_as_list = True, temperature = 1.0)[0].split("\n")
    for i in range(3, len(haiku_raw) - (len(haiku_raw) % 3)):
        haiku = optimize_accuracy(haiku_raw[i-3:i])
        if isinstance(haiku, list): return haiku
        if isinstance(haiku, set):
            if haiku[0] < score: score, final_haiku = haiku[0], haiku[1]
    return "\n".join(haiku)

def optimize_accuracy(haiku):
    final_haiku, score = [], 0
    for i in range(len(haiku)): #loop through lines
        expected_length = ((i % 2) * 2) + 5
        cur_haiku = "".join([x for x in haiku[i] if x.isalpha() or x == " "]) # remove unneaded characters
        words = cur_haiku.split(" ") # get individual words
        
        length = sum([count(word) for word in words])
        if length != expected_length:
            index_list = list(range(len(words)))
            for x in range(5):
                shuffle(index_list)
                for index in index_list:
                    word = words[index]
                    if word in exceptions: continue
                    base_len, synonyms = count(word), word_net.synsets(word)
                    for syn in synonyms:
                        new_word = syn.lemmas()[0].name()
                        new_len = count("".join([" " if i == "_" else i for i in new_word]))
                        
                        if abs(((length - base_len) + new_len) - expected_length) < abs(length - expected_length):
                            words[index] = new_word
                            length = length - base_len + new_len
                            base_len = new_len

            original_words = haiku[i].split(" ")
            for index in range(len(original_words)):
                trail = ""
                for c in range(len(original_words[index]) - 1, 0, -1):
                    if original_words[index][c].isalpha(): break
                    trail = trail + original_words[index][c]
                words[index] = words[index] + trail[::-1]

        for w in range(len(words)): words[w] = "".join([" " if i == "_" else i for i in words[w]])
        final_haiku.append(" ".join(words))

        score += abs(expected_length - count("".join(words)))
    if score != 0: return (score, final_haiku)
    return final_haiku
