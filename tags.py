import sys
from difflib import SequenceMatcher
from functools import lru_cache

import numpy as np
import pandas as pd
import spacy
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases
from gensim.utils import tokenize
from spellchecker import SpellChecker
from transliterate import translit

MODEL_PATH = 'models/word2vec_clean5.model'
SIMILARITY_THRESHOLD = 0.75
SEMANTIC_SIMILARITY_THRESHOLD = 0.7


def contains_fuzzy(s, q):
    for val in s:
        if are_similar(val, q):
            return True
    return False


def are_similar(a, b):
    similarity = SequenceMatcher(a=a, b=b).ratio()
    return similarity >= SIMILARITY_THRESHOLD


class TagGenerator:
    def __init__(self, model_path):
        self.model = Word2Vec.load(model_path)
        self.spell_checker = SpellChecker(language='ru')
        self.nlp = spacy.load("ru_core_news_md")
        print("Initialized")

    def generate(self, query):
        try:
            similar = self.__try_find_similar(query)
        except:
            similar = []

        try:
            extended = self.__try_predict_next(query)
        except:
            extended = []

        return similar, extended

    def __try_find_similar(self, query):
        doc = self.nlp(query)
        nouns = []
        for token in doc:
            if token.pos_ == 'NOUN':
                nouns.append(token.text)
        print(nouns)

        proposals = []
        for noun in nouns:
            used_matches = set()
            for match, semantic_similarity in self.model.wv.most_similar(noun):
                match = self.__spell_check(match)
                # match = self.nlp(match)[0].lemma_
                if semantic_similarity < SEMANTIC_SIMILARITY_THRESHOLD \
                or are_similar(noun, match) \
                or contains_fuzzy(used_matches, match):
                    continue

                used_matches.add(match)
                proposals.append((match, semantic_similarity))

        return proposals

    def __try_predict_next(self, query):
        tokenized = list(tokenize(self.__spell_check(str(query).lower())))
        used = set()
        proposals = []
        for nxt, confidence in self.model.predict_output_word(tokenized):
            nxt = self.__spell_check(nxt)
            if contains_fuzzy(tokenized, nxt) or contains_fuzzy(used, nxt):
                continue

            used.add(nxt)
            proposals.append((f'{query} {nxt}', confidence))
        return proposals

    def __spell_check(self, text):
        return text
        # its buggy and slow so goodbye
        return self.spell_checker.correction(text)


if __name__ == '__main__':
    tg = TagGenerator(MODEL_PATH)

    for line in sys.stdin:
        print(tg.generate(line.strip()))
