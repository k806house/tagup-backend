from difflib import SequenceMatcher

import numpy as np
import pandas as pd
import spacy
from gensim.models import Word2Vec
from gensim.models.phrases import Phrases
from gensim.utils import tokenize
from spellchecker import SpellChecker
from transliterate import translit

MODEL_PATH = 'models/word2vec_clean5.model'
SIMILARITY_THRESHOLD = 0.8


class TagGenerator:
    def __init__(self, model_path):
        self.model = Word2Vec.load(model_path)
        self.spell_checker = SpellChecker(language='ru')
        self.nlp = spacy.load("ru_core_news_md")

    def generate(self, query):
        print("Initialized")
        similar = self.__try_find_similar(query)
        extended = self.__try_predict_next(query)
        return similar, extended

    def __try_find_similar(self, query):
        # print([token.similarity(self.nlp('айфон')) for token in self.nlp('iphone стиралка обувь брюки самсунг samsung')])
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
                if match in used_matches:
                    continue
                match = self.spell_checker.correction(match)
                if match in used_matches:
                    continue

                similarity = SequenceMatcher(a=noun, b=match).ratio()
                if similarity >= SIMILARITY_THRESHOLD:
                    continue

                used_matches.add(match)
                proposals.append((match, semantic_similarity))

        return proposals

    def __try_predict_next(self, query):
        tokenized = list(tokenize(self.spell_checker.correction(str(query).lower())))
        used = set()
        proposals = []
        for nxt, confidence in self.model.predict_output_word(tokenized):
            if nxt in used:
                continue
            nxt = self.spell_checker.correction(nxt)
            if nxt in used:
                continue

            used.add(nxt)
            proposals.append((f'{query} {nxt}', confidence))
        return proposals


if __name__ == '__main__':
    tg = TagGenerator(MODEL_PATH)

    print(tg.generate('ботинки красные осенние'))
