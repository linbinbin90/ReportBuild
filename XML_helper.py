__author__ = 'linbinbin'
from bs4 import BeautifulSoup
import urllib2

class XML_helper:
    def __init__(self, filename):
        self.f = open(filename, 'r')
        self.soup = BeautifulSoup(self.f.read())

    def read(self):
        # result = []
        brands = self.soup.find_all("brand")
        brand = {}
        for brand_tag in brands:
            # print brand_tag["name"]
            # print "------------"
            model = {}
            for model_tag in brand_tag.find_all("model"):
                # print model_tag["name"]
                # print "***************"
                website = {}
                for website_tag in model_tag.find_all("website"):
                    # print website_tag["name"]
                    # print website_tag["year"]
                    # print "============="
                    parts = []
                    parts.append(website_tag["year"])
                    for part_tag in website_tag.find_all("part"):
                        parts.append(part_tag.next)
                    website[website_tag["name"]] = parts
                model[model_tag["name"]] = website
            brand[brand_tag["name"]] = model
            # result.append(brand)
        # print brand
        return brand