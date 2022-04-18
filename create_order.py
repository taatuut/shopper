import random
import time
import datetime

# create order with order id, bonuskaart, some products, a location in geojson format, a timestamp and some notes
def shopper():
    orders = []
    oid = round(time.time() * 1000)
    lonmin, lonmax, latmin, latmax = 3.0, 8.0, 51.0, 54.0
    orglatmin = latmin
    stepsize = 1
    while lonmin < lonmax:
        n1 = random.random() * random.randint(-1,1)
        n2 = random.random() * random.randint(-1,1)
        notes = str(random_lines(3).strip()).replace("'",'"').replace("\n","")
        order = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [round(float(lonmin)+n1,3), round(float(latmin)+n2,3)]
            },
            "properties": {
                "Order": {
                    "Bonuskaart": random.randint(10000000,20000000),
                    "Ordernummer": oid, 
                    "Products": [
                        {"id": "346182", "cat": "AH", "name": "Appelsap", "quantity": random.randint(2,3), "price": 1.29},
                        {"id": "550-35", "cat": "AH", "name": "Avocado eetrijp", "quantity": random.randint(1,2), "price": 2.39},
                        {"id": "742-90", "cat": "AH", "name": "Biologisch Halfvolle melk", "quantity": random.randint(1,5), "price": 1.09},
                        {"id": "742-91", "cat": "AH", "name": "Biologisch Karnemelk", "quantity": random.randint(2,3), "price": 1.06},
                        {"id": "742-32", "cat": "AH", "name": "Biologisch Volle yoghurt", "quantity": random.randint(1,2), "price": 1.09}
                    ]
                },
                "Timestamp": datetime.datetime.now().replace(microsecond=0).isoformat(),
                "Notes": notes
            }
            }
        orders.append(order)
        latmin += stepsize
        oid += 1
        if latmin > latmax:
            latmin = orglatmin
            lonmin += stepsize
    return str(orders).replace("'",'"')


# return number of random lines from a Dutch text corpus to use as notes in the order
def random_lines(nol):
    lines = ""
    for l in range(nol):
        with open("text/nld_sentences.txt", "r", encoding="utf-8") as afile:
            line = next(afile)
            for num, aline in enumerate(afile, 2):
                if random.randrange(num):
                    continue
                line = aline
        lines = lines + " " + line
    return lines


# print the output: ends up in console or pipe to mongoimport
print(shopper())