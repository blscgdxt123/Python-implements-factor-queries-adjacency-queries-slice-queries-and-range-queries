import pymongo


def geohash(lng, lat, length):
   # Longitude range
    xmin = -180
    xmid = 0
    xmax = 180
    x = ''
    for i in range(int(length / 2 + 1) * 5):
        if (lng < xmid):
            xmax = xmid
            xmid = (xmax + xmin) / 2
            x = x + '0'
        else:
            xmin = xmid
            xmid = (xmax + xmin) / 2
            x = x + '1'
    # Latitude range
    ymin = -90
    ymid = 0
    ymax = 90
    y = ''
    for i in range(int(length / 2 + 1) * 5):
        if (lat < ymid):
            ymax = ymid
            ymid = (ymax + ymin) / 2
            y = y + '0'
        else:
            ymin = ymid
            ymid = (ymax + ymin) / 2
            y = y + '1'
    co = ''
    encode = ''
   # Define base32
    base32 = '0123456789bcdefghjkmnpqrstuvwxyz'
    for i in range(int(length / 2 + 1) * 5):
        co = co + x[i] + y[i]
    for i in range(length):
        a = int(co[i * 5 : (i + 1) * 5], 2)
        encode = encode + base32[a]
    return encode

def search2encode(county):
    # Connect to MongoDB
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["test"]
    col = db["huangxingyi"]
    temp = []
    code = ''
    # Database queries
    for a in col.find({'properties.NL_NAME_3': f'{county}'}):
        # if a["properties"]["NL_NAME_1"] == province and a["properties"]["NL_NAME_2"] == city and a["properties"]["NL_NAME_3"] == county:
        temp.append(a["geometry"]["coordinates"])
        # print(a["geometry"]["coordinates"])
    # print(temp)
    for b in temp[0][0]:
        code = code + geohash(b[0], b[1], 8)
    return code


# print(geohash(66.6666, 66.6666, 8))
print(search2encode('鄂城市'))
