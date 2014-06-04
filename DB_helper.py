__author__ = 'linbinbin'

import mysql.connector
from mysql.connector import errorcode

# sql = DB_helper("root", "900129lbb", "127.0.0.1", "LKQCar")
#
# brand_name = "toyota"
# model_name = "camry"
# model_year = "2007"
# part_title = "hood123213"

class DB_helper:
    def __init__(self, user, password, host, database):
        try:
            self.cnx = mysql.connector.connect(user=user, password=password, host=host, database=database)
            self.cursor = self.cnx.cursor()
            self.cur = self.cnx.cursor(buffered=True)
            print "connect to database successfully"
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exists"
            else:
                print "connection error: " + err

    def query_table(self, brand_name, website_type, model_name):
        query = (
            "SELECT p.Part_title, m.year, round(avg(p.Sale_Price), 2) "
            "FROM part p "
            "INNER JOIN part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) and w.Type = (%s) and m.Name = (%s) "
            "group by p.Part_title, m.year order by p.Part_title, m.year"
        )
        rows = []
        try:
            self.cur.execute(query, (brand_name, website_type, model_name))
            for (row) in self.cur:
                rows.append(row)
        except mysql.connector.Error as err:
            print "table error: " + err
        finally:
            return rows

    def query_prices_row(self, brand_name, website_type, model_name, part_title):
        query = (
            "SELECT round(avg(p.Sale_Price), 2) "
            "FROM part p "
            "INNER JOIN part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) and w.Type = (%s) and m.Name = (%s) and p.Part_title = (%s) "
            "group by p.Part_title, m.year order by p.Part_title, m.year"
        )
        prices = []
        try:
            self.cur.execute(query, (brand_name, website_type, model_name, part_title))
            for (price) in self.cur:
                prices.append(price[0])
        except mysql.connector.Error as err:
            print "prices by row error: " + err
        finally:
            return prices

    def query_price(self, brand_name, website_type, model_name, model_year, part_title):
        query = (
            "SELECT round(avg(p.Sale_Price), 2) "
            "FROM part p "
            "INNER JOIN part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) and w.Type = (%s) and m.Name = (%s) and m.Year = (%s) and p.Part_title like (%s)  "
            "group by p.part_title"
        )
        avg_price = 0
        try:
            self.cur.execute(query, (brand_name, website_type, model_name, model_year, "%" + part_title + "%"))
            for (price) in self.cur:
                avg_price = price[0]
        except mysql.connector.Error as err:
            print "price error: " + err
        finally:
            return avg_price

    #just for create table to olivia
    def query_price_oli(self, brand_name, website_type, model_name, model_year, part_title):
        query = (
            "SELECT round(avg(p.Sale_Price), 2) "
            "FROM part p "
            "INNER JOIN part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) and w.Type = (%s) and m.Name = (%s) and m.Year = (%s) and p.Part_title like (%s)  "
            "group by p.part_title"
        )
        avg_price = 0
        try:
            self.cur.execute(query, (brand_name, website_type, model_name, model_year, part_title))
            for (price) in self.cur:
                avg_price = price[0]
        except mysql.connector.Error as err:
            print "price error: " + err
        finally:
            return avg_price

    def query_price_top(self, brand_name, website_type, model_name, model_year, part_title):
        query = (
            "SELECT p.Sale_Price "
            "FROM part p "
            "INNER JOIN part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) and w.Type = (%s) and m.Name = (%s) and m.Year = (%s) and p.Part_title like (%s)  "
            "order by p.Sale_Price desc"
        )
        top_price = 0
        words = part_title.split()
        part = "%"
        for word in words:
            part = part + word + "%"

        try:
            self.cur.execute(query, (brand_name, website_type, model_name, model_year, part))
            for (price) in self.cur:
                top_price = price[0]
                break
        except mysql.connector.Error as err:
            print "price error: " + err
        finally:
            return top_price

    def query_parts(self, brand_name, website_type, model_name):
        query = (
            "SELECT distinct p.Part_title "
            "FROM part p "
            "INNER JOIN part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) and w.Type = (%s) and m.Name = (%s) "
        )
        parts = []
        try:
            self.cur.execute(query, (brand_name, website_type, model_name))
            for (part) in self.cur:
                parts.append(part[0])
        except mysql.connector.Error as err:
            print "parts error: " + err
        finally:
            return parts

    def query_years(self, brand_name, website_type, model_name):
        query = (
            "SELECT distinct m.Year "
            "FROM part p "
            "INNER JOIN Part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN Model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) and w.Type = (%s) and m.Name = (%s) "
            "order by m.Year"
        )
        years = []
        try:
            self.cur.execute(query, (brand_name, website_type, model_name))
            for (year) in self.cur:
                years.append(year[0])
        except mysql.connector.Error as err:
            print "year error: " + err
        finally:
            return years

    def query_models(self, brand_name):
        query = (
            "SELECT distinct m.name "
            "FROM part p "
            "INNER JOIN part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) "
        )
        models = []
        try:
            self.cur.execute(query, (brand_name,))
            for (model) in self.cur:
                models.append(model[0])
        except mysql.connector.Error as err:
            print "model error: " + err
        finally:
            return models

    def query_websites(self, brand_name, model_name):
        query = (
            "SELECT distinct w.type "
            "FROM part p "
            "INNER JOIN part_model_spot pms "
            "ON p.Part_id = pms.Part_id "
            "INNER JOIN model m "
            "ON pms.Model_id = m.Model_id "
            "INNER JOIN brand b "
            "ON b.Brand_id = m.Brand_id "
            "INNER JOIN website w "
            "ON w.Website_id = p.Website_id "
            "where b.Name = (%s) and m.Name = (%s)"
        )
        websites = []
        try:
            self.cur.execute(query, (brand_name, model_name))
            for (website) in self.cur:
                websites.append(website[0])
        except mysql.Error as err:
            print "website error: " + err
        finally:
            return websites

    def query_brands(self):
        query = (
            "SELECT distinct b.Name "
            "FROM brand b"
        )
        brands = []
        try:
            self.cur.execute(query)
            for (brand) in self.cur:
                brands.append(brand[0])
        except mysql.connector.Error as err:
            print "brand error: " + err
        finally:
            return brands

    def __del__(self):
        self.cur.close();
        print "disconnect database"