# -*- coding: utf-8 -*-
request_location_templates = {
    'all_info':
        [
        'The doctor [doctor_name] [doctor_surname] is attending on [area], on the consulting room [room].',
        'In room number [room], placed on [floor] floor you will find the doctor [doctor_name] [doctor_surname]. ',
        'If you move to the [side] side of the [floor] floor, you will find doctor [doctor_name] [doctor_surname] on room [room].',
        ],
    'all_minus_surname':
        [
        'The doctor [doctor_name] is attending on [area], on the consulting room [room].',
        'In room number [room] , placed on the [floor] floor, you will find the doctor [doctor_name]. ',
        'If you move to the [side] side of [floor] floor, you will find doctor [doctor_name] on room [room].',
        ],
    'area':
        [
        'The [area] area is placed on the [floor] floor in the [side] part.',
        'If you are looking for [area] area, it is placed on the [floor] floor, just in the [side] side.',
         ],
    'place':
        [
        'The [place] is situated in the [side] side of the [floor] floor.',
        'You can find the [place] in the [side] side of the [floor] floor',
        ]
}
    
request_doctor_templates = {
    'request_2_doctors':
        [
        'Currently the [area] area has [number] doctors attending there. [doctor1] and [doctor2]. What else can I do for you?'
        ],
                
    'request_3_doctors':
        [
        'Currently the [area] area has [number] doctors attending there. [doctor1],[doctor2] and [doctor3]. What else can I do for you?'
        ],
    'doctor_location':
        [
        'Currently the doctor [doctor_name] is attending on [area], on the consulting room [room].',
        'The doctor [doctor_name] is currently visiting in the consulting room [room], on the [area] area.'
        ]
}
    
request_waiting_templates = {
    'waiting_pattern':
        [
        'Currently the [area] area has a waiting time of [waiting_list] minutes.',
        'To be visited in the [area] area, there is a [waiting_list] minutes waiting time.',
        'The [area] area has a waiting time of [waiting_list] minutes.'
        ]
}
    
request_room_templates = {
    'room_pattern':
        [
        'The consulting office [room_code] is placed on the [floor] floor. You will find it in the [side] side, inside the [area] area',
        'The office room [room_code] can be found on the [side] side of the [floor] floor in the [area] area.', 
        'You are asking for the [area] [room_code] consulting room. It is placed on the [floor] floor, in the [side] side.'
        ]
}
    
request_appointment_templates = {
    'no_info':
        [
        'Sorry, I need more info to help you with that. If you don\'t mind need a doctor or an area to check the availability.'
        ],
    
    'appointment_area_2_doctors':
        [
        'You want to do an appointment in the [area] area. Currently there are [number] doctors attending there. [doctor1] and [doctor2]. Do you have any preference?'
        ],
                
    'appointment_area_3_doctors':
        [
        'You want to do an appointment in the [area] area. Currently there are [number] doctors attending there. [doctor1], [doctor2] and [doctor3]. Do you have any preference?'
        ],
                
    'appointment_doctor':
        [
        'You want to do an appointment with the doctor [doctor]. I checked that his next free slot is for the [slot].'
        ]
         
                
}