from webdriver_manager.chrome import ChromeDriverManager   #-------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import json
from dateutil.relativedelta import *
import os
from selenium.webdriver.support.ui import Select
import configure
import sys
import csv
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrolling_down(t):
    for i in range(t):
        driver.execute_script("window.scrollBy(0,2000)","")
        time.sleep(0.5)
        
def get_text(x):
    return driver.find_element(By.XPATH,x).text

def get_herf(x):
    attb = ['href','onclick','src']
    for a in attb:
        v = driver.find_element(By.XPATH,x).get_attribute(a)
        if v:
            break 
    return v

def click(x):
    driver.find_element(By.XPATH,x).click()
    
def sent_key(x,val):
    driver.find_element(By.XPATH, x).send_keys(val)
    
def clear(x):
    driver.find_element(By.XPATH, x).clear()
    

def select_scroll(x,val):
    #     x = '/html/body/nav/form[1]/div/select'
        element= Select(driver.find_element(By.XPATH,x))
        element.select_by_visible_text(val)   # ddelement.select_by_value('12')
        
def list_aumphers(province):
    provinces = get_text('/html/body/nav/form[1]/div/select').split('\n')[1:]
    aumphers = []
    if province in provinces:
        select_scroll('/html/body/nav/form[1]/div/select',province)
        aumphers = get_text('/html/body/nav/form[2]/div/select').split('\n')[1:]
    return aumphers
        
def find_gps(province,aumper,deed_no):
    def read_box():
        data = {}
        L = ['deed_id','page_explor','land_id','position','tumbon','aumpher','province','area','eva_price','gps']
        for i,l in enumerate(L):
            
            driver.implicitly_wait(10)
            start = time.time()
            d = None
            while not d and time.time()-start < 10:
                d = get_text(f'/html/body/div[1]/div[3]/span/div/div[2]/div[2]/div/div[2]/div[{i+1}]/div[2]')
#                 print(d)
                data[l] = d

        return data
    
    # print('\n\n\nx',x)
#     print('aumper',aumper)
#     aums = [x for x in aumphers if aumper in x]
#     print('aums',aums)
    
    # aumper = 'บางกรวย'
#     aumper = 'บางกรวย (บางใหญ่)บางกรวย'
    aumper = aumper.split()
    aumper = [x.replace('(',' ').replace(')',' ') for x in aumper]
    aumper = [x.split() for x in aumper]
    a = []
    aumper = [[a.append(xx) for xx in x] for x in aumper]
    aumper = list(set(a))

    aums = []
    for a in aumper:
        aums += [x for x in aumphers if a in x]
    #     aums += 
    print('aums',aums)

    for aumper in aums:
        print(aumper)
        try:
            select_scroll('/html/body/nav/form[1]/div/select',province)
            select_scroll('/html/body/nav/form[2]/div/select',aumper)

            clear('/html/body/nav/form[3]/span/input')
            sent_key('/html/body/nav/form[3]/span/input',deed_no)

            click('/html/body/nav/form[4]/button')
            time.sleep(6)
            box = read_box()
        #     click('/html/body/div[1]/div[3]/span/div/div[1]/button')
            return box
        except:
            pass
    return None

def find_exist_gps(id):
    try:
        with open(f'data/{province}_gps_data.json', 'r') as openfile:
            gps_data = json.load(openfile)
    except:
        gps_data = {}

    if id in gps_data.keys():
        return gps_data[id]

# province = 'nonthaburi'
# find_exist_gps('30715')

#---------------------------------------------------------------
# province = 'nonthaburi'
province = sys.argv[1]
thai_province = configure.search_province[province][0]
chrome_headless = configure.chrome_headless

options = webdriver.ChromeOptions()
if chrome_headless:
    options.add_argument("headless")
options.add_argument('window-size=800x600')
driver = webdriver.Chrome(ChromeDriverManager(version=configure.chrome_version).install(),chrome_options=options)   #-----------------
driver.maximize_window()
print('driver.get_window_size()',driver.get_window_size())

driver.get('https://landsmaps.dol.go.th/')

try:
    # u = '/html/body/div[25]/div/div/div/div[1]/button/i'
    u = '/html/body/div[25]/div/div/div/div[3]/button'
    element_order = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH,u)))
    # time.sleep()
    # driver.find_element(By.XPATH,u).click()
    time.sleep(10)
    click(u)
except:
    pass


# time.sleep(10)
# try:
#     click(u)
# except:
#     pass

aumphers = list_aumphers(thai_province)
print('aumphers',aumphers)

with open(f'data/{province}_led.json', 'r') as openfile:
    data = json.load(openfile)
try:
    with open(f'data/{province}_gps_data.json', 'r') as openfile:
        gps_data = json.load(openfile)
except:
    gps_data = {}
exist_gps = gps_data.keys()
# data

for k in data.keys():
    deed = data[k]['deed_number'].split(',')
    print('\n\n\n',deed,type(deed))
    for d in deed:
        print(d)
        if d in exist_gps:
            print('exist gps')
        else:
#             print('not exist gps',province,d,data[p]['data']['aumper'])
            thai_province = data[k]['province'].strip()
            aumper = data[k]['aumper']
            print(d,'thai_province',thai_province,'aumper',aumper)
            a = find_gps(thai_province,aumper,d)
            print('find gps from website',a)
            
            if a:
                gps_data[str(d)] = a
                with open(f"data/{province}_gps_data.json", "w") as outfile:
                    outfile.write(json.dumps(gps_data, indent=4))
        
    