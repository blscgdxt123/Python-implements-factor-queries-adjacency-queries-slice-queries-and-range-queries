import psycopg2
from PIL import Image
from PIL import ImageDraw
import numpy
import math
#Randomly generate colors
def random_color():
    color = list(numpy.random.choice(range(256), size=3))
    return color
#Geographic coordinates to pixel coordinates
def geo2pixel(X,Y,lx,ly,cell,c):
    pixelx = round(c-(lx-X)/cell)
    pixely = round((ly-Y)/cell)
    return [pixelx, pixely]

def myfunction(name,pixel,out_path):
    # Gets the largest bounding rectangle
    max_lat = -90.0
    max_lng = -180.0
    min_lat = 90.0
    min_lng = 180.0
    # Save the latitude and longitude of all points
    lat = {}
    lng = {}
    #Assign colors
    a_co={}
    #Give each province a number
    a_i={}
    i=0
    #The number of counties in each province
    a_j={}
    #The province where each county is located
    a_t={}

    # Connect to the database test, establish a cursor
    conn = psycopg2.connect(database="test", user="postgres", password="666666", host="localhost", port="5432")
    cur = conn.cursor()
    #Query all the wkb_geometry data for that country and ST_AsText conversion
    cur.execute("select ST_AsText(wkb_geometry::geography),name_1,name_2 from huangxingyi where name_0 ="+'\''+name+'\'')
    multipolygons_name1=cur.fetchall()

    #Remove excess data such as "(", only deposit points, and divide
    for cors_t in multipolygons_name1:
        cors=cors_t[0].strip('MULTIPOLYGON(((').strip(')))').split('),(')
        province = cors_t[1]
        town=cors_t[2]
        a_t[town]=province
        #If the province does not appear, it is assigned a color and numbered
        if province not in a_co.keys():
            a_co[province]=random_color()
            #Set the number of the province
            a_i[province]=i
            a_j[province]=1
            #Set the features contained in the province
            i+=1
        else:
            #If it does, add one
            a_j[province] += 1
        m = 0
        for cors_1 in cors:
            #Each piece of data may have multiple polygons
            cors_1=cors_1.strip('(').strip(')').split(',')
            #Stores all the data for a polygon
            lat_0 = []
            lng_0 = []
            m += 1
            for cor in cors_1:
               # Split latitude and longitude
               cor = cor.split(' ')
               a=float(cor[1])
               o=float(cor[0])
               lat_0.append(a)
               lng_0.append(o)
               # Gets the smallest outer rectangle
               if a > max_lat:
                  max_lat = a
               if a < min_lat:
                  min_lat = a
               if o > max_lng:
                  max_lng = o
               if o < min_lng:
                  min_lng = o
            lat.setdefault(town, [[]]).append([lat_0,lng_0])

    #Get the length and width
    dist_x = max_lng - min_lng
    dist_y = max_lat - min_lat
    c_x = round(dist_x / pixel)
    c_y = round(dist_y / pixel)
    img = Image.new("RGB", (c_x, c_y),"white")
    #Render the entire image
    for name in a_i.keys():
        color=a_co[name]
        #Traverse all counties in each province
        for j in a_t.items():
            if j[1]==name:
              #Traverse all the data for each county
              for r in lat[j[0]][1:]:
                    p=[]
                    for num in range(len(r[0])):
                        p_0=geo2pixel(r[1][num],r[0][num], max_lng, max_lat, pixel, c_x)
                        p.append((p_0[0],p_0[1]))
                    draw = ImageDraw.Draw(img)
                    draw.polygon(p,outline="rgb(0,0,0)",fill="rgb({0}, {1}, {2})".format(color[0],color[1],color[2]))
    img.save(out_path+'all.jpg')

    #Confirm cropping to rows and columns
    rows = math.ceil(c_y/256)
    columns = math.ceil(c_x/256)

    #Pillow cropping
    for row in range(rows):
        for column in range(columns):
            #crop
            if row!=rows-1 or column!=columns-1:
                cropped = img.crop((256*column, 256*row, 256*(column+1), 256*(row+1)))  # (left, upper, right, lower)
                cropped.save(out_path+str(rows-row)+"-"+str(column + 1)+".jpg")

            elif row==rows -1 and column!=columns-1:
                cropped = img.crop((256 * column, 256 * row, 256 * (column + 1), c_y))  # (left, upper, right, lower)
                cropped.save(out_path + str(rows - row) + "-" + str(column + 1) + ".jpg")

            elif row != rows - 1 and column == columns - 1:
                cropped = img.crop((256 * column, 256 * row, c_x, 256 * (row + 1)))  # (left, upper, right, lower)
                cropped.save(out_path + str(rows - row) + "-" + str(column + 1) + ".jpg")

            elif row == rows - 1 and column == columns - 1:
                cropped = img.crop((256 * column, 256 * row, c_x ,c_y) ) # (left, upper, right, lower)
                cropped.save(out_path + str(rows - row) + "-" + str(column + 1) + ".jpg")

            lx = 180-(max_lng - column * 256 * pixel)
            ly = max_lat - row * 256 * pixel
            f = open(out_path+str(rows-row)+"-"+str(column+1)+".jgw", 'a')
            #Write the contents of the file
            content=str(pixel)+"\n"  "0.0000000000\n"  "0.0000000000\n" +str(-pixel)+"\n" +str(lx)+"\n" +str(ly)+"\n"
            f.write(content)
    print("done")
# Test
myfunction('China',0.2,"D:\\Desktop\\output1\\")