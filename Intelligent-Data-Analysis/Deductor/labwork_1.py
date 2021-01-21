import random

products = ["Ледокаин", 
            "Новокаин", 
            "Арбидол", 
            "Новопассит", 
            "Ношпа", 
            "Гематоген", 
            "Спазмалгон", 
            "Пенталгин"]

f = open("Pharmacy.txt", "w")


random.seed()

begin_number = 578432
for i in range(50):
    prod_count = random.randint(1, 5)
    result = ""
    for j in range(prod_count):
        result += str(begin_number) + " " + random.choice(products) + "\n"
    f.write(result)
    begin_number += random.randint(3, 10)