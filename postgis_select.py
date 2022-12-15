import psycopg2

def mycount(name):
    conn = psycopg2.connect(database="test", user="postgres", password="666666", host="localhost",port="5432")
    cur = conn.cursor()
    cur.execute("SELECT name_3,ST_Area(wkb_geometry::geography) FROM public.huangxingyi WHERE name_0 = '"+name+"'")
    count = 0
    area = cur.fetchall()
    for i in area:
        count += 1
    print("count", count)
    for i in range(0, count):
        for j in range(i + 1, count):
            if area[i][1] < area[j][1]:
                temp = area[i]
                area[i] = area[j]
                area[j] = temp
    print('The First One', area[0])
    print('The Second One', area[1])
    print('The Third One', area[2])

    # count = cur.fetchall()

    return count


def myneighbour(name):
    conn = psycopg2.connect(database="test", user="postgres", password="666666", host="localhost", port="5432")
    cur = conn.cursor()
    cur.execute("SELECT distinct name_0 FROM public.huangxingyi as nearby,(SELECT wkb_geometry FROM public.huangxingyi WHERE name_0 = '" +
                name + "') as country WHERE ST_touches(nearby.wkb_geometry, country.wkb_geometry) AND name_0 <> '"+name+"'")
    result = cur.fetchall()
    neighbour = []
    for i in result:
        neighbour.append(i[0])
    return neighbour

# count = mycount()
name = ''
print(mycount(name))

neighbour = myneighbour(name)
print(neighbour)