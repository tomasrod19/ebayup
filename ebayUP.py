from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

service = ChromeService(executable_path=r"C:\Program Files (x86)\chromedriver.exe")
service.start()

driver = webdriver.Remote(service.service_url)
def ebay_price(link_here):
    driver.get(link_here)
    prices = driver.find_elements(by=By.CLASS_NAME, value='s-item__price')
    attempts = 5
    average_price = []
    for items in prices:
        # print(items.text)
        attempts -= 1
        average_price.append(items.text)
        if attempts == 0:
            break
    prices_list = [string.replace('$','')for string in average_price]
    del prices_list[0]
    total = 0
    p_listintegers = [float(s) for s in prices_list]
    sum_plist = sum(p_listintegers)
    average_prices_final = sum_plist/len(p_listintegers)
    return average_prices_final

with open(r'C:\Users\Adrian Rod\PycharmProjects\ebayUP\venv\offer_items', 'r', encoding='utf-8') as file:
    contents = file.read()
    data = {}
    lines = contents.strip().split('\n')
    for i in range(0, len(lines), 7):
        key = lines[i]
        value = lines[i + 3]
        data[key] = value                               #Creates list from items in offerUp
offer_items = []
pairs = data.items()
for pair in pairs:
    key = pair[0]
    offer_items.append(key)
print(offer_items)
ideal_items = []
for items in offer_items:
    try:
        driver.get('http://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw='+items+'&_sacat=0')
        results = driver.find_element(by=By.XPATH, value='// *[ @ id = "mainContent"] / div[1] / div / div[2] / div / '                                                         'div[1] / h1 / span[1]')
        #results being the number of items that showed up when searched
        value = results.text.replace(',', '')
        ebay_value = ebay_price('http://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw='+items+'&_sacat=0')
        offerup_value_dollars = (data[items])
        offerup_final_value = float(offerup_value_dollars.replace('$',""))
        if 15000 > int(value) > 5  and ebay_value > offerup_final_value:
            ideal_items.append(items)
            print(items + ' '+ str(ebay_value) + ' vs ' + str(offerup_final_value) + " " +str(value) + ' results')
    except:
        continue
print(ideal_items)