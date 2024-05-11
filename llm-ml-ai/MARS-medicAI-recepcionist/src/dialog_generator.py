# -*- coding: utf-8 -*-
import random
import sentences as repo

kind_intros = ['Give me a second, please. ', 
               'Let me check it. ', 
               'I can try to help you with that. ']

class DialogGenerator:
    def __init__(self):
        # Load ontology with owlready2 methods
        self.id = 0
        self.version = 1
        self.multiple_answer = False
    
    def generateSentenceByType(self, response_type, response):
        if response_type == "request_location":
            response = self.generateResponseRequestLocation(response)
            intro = random.choice(kind_intros)
            response = intro + response
            return response
        elif response_type == "request_doctor":
            response = self.generateResponseRequestDoctor(response)
            intro = random.choice(kind_intros)
            response = intro + response
            return response
        elif response_type == "request_waiting":
            response = self.generateResponseRequestWaiting(response)
            intro = random.choice(kind_intros)
            response = intro + response
            return response
        elif response_type == "request_consulting_room":
            response = self.generateResponseRequestRoom(response)
            intro = random.choice(kind_intros)
            response = intro + response
            return response
        elif response_type == "request_appointment":
             response = self.generateResponseRequestAppointment(response)
             intro = random.choice(kind_intros)
             response = intro + response
             return response
    
    def generateResponseRequestLocation(self, response):
        data = response.data
        # Surname not provided in the response, just for some cases
        if 'surname' not in data and 'name' in data:
            sentence = self.getRandomSentence(repo.request_location_templates, 'all_minus_surname')
            sentence = sentence.replace('[doctor_name]', str(data['name']))
            floor = data['floor']
            if floor == 0:
                floor_string = 'zero'
            elif floor == 1:
                floor_string = 'first'
            elif floor == 2:
                floor_string = 'second'
            else:
                floor_string = 'third'
            sentence = sentence.replace('[floor]', floor_string)
            sentence = sentence.replace('[side]', str(data['side'].lower()))
            sentence = sentence.replace('[room]', str(data['room_code']))
            sentence = sentence.replace('[area]', str(data['area'].lower()))
            return sentence
        # everything provided in the response
        elif 'name' in data and 'floor' in data and 'side' in data and 'room_code' in data:
            sentence = self.getRandomSentence(repo.request_location_templates, 'all_info')
            sentence = sentence.replace('[doctor_name]', str(data['name']))
            sentence = sentence.replace('[doctor_surname]', str(data['surname']))
            floor = data['floor']
            if floor == 0:
                floor_string = 'zero'
            elif floor == 1:
                floor_string = 'first'
            elif floor == 2:
                floor_string = 'second'
            else:
                floor_string = 'third'
            sentence = sentence.replace('[floor]', floor_string)
            sentence = sentence.replace('[side]', str(data['side'].lower()))
            sentence = sentence.replace('[room]', str(data['room_code']))
            sentence = sentence.replace('[area]', str(data['area'].lower()))
            return sentence
        # when no doctor name is provided, we only have floor and side
        else: 
            # in case we are answering for a place
            print('data', data)
            if 'location' in data:
                print('done!', data['location'])
                sentence = self.getRandomSentence(repo.request_location_templates, 'place')
                sentence = sentence.replace('[place]', str(data['location'].lower()))
                sentence = sentence.replace('[side]', str(data['side'].lower()))
                floor = data['floor']
                if floor == 0:
                    floor_string = 'zero'
                elif floor == 1:
                    floor_string = 'first'
                elif floor == 2:
                    floor_string = 'second'
                else:
                    floor_string = 'third'
                sentence = sentence.replace('[floor]', floor_string)
                return sentence
            # in case we are answering for an area
            else:
                sentence = self.getRandomSentence(repo.request_location_templates, 'area')
                print(data['area'])
                sentence = sentence.replace('[area]', str(data['area'].lower()))
                sentence = sentence.replace('[side]', str(data['side'].lower()))
                floor = data['floor']
                print(floor)
                if floor == 0:
                    floor_string = 'zero'
                elif floor == 1:
                    floor_string = 'first'
                elif floor == 2:
                    floor_string = 'second'
                else:
                    floor_string = 'third'
                sentence = sentence.replace('[floor]', floor_string)
                return sentence
    
    def generateResponseRequestDoctor(self, response):
        data = response.data
        if 'area' in data:
            name = data['name']
            surname = data['surname']
            room = data['room']
            area = data['area']
            number_doctors = len(name)
                        
            if 'area' in data and 'doctor' not in data:
                if number_doctors == 2:
                    sentence = self.getRandomSentence(repo.request_doctor_templates, 'request_2_doctors')
                    name_1 = name[0]
                    surname_1 = surname[0]
                    doctor1 = name_1 + ' ' + surname_1
                    name_2 = name[1]
                    surname_2 = surname[1]
                    doctor2 = name_2 + ' ' + surname_2
                    sentence = sentence.replace('[doctor1]', str(doctor1))
                    sentence = sentence.replace('[doctor2]', str(doctor2))
                    sentence = sentence.replace('[area]', area.lower())
                    sentence = sentence.replace('[number]', 'two')
                
                elif number_doctors == 3:
                    sentence = self.getRandomSentence(repo.request_doctor_templates, 'request_3_doctors')
                    name_1 = name[0]
                    surname_1 = surname[0]
                    doctor1 = name_1 + ' ' + surname_1
                    name_2 = name[1]
                    surname_2 = surname[1]
                    doctor2 = name_2 + ' ' + surname_2
                    name_3 = name[2]
                    surname_3 = surname[2]
                    doctor3 = name_3 + ' ' + surname_3
                    sentence = sentence.replace('[doctor1]', str(doctor1))
                    sentence = sentence.replace('[doctor2]', str(doctor2))
                    sentence = sentence.replace('[doctor3]', str(doctor3))
                    sentence = sentence.replace('[area]', area.lower())
                    sentence = sentence.replace('[number]', 'three')
            
            return sentence
        else:
            return False

    def generateResponseRequestWaiting(self, response):
        data = response.data
        if 'waiting_list' in data:
            wt = data['waiting_list']
            if wt < 25:
                sporadic_sentence = 'There is no much queue. You won\'t have to wait for long!'
            else:
                sporadic_sentence = 'You will have to wait for a while.'
            sentence = self.getRandomSentence(repo.request_waiting_templates, 'waiting_pattern')
            sentence = sentence.replace('[area]', data['area'].lower())
            sentence = sentence.replace('[waiting_list]', str(data['waiting_list']))           
        return sentence + ' ' + sporadic_sentence

    def generateResponseRequestRoom(self, response):
        data = response.data
        sentence = self.getRandomSentence(repo.request_room_templates, 'room_pattern')
        sentence = sentence.replace('[area]', data['area'].lower())
        floor = data['floor']
        if floor == 0:
            floor_string = 'zero'
        elif floor == 1:
            floor_string = 'first'
        elif floor == 2:
            floor_string = 'second'
        else:
            floor_string = 'third'
        sentence = sentence.replace('[floor]', floor_string)
        sentence = sentence.replace('[side]', data['side'].lower())
        sentence = sentence.replace('[room_code]', str(data['room_code']))
        return sentence
    
    def generateResponseRequestAppointment(self, response):
        data = response.data
        #Si hay una entrada doctor, tenemos un doctor definido.
        if 'doctor' in data:
            sentence = self.getRandomSentence(repo.request_appointment_templates, 'appointment_doctor')
            sentence = sentence.replace('[doctor]', data['doctor'])
            sentence = sentence.replace('[area]', data['speciality'])
            sentence = sentence.replace('[slot]', data['free_slot'])
            
        #Si no tenemos doctor definido, vamos por area, donde tendremos más de un doctor    
        elif 'speciality' in data and 'doctor' not in data:
            name = data['name']
            surname = data['surname']
            area = data['speciality']
            number_doctors = len(name)
            if number_doctors == 2:
                sentence = self.getRandomSentence(repo.request_appointment_templates, 'appointment_area_2_doctors')
                name_1 = name[0]
                surname_1 = surname[0]
                doctor1 = name_1 + ' ' + surname_1
                name_2 = name[1]
                surname_2 = surname[1]
                doctor2 = name_2 + ' ' + surname_2
                sentence = sentence.replace('[doctor1]', str(doctor1))
                sentence = sentence.replace('[doctor2]', str(doctor2))
                sentence = sentence.replace('[area]', area.lower())
                sentence = sentence.replace('[number]', 'two')
            
            elif number_doctors == 3:
                sentence = self.getRandomSentence(repo.request_appointment_templates, 'appointment_area_3_doctors')
                name_1 = name[0]
                surname_1 = surname[0]
                doctor1 = name_1 + ' ' + surname_1
                name_2 = name[1]
                surname_2 = surname[1]
                doctor2 = name_2 + ' ' + surname_2
                name_3 = name[2]
                surname_3 = surname[2]
                doctor3 = name_3 + ' ' + surname_3
                sentence = sentence.replace('[doctor1]', str(doctor1))
                sentence = sentence.replace('[doctor2]', str(doctor2))
                sentence = sentence.replace('[doctor3]', str(doctor3))
                sentence = sentence.replace('[area]', area.lower())
                sentence = sentence.replace('[number]', 'three')
                
        else: 
            sentence = self.getRandomSentence(repo.request_appointment_templates, 'no_info')
           
        return sentence

            
            
            
        return False
    
        
    def getRandomSentence(self, dict_, key):
        list_ = dict_[key]
        sent = random.choice(list_)
        return sent