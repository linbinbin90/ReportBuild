__author__ = 'linbinbin'
from DB_helper import DB_helper

sql = DB_helper("root", "900129lbb", "127.0.0.1", "LKQCar")

brand_name = "toyota"
model_name = "camry"
model_year = "2007"
part_title = "hood123213"

print sql.query_years(brand_name, model_name)
