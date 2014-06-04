__author__ = 'linbinbin'

import CSV_helper
import DB_helper
import XML_helper
import threading
import time



def main():
    #initial the database connection
    database = DB_helper.DB_helper("root", "900129lbb", "127.0.0.1", "Webscraping")
    csv = CSV_helper.CSV_helper()
    xml = XML_helper.XML_helper("Config.xml")

    threads = []
    brands = xml.read()

    for brand, v_b in brands.items():
        #every csv file is a brand
        thread = thread_handle(brand, v_b)
        thread.start()
        threads.append(thread)
        print len(threading.enumerate())
        while True:
            if (len(threading.enumerate()) < 10):
                break
            else:
                print "sleep"
                time.sleep(10)
    for thread in threads:
        thread.join()
    #combine every csv into one xls file,
    #every csv file name is the sheet name
    print "start merging"
    csv.csvs_to_excel()


class thread_handle(threading.Thread):
    def __init__(self, brand, detail):
        threading.Thread.__init__(self)
        self.brand = brand
        self.detail = detail
        self.database = DB_helper.DB_helper("root", "900129lbb", "127.0.0.1", "Webscraping")
        self.csv = CSV_helper.CSV_helper()


    def run(self):
        print "thread start parsing  " + self.brand
        tables = []
        # models = self.database.query_models(self.brand)
        # print models
        for model, v_m in self.detail.items():
            # websites = self.database.query_websites(self.brand, model)
            # print "brand: " + self.brand + " Model: " + model + " is parsing websites: "
            # print websites
            tables.append([("Model: ", model), ()])
            for website, v_w in v_m.items():
                # print website
                tables.append([("", "Website: ", website)])
                table = []
                # years = self.database.query_years(self.brand, website, model)
                # parts = self.database.query_parts(self.brand, website, model)
                start, end = [int(x) for x in v_w[0].split("-")]
                years = []
                while(start <= end):
                    years.append(start)
                    start = start + 1
                row = [""]
                row.append("Auto Parts Name")
                for year in years:
                    row.append(year)
                iterator = 1
                parts = []
                while(iterator < len(v_w)):
                    parts.append(v_w[iterator])
                    iterator = iterator + 1
                # print "first row: "
                # print row
                table.append(row)
                for part in parts:
                    #print "now computing this part: " + part
                    row = [""]
                    row.append(part)
                    for year in years:
                        price = self.database.query_price_top(self.brand, website, model, year, part)
                        row.append(price)
                    # print part + "row value: "
                    # print row
                    table.append(row)
                tables.append(table)
                # print table
                tables.append([""])
        #write a brand info into a csv file
        self.csv.write_to_csv(self.brand + ".csv", tables)
        print "thread finish parsing " + self.brand


print "start running"
main()

