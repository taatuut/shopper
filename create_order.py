import random
import time
import datetime

# function shopper creates order with order id, bonuskaart, some products, a location in geojson format, and a timestamp
def shopper():
    oid = round(time.time() * 1000)
    lonmin, lonmax, latmin, latmax = 5.0, 6.0, 51.7, 52.8
    orglatmin = latmin
    stepsize = .1
    while lonmin < lonmax:
        n1 = random.random() * random.randint(-1,1)
        n2 = random.random() * random.randint(-1,1)
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
                "Timestamp": str(datetime.datetime.now().replace(microsecond=0).isoformat())
            }
            }
        yield(order)
        latmin += stepsize
        oid += 1
        if latmin > latmax:
            latmin = orglatmin
            lonmin += stepsize

# print the output in a json array
i = 0
print("[")
for g in shopper():
    if i > 0:
      print(",")
    print(str(g).replace("'",'"'))
    i += 1
print("]")
