# -*- coding: utf-8 -*-
from owlready2 import *
import numpy as np
import random

# Es como un objeto, pero lo hago clase para que ya tenga las propiedades 
# que queremos y sea más bonito y organizado
class Response:
    def __init__(self):
        self.asked = ''
        self.data = {}
        self.status = ''
        self.baked_sent = ''

    def pretty_print(self):

        print('Asked for: ',self.asked)
        print('Response:')
        for i in self.data:
            print(i, self.data[i])

# Class to manage the intent request, get the info from ontology, and return 
# the desired data
class DialogManager:
    def __init__(self):
        # Load ontology with owlready2 methods
        self.my_world = World()
        self.onto = self.my_world.get_ontology( "..//MARS_Onto_lite.owl"  )
        self.onto.load()
        
        # not used yet, to get by default not knowig answers takin into 
        # account the type of intent
        self.unknown_baked_expressions = {
            'request_appointment': ['Sorry, to make an appointment I need at least the doctor or the speciality', 
                                    'With the data provided, I can not set up an appointment. Try with more info, such as an area or a doctor'], 
            
            'request_doctor': ['I would like to help you, but I need to know the speciality or the location of the doctor.'] , 
            'request_location':['If you are looking for a certain location, I will need more information such as a doctor name or an area name.'], 
            'request_waiting':['I am really sorry, but I need at least a valid area name to provide you the waiting list.'], 
            'request_consulting_room':['If you want information of a particular room, please, tell me the room number or the doctor of such room.'], 
            'invalid':["Sorry. I don't understand you. Can you say it again?"]
            }
    
    # metodo principal al que llamar cuando tenemos el intent
    def processQuery(self, intent, lack_info):
        print('\n____________________________________________')
        if lack_info == True:
            # ToDo: Esto es simplemente en caso de que nos llegue directamente que 
            # nos falta informacion. falta por testear
            more_info = True
            print('DM says: LACK INFO')
            response = Response()
            response.data['request_type'] = intent.i_type
            response.status = 'lack_info'
            response.baked_sent = self.unknownResponseByType(intent.i_type)
            return response
        else:
            # este if es para le caso que no nos conteste algo valido despues de pedir mas info
            if checkIfLackInfo(): #recorrer atributos y si todos son 'unknown' return true
                print('DM says: LACK INFO')
                result = self.unknownResponseByType(intent.i_type)
            else:
                print('DM says: Let me check it')
                result = self.searchByIntent(intent)
            return result
    
    # ToDo: Select one previously baked non-known answert by type (hasta que 
    # consigamos dialog generation bien, por si acaso tenemos esto)
    def unknownResponseByType(self, intent_type):
        sent_list = self.unknown_baked_expressions[str(intent_type)]
        result = random.choice(sent_list)
        return result
        return 'baked sentence: ToDo the method to get a by default sentence to say I need more info'

    def searchByIntent(self, intent):
        # pillamos el tipo del intent y los atributos
        ##INTENTS: 1. request_location (done), 2.request_consulting_room (done), 3. request_doctor (done), 
        ##         4. request_waiting (done) 5. request_appointment (done)
        t = intent.i_type
        attr = intent.attributes 
        
####### 1.REQUEST LOCATION DATA MANAGEMENT#####################################
################################################################################
        if t == 'request_location':
            # NO Doctor name YES Speciality
            unk = 'Unknown'
            # intentamos pillar los dos atributos principales que esperamos del
            # user cuando haga request_location
            spec = attr['speciality']; spec = str(spec).strip(); spec = spec.capitalize(); #con el .strip() nos aseguramos que no haya ningun espacio en blanco
            location = attr['Place_to_go']; location = str(location).strip(); location = location.capitalize();
            doc = attr['doctor_name']; doc = str(doc).strip(); doc = doc.capitalize();
            response = Response()
            response.data['request_type'] = t
            #Nos dan tanto especialidad como el nombre del doctor
            if str(doc) != str(unk) and str(spec) != str(unk) :
                print('DM says: Speciality and Doctor name provided')
                #we start checking the specialty specialty
                area_ont = self.onto.search_one(is_a = self.onto.Area, Speciality = spec ); #Miramos el area en la ontologia
                checking_doctor = self.onto.search(is_a = self.onto.Doctor, Speciality = spec); #Comprobamos que el doctor existe
                if area_ont and checking_doctor:
                    area_ont = str(area_ont).split('.')[1]
                    # Este metodo es el que recorre las propiedades de la respuesta
                    # de la ontology y los devuelve en forma de objeto
                    a = self.getOWLResponseProps(area_ont)
                    doctor = self.onto.search_one(is_a = self.onto.Doctor, Name = doc);
    #                dd = str(doctor).split('.')[1]
    #                e = self.getOWLResponseProps(dd)
    #                print(e)
                    #We check that the doctor and the speciality provided really match
                    for ii in np.arange(len(checking_doctor)):
                        if doctor == checking_doctor[ii]:
                            print('DM says: Both Doctor and speciality provided match.')
                            
                    cr = self.onto.search_one(is_a = self.onto.Consulting_Room, RoomHasDoctor = doctor)
                    consulting_room = str(cr).split('.')[1]
                    consulting_room = str(consulting_room).split('_')[1]
    
                    # La clase response es como la Clase Intent, es por no hacer un
                    # objeto de 0 cada vez, sino uno ya bien esructurado
                    
                    response.asked = 'Doctor ' + str(doc) + ' location in ' + str(spec) 
                    response.data['name'] = doc
                    # response.data['surname'] = d['Surname']
                    response.data['floor'] = a['Floor']
                    response.data['area'] = area_ont
                    response.data['side'] = a['Side']
                    response.data['room_code'] = consulting_room
                    response.data['waiting_time'] = a['Waiting_List']
                    response.status = 'success'
                    # response.pretty_print()
                    return response
                else:
                    response.status = 'fail'
                    response.baked_sent = "Sorry. It seems I got a big issue here..."
                    return response
                    
                
            # Solo sabemos el area        
            elif str(spec) != str(unk):
                # se supone que aquí te devuelve el DataOntology.Area 
                area_ont = self.onto.search_one(is_a = self.onto.Area, Speciality = str(spec));
                if area_ont:
                    area_ont = str(area_ont).split('.')[1]
                    print('DM says: Speciality name provided')
                    # Este metodo es el que recorre las propiedades de la respuesta
                    # de la ontology y los devuelve en forma de objeto
                    a = self.getOWLResponseProps(area_ont)
                    
                    # La clase response es como la Clase Intent, es por no hacer un
                    # objeto de 0 cada vez, sino uno ya bien esructurado
                    
                    response.asked = str(area_ont) + ' location'
                    response.data['area'] = a['Speciality']
                    response.data['floor'] = a['Floor']
                    response.data['side'] = a['Side']
                    response.data['waiting_time'] = a['Waiting_List']
                    response.status = 'success'
                    # response.pretty_print()
                    return response
                else: 
                    # print('DM says: Sorry. It seems I got some problems... :/')
                    response.status = 'fail'
                    response.baked_sent = "Sorry. It seems I got a big issue here..."
                    return response
                    
                
            # YES Doctor name, por lo que hay que buscar la localizacion de la
            # consulta del doctor
            elif str(doc) != str(unk):
                print('DM says: Doc name provided')
                doctor = self.onto.search_one(is_a = self.onto.Doctor, Name = doc);
                print(doctor)
                if doctor == None:
                    response.asked = 'Doctor ' + doc + ' location'
                    response.baked_sent = "There's no Doctor " + doc + " in this Hospital" 
                    response.status = 'fail'
                    return response
                    
                dd = str(doctor).split('.')[1]
                d = self.getOWLResponseProps(dd)
                
                Room = str(d['AttendsIn']).split('.')[1]
                Room_code = str(Room).split('_')[1]
                
                #We obtain the location of the Area
                res_area = self.onto.search_one(is_a = self.onto.Area, Speciality = d['Speciality'] );
                ee = str(res_area).split('.')[1]
                Area_info  = self.getOWLResponseProps(ee)
                

                # La clase response es como la Clase Intent, es por no hacer un
                # objeto de 0 cada vez, sino uno ya bien esructurado
                response.asked = 'Doctor ' + str(d['Name']) +' ' +  str(d['Surname']) + ' location'
                response.data['name'] = d['Name']
                response.data['surname'] = d['Surname']
                response.data['area'] = d['Speciality']
                response.data['room_code'] = Room_code[:3]
                response.data['floor'] = Area_info['Floor']
                response.data['side'] = Area_info['Side']
                response.status = 'success'
                # response.pretty_print()
                return response
                
            elif str(location) != str(unk):
                if location == 'Elevator':
                        location = location + '_0'
                loc = self.onto.search(is_a = self.onto.Space, Space_name = location)
                print(loc)
                if loc:
                    print('DM says: Location name provided')
                    ll = str(loc).split('.')[1]
                    ll = ll[:-1]
                    l = self.getOWLResponseProps(ll)
                    
                    response.asked = ll + ' location'
                    response.data['location'] = ll
                    response.data['side'] = l['Side']
                    response.data['floor'] = l['Floor']
                    response.status = 'success'
                    # response.pretty_print()
                    return response
                else :
                    print('DM says: Sorry. It seems I got some problems... :/')
                    response.status = 'fail'
                    response.baked_sent = "Sorry. It seems I got a big issue here..."
                    return response
            else: 
                print('DM says: Sorry. It seems I got a big issue here... :(')
                self.unknownResponseByType(t)
                response.status = 'fail'
                response.baked_sent = "Sorry. It seems I got a big issue here..."
                return response
        


                   

                
####### 2.REQUEST DOCTOR DATA MANAGEMENT#######################################
################################################################################

        elif t == 'request_doctor':
            unk = 'Unknown'
            spec = attr['speciality'];  spec = str(spec).strip(); spec = spec.capitalize();

            response = Response()
            response.data['request_type'] = t
            #The name of the area is provided    
            if str(spec) != str(unk):
                
                area_ont = self.onto.search_one(is_a = self.onto.Area, Speciality = str(spec) ); #Busco el objeto pediatria
                if area_ont:
                    area_ont = str(area_ont).split('.')[1]
                    a = self.getOWLResponseProps(area_ont)
                    print(a)
                    cr = a['Contains']
                    doctor_vec = []; name_vec = []; surname_vec = []; room_vec = [];
                    print('cr',cr)
                    for i in np.arange(len(cr)):
                        consulting_room = cr[i];
                        doc = self.onto.search(is_a = self.onto.Doctor, AttendsIn = consulting_room)
                        if doc != None:
                            real_consulting_room = str(consulting_room).split('.')[1]
                            for j in np.arange(len(doc)):
                                doctor = str(doc[j]).split('.')[1]
                                room_code = str(real_consulting_room).split('_')[1]
                                room_vec.append(room_code)
                                doctor_vec.append(doctor)
                                Name = str(doctor).split('_')[0]
                                name_vec.append(Name)
                                Surname = str(doctor).split('_')[1]
                                surname_vec.append(Surname)
                    
                else: 
                    print('DM says: Sorry. It seems I got some problems... :/')
                    return response
                
                print('DM says: Speciality name provided')
                if len(doctor_vec) > 1:
                    print('DM says: There is more than one Doctor. Any preference?')
                    response.asked = 'Doctors attending in ' + str(spec)
                else:
                    response.asked = str(doctor) + ' attending in ' + str(spec)
                response.data['name'] = name_vec[:]
                response.data['surname'] = surname_vec[:]
                response.data['room'] = room_vec[:]
                response.data['area'] = str(spec)
                response.status = 'success'
                return response                
            else:
                # print('DM says: Sorry. It seems I got a big issue here... :(')
                self.unknownResponseByType(t)
                response.status = 'fail'
                response.baked_sent = "Sorry. It seems I got a big issue here..."
                return response

####### 3.REQUEST WAITING LIST DATA MANAGEMENT##################################
################################################################################
                
        elif t == 'request_waiting':
            unk = 'Unknown'
            spec = attr['speciality']; spec = str(spec).strip(); spec = spec.capitalize();
            response = Response()
            response.data['request_type'] = t
            if(str(spec) != str(unk)):
                area_ont = self.onto.search_one(is_a = self.onto.Area, Speciality = str(spec))
                
                if area_ont:
                    area_ont = str(area_ont).split('.')[1]
                    a = self.getOWLResponseProps(area_ont)
                    response.asked = str(spec) + ' waiting list'
                    response.data['area'] = a['Speciality']
                    response.data['waiting_list'] = a['Waiting_List']
                    response.status = 'success'
                    return response

                else:
                    # print('DM says: Sorry. It seems I got some problems... :/')
                    response.status = 'fail'
                    response.baked_sent = "Sorry. It seems I got a big issue here..."
                    return response
            else:
                # print('DM says: Sorry. It seems I got a big issue here... :(')
                self.unknownResponseByType(t)
                response.status = 'fail'
                response.baked_sent = "Sorry. It seems I got a big issue here..."
                return response
                
                

        
####### 4.REQUEST CONSULTING ROOOM DATA MANAGEMENT##############################
################################################################################
        
                    
        elif t == 'request_consulting_room':
            unk = 'Unknown'
            spec = attr['location']; spec = str(spec).strip(); spec = spec.capitalize();
            coding = attr['Room_code']; 
            response = Response()
            response.data['request_type'] = t
            if(str(coding) != str(unk)):
                cr = self.onto.search_one(is_a = self.onto.Consulting_Room, Consulting_number = int(str(coding)))
                if cr:
                    cc = str(cr).split('.')[1]
                    c = self.getOWLResponseProps(cc)
                    spec = str(c['IsLocatedIn']).split('.')[1]
                    spec = spec[:-1]
                    doctor = c['RoomHasDoctor'];
                    doctor = str(doctor).split('.')[1]
                    Name = str(doctor).split('_')[0]
                    Surname = str(doctor).split('_')[1]
                    Surname = Surname[:-1]
                    
                    #Area info
                    area_ont = self.onto.search_one(is_a = self.onto.Area, Speciality = str(spec))
                    aa = str(area_ont).split('.')[1]
                    a = self.getOWLResponseProps(aa)
                    
                    response.asked = str(coding) + ' location'
                    response.data['area'] = spec
                    response.data['doctor'] = Name +' ' + Surname
                    response.data['floor'] = a['Floor']
                    response.data['side'] = a['Side']
                    response.data['waiting_list'] = a['Waiting_List']
                    response.data['room_code'] = attr['Room_code']; 
                    response.status = 'success'
                    return response
                else: 
                    # print('DM says: Sorry. It seems I got some problems... :/')
                    response.status = 'fail'
                    response.baked_sent = "Sorry. It seems I got a big issue here..."
                    return response
            else: 
                # print('DM says: Sorry. It seems I got a big issue here... :(')
                self.unknownResponseByType(t)
                response.status = 'fail'
                response.baked_sent = "Sorry. It seems I got a big issue here..."
                return response
                
                    
        
####### 5.REQUEST APPOINTMENT DATA MANAGEMENT##################################
################################################################################
        
        elif t == 'request_appointment':
            unk = 'Unknown'
            spec = attr['area']; spec = str(spec).strip(); spec = spec.capitalize();
            doc = attr['doctor']; doc = str(doc).strip(); doc = doc.capitalize();
            response = Response()
            response.data['request_type'] = t

            #We don't have any info
            if str(spec) == str(unk) and str(doc) == str(unk):
                print('DM says: I need more information to make an appointment')
                response.asked = "Appointment"
                response.status = 'lack_info'
                return response
                
            #The area is given
            elif str(spec) != str(unk):
                print('DM says: Speciality has been provided')
                
                area_ont = self.onto.search_one(is_a = self.onto.Area, Speciality = str(spec) ); #Busco el objeto pediatria
                if area_ont:
                    aa = str(area_ont).split('.')[1]
                    a = self.getOWLResponseProps(aa)
                    cr = a['Contains']
                    doctor_vec = []; name_vec = []; surname_vec = []; room_vec = []; slots_vec = [];
                    for i in np.arange(len(cr)):
                        consulting_room = cr[i];
                        doc = self.onto.search(is_a = self.onto.Doctor, AttendsIn = consulting_room)
                        if doc:
                            real_consulting_room = str(consulting_room).split('.')[1]
                            for j in np.arange(len(doc)):
                                doctor = str(doc[j]).split('.')[1]
                                room_code = str(real_consulting_room).split('_')[1]
                                room_vec.append(room_code)
                                doctor_vec.append(doctor)
                                Name = str(doctor).split('_')[0]
                                name_vec.append(Name)
                                doc_temp = self.onto.search_one(is_a = self.onto.Doctor, Name = str(Name))
                                dd = str(doc_temp).split('.')[1]
                                d = self.getOWLResponseProps(dd)
                                free_slot = d['Next_free_slot']
                                slots_vec.append(free_slot);
                                Surname = str(doctor).split('_')[1]
                                surname_vec.append(Surname) 
                        else:
                            print('DM says: No doctor found')        
                    print('DM says: Speciality name provided')
                    response.asked = 'Appointment in ' + str(spec)
                    if len(name_vec)>1:
                        print('DM Says: More than one doctor avilable.')
                    response.data['name'] = name_vec[:]
                    response.data['surname'] = surname_vec[:]
                    response.data['room'] = room_vec[:]
                    response.data['free_slots'] = slots_vec[:]
                    response.data['speciality'] = str(spec)
                    response.data['floor'] = a['Floor']
                    response.data['side'] = a['Side']
                    response.data['waiting_List'] = a['Waiting_List']
                    response.status = 'success'
                    return response
                else: 
                    # print('DM says: Sorry. It seems I got some problems... :/')
                    response.status = 'fail'
                    response.baked_sent = "Sorry. It seems I got a big issue here..."
                    return response

            #The doctor is given  
            elif str(doc) != str(unk):
                doctor = self.onto.search_one(is_a = self.onto.Doctor, Name = str(doc));
                if doctor:
                    dd = str(doctor).split('.')[1]
                    d = self.getOWLResponseProps(dd)
                    print(d)
                    Name = d['Name']
                    if d['Surname']:
                        Surname = d['Surname']
                    area = d['Speciality']
                    a = self.getOWLResponseProps(area)
                    print('DM says: Doctor has been provided')
                    response.asked = 'Appointment with Doctor ' + Name + ' ' + Surname
                    response.data['speciality'] = d['Speciality']
                    response.data['doctor'] = Name +' ' + Surname
                    response.data['floor'] = a['Floor']
                    response.data['side'] = a['Side']
                    response.data['waiting_list'] = a['Waiting_List']
                    response.data['free_slot'] = d['Next_free_slot']
                    response.status = 'success'
                    return response
                else:
                    # print('DM says: Sorry. It seems I got some problems... :/')
                    response.status = 'fail'
                    response.baked_sent = "Sorry. It seems I got a big issue here..."
                    return response
            else:
                # print('DM says: Sorry. It seems I got a big issue here... :(')
                self.unknownResponseByType(t)
                response.status = 'fail'
                response.baked_sent = "Sorry. It seems I got a big issue here..."
                return response
      
        return
    
    def printOntoProperties(self, elem):
        for prop in self.onto[elem].get_properties():
            for value in prop[self.onto[elem]]:
                print(".%s == %s" % (prop.python_name, value))
                

#    def getOWLResponseProps(self, elem):
#        data = {}
#        for prop in self.onto[elem].get_properties():
#            for value in prop[self.onto[elem]]:
#                clean_prop_name = prop.python_name
#                data[clean_prop_name] = value
#        return data

    def getOWLResponseProps(self, elem):
        data = {}
        for prop in self.onto[elem].get_properties():
            for value in prop[self.onto[elem]]:
                clean_prop_name = prop.python_name
                checking = "MARS_Onto_lite"
                if checking in str(value):

                    if clean_prop_name not in data:
                        data[clean_prop_name] = []
                    data[clean_prop_name].append(value)
                else:
                  data[clean_prop_name] = value
        return data
    


#    def getOWLResponseProps_mult(self, elem):
#        data = {}
#        for prop in self.onto[elem].get_properties():
#            for value in prop[self.onto[elem]]:
#                clean_prop_name = prop.python_name
#                checking = "NewOntology"
#                if checking in str(value):
#
#                    if clean_prop_name not in data:
#                        data[clean_prop_name] = []
#                    data[clean_prop_name].append(value)
#                else:
#                  data[clean_prop_name] = value
#        return data
#    
    
def checkIfLackInfo():
    return False

def getDoctorsFromArea(onto, elem):
    rooms = []
    for prop in onto[elem].get_properties():
        for value in prop[onto[elem]]:
            if prop.python_name == 'AreaContains':
                rooms.append(str(value).split('.')[1])
    
    docs = []
    for r in rooms:
        res = onto.search(is_a = onto.Doctor, IsInRoom = onto[str(r)])
        res = onto.search_one(Room_Code = str(r)[-3:])
        print(res)
        
    return docs