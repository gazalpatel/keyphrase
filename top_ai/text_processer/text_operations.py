import nltk
import spacy

class TextOperations():

    def __init__(self):
        #load spacy model
        self.nlp = spacy.load('en_core_web_md')

    def change_text_case(self, text, text_case=""):
        """changing the text case to expected text case"""
        if text_case == "lower":
            return text.lower()
        if text_case == "upper":
            return text.upper()
        if text_case == "captial":
            return text.title()
        # default
        return text

    def get_token_info(self, sentence, get_ner=True, get_pos=True, get_lemma=True):
        '''
        :param sentence: sentence
        :return: list of tokens with POS, NER tags.
        '''
        tokens = self.nlp(sentence)
        tags = []
        entities = [str(ent) for ent in tokens.ents]
        for i, tok in enumerate(tokens):
            #token_info = [{'tok':tok}]
            t_info = {'token':tok, 'index':i}
            t_info["is_stopword"] = tok.is_stop

            if get_lemma:
                t_info["lemma"] = tok.lemma_
            if get_pos:
                pos = tok.tag_
                #token_info.append({"pos": pos})
                t_info["pos"] = pos
            if get_ner:
                if tok.text in entities:
                    ner = (entities[entities.index(tok.text)], str(spacy.explain(entities[entities.index(tok.text)])))
                    #token_info.append({"ner": ner})
                else:
                    #token_info.append({"ner":''})
                    ner = ""
                t_info["ner"] = ner
            tags.append(t_info)
        return tags
