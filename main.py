__author__ = 'linbinbin'
# import the module.

import csv

# open a file for writing.

tutorial_out = open("tutorial.csv", "wb")

# create the csv writer object.

mywriter = csv.writer(tutorial_out)

# create an object called data that holds the records.

data = [

("Employee No","Employee Name","Job Desription","Salary"),

("123453","Jack","CEO","12000"),

("453124","Jane","Director","25000"),

("4568354","Sally","Marketing","68000"),

("684535","Harry","Sales","56000")

]

# write the rows.

for item in data:

    mywriter.writerow(item)

# always make sure that you close the file.

# to ensure the data is saved.

tutorial_out.close()