from spacy.matcher import Matcher
import spacy

nlp = spacy.load("en_core_web_sm")
pron_matcher = Matcher(nlp.vocab)
pron_loc_matcher = Matcher(nlp.vocab)

pron_pattern = [{'LOWER':{'IN':['she','he','him','her']}}] 
pron_pattern_loc = [{'LOWER':{'IN':['it']}}] 

pron_matcher.add("pronoum", None, pron_pattern)
pron_loc_matcher.add("pronoum_loc", None, pron_pattern_loc)

class History_Element():
    def __init__(self, speaker, D_type, text):
        self.speaker = speaker
        self.D_type = D_type
        self.text = text
        self.pron_person = None
        self.has_pron = False
    
    def find_pronoum(self):
        doc = nlp(self.text)
        if len(list(pron_matcher(doc))):
            vec= list(pron_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.has_pron  = True
            self.pron_person = True
        if len(list(pron_loc_matcher(doc))):
            vec= list(pron_loc_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.has_pron  = True
            self.pron_person = False
        