from bs4 import BeautifulSoup
import spacy
import unidecode
from word2number import w2n
import contractions
import re, nltk, string


class TextCleaner():

    def __init__(self, deselect_stop_words=[]):
        """
        initiate variables: 
        spacy model, vocab

        input:
        deselect_stop_words: list of stopwords (strings) to exclude words from spacy stopwords list
        """
        self.nlp = spacy.load('en_core_web_md')
        
        #deselect_stop_words = ['no', 'not']
        for w in deselect_stop_words:
            self.nlp.vocab[w].is_stop = False


    def strip_html_tags(self, text):
        """remove html tags from text"""
        text = "<GENERATEDBODY>" + text + "</GENERATEDBODY>"
        soup = BeautifulSoup(text, "html.parser")
        stripped_text = soup.get_text(separator=" ")
        return stripped_text


    def remove_whitespace(self, text):
        """remove extra whitespaces from text"""
        #text = text.strip()
        #return " ".join(text.split())
        text = re.sub(' +', ' ', text)
        return text


    def remove_accented_chars(self, text):
        """remove accented characters from text, e.g. café"""
        text = unidecode.unidecode(text)
        return text


    def expand_contractions(self, text):
        """expand shortened words, e.g. don't to do not"""
        # CAREFUL: this will mess u.s.c to you.s.c.
        text = contractions.fix(text)
        return text


    def remove_urls(self, text):
        """remove url from the text """
        url_pattern = re.compile(r'https?://\S+|www\.\S+')
        return url_pattern.sub(r'', text)


    def remove_punctuation(self, text):
        """custom function to remove the punctuation"""
        PUNCT_TO_REMOVE = string.punctuation
        text = text.translate(str.maketrans('', '', PUNCT_TO_REMOVE))
        text = text.replace('“', "")
        text = text.replace("”","")
        return text


    def para_preprocessing(self, text, accented_chars=True, contractions=True, 
                        convert_num=True, extra_whitespace=True, 
                        lemmatization=True, lowercase=True, punctuations=True,
                        remove_html=True, remove_num=True, special_chars=True, 
                        stop_words=True, remove_url=True, para_delim = "\n"):
        
        """preprocess paragraph text with default option set to true for all steps"""
        lines = text.split(para_delim)
        output_lines = []
        for line in lines:
            new_line = self.text_preprocessing(self, text, accented_chars, contractions, convert_num, 
                            extra_whitespace, lemmatization, lowercase, punctuations,
                            remove_html, remove_num, special_chars, 
                            stop_words, remove_url)
            output_lines.append(new_line)
        
        output_para = para_delim.join(output_lines)
        return output_para
        

    def text_preprocessing(self, text, accented_chars=True, contractions=True, 
                        convert_num=True, extra_whitespace=True, 
                        lemmatization=True, lowercase=True, punctuations=True,
                        remove_html=True, remove_num=True, special_chars=True, 
                        stop_words=True, remove_url=True):
        
        """preprocess text with default option set to true for all steps"""
        if remove_html == True: #remove html tags
            text = self.strip_html_tags(text)
        if extra_whitespace == True: #remove extra whitespaces
            text = self.remove_whitespace(text)
        if accented_chars == True: #remove accented characters
            text = self.remove_accented_chars(text)
        if contractions == True: #expand contractions
            text = self.expand_contractions(text)
        if lowercase == True: #convert all characters to lowercase
            text = text.lower()
        if remove_url == True:
            text = self.remove_urls(text)
        
        text = re.sub('[.]{2,}', '.', text)
        texts = nltk.sent_tokenize(text)
        
        output_text = ""
        for i, t in enumerate(texts):
            if punctuations == True:
                t = self.remove_punctuation(t)
            
            doc = self.nlp(t) #tokenise text

            clean_text = []

            for token in doc:
                flag = True
                edit = token.text
                print(edit)
                # remove stop words
                if stop_words == True and token.is_stop and token.pos_ != 'NUM': 
                    flag = False
                # remove punctuations
                #if punctuations == True and token.pos_ == 'PUNCT' and flag == True: 
                #    flag = False
                # remove special characters
                if special_chars == True and token.pos_ == 'SYM' and flag == True: 
                    flag = False
                # remove numbers
                if remove_num == True and (token.pos_ == 'NUM' or token.text.isnumeric()) \
                and flag == True:
                    flag = False
                # convert number words to numeric numbers
                if convert_num == True and token.pos_ == 'NUM' and flag == True:
                    edit = w2n.word_to_num(token.text)
                # convert tokens to base form
                elif lemmatization == True and token.lemma_ != "-PRON-" and flag == True:
                    edit = token.lemma_
                # append tokens edited and not removed to list 
                if edit != "" and flag == True:
                    clean_text.append(edit)    
            
            if(i==0):
                output_text = " ".join(clean_text)
            else:
                output_text = output_text + ". " + " ".join(clean_text)
            
        return output_text


if __name__ == '__main__':
    text = """I'd like to have three cups   of coffee<br /><br />from your Café in 15 u.s.c. section 45(a)(1) #delicious"""
    tc = TextCleaner()
    tc.text_preprocessing(text, contractions=False) 