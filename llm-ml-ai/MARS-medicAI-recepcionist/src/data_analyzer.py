# -*- coding: utf-8 -*-
import spacy
from spacy import displacy
import pandas as pd
from spacy.matcher import Matcher
import numpy as np
import marsutils as utils
nlp = spacy.load("en_core_web_sm")

# Class which identifies the act of the input sentence
class DAParser:
    def __init__(self, nlp):
        self.current_DA = 'greeting'
        self.matchers = []
        self.greeting_matcher = Matcher(nlp.vocab)
        self.farewell_matcher = Matcher(nlp.vocab)
        self.thanks_matcher = Matcher(nlp.vocab)
      
        greeting_pattern_1 = [{'LOWER':{'IN':['hello','hi']}}]
        greeting_pattern_2 = [{'LOWER':'good'},
                              {'LOWER':{'IN':['morning', 'afternoon', 
                                              'evening', 'night']}}]
        farewell_pattern = [{'LOWER':{'IN':['bye','goodbye', 'ciao']}}]
        farewell_pattern2 = [{'LOWER':'good'}, 
                             {'LOWER': 'bye'}]
        thanks_pattern = [{'LOWER':{'IN':['thanks','perfect','thank']}}]
      
        self.greeting_matcher.add("greeting", None, greeting_pattern_1)
        self.greeting_matcher.add("greeting_2", None, greeting_pattern_2)
        self.farewell_matcher.add("farewell", None, farewell_pattern)
        self.farewell_matcher.add("farewell2", None, farewell_pattern2)
        self.thanks_matcher.add("thanks", None, thanks_pattern)
    
    
    def compute_DA(self, text):
        doc = nlp(text)
        if len(list(self.greeting_matcher(doc))):
            vec= list(self.greeting_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.current_DA = 'greeting'
      
        elif len(list(self.farewell_matcher(doc))):
            vec= list(self.farewell_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.current_DA = 'farewell'
      
        elif len(list(self.thanks_matcher(doc))):
            vec= list(self.thanks_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.current_DA = 'thanks'
      
        else:
            if '?' in text:
                self.current_DA = 'question'
            else:
                self.current_DA = 'statement'
        
        return self.current_DA

# Class wich determines the intention of the user sentence 
# i.e. request_location, request_doctor...
class Intent:
    def __init__(self, intent_type = '', attrib = {}):
    
        self.i_type = intent_type
        self.attributes = attrib
    
    def pretty_print(self):
        print('Intent type: ',self.i_type)
        print('Attrib: ',list(self.attributes.values()))
    
    def set_attrib(self, name, value):
        self.attributes[name] = value
    
    def set_attribs(self, object_):
        self.attributes = object_
    
    def get_attrib(self, name):
        return self.attributes[name]

class IntentBuilder:
    
    def __init__(self, nlp):
        self.intent_type = ''
        self.lack_info = False
        self.current_intent = Intent()
        self.appointment_matcher = Matcher(nlp.vocab)
        self.area_matcher = Matcher(nlp.vocab)
        self.consulting_matcher = Matcher(nlp.vocab)
        self.doctor_matcher = Matcher(nlp.vocab)
        self.doctor_name_matcher = Matcher(nlp.vocab)
        self.waiting_matcher = Matcher(nlp.vocab)
        self.area_name_matcher = Matcher(nlp.vocab)
        self.location_name_matcher = Matcher(nlp.vocab)
        self.emergency_matcher = Matcher(nlp.vocab)
        self.room_code_matcher = Matcher(nlp.vocab)
      
        #We define the different intent patterns
        request_appointment_pattern = [{'LOWER':{'IN':['appointment']}}]
      
        # DOCTOR PATTERNS
        doctor_request_pattern = [{'LOWER':{'IN':['who','visits','visiting', 
                                                  'attends', 'attending','in']}},
                                  {'POS':'PROPN'}]
      
        doctor_request_pattern2 = [{'LOWER':{'IN':['who','visits','visiting', 
                                             'attends', 'attending','in']}},
                                   {'POS':'NOUN'}]
        # LOCATION PATTERNS
        location_pattern1 = [{'LEMMA':'where'}, 
                             {'POS':'DET', 'OP':'?'},
                             {'POS':'NOUN'}, 
                             {'LOWER':{'IN':['is', 'visits', 'attends']}}]
                                  
        # Example: Where does (doctor) Valls attend?
        # Example 2: I want to know where doctor Valls attends
        location_pattern2 = [{'LOWER':'where'}, 
                             {'POS':'AUX', 'OP':'?'},
                             {'LOWER':{'IN':['doctor']}, 'OP':'?'}, 
                             {'POS':'PROPN'}]
        
        #Example:  Where is the Oncology Area?
        location_pattern3 = [{'LOWER':'where'}, 
                             {'LOWER':{'IN':['is', 'are']}}]
        
        # REQUEST_CONSULTING
        consulting_pattern1 =  [{'LOWER':{'IN':['room','office','consulting']}}]
        
        #What is Dr. Garcia consulting room?
        
        consulting_pattern2 =  [{'LEMMA':'what'}, 
                                  {'POS':'DET', 'OP':'?'},
                                  {'POS':'NOUN'}, 
                                  {'LOWER':{'IN':['is', 'room', 'office',
                                                  'number','consulting']}}]
        consulting_code_pattern = [{'LOWER':{'IN':['101','102','103','104','105',
                                                   '111','112','113','201','202',
                                                   '221','222','223','301','302']}}]
      
        # WAITING LIST PATTERNS
        waiting_pattern = [{'LOWER':'how'}, 
                           {'LOWER': 'many'}]
        
        waiting_pattern2 = [{'LOWER':'waiting'}, 
                           {'LOWER': {'IN':['time', 'list']}, 'OP':'?'}]
        
        # EMERGENCY VISIT PATTERN
        emergency_pattern1 = [{'LOWER':{'IN':['emergency', 'urgent']}}]
      
        area_name_pattern = [{'LOWER':{'IN':['radiology', 'oncology', 
                                             'emergency', 'pediatrics',
                                             'trauma', 'administration', 
                                             'traumatology','reception',
                                             'cardiology']}}]
        
        location_name_pattern = [{'LOWER':{'IN':['stairs', 'elevator', 
                                                   'vending', 'machine',
                                                   'cafeteria','entrance']}}]
    
        doctor_name_pattern = [{'LOWER':'doctor', 'OP':'?'}, 
                               {'POS':'PROPN'}, 
                               {'POS':'PROPN', 'OP':'?'}]
        
    
    
#        doctor_name_pattern = [{'LOWER':'doctor', 'OP':'?'}, 
#                               {'POS':'PROPN'}, 
#                               {'POS':'PROPN', 'OP':'?'}]
        
        #The patterns are included to the different matchers
                              
        self.appointment_matcher.add("Appointment",None, 
                                     request_appointment_pattern)
      
        self.area_matcher.add("Area1", None, location_pattern1)
        self.area_matcher.add("Area2", None, location_pattern2)
        self.area_matcher.add("Area3", None, location_pattern3)
      
        self.consulting_matcher.add("Location1", None, consulting_pattern1)
        self.consulting_matcher.add("Location2", None, consulting_pattern2)
        self.room_code_matcher.add("Location2", None, consulting_code_pattern)
      
        self.doctor_matcher.add('Doctor', None, doctor_request_pattern)
        self.doctor_matcher.add('Doctor', None, doctor_request_pattern2)
      
        self.waiting_matcher.add('Waiting', None, waiting_pattern)
        self.waiting_matcher.add('Waiting2', None, waiting_pattern2)
      
        self.emergency_matcher.add('Emergency', None, emergency_pattern1)
        
        self.area_name_matcher.add('AreaName', None, area_name_pattern)
        self.location_name_matcher.add('AreaName', None, location_name_pattern)
        self.doctor_name_matcher.add('DoctorName', None, doctor_name_pattern)
    
    ##INTENTS: 1. request_location, 2.request_consulting_room, 3. request_doctor, 
    ##         4. request_waiting 5. request_appointment
    
    # dado un texto, pasarlo por los filtros para saber cual cumple y poner el
    # tipo de intent al que corresponde
    # Al final de la funcion se llama al get_ifo... que es el que devuelve el 
    # intent en si
    def compute_intent(self,text):
        doc = nlp(text)
        if len(list(self.area_matcher(doc))):
          vec= list(self.area_matcher(doc))[0]
          (start, end) = vec[1:]
          
          if len(self.consulting_matcher(doc)):
             vec= list(self.area_matcher(doc))[0]
             (start, end) = vec[1:]
             self.intent_type = 'request_consulting_room'
          else:
             # key_word = doc[start:end]
             self.intent_type = 'request_location'
        
        elif len(list(self.consulting_matcher(doc))):
            vec= list(self.consulting_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.intent_type = 'request_consulting_room'
        
        elif len(list(self.waiting_matcher(doc))):
            vec= list(self.waiting_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.intent_type = 'request_waiting'
            
        elif len(list(self.appointment_matcher(doc))):
            vec= list(self.appointment_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.intent_type = 'request_appointment'
          
        elif len(list(self.doctor_matcher(doc))):
            vec= list(self.doctor_matcher(doc))[0]
            (start, end) = vec[1:]
            # key_word = doc[start:end]
            self.intent_type = 'request_doctor'

      
     
        
      

          
        self.get_info_from_type(text, doc)
        # print(self.current_intent.i_type)
        return self.current_intent
    
    
    def get_info_from_type(self, text, doc):
        
        # print(self.intent_type)
        # Start assuming user will give all the info
        self.lack_info = False
        
        # Build request location intent ***************************************
        if self.intent_type == 'request_location':
            # print('Intent: request_location')
            area = 'unknown'
            doctor = 'unknown'
            location_name = 'unknown'
            # If there is some area in the request sentence
            if len(list(self.area_name_matcher(doc))):
                vec= list(self.area_name_matcher(doc))[0]
                (start, end) = vec[1:]
                area = doc[start:end]
            # Refer to some doctor as 'doctos Xavi Mir' or 'Xavi Mir' or 'Mir
            if len(list(self.doctor_name_matcher(doc))):
                vec= list(self.doctor_name_matcher(doc))[0]
                (start, end) = vec[1:]
                doctor = doc[start:end]
            # if it refers to some place in the hospital
            if len(list(self.location_name_matcher(doc))):
                vec= list(self.location_name_matcher(doc))[0]
                (start, end) = vec[1:]
                location_name = doc[start:end]
            
            if str(doctor) == str(area):
                doctor = 'unknown'
            
            if str(doctor) == str(location_name):
                doctor = 'unknown'
                
            
            # delete the word 'doctor': unnecesary for the query
            d = 'doctor'
            doctor = str(doctor)
            
            if d in doctor:
                doctor = doctor.replace('doctor', '')
                # print('Area: ',str(area))
                # print('Doc: ',str(doctor))
            
            # create the intent object
            if str(area) == 'unknown' and str(doctor) == 'unknown' and str(location_name) == 'unknown':
                self.lack_info = True
            attributes = {'speciality':   area, 
                          'doctor_name':  doctor,
                          'Place_to_go': location_name}
            
            if len(list(self.consulting_matcher(doc))):
                self.current_intent.i_type = 'request_consulting_room'
                vec= list(self.consulting_matcher(doc))[0]
                (start, end) = vec[1:]
                area = doc[start:end]
                
                code = 'unknown'
                if len(list(self.room_code_matcher(doc))):
                    vec= list(self.room_code_matcher(doc))[0]
                    (start, end) = vec[1:]
                    code = doc[start:end]
                
                attributes = {'speciality':area, 
                             'doctor_name':doctor,
                             'Place_to_go:':location_name,
                             'Room_code':code}
                
            else:
                self.current_intent.i_type = 'request_location'
            self.current_intent.set_attribs(attributes) 
          
        # Build request consulting room intent ********************************      
        if self.intent_type == 'request_consulting_room':
            # print('Intent: request_consulting_room')
            area = 'unknown'
            doctor = 'unknown'
            code = 'unknown'
            # day = 'unknonw' --> When we know how to deal with it
            # If there is some area in the request sentence
            if len(list(self.area_name_matcher(doc))):
                vec= list(self.area_name_matcher(doc))[0]
                (start, end) = vec[1:]
                area = doc[start:end]
              
            # Refer to some doctor as 'doctos Xavi Mir' or 'Xavi Mir' or 'Mir
            if len(list(self.doctor_name_matcher(doc))):
                vec= list(self.doctor_name_matcher(doc))[0]
                (start, end) = vec[1:]
                doctor = doc[start:end]
            
            if len(list(self.room_code_matcher(doc))):
                vec= list(self.room_code_matcher(doc))[0]
                (start, end) = vec[1:]
                code = doc[start:end]
          
#            if d in doctor:
#                doctor = doctor.replace('doctor', '')
#            # print('Area: ',str(area))
#            print('Doc: ',str(doctor))
            
            # If there is no info, set lack_info true to know in the DM that  
            # has to ask for more info 

            vec = list(self.consulting_matcher(doc))[0]
            (start, end) = vec[1:]
            location = doc[start:end]
            
            # create the intent object
            if str(code) == 'unknown' and str(doctor) == 'unknown' and str(location) == 'room': 
                self.lack_info = True
            attributes = {'location':   location, 
                          'doctor_name':  doctor,
                          'Room_code': code}
            
                
            self.current_intent.i_type = 'request_consulting_room'
            self.current_intent.set_attribs(attributes) 
      
      
      
        # Build request_doctor intent *****************************************
        if self.intent_type == 'request_doctor':
            # print('Intent: request_doctor')
            area = 'unknown'
            doctor = 'unknown'
            # day = 'unknonw' --> When we know how to deal with it
            # If there is some area in the request sentence
            if len(list(self.area_name_matcher(doc))):
                vec= list(self.area_name_matcher(doc))[0]
                (start, end) = vec[1:]
                area = doc[start:end]
                
            if len(list(self.doctor_name_matcher(doc))):
                vec= list(self.doctor_name_matcher(doc))[0]
                (start, end) = vec[1:]
                doctor = doc[start:end]
                
            if str(doctor) == str(area):
                doctor = 'unknown'

            
            # If there is no info, set lack_info true to know in the DM that  
            # has to ask for more info 
            if str(area) == 'unknown' and str(doctor) == 'unknown':
                self.lack_info = True
            attributes = {'speciality': area,
                          'doctor_name': doctor}
            self.current_intent.i_type = 'request_doctor'
            self.current_intent.set_attribs(attributes) 
          
        # Build request waiting time intent ***********************************
        if self.intent_type == 'request_waiting':
            # print('Intent: request_waiting')
            # If there is some time in the request sentence
            area = 'unknown'
            if len(list(self.area_name_matcher(doc))):
                vec= list(self.area_name_matcher(doc))[0]
                (start, end) = vec[1:]
                area = doc[start:end]
            # If there is no info, set lack_info true to know in the DM that 
            # has to ask for more info 
            if str(area) == 'unknown':
                self.lack_info = True
            attributes = {'speciality': area }
            self.current_intent.i_type = 'request_waiting'
            self.current_intent.set_attribs(attributes) 
          
        # Build request appointment time intent *******************************
        if self.intent_type == 'request_appointment':
            # print('Intent: request_waiting')
            # If there is some time in the request sentence
            area = 'unknown'
            doctor = 'unknown'
            if len(list(self.area_name_matcher(doc))):
                vec= list(self.area_name_matcher(doc))[0]
                (start, end) = vec[1:]
                area = doc[start:end]
              
            if len(list(self.doctor_name_matcher(doc))):
                vec= list(self.doctor_name_matcher(doc))[0]
                (start, end) = vec[1:]
                doctor = doc[start:end]
            
            if str(doctor) == str(area):
                doctor = 'unknown'
                
            # If there is no info, set lack_info true to know in the DM that 
            # has to ask for more info 

            if str(doctor) =='unknown' and str(area) =='unknown':
                self.lack_info = True

            attributes = {'area': area, 
                          'doctor':doctor}

            self.current_intent.i_type = 'request_appointment'
            self.current_intent.set_attribs(attributes) 





        



