from bs4 import BeautifulSoup
import spacy
import unidecode
from word2number import w2n
import contractions
import re, nltk, string


class TextCleaner():

    def __init__(self, text_case="", deselect_stop_words=[],
                 accented_chars=True, contractions=True, text_to_number=True,
                 lemmatization=True, remove_extra_whitespace=True, remove_punctuations=True,
                 remove_html=True, remove_numbers=True, remove_special_characters=True,
                 remove_stop_words=True, remove_url=True, para_delim="\n",
                 sentence_delim=".", sentence_tokenizer="default"):

        """
        initiate variables:
        spacy model, vocab

        input:
        deselect_stop_words: list of stopwords (strings) to exclude words from spacy stopwords list
        """
        self.nlp = spacy.load('en_core_web_md')

        # deselect_stop_words = ['no', 'not']
        for w in deselect_stop_words:
            self.nlp.vocab[w].is_stop = False

        self.text_case = text_case
        self.accented_chars = accented_chars
        self.contractions = contractions
        self.text_to_number = text_to_number
        self.lemmatization = lemmatization
        self.remove_extra_whitespace = remove_extra_whitespace
        self.remove_punctuations = remove_punctuations
        self.remove_html = remove_html
        self.remove_numbers = remove_numbers
        self.remove_special_characters = remove_special_characters
        self.remove_stop_words = remove_stop_words
        self.remove_url = remove_url
        self.para_delim = para_delim
        self.sentence_delim = sentence_delim
        self.sentence_tokenizer = sentence_tokenizer

    def strip_html_tags(self, text):
        """remove html tags from text"""
        text = "<KPGENERATEDBODY>%s</KPGENERATEDBODY>" % (text)
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        return stripped_text

    def expand_contractions(self, text):
        """expand shortened words, e.g. don't to do not"""
        # CAREFUL: this will mess u.s.c to you.s.c.
        text = contractions.fix(text)
        return text

    def remove_whitespace(self, text):
        """remove extra whitespaces from text"""
        # text = text.strip()
        # return " ".join(text.split())
        text = re.sub(r' +', ' ', text)
        return text

    def remove_accented_chars(self, text):
        """remove accented characters from text, e.g. café"""
        text = unidecode.unidecode(text)
        return text

    def remove_urls(self, text):
        """remove url from the text """
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub(r'', text)

    def remove_empty_entries(self, text):
        if self.sentence_delim:
            # blank_sentence_regex = "[%s]{2,}" % (self.sentence_delim)
            # blank_sentence_regex = re.compile("[%s]{2,}" % (self.sentence_delim))
            # print(blank_sentence_regex)
            blank_sentence_regex = re.compile("[%s]{2,}" % (self.sentence_delim))
            text = re.sub(blank_sentence_regex, self.sentence_delim, text)
        
        return text

    def remove_punctuation(self, text):
        """custom function to remove the punctuation"""
        PUNCT_TO_REMOVE = string.punctuation
        text = text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))
        text = text.replace('“', "")
        text = text.replace("”", "")

        # sd = self.sentence_delim if self.sentence_delim else ""
        # punct_regex = '[^\w\s%s]' % (sd)
        # punct_regex = re.compile(punct_regex)
        # text = re.sub(punct_regex,text)
        return text

    def sentence_split(self, text):
        """ custom function to split text in multiple sentences """
        if type(self.sentence_tokenizer) == type("") and self.sentence_tokenizer == "default":
            return text.split(self.sentence_delim)
        else:
            return self.sentence_tokenizer(text)

    def text_casing(self, text):
        if self.text_case == "lower":
            return text.lower()
        if self.text_case == "upper":
            return text.upper()
        if self.text_case == "captial":
            return text.title()
        # default
        return text

    def sentence_preprocessing(self, sentence):
        doc = self.nlp(sentence)  # tokenise text

        clean_text = []

        for token in doc:
            flag = True
            edit = token.text

            # remove stop words
            if self.remove_stop_words == True and token.is_stop and token.pos_ != 'NUM':
                flag = False
            # remove punctuations
            # if punctuations == True and token.pos_ == 'PUNCT' and flag == True:
            #    flag = False
            # remove special characters
            if self.remove_special_characters == True and token.pos_ == 'SYM' and flag == True:
                flag = False
            # remove numbers
            if self.remove_numbers == True and (token.pos_ == 'NUM' or token.text.isnumeric()) \
                    and flag == True:
                flag = False
            # convert number words to numeric numbers
            if self.text_to_number == True and token.pos_ == 'NUM' and flag == True:
                edit = w2n.word_to_num(token.text)
            # convert tokens to base form
            elif self.lemmatization == True and token.lemma_ != "-PRON-" and flag == True:
                edit = token.lemma_
            # append tokens edited and not removed to list
            if edit != "" and flag == True:
                clean_text.append(edit)
        
        clean_text = " ".join(clean_text).strip()
        return clean_text


    def text_preprocessing(self, text):
        """preprocess text with default option set to true for all steps"""
        text = self.text_casing(text)  # convert all characters to lowercase
        text = self.remove_empty_entries(text)

        if self.remove_url:
            text = self.remove_urls(text)
        if self.remove_html:  # remove html tags
           text = self.strip_html_tags(text)
        if self.accented_chars:  # remove accented characters
            text = self.remove_accented_chars(text)
        if self.contractions:  # expand contractions
            text = self.expand_contractions(text)
        if self.remove_punctuations: # remove punctuations
            text = self.remove_punctuation(text)

        texts = self.sentence_split(text)

        output = []
        for i, t in enumerate(texts):
            if self.remove_extra_whitespace:  # remove extra whitespaces
                t = self.remove_whitespace(t)

            clean_text = self.sentence_preprocessing(t)
            output.append(clean_text)

        # self.sentence_delim = "%s " % (self.sentence_delim)
        output_text = self.sentence_delim.join(output)
        return output_text


    def para_preprocessing(self, text):
        """preprocess paragraph text with default option set to true for all steps"""

        # get list of paragraphs from page/text
        if type(text) == type(""):
            # for single page text
            pages = [text.split(self.para_delim)]
        else:
            if self.para_delim:
                # paragraphs from multiple page
                pages = [t.split(self.para_delim) for t in text]
            else:
                # paragraph list from one page
                pages = [list(text)]

        output_para = []
        for page in pages:
            output_lines = []
            for para in page:
                if para and para!="":
                    new_line = self.text_preprocessing(para)
                    if new_line and new_line!="":
                        output_lines.append(new_line)
            output_para.append(self.para_delim.join(output_lines))

        # if len(pages) == 1:
        #     return output_para[0]

        return output_para


if __name__ == '__main__':
    text = """I'd like to have three cups   of coffee<br /><br />from your Café in 15 u.s.c. section 45(a)(1) #delicious"""
    tc = TextCleaner(contractions=False)
    tc.text_preprocessing(text)