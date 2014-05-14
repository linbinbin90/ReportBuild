__author__ = 'linbinbin'

import csv
import CSV_helper
import DB_helper

#initial the database connection
database = DB_helper.DB_helper("root", "900129lbb", "127.0.0.1", "LKQCar")
csv = CSV_helper.CSV_helper()

brands = database.query_brands();
for brand in brands:
    #every csv file is a brand
    tables = []
    print brand

    models = database.query_models(brand)
    print models
    for model in models:
        websites = database.query_websites(brand, model)
        print websites
        tables.append([("Model: ", model), ()])
        for website in websites:
            tables.append([("","Website: ", website)])
            table = []
            years = database.query_years(brand, website, model)
            parts = database.query_parts(brand, website, model)
            row = [""]
            row.append("Auto Parts Name")
            for year in years:
                row.append(year)
            table.append(row)
            for part in parts:
                row = [""]
                row.append(part)
                for year in years:
                    price = database.query_price(brand, website, model, year, part)
                    row.append(price)
                table.append(row)
            tables.append(table)
            tables.append([""])
    #write a brand info into a csv file
    csv.write_to_csv(brand + ".csv", tables)
#combine every csv into one xls file,
#every csv file name is the sheet name
csv.csvs_to_excel()





