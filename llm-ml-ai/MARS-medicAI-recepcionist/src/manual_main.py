# -*- coding: utf-8 -*-
import data_analyzer as DA
import dialog_manager as DM
import dialog_generator as DG
import speech_recognition as sr
import numpy as np
import spacy
nlp = spacy.load("en_core_web_sm")
# FOLLOWING THE PIPELINE
# 1. USER INPUT

##             1. request_location, 2.request_consulting_room, 3. request_doctor, 
##             4. request_waiting,  5. request_appointment

sentences_request_location =    ['Where is the area?',
                                 'I want to know where doctor Maria Garcia visits in Pediatrics',  
                                 'Where is doctor Maria Garcia in Pediatrics?',  
                                 'Where is doctor Pen Miller in Pediatrics?',
                                 'I want to know where doctor Helena visits in Oncology',
                                 'Where is oncology?',
                                 'Where is Pediatrics?',
                                 'Where is the emergency?',
                                 'Where is Helena Garcia?',
                                 'Where is Juan?',
                                 'Where is Pen Miller',
                                 'Where is the Elevator?',
                                 'Where is the Entrance?'
                                 ] 

#vec = str(np.arange(len(sentences_request_location)));
#index = input("Input in " + vec + ":") # start form 0
#
#print(sentences_request_location[int(index)])
#sample = sentences_request_location[int(index)]


sentences_request_doctor =       [
                                  'Who is attending Area?',
                                  'Who is visiting Pediatrics?', 
                                  'Who is attending Pediatrics?',
                                  'Who is attending Oncology?',
                                  'Who is attending Traumatology?',
                                  'Who is attending Radiology?', 
                                  'Who is attending Emergency?',
                                  'Who is visiting Cardiology?'
                                  #'Does Maria attends in Pediatrics?',
                                  ]

# vec = str(np.arange(len(sentences_request_doctor)));
# index = input("Input in " + vec + ":") # start form 0

# print(sentences_request_doctor[int(index)])
# sample = sentences_request_doctor[int(index)]


sentences_request_waiting =      ['How much waiting time there is in Area?',
                                  'How much waiting time there is in Pediatrics?',
                                  'How much waiting time has Oncology?',
                                  'How much waiting time has Traumatology?',
                                  'How much waiting time has Oncology?',
                                  'How much waiting time there is in Radiology?'
                                  ]

# vec = str(np.arange(len(sentences_request_waiting)));
# index = input("Input in " + vec + ":") # start form 0

# print(sentences_request_waiting[int(index)])
# sample = sentences_request_waiting[int(index)]


sentences_request_consulting =   ['Where is the room?',
                                  'Where is the room 111?',
                                  'Where I can find the room 111',
                                  'Where is the consulting office 221',
                                  'Where I can find the consulting office 112'
                                  ]

# vec = str(np.arange(len(sentences_request_consulting)));
# index = input("Input in " + vec + ":") # start form 0

# print(sentences_request_consulting[int(index)])
# sample = sentences_request_consulting[int(index)]


sentences_request_appointment =   ['Jason',
                                   'I have an appointment',
                                   'I would like to make an appointment with Pediatrics', 
                                   'I would like to make an appointment with docor Pen Miller', 
                                   'Where is Oncology?'
                                  ]

vec = str(np.arange(len(sentences_request_appointment)));
index = input("Input in " + vec + ":") # start form 0
print(sentences_request_appointment[int(index)])
sample = sentences_request_appointment[int(index)]


# 2. DIALOG ACT DETECTION
dialog_act = DA.DAParser(nlp)
# 3. & 4. INTENT BUILDER
intent_builder = DA.IntentBuilder(nlp)
# 5. DIALOG MANAGER
dialog_manager = DM.DialogManager()

type_ = dialog_act.compute_DA(sample)
# print('Dialog Act: ',type_)

# intent = intent_builder.compute_intent(sample)
# if intent.i_type == 'invalid':
#     final_text = dialog_manager.unknownResponseByType('invalid')
#     print('__________________________________________________________')
#     print(final_text)
# else:
#     print('Dialogue Act: ',dialog_act.current_DA)
#     intent.pretty_print()
    
#     # create dialog manages (auto print the results, that should be modified to
#     # return the response and print it afterwards but not a problem rn)
    
#     response = dialog_manager.processQuery(intent, intent_builder.lack_info)
#     print('____________________________________________________')
#     response.pretty_print()
#     if response.status == 'success':
#         dialog_generator = DG.DialogGenerator()
#         sent_text = dialog_generator.generateSentenceByType(response.data['request_type'], response)
#     else: 
#         sent_text = response.baked_sent
#     print('__________________________________________________________')
#     print(sent_text)
# r = sr.Recognizer()
# text = ''
listener = sr.Recognizer()
while(1):
    with sr.Microphone() as source:
        print("Speak :")
        audio = listener.listen(source)
        try:
            text = listener.recognize_google(audio)
            print(text)
            type_ = dialog_act.compute_DA(text)
            print("You said : {}".format(text))
            print('Dialog Act: ',type_)

        except:
            print("Sorry could not recognize what you said")
            