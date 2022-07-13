# sourcery skip: do-not-use-bare-except
import selenium
from selenium import webdriver
import requests
import time
import os
import sys
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from googletrans import Translator



url ="https://www.trustedshops.de/bewertung/info_X57A331B7ED69F5AD672C329957393438.html"

translator = Translator()



options = webdriver.ChromeOptions()
options.add_argument("--disable-gpu")
options.add_argument("--window-size=1200,700")
options.add_argument("--disable-dev-shm-usage")

reviews = {"name": [], "ratings": [], "comments": [], "date": []}



driver = webdriver.Chrome(options=options)







def each_page(url):
  driver.get(url)
  time.sleep(5)
  driver.maximize_window()
  time.sleep(5)
  try:
    driver.find_element(By.CSS_SELECTOR,"#uc-btn-accept-banner").click()
    time.sleep(5)
  except:
    pass
  noma = driver.find_elements(By.CSS_SELECTOR, "#top > div > div.sc-3df8da41-0.bIqhFi > div")
  for i in noma[3:]:
    juma = i.find_elements(By.CSS_SELECTOR, "div.sc-f4262d32-0.jHRTaH > div.sc-f4262d32-1.jEwCTV > div.Starsstyles__Stars-sc-4o1xbr-0.cxdkxr > span")
    jumastars = sum("rgb(255, 220, 15);" in j.get_attribute("style") for j in juma)
    try:
      reviews["ratings"].append(jumastars)
      print(jumastars)
    except: 
      reviews["ratings"].append(0)
    comment =   i.find_elements(By.CSS_SELECTOR,"div.sc-94f04969-1.dafdRI")
    for j in comment:
      try:
        reviews["comments"].append( j.text)
        print(j.text)
      except:
        reviews["comments"].append("no commnents")
    timeandname = i.find_elements(By.CSS_SELECTOR,"div.sc-f4262d32-0.jHRTaH > div.sc-f4262d32-2.bnfPGY")
    for j in timeandname:
      try:
        reviews["date"].append(j.text)
        print(j.text)
      except:
        reviews["date"].append("no date")          
    names = i.find_elements(By.CSS_SELECTOR, "div.sc-f4262d32-0.jHRTaH > div.sc-f4262d32-2.bnfPGY > div")
    for j in names:
      try:
        reviews["name"].append(j.text)
        print(j.text)
      except:
        reviews["name"].append("no name")

 





for i in range(1,934):
  try:
    each_page(url+"?page="+str(i))
    time.sleep(5)
    df = pd.DataFrame(dict([(k,pd.Series(v)) for k,v in reviews.items()]))
    df.to_csv(f"reviews{str(i)}.csv")
  except:
    print("error")
    continue


