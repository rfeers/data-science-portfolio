from owlready2 import *
my_world = World()
onto = my_world.get_ontology( "..//NewOntology.owl" )
onto.load()



#a = onto.search(is_a = onto.Consulting_Room, RoomHasDoctor = onto["Maria_Garcia"])
#print('a:',a)
#b = str(a[0])
#c = b.split('.')[1]
#
#for prop in onto[c].get_properties():
#    for value in prop[onto[c]]:
#        print(".%s == %s" % (prop.python_name, value))
        
#a = onto.search(is_a = onto.Consulting_Room, IsLocatedIn = onto["Pediatrics"])
#print('answer:',a)
#
#a = onto.search(is_a = onto.Doctor, AttendsIn = onto["Room_111"])
#a = onto.search_one(is_a = onto.Area, Speciality='Pediatrics')
#doc = " Maria"
#doc = doc.strip()
#doctor = onto.search_one(Name = str(doc) );
#doctor = onto.search(is_a = onto.Doctor, Name = str(doc));
#cr = onto.search_one(is_a = onto.Consulting_Room, RoomHasDoctor = doctor)
#print('answer:',cr)
#
#spec = 'Pediatrics'
#res = onto.search(is_a = onto.Doctor, Speciality = spec);
#print(res)
#location = "entrance";
#loc = onto.search(is_a = onto.Space, Space_name = "Entrance")
#print(loc)

#x = ' Entrance'
#x=x.strip()
#res = onto.search(is_a = onto.Space, Space_name = x)
#print(res)


index = input("Write here your statement:") 
print(str(index))

#import spacy
#from spacy import displacy
#import pandas as pd
#from spacy.matcher import Matcher
#import numpy as np
#import marsutils as utils
#nlp = spacy.load("en_core_web_sm")
#text = 'Who is attending Traumatology?'
#doc = nlp(text)
#
## DOCTOR PATTERNS
#doctor_request_pattern = [{'LOWER':{'IN':['who','visits','visiting', 
#                                          'attends', 'attending','in']}},
#                          {'POS':'PROPN'}]
#
#doctor_request_pattern3 = [{'LOWER':{'IN':['who','visits','visiting', 
#                                          'attends', 'attending','in']}},
#                          {'POS':'NOUN'}]
#  
#  
#
#doctor_matcher = Matcher(nlp.vocab)
#doctor_matcher.add('Doctor', None, doctor_request_pattern)
#doctor_matcher.add('Doctor', None, doctor_request_pattern3)
#
#l = len(list(doctor_matcher(doc)))
#print(l)
#if l:
#    vec= list(doctor_matcher(doc))[0]
#    (start, end) = vec[1:]
#    key_word = doc[start:end]
#    intent_type = 'request_doctor'
#    print(key_word)




