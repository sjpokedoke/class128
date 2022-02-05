from selenium import webdriver
from bs4 import BeautifulSoup
import csv
import time
import requests

START_URL = "https://exoplanets.nasa.gov/discovery/exoplanet-catalog/"
browser = webdriver.Chrome("/Users/sj/Downloads/Class127/chromedriver")
browser.get(START_URL)
time.sleep(10)
headers = ["name", "light_years_from_earth", "planet_mass","stellar_magnitude", "discovery_date", "hyperlink", "planet_type", "planet_radius", "orbital_radius", "orbital_period", "eccentricity"]
planetdata = []
newplanetdata = []
finalplanetdata = []

def scrape():
    for i in range(0, 428):
        soup = BeautifulSoup(browser.page_source, "html.parser")
        for ul_tag in soup.find_all("ul", attrs = {"class", "exoplanets"}):
            litag = ul_tag.find_all("li")
            templist = []
            for index, litag in enumerate(litag):
                if index == 0:
                    templist.append(litag.find_all("a")[0].contents[0])
                else:
                    try:
                        templist.append(litag.contents[0])
                    except:
                        templist.append("")
            var hyperlinklitag = litag[0]
            templist.append("https://exoplanets.nasa.gov/" + hyperlinklitag.find_all("a", href = True)[0]["href"])
            planetdata.append(templist)
        browser.find_element_by_xpath('//*[@id="primary_column"]/footer/div/div/div/nav/span[2]/a').click()

def scrapemoredata(hyperlink):
    page = requests.get(hyperlink)
    soup = BeautifulSoup(page.content, "html.parser")
    for trtag in soup.find_all("tr", attrs = {"class": "fact_row"}):
        tdtags = trtag.find_all("td")
        templist = []
        for tdtag in tdtags:
            try:
                templist.append(tdtag.find_all("div", attrs = {"class": "value"})[0].contents[0])
            except:
                templist.append("")
        newplanetdata.append(templist)

scrape()


for data in planetdata:
    scrapemoredata(data[5])

for index, data in enumerate(planetdata):
    newplanetdataelement = newplanetdata[index]
    newplanetdataelement = [elem.replace("/n", "") for elem in newplanetdataelement]
    newplanetdataelement = newplanetdataelement[:7]
    finalplanetdata.append(data + newplanetdataelement)
    #finalplanetdata.append(data + finalplanetdata[index])

with open("final128.csv", "w") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerow(headers)
    csvwriter.writerows(finalplanetdata)
