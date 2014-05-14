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
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
                print "Something is wrong with your user name or password"
            elif err.errno == errorcode.ER_BAD_DB_ERROR:
                print "Database does not exists"
            else:
                print err
        finally:
            print "connect to database successfully"

    def query_price(self, brand_name, website_type, model_name, model_year, part_title):
        query = (
            "SELECT round(avg(p.orignial_price), 2) "
            "FROM LKQCar.part p "
            "INNER JOIN LKQCar.part_model_spot pms "
            "ON p.part_id = pms.part_id "
            "INNER JOIN LKQCar.model m "
            "ON pms.model_id = m.model_id "
            "INNER JOIN LKQCar.brand b "
            "ON b.brand_id = m.brand_id "
            "INNER JOIN LKQCar.website w "
            "ON w.site_id = p.website_id "
            "where b.name = (%s) and w.type = (%s) and m.name = (%s) and m.year = (%s) and p.part_title = (%s)  "
            "group by p.part_title"
        )
        avg_price = 0
        try:
            self.cur.execute(query, (brand_name, website_type, model_name, model_year, part_title))
            for (price) in self.cur:
                avg_price = price[0]
        except mysql.connector.Error as err:
            print err
        finally:
            return avg_price

    def query_parts(self, brand_name, website_type, model_name):
        query = (
            "SELECT distinct p.part_title "
            "FROM LKQCar.part p "
            "INNER JOIN LKQCar.part_model_spot pms "
            "ON p.part_id = pms.part_id "
            "INNER JOIN LKQCar.model m "
            "ON pms.model_id = m.model_id "
            "INNER JOIN LKQCar.brand b "
            "ON b.brand_id = m.brand_id "
            "INNER JOIN LKQCar.website w "
            "ON w.site_id = p.website_id "
            "where b.name = (%s) and w.type = (%s) and m.name = (%s) "
        )
        parts = []
        try:
            self.cur.execute(query, (brand_name, website_type, model_name))
            for (part) in self.cur:
                parts.append(part[0])
        except mysql.connector.Error as err:
            print err
        finally:
            return parts

    def query_years(self, brand_name, website_type, model_name):
        query = (
            "SELECT distinct m.year "
            "FROM LKQCar.part p "
            "INNER JOIN LKQCar.part_model_spot pms "
            "ON p.part_id = pms.part_id "
            "INNER JOIN LKQCar.model m "
            "ON pms.model_id = m.model_id "
            "INNER JOIN LKQCar.brand b "
            "ON b.brand_id = m.brand_id "
            "INNER JOIN LKQCar.website w "
            "ON w.site_id = p.website_id "
            "where b.name = (%s) and w.type = (%s) and m.name = (%s)"
        )
        years = []
        try:
            self.cur.execute(query, (brand_name, website_type, model_name))
            for (year) in self.cur:
                years.append(year[0])
        except mysql.connector.Error as err:
            print err
        finally:
            return years

    def query_models(self, brand_name):
        query = (
            "SELECT distinct m.name "
            "FROM LKQCar.part p "
            "INNER JOIN LKQCar.part_model_spot pms "
            "ON p.part_id = pms.part_id "
            "INNER JOIN LKQCar.model m "
            "ON pms.model_id = m.model_id "
            "INNER JOIN LKQCar.brand b "
            "ON b.brand_id = m.brand_id "
            "INNER JOIN LKQCar.website w "
            "ON w.site_id = p.website_id "
            "where b.name = (%s) "
        )
        models = []
        try:
            self.cur.execute(query, (brand_name,))
            for (model) in self.cur:
                models.append(model[0])
        except mysql.connector.Error as err:
            print err
        finally:
            return models

    def query_websites(self, brand_name, model_name):
        query = (
            "SELECT distinct w.type "
            "FROM LKQCar.part p "
            "INNER JOIN LKQCar.part_model_spot pms "
            "ON p.part_id = pms.part_id "
            "INNER JOIN LKQCar.model m "
            "ON pms.model_id = m.model_id "
            "INNER JOIN LKQCar.brand b "
            "ON b.brand_id = m.brand_id "
            "INNER JOIN LKQCar.website w "
            "ON w.site_id = p.website_id "
            "where b.name = (%s) and m.name = (%s)"
        )
        websites = []
        try:
            self.cur.execute(query, (brand_name, model_name))
            for (website) in self.cur:
                websites.append(website[0])
        except mysql.Error as err:
            print err
        finally:
            return websites

    def query_brands(self):
        query = (
            "SELECT distinct b.name "
            "FROM LKQCar.brand b"
        )
        brands = []
        try:
            self.cur.execute(query)
            for (brand) in self.cur:
                brands.append(brand[0])
        except mysql.connector.Error as err:
            print err
        finally:
            return brands

    def __del__(self):
        self.cur.close();
        print "disconnect database"