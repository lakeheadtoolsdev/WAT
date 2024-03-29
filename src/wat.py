import paraphraser
import models
import frequency
import directphrase
import similarity
import string
import regex as re
from sentence_splitter import SentenceSplitter, split_text_into_sentences

class WAT():

    def __init__(self):
        self.splitter = SentenceSplitter(language='en')
        self.model = models.Model()
        # self.parapharser = paraphraser.Parapharser()
        self.freq = frequency.Frequency(self.model)
        self.direct_phrase = directphrase.DirectPhrase()
        self.similarity = similarity.Similarity(self.model)

    def search(self, text, sub):
        match = re.search(r"[\W_]*".join(sub), text, flags=re.IGNORECASE)
        return match and match.span(0)

    def analyse(self, given_paragraph, user_paragraph):
        sentence_list = self.splitter.split(given_paragraph)
        directphrase, full_sentences = self.direct_phrase.direct_phrase(sentence_list, user_paragraph)
        bold_text, frequent_words = self.freq.get_frequency(user_paragraph)
        lexical_sim, semantic_sim = self.similarity.get_similarity_index(given_paragraph, user_paragraph)
        lexical_similarity = lexical_sim.item() * 100
        lexical_similarity = round(lexical_similarity, 2)
        context_similarity = semantic_sim.item() * 100
        context_similarity = round(context_similarity, 2)
        freq_words = {}

        if len(frequent_words) > 0:
            for x in frequent_words:
                word = x[0]
                freq = x[1]
                freq_words[word] = freq
        else:
            word = "No frequent words found"
            freq = ""
            freq_words[word] = freq

        # sort freq_words by value
        freq_words = sorted(freq_words.items(),
                            key=lambda x: x[1], reverse=True)

        serialised_freq_words = {}
        for x in freq_words:
                word = x[0]
                freq = x[1]
                serialised_freq_words[word] = freq

        # for phrase in directphrase:    
        #     span = self.search(bold_text, phrase)
        #     if span:
        #         start, end = span
        #         bold_text = bold_text[:start] + '<u>' +bold_text[start:]
        #         bold_text = bold_text[:end+3] + '</u>' + bold_text[end+3:]
        #         print(start, end)
        #         print(bold_text[start:end])

        # print(bold_text)
        return bold_text, serialised_freq_words, directphrase, lexical_similarity, context_similarity, full_sentences