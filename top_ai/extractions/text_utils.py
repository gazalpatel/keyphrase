import itertools, re, string, inflect, nltk
from top_ai.text_processer.text_operations import TextOperations
from top_ai.text_processer.cleaning import TextCleaner


class KeyphraseUtility():

    def __init__(self):
        self.inflect_engine = inflect.engine()
        self.stop_words = set(nltk.corpus.stopwords.words('english'))
        self.punct = set(string.punctuation)
        self.sno = nltk.stem.SnowballStemmer('english')


    def get_candidate_phrases(self, text, grammar=r'KT: {(<JJ>* <NN.*>+ <IN>)? <JJ>* <NN.*>+|(<VB.*>+<DT>*)+<NN.*>+}',
                            drop_single_words=True,
                            return_stemmed_words=False):

        chunker = nltk.chunk.regexp.RegexpParser(grammar)
        tagged_sents = [TextOperations(TextCleaner().nlp, get_ner=False, get_pos_tags=TextCleaner().get_pos_tags)._get_token_info(sent)[0] for sent in nltk.sent_tokenize(text)]

        all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                        for tagged_sent in tagged_sents))
        candidates = [' '.join(word for word, pos, chunk in group)
                    for key, group in itertools.groupby(all_chunks, lambda x: x[2] != 'O') if key]

        candidates = [cand.lower() for cand in candidates
                    if cand not in self.stop_words and not all(char in self.punct for char in cand) and len(cand) > 2]
        candidates = [self.strip_stop_words(phrase) for phrase in candidates]
        if drop_single_words:
            candidates = [candidate for candidate in candidates if len(candidate.split(' ')) > 1]
        if return_stemmed_words:
            candidates = [self.get_stemmed_phrase(token) for token in candidates]
        candidates = [candidate for candidate in candidates if len(candidate) > 1]
        return list(set(candidates))


    def get_noun_tokens(self, text, grammar=r'nw: {<NN.*>{1}}', drop_single_words=False, return_stemmed_words=False):
        chunker = nltk.chunk.regexp.RegexpParser(grammar)
        tagged_sents = [TextOperations(TextCleaner().nlp, get_ner=False, get_pos_tags=TextCleaner().get_pos_tags)._get_token_info(sent)[0] for sent in nltk.sent_tokenize(text)]
        all_chunks = list(itertools.chain.from_iterable(nltk.chunk.tree2conlltags(chunker.parse(tagged_sent))
                                                        for tagged_sent in tagged_sents))
        candidates = [' '.join(word for word, pos, chunk in group)
                    for key, group in itertools.groupby(all_chunks, lambda x: x[2] != 'O') if key]

        candidates = [cand.lower() for cand in candidates
                    if cand not in self.stop_words and not all(char in self.punct for char in cand) and len(cand) > 2]
        candidates = [self.strip_stop_words(phrase) for phrase in candidates]
        if drop_single_words:
            candidates = [candidate for candidate in candidates if len(candidate.split(' ')) > 1]
        if return_stemmed_words:
            candidates = [self.get_stemmed_phrase(token) for token in candidates]
        candidates = list(itertools.chain(*[candidate.strip().split(' ') for candidate in candidates]))
        candidates = [candidate for candidate in candidates if len(candidate) > 1]
        return list(set(candidates))


    def get_pos_tags(self, text):
        tagged_sents = nltk.pos_tag_sents(nltk.word_tokenize(sent) for sent in nltk.sent_tokenize(text))
        return tagged_sents


    def preprocess_text(self, text):
        text = re.sub(r"\r\n+", ". ", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\t+", " ", text)
        text = re.sub('@\w*\d*', '', text)
        text = re.sub(' +', ' ', text)
        text = text.strip()
        #text = self.remove_emoji(text)
        return text


    def filter_plurals(self, kp_list):
        drop_list = []
        for phrase in kp_list:
            if phrase + 's' in kp_list:
                drop_list.append(phrase + 's')
            if phrase + 'es' in kp_list:
                drop_list.append(phrase + 'es')
        return list(set(kp_list) - set(drop_list))


    def strip_stop_words(self, text):
        text_list = text.split()
        while text_list != [] and text_list[0].lower() in self.stop_words:
            text_list.pop(0)
        while text_list != [] and text_list[-1].lower() in self.stop_words:
            text_list.pop(-1)
        return ' '.join(text_list)


    def get_stemmed_phrase(self, phrase):
        phrase_list = [self.sno.stem(tok) for tok in phrase.split(" ")]
        return ' '.join(phrase_list)


    def drop_stop_words(self, text):
        if type(text) == str:
            text_toks = text.split(' ')
            text_toks = [tok for tok in text_toks if tok not in self.stop_words]
            return ' '.join(text_toks)
        return


    def get_phrase_subtexts(self, phrase):
        if type(phrase) == str:
            max_threshold = len(self.drop_stop_words(phrase).split(' ')) - 1
            master_list = []
            if max_threshold >= 2:
                for len_ in range(2, max_threshold + 1):
                    phrase_word_list = phrase.split(' ')
                    phrase_stubs = [phrase_word_list[i:i + len_]
                                    for i in range(len(phrase_word_list) - (len_ - 1))]
                    phrase_stubs = [' '.join(ele) for ele in phrase_stubs]
                    master_list.extend(phrase_stubs)
                master_list.append(phrase)
                return master_list
        return list([phrase])


    def get_phrase_variations(self, phrase_list):
        phrase_variations = []
        for phrase in phrase_list:
            singular_form = self.inflect_engine.singular_noun(phrase.split(' ')[-1])
            plural_form = self.inflect_engine.plural_noun(phrase.split(' ')[-1])
            if singular_form:
                new_phrase = ' '.join(phrase.split(' ')[:-1]) + ' ' + singular_form
                phrase_variations.append(new_phrase.strip())
            if plural_form:
                new_phrase = ' '.join(phrase.split(' ')[:-1]) + ' ' + plural_form
                phrase_variations.append(new_phrase.strip())
        return list(set(phrase_list + phrase_variations))