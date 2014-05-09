__author__ = 'linbinbin'

import csv
import os
import glob
import xlwt

class CSV_helper:

    def write_to_csv(self, file_name, data):
        file = open(file_name, "wb")
        csv_writer = csv.writer(file)
        for item in data:
            csv_writer.writerow(item)
        file.close();

    def csvs_to_excel(self):
        wb = xlwt.Workbook()
        for csvfile in glob.glob(os.path.join('.', '*.csv')):
        fpath = csvfile.split("/", 1)
        fname = fpath[1].split(".", 1) ## fname[0] should be our worksheet name

        ws = wb.add_sheet(fname[0])
        with open(csvfile, 'rb') as f:
            reader = csv.reader(f)
            for r, row in enumerate(reader):
                for c, col in enumerate(row):
                    ws.write(r, c, col)
        wb.save('output.xls')
