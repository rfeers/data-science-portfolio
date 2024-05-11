#We import what we need
import data_analyzer as DA
import dialog_manager as DM
import dialog_history as DH
import dialog_generator as DG
import numpy as np
import spacy
import coref_utils
import speech_recognition as sr

#import pyttsx3
nlp = spacy.load("en_core_web_sm")
# 2. DIALOG ACT DETECTION
dialog_act = DA.DAParser(nlp)
# 3. & 4. INTENT BUILDER
intent_builder = DA.IntentBuilder(nlp)
# 5. DIALOG MANAGER
dialog_manager = DM.DialogManager()

#History
history = [];

# Toggle comment to allow speech recognition

#engine = pyttsx3.init()
#voices = engine.getProperty('voices')
#engine.setProperty('voice', voices[1].id)   # 0 for male voice
#rate = engine.getProperty('rate')           # getting details of current speaking rate
#print (rate)                                # printing current voice rate
# engine.setProperty('rate', 225)           # setting up new voice rate (200 by default)


it = 0;
user_sample_vec = []; DM_sample_vec = []; total_sample_vec = [];
sample_DM = 'Hello. How may I help you?';
print('DM Says: ' + sample_DM);
DM_sample_vec.append(sample_DM); total_sample_vec.append(sample_DM);

history.append(DH.History_Element('MARS','Greeting', sample_DM))
dialog_generator = DG.DialogGenerator()


    
while dialog_act.current_DA != 'farewell': 
    
    # Toggle comment to allow speech recognition
    
    # text = None
    # listener = sr.Recognizer()
    # with sr.Microphone() as source:
    #     print("Speak :")
    #     audio = listener.listen(source)
    #     try:
    #         text = listener.recognize_google(audio)
    #         print(text)
    #         type_ = dialog_act.compute_DA(text)
    #         print("You said : {}".format(text))
    #         print('Dialog Act: ',type_)
         
    #     except:
    #         print("Sorry could not recognize what you said")
    sample = input("Write here your statement:") 
    #sample = text 
    print(sample)
    user_sample_vec.append(sample); total_sample_vec.append(sample);    
    type_ = dialog_act.compute_DA(sample)
    history.append(DH.History_Element('User',type_, sample)) #Store what user says
    
    history[-1].find_pronoum()
    if(history[-1].has_pron):
       sample = functions.generate_new_sample(history)
    
    history[-1].text = sample
    print(sample)
    #Diferenciamos por diferente tipo de Dialogue_Act
    if dialog_act.current_DA == 'greeting':
        
        sample_DM = 'Good Morning! Do you need any help?';
       # engine.say(sample_DM)
       # engine.runAndWait()
        print('DM Says: ' + sample_DM);
        DM_sample_vec.append(sample_DM); total_sample_vec.append(sample_DM);
        history.append(DH.History_Element('MARS','greeting', sample_DM))
        
    elif dialog_act.current_DA == 'farewell':
        
        sample_DM = 'Thank you so much for your time! Have a nice day :)'
        print('DM Says: ' + sample_DM);
       # engine.say(sample_DM)
       # engine.runAndWait()
        DM_sample_vec.append(sample_DM); total_sample_vec.append(sample_DM)
        history.append(DH.History_Element('MARS','farewell', sample_DM))
        
    elif dialog_act.current_DA == 'thanks':
        
        sample_DM = 'It is all my pleasure! Do you need any help more?';
        print('DM Says: ' + sample_DM);
       # engine.say(sample_DM)
       # engine.runAndWait()
        DM_sample_vec.append(sample_DM); total_sample_vec.append(sample_DM)
        history.append(DH.History_Element('MARS','Thanks', sample_DM))
    
    elif dialog_act.current_DA == 'question' or 'statement':

        
        intent = intent_builder.compute_intent(sample)
        if intent.i_type == '':
            answer = dialog_manager.unknownResponseByType('invalid')
            print('__________________________________________________________')
            print(answer)
            continue
       
        intent.pretty_print()
        
        response = dialog_manager.processQuery(intent, intent_builder.lack_info)
        print('____________________________________________________')
        response.pretty_print()
        # print('STATUS: ',response.status)
        if response.status == 'success':
            dialog_generator = DG.DialogGenerator()
            sent_text = dialog_generator.generateSentenceByType(response.data['request_type'], response)
            print(sent_text)
         #   engine.say(sent_text)
         #  engine.runAndWait()

        else: 
            sent_text = response.baked_sent
            print('__________________________________________________________')
            print(sent_text)
         #   engine.say(sent_text)
         #   engine.runAndWait()
        
        #Diferenciamos con cada intent type el tipo de respuesta que deberemos dar.
        t = intent.i_type;
        history.append(DH.History_Element('MARS','answer to ' + t, 'dialog_flow_data'))
        
    
    else:  
        sample_DM = 'Sorry. I dont understand you. Can you say it again?';
        print('DM Says: ' + sample_DM);
        DM_sample_vec.append(sample_DM); total_sample_vec.append(sample_DM);
        
        sample = input("Write here your statement:") 
        user_sample_vec.append(sample); total_sample_vec.append(sample);
        

print('Total: ', total_sample_vec)
print('User: ', user_sample_vec)
print('DM: ', DM_sample_vec)

print('HISTORY DIALOG')
for dialog in history:
    print(dialog.speaker + ': ' + dialog.text + '----->Type:' + dialog.D_type)

        
    