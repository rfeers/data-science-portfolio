from owlready2 import *
my_world = World()
onto = my_world.get_ontology( "file://DataOntology_2.owl" )
onto.load()
#print(onto.Area)
#for i in onto.individuals():
#    print(i)
    
#a = onto.search(is_a = onto.Area)
#print(a)
result = onto.search_one( Name = "Ophthalmology" )

x = onto.search(is_a = onto.Doctor, IsInRoom = onto.Room_111)
x = onto.search(is_a = onto.Consulting_Room, RoomHasDoctor = onto["Leo_Wanner"])
x = onto.search(is_a = onto.Area, AreaContains = onto["Room_221"])

res = onto.search_one( Name = str("Room_221"))


data = {}
for prop in onto[elem].get_properties():
    for value in prop[onto[elem]]:
        clean_prop_name = prop.python_name
        data[clean_prop_name] = value
print(data)
#res = onto.search_one(Name = 'Ophthalmology')

#res = str(res).split('.')[1]
print(res)