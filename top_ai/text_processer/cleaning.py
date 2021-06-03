from bs4 import BeautifulSoup
import spacy
import unidecode
from word2number import w2n
import contractions
import re, string

import os, sys
p = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(p)
from top_ai.text_processer.text_operations import TextOperations


class TextCleaner():

    def __init__(self, text_case="", deselect_stop_words=[],stop_words_list=[],
                 accented_chars=True, expand_contractions=True, text_to_number=True,
                 lemmatization=True, remove_extra_whitespace=True, remove_punctuations=True,
                 remove_html=True, remove_numbers=True, remove_special_characters=True,
                 remove_stop_words=True, remove_emoji=True, remove_url=True, para_delim="\n",
                 sentence_delim=".", sentence_tokenizer="default"):

        """
        initiate variables:
        spacy model, vocab

        input:
        deselect_stop_words: list of stopwords (strings) to exclude words from spacy stopwords list
        """
        #spacy model
        self._to = TextOperations()
        # deselect_stop_words = ['no', 'not']
        for w in deselect_stop_words:
            self._to.nlp.vocab[w].is_stop = False

        self.text_case = text_case
        self.accented_chars = accented_chars
        self.expand_contractions = expand_contractions
        self.text_to_number = text_to_number
        self.lemmatization = lemmatization
        self.remove_extra_whitespace = remove_extra_whitespace
        self.remove_punctuations = remove_punctuations
        self.remove_html = remove_html
        self.remove_numbers = remove_numbers
        self.remove_special_characters = remove_special_characters
        self.remove_stop_words = remove_stop_words
        self.remove_emoji = remove_emoji
        self.remove_url = remove_url
        self.para_delim = para_delim
        self.sentence_delim = sentence_delim
        self.sentence_tokenizer = sentence_tokenizer
        self.stop_words_list = stop_words_list

    def _remove_html(self, text):
        """remove html tags from text"""
        text = "<KPGENERATEDBODY>%s</KPGENERATEDBODY>" % (text)
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        return stripped_text

    def _expand_contractions(self, text):
        """expand shortened words, e.g. don't to do not"""
        # CAREFUL: this will mess u.s.c to you.s.c.
        text = contractions.fix(text)
        return text

    def _remove_extra_whitespace(self, text):
        """remove extra whitespaces from text"""
        # text = text.strip()
        # return " ".join(text.split())
        text = re.sub(r' +', ' ', text)
        return text

    def _accented_chars(self, text):
        """remove accented characters from text, e.g. café"""
        text = unidecode.unidecode(text)
        return text

    def _remove_url(self, text):
        """remove url from the text """
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        text = url_pattern.sub(r'', text)

        # WEB_URL_REGEX = r"""(?i)\b((?:https?:(?:/{1,3}|[a-z0-9%])|[a-z0-9.\-]+[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)/)(?:[^\s()<>{}\[\]]+|\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\))+(?:\([^\s()]*?\([^\s()]+\)[^\s()]*?\)|\([^\s]+?\)|[^\s`!()\[\]{};:'".,<>?«»“”‘’])|(?:(?<!@)[a-z0-9]+(?:[.\-][a-z0-9]+)*[.](?:com|net|org|edu|gov|mil|aero|asia|biz|cat|coop|info|int|jobs|mobi|museum|name|post|pro|tel|travel|xxx|ac|ad|ae|af|ag|ai|al|am|an|ao|aq|ar|as|at|au|aw|ax|az|ba|bb|bd|be|bf|bg|bh|bi|bj|bm|bn|bo|br|bs|bt|bv|bw|by|bz|ca|cc|cd|cf|cg|ch|ci|ck|cl|cm|cn|co|cr|cs|cu|cv|cx|cy|cz|dd|de|dj|dk|dm|do|dz|ec|ee|eg|eh|er|es|et|eu|fi|fj|fk|fm|fo|fr|ga|gb|gd|ge|gf|gg|gh|gi|gl|gm|gn|gp|gq|gr|gs|gt|gu|gw|gy|hk|hm|hn|hr|ht|hu|id|ie|il|im|in|io|iq|ir|is|it|je|jm|jo|jp|ke|kg|kh|ki|km|kn|kp|kr|kw|ky|kz|la|lb|lc|li|lk|lr|ls|lt|lu|lv|ly|ma|mc|md|me|mg|mh|mk|ml|mm|mn|mo|mp|mq|mr|ms|mt|mu|mv|mw|mx|my|mz|na|nc|ne|nf|ng|ni|nl|no|np|nr|nu|nz|om|pa|pe|pf|pg|ph|pk|pl|pm|pn|pr|ps|pt|pw|py|qa|re|ro|rs|ru|rw|sa|sb|sc|sd|se|sg|sh|si|sj|Ja|sk|sl|sm|sn|so|sr|ss|st|su|sv|sx|sy|sz|tc|td|tf|tg|th|tj|tk|tl|tm|tn|to|tp|tr|tt|tv|tw|tz|ua|ug|uk|us|uy|uz|va|vc|ve|vg|vi|vn|vu|wf|ws|ye|yt|yu|za|zm|zw)\b/?(?!@)))"""
        # text = re.sub(WEB_URL_REGEX, 'FILLER_URL_FILLER', text)

        # remove email ids
        # text = re.sub(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\w", 'FILLER_EMAIL_FILLER', text)
        return text

    def _remove_empty_entries(self, text):
        """ removes multiple occurences of delimeter together"""
        if self.sentence_delim:
            # blank_sentence_regex = "[%s]{2,}" % (self.sentence_delim)
            # blank_sentence_regex = re.compile("[%s]{2,}" % (self.sentence_delim))
            # print(blank_sentence_regex)
            # blank_sentence_regex = re.compile("[%s]{2,}" % (self.sentence_delim))
            blank_sentence_regex = re.compile("[.]{2,}")
            text = re.sub(blank_sentence_regex, self.sentence_delim, text)

        return text

    def _remove_punctuations(self, text):
        """custom function to remove the punctuation"""
        PUNCT_TO_REMOVE = string.punctuation
        # logic to ignore ' in contracted words and braces for section nos.
        if self.expand_contractions == False:
            PUNCT_TO_REMOVE = PUNCT_TO_REMOVE.replace("'", "")
        text = text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))
        text = text.replace('“', "")
        text = text.replace("”", "")

        # sd = self.sentence_delim if self.sentence_delim else ""
        # punct_regex = '[^\w\s%s]' % (sd)
        # punct_regex = re.compile(punct_regex)
        # text = re.sub(punct_regex,text)
        return text

    def _remove_emoji(self, text):
        """
        cleans emoji unicodes from the text
        """
        emoji_pattern = re.compile("["
                                   u"\U0001F600-\U0001F64F"  # emoticons
                                   u"\U0001F300-\U0001F5FF"  # symbols & pictographs
                                   u"\U0001F680-\U0001F6FF"  # transport & map symbols
                                   u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
                                   u"\U00002500-\U00002BEF"  # chinese char
                                   u"\U00002702-\U000027B0"
                                   u"\U00002702-\U000027B0"
                                   u"\U000024C2-\U0001F251"
                                   u"\U0001f926-\U0001f937"
                                   u"\U00010000-\U0010ffff"
                                   u"\u2640-\u2642"
                                   u"\u2600-\u2B55"
                                   u"\u200d"
                                   u"\u23cf"
                                   u"\u23e9"
                                   u"\u231a"
                                   u"\ufe0f"  # dingbats
                                   u"\u3030"
                                   "]+", flags=re.UNICODE)
        text = emoji_pattern.sub(r'', text)
        return text

    def sentence_split(self, text):
        """ custom function to split text in multiple sentences """
        if type(self.sentence_tokenizer) == type("") and self.sentence_tokenizer == "default":
            return text.split(self.sentence_delim)
        else:
            return self.sentence_tokenizer(text)

    def sentence_preprocessing(self, sentence):
        token_info = self._to.get_token_info(sentence, get_ner=False, get_pos=True, get_lemma=True)

        clean_text = []

        for token_i in token_info:
            token = token_i.get("token")
            include_token = True
            edit = token.text

            # remove numbers
            if self.remove_numbers == True and (token.pos_ == 'NUM' or token.text.isnumeric()) \
                    and include_token == True:
                include_token = False

            # remove stop words
            if self.remove_stop_words == True:
                if token.is_stop and token.pos_ != 'NUM':
                    include_token = False
                elif token.text in self.stop_words_list:
                    include_token = False

            # remove punctuations
            # if punctuations == True and token.pos_ == 'PUNCT' and include_token == True:
            #    include_token = False

            # remove special characters
            if self.remove_special_characters == True and token.pos_ == 'SYM' and include_token == True:
                include_token = False

            # convert number words to numeric numbers
            if self.text_to_number == True and token.pos_ == 'NUM' and include_token == True:
                edit = w2n.word_to_num(token.text)

            # convert tokens to base form
            elif self.lemmatization == True and token.lemma_ != "-PRON-" and include_token == True:
                edit = token.lemma_

            # append tokens edited and not removed to list
            if edit != "" and include_token == True:
                clean_text.append(edit)

        clean_text = " ".join(clean_text).strip()
        return clean_text


    def para_preprocessing(self, text):
        """preprocess text with default option set to true for all steps"""

        text = self._to.change_text_case(text, self.text_case)  # convert all characters to lowercase

        # text = self._remove_empty_entries(text) # removes multiple occurences of sentence splitter together

        if self.remove_url:  # removes email ids and urls from text
            text = self._remove_url(text)

        if self.remove_html:  # remove html tags
            text = self._remove_html(text)

        if self.accented_chars:  # remove accented characters
            text = self._accented_chars(text)

        if self.expand_contractions:  # expand contractions, we're to we are
            text = self._expand_contractions(text)

        if self.remove_emoji:  # removes emoji unicodes
            text = self._remove_emoji(text)

        if self.remove_punctuations:  # remove punctuations
            text = self._remove_punctuations(text)

        texts = self.sentence_split(text)  # custom sentence splitting based on configuration

        output = []
        for i, t in enumerate(texts):
            if self.remove_extra_whitespace:  # remove extra whitespaces
                t = self._remove_extra_whitespace(t)

            # clean up sentence
            clean_text = self.sentence_preprocessing(t)
            output.append(clean_text)

        # self.sentence_delim = "%s " % (self.sentence_delim)
        output_text = self.sentence_delim.join(output)

        #computing the NER,POS-TAGS.
        return output_text


    def page_preprocessing(self, text):
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

        output_page = []

        for page in pages:
            output_para = []

            for para in page:
                if para and para != "":
                    new_line = self.para_preprocessing(para)
                    if new_line and new_line != "":
                        output_para.append(new_line)

            output_page.append(self.para_delim.join(output_para))

        # if len(pages) == 1:
        #     return output_para[0]

        return output_page


if __name__ == '__main__':
    text = """I'd like to have three cups   of coffee<br /><br />from your Café in 15 u.s.c. section 45(a)(1) #delicious"""
    tc = TextCleaner(expand_contractions=False)
    tc.para_preprocessing(text)