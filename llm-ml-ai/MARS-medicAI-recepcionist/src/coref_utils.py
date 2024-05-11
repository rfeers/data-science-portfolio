import numpy as np
import spacy
import neuralcoref

nlp = spacy.load("en_core_web_sm")
neuralcoref.add_to_pipe(nlp)

list_areas = ['radiology', 'oncology', 
              'emergency', 'pediatrics',
              'trauma', 'administration', 
              'traumatology','reception',
              'cardiology','Radiology', 'Oncology', 
              'Emergency', 'Pediatrics',
              'Trauma', 'Administration', 
              'Traumatology','Reception',
              'Cardiology']



def generate_new_sample(history):  
            
            
    final_sample = history[-1]
    final_text = final_sample.text
    substitute = None
    
    #Where is it?  --> Location
    if final_sample.pron_person == False:        
        search_area =  history[-3]        
        for l_a in list_areas:
            if l_a in search_area.text:
                substitute = l_a   
        final_text = final_text.replace('it', substitute)
        
        
    #Persons
    if final_sample.pron_person == True: 
        
        if 'Where' in final_text or 'where' in final_text or 'appointment' in final_text:
            
            sample_analisis = history[-3].text  + ' ' + history[-1].text 
            print(sample_analisis)
            doc1 = nlp(sample_analisis)
            print(doc1._.coref_clusters)
            sample = str(doc1._.coref_clusters)
            start = sample.find("[") + len("[")
            end = sample.find(":")
            noum = sample[start:end]
            start_target = sample.find(", ") + len(", ")
            end_target = sample.find("]]")
            target = sample[start_target:end_target]
            final_text = history[-1].text.replace(target, noum)
            print(noum)         
                    

        
    return final_text
      
    
    
    