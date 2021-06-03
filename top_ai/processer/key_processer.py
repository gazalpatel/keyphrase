import os, sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)

from top_ai.text_processer.cleaning import TextCleaner
class KeyProcesser:

    def __init__(self, subject_model="default", text_case="default"):

        # model for topic extraction, default regex parser
        self.subject_model = subject_model
        # case sentivity for topics and text processer, options: ["default", "lower", "upper", "capital"]
        self.text_case = text_case

    def process_text(self, texts, deselect_stop_words=[], stop_words_list=[],
                     accented_chars=True, contractions=True, text_to_number=True,
                     lemmatization=True, remove_extra_whitespace=True, remove_punctuations=True,
                     remove_html=True, remove_numbers=True, remove_special_characters=True,
                     remove_stop_words=True, remove_emoji=True, remove_url=True, para_delim="\n",
                     sentence_delim=". ", sentence_tokenizer="default"):

        tc = TextCleaner(self.text_case, deselect_stop_words, stop_words_list,
                        accented_chars, contractions, text_to_number, lemmatization,
                        remove_extra_whitespace, remove_punctuations, remove_html, remove_numbers,
                        remove_special_characters,
                        remove_stop_words, remove_emoji, remove_url, para_delim, sentence_delim, sentence_tokenizer)

        if para_delim:
            new_text = tc.page_preprocessing(texts)
        else:
            new_text = tc.para_preprocessing(texts)

        return new_text
