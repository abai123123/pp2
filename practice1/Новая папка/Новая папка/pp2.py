dic = [
    {"Gender" : "male" , "name" : "Abay"},
    {"Gender" : "female" , "name" : "Aida"}
]
fameles = []
males = []
for genders in dic:
    if genders['Gender'] == 'male':
        males.append(genders['name'])
    else:
        fameles.append(genders['name'])
print(fameles, males)