import pymongo
import time

# Connect to the MongoDB database
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["test"]
col = db["huangxingyi"]
a = []
start = time.time()
# Retrieval
for i in col.find({
   "geometry": {"$geoIntersects":{"$geometry": {"type": "LineString", "coordinates": [[-60, -90], [60, 90]]}}}},
   {"properties": 1, "_id": 0}): a.append(i["properties"]["NAME_0"])
b = []
# Iteratively output results
for i in a:
  if i not in b:
    b.append(i)
print(b)
end = time.time()
print("Time-consuming", end - start)