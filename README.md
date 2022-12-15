# Python-implements-factor-queries-adjacency-queries-slice-queries-and-range-queries
Python code implements factor queries, adjacency queries, slice queries, and range queries with postgis and mongodb

Using gadm data, perform the following operations and functions in postgis and mongodb respectively:
Download the data from https://gadm.org/

Requirements: Data with county-level boroughs worldwide are used

1. Using the program, based on the postgis database is now the following functions and tests
Requirements:

(1) To achieve a function, input any country, the number of county-level administrative regions of the country (that is, the number of elements contained in the data of a country), and the statistics of the country in the county level administrative areas of the largest three, print out the name and area value;

(2) To achieve a function, input any country, the statistics of the country in the region of the neighboring other countries (need to do data integration);

(3) Realize a data processing function, the function accepts three parameters: country name, pixel resolution, output directory. Input any country, render the data of this country at the specified pixel resolution (pixel resolution is the size of the actual geographic range represented by a pixel, wide and high resolution), and then shred the rendered grid of the specified country according to the 256x256 pixel size index grid. Image data cut into squares and written to the output directory (this process is also called slicing). You need to take into account the maximum outer rectangular boundaries of the corresponding countries, and then generate a picture to scale, with each small administrative area assigned a random color, and all county boundaries separated by black lines. The output section image data is named in an index way. For example, the section file in the upper left corner is named 1-1, the one below is 2-1, the one on the right is 1-2, and so on. If the output data format is jpg or other raster data without coordinate information, corresponding coordinate registration files will be generated according to the data coordinate parameters of each slice file. For example, jpg files will output corresponding jgw files, and finally open all slice data in qgis for comprehensive display. ;

2. Implement the following functions and test based on mongodb database with the program
Requirements:

(1) Implement a function, given a latitude and longitude coordinates and coding length, then generate a geohash code;

(2) Implement a function, given the name of a mongodb county administrative region as the query condition, you can query a county administrative region, and then the geometric boundary of this county administrative region is organized into a large section of text with 8-bit geohash encoded data for description (no Spaces are left between adjacent vertices, encoding is continuously stored);

(3) The test program calls the above two functions, and tests with the data of "Echeng City, Ezhou City, Hubei Province", and prints out the results.
