from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import gspread
import time

gc = gspread.service_account(filename=r'C:\Users\Adrian Rod\PycharmProjects\ebayUP\venv\credentials.json')
sh = gc.open_by_key('1-4uZ-zgZcU66b_au-qV7-9xGY-iZ3PGkODI-TCJqL4I')                                                 #uploading data to google sheets
sh_items = gc.open_by_key('1J-aJZRFK5uU86ouPSCb-0JkaEt898QlglsR4Pi5c-KY')
worksheet = sh.sheet1
worksheet_items = sh_items.sheet1


service = ChromeService(executable_path=r"C:\Program Files (x86)\chromedriver.exe")
service.start()

driver = webdriver.Remote(service.service_url)      #gets price of item on ebay sold listings 
def ebay_price(link_here):
    driver.get(link_here)
    prices = driver.find_elements(by=By.CLASS_NAME, value='s-item__price')
    results = driver.find_element(by=By.XPATH, value='// *[ @ id = "mainContent"] / div[1] / div / div[2] / div / '                                                         'div[1] / h1 / span[1]')
    results_number = results.text.replace(',', '')
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
    return average_prices_final, results_number


offer_up_items = worksheet_items.get_all_values()           #dictionary of the items with the the price attached
ou_names = [i for i in offer_up_items[::7]]
new_ou_names = sum(ou_names, [])
ou_prices = [i for i in offer_up_items[3::7]]
new_ou_prices = sum(ou_prices, [])
my_dict = {}
x = 0
for i in new_ou_names:
    my_dict[i] = new_ou_prices[x]
    x += 1
print(my_dict)
offer_items = []
pairs = my_dict.items()
for pair in pairs:
    key = pair[0]
    offer_items.append(key)
print(offer_items)

pairs = my_dict.items()
for pair in pairs:
    key = pair[0]
    offer_items.append(key)
# print(offer_items)

a = [] #offerUp item names
b = [] #offerUp price
c = [] #Ebay price 
d = [] #Ebay results
for items in offer_items:
    try:
        ebay_value, ebay_results = ebay_price('http://www.ebay.com/sch/i.html?_odkw=&_ipg=25&_sadis=200&_adv=1&_sop=12&LH_SALE_CURRENCY=0&LH_Sold=1&_osacat=0&_from=R40&_dmd=1&LH_Complete=1&_trksid=m570.l1313&_nkw='+items+'&_sacat=0')
        offerup_value_dollars = (my_dict[items])
        offerup_final_value = float(offerup_value_dollars.replace('$',""))
        if ebay_value > offerup_final_value * 1.1:
            a.append(items)
            b.append(offerup_final_value)
            c.append(ebay_value)
            d.append(ebay_results)
    except:
        continue
combined_list = [[a[i], b[i], c[i], d[i]] for i in range(int(len(a)/2))]
worksheet.update('A2',combined_list)
