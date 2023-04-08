from webdriver_manager.chrome import ChromeDriverManager   #-------
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime
import json
from dateutil.relativedelta import *
import os
import configure
import sys
import csv

def scrolling_down(t):
    for i in range(t):
        driver.execute_script("window.scrollBy(0,2000)","")
        time.sleep(0.5)
        
def get_text(x):
    return driver.find_element(By.XPATH,x).text

def get_herf(x):
    attb = ['href','onclick','src','data-responsive']
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

def isoDate(b,k):
    if k == 'bit_date':
        bb = b.split('/')
        iso_date = datetime(int(bb[2])-543, int(bb[1]), int(bb[0]), 0, 0, 0, 0)
        # iso_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return iso_date
    elif k == 'announce_date':
        bb = b.split('-')
        iso_date = datetime(int(bb[2])-543, int(bb[1]), int(bb[0]), 0, 0, 0, 0)
        # iso_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return iso_date
    elif k == 'timestamp_date':
        bb = b.split('-')
        iso_date = datetime(int(bb[0]), int(bb[1]), int(bb[2]), 0, 0, 0, 0)
        # iso_date = dt.strftime('%Y-%m-%dT%H:%M:%S.%fZ')
        return iso_date

#----------------------------------------------
def detail_row(r):
#     r = 3
    row = {}
    H = ['sell_order','case_id','type','size2','size1','size0','eva_price','tumbon','aumper','province']
    for c,h in enumerate(H):
        t = get_text(f'/html/body/table[3]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[{2+r}]/td[{c+1}]')
        t = t.strip().replace(',','')
        if t.isnumeric():
            t = int(t)
        elif t.replace(".", "").isnumeric():
            t = float(t)
        row[h] = t
    return row

def detail_click(r,d):
#     r = 1
    # D = {}
    D = d
    click(f'/html/body/table[3]/tbody/tr/td[1]/table[1]/tbody/tr[2]/td/table/tbody/tr[{2+r}]')
    
    driver.switch_to.window(driver.window_handles[1])
    url = driver.current_url
    
    element_order = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, '/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[1]/td/b/font/font')))
    
    try:
        deed_number = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[5]/td/font')
        D['deed_number'] = deed_number
    except:
        pass
    try:
        pay_down = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[16]/td/font')
        pay_down = pay_down.replace(',','')
        D['pay_down'] = int(float(pay_down))
    except:
        pass
    try:
        sell_table = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[17]')
        # print(sell_table)
        sell_table
        sell_table = sell_table.split('\n')
        sell_table = [x.split() for x in sell_table]
        sell_table = [[x for x in x if x not in ['นัดที่','วันที่']] for x in sell_table]
        sell_table
        S = {}
        for s in sell_table:
            S[s[0]] = {
                'date' : s[1],
                'sta' : s[2]
            }
        D['sell_table'] = S
    except:
        pass
    try:
        D['status'] = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[18]/td/font')
    except:
        pass
    try:
        EVA_PRICE = ['/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[19]/td/font','/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[20]/td/font','/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[21]/td/font','/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[22]/td/font']
        max_price = []
        for e in EVA_PRICE:
            x = get_text(e)
            max_price.append(x)
        D['max_price'] = max([int(float(x.replace(',',''))) for x in max_price if x.replace(',','').replace('.','').isnumeric()] )
    except:
        pass
    try:
        announce_date = get_text('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[2]/table/tbody/tr[23]/td/font')
        D['announce_date'] = announce_date
#         D['announce_date'] = isoDate(announce_date,'announce_date')
    except:
        pass
    img = []
    try:
        img1 = get_herf('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[3]/table/tbody/tr[2]/td/div/a/img')
        img.append(img1)
    except:
        pass
    try:
        img2 = get_herf('/html/body/table/tbody/tr[3]/td/div/table/tbody/tr/td[3]/table/tbody/tr[4]/td/table[1]/tbody/tr/td')
        img2 = 'https://asset.led.go.th' + img2.split(",")[0].split('window.open(')[1].replace("'",'')
        img.append(img2)
    except:
        pass
    if img:
        D['img'] = img
        driver.close()
        driver.switch_to.window(driver.window_handles[0])
    return url,D
    
#-----------------------------------------
if not os.path.exists('data'):
   os.makedirs('data')

chrome_headless = False

options = webdriver.ChromeOptions()
if chrome_headless:
    options.add_argument("headless")
options.add_argument('window-size=800x600')
driver = webdriver.Chrome(ChromeDriverManager(version=configure.chrome_version).install(),chrome_options=options)   #-----------------
# driver.maximize_window()
print('driver.get_window_size()',driver.get_window_size())

# province = sys.argv[1]
province = 'nonthaburi'
search_province = configure.search_province[province][1]

#find lastpage
dtn = datetime.now().strftime("%Y%m%d")
try:
    with open(f'data/{province}_currentlink.json', 'r') as openfile:
        C = json.load(openfile)
except:
    C = {}
# print(C)
d = list(C.keys())
if dtn in d:
    d = max([int(x) for x in d])
    p = C[str(d)].keys()
    last_page = max([int(x.split('/')[-1]) for x in p])
    start_page = last_page
else:
    start_page = 1
print('start_page',start_page)

p = start_page
driver.get(f'https://asset.led.go.th/newbid-old/asset_search_province.asp?search_asset_type_id=&search_tumbol=&search_ampur=&search_province={search_province}&search_sub_province=&search_price_begin=&search_price_end=&search_bid_date=&page={p}')   
u = '/html/body/table[3]/tbody/tr/td[1]/table[2]/tbody/tr/td[2]/div'
page = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, u)))
page = get_text(u)
current_page,max_page = [int(x) for x in page.split()[-1].split('/')]
print('(current_page,max_page)',current_page,max_page)

for p in range(start_page,max_page+1):
    try:
        driver.get(f'https://asset.led.go.th/newbid-old/asset_search_province.asp?search_asset_type_id=&search_tumbol=&search_ampur=&search_province={search_province}&search_sub_province=&search_price_begin=&search_price_end=&search_bid_date=&page={p}')
        
        u = '/html/body/table[3]/tbody/tr/td[1]/table[2]/tbody/tr/td[2]/div'
        page = WebDriverWait(driver, 15).until(EC.presence_of_element_located((By.XPATH, u)))
        page = get_text(u)
        current_page,max_page = [int(x) for x in page.split()[-1].split('/')]
        print(f"\n\n\ncurrent_page {current_page}/max_page {max_page}")

        for r in range(1,51):
            print(r,'/',p,'-'*20)
            #read exist data
            try:
                with open(f'data/{province}_led.json', 'r') as openfile:
                    D = json.load(openfile)
            except:
                D = {} 
            try:
                with open(f'data/{province}_currentlink.json', 'r') as openfile:
                    C = json.load(openfile)
            except:
                C = {}
                
            #--------------------
            d = detail_row(r)

            url,d = detail_click(r,d)
            page = f"{r}/{p}"
            
            D[url] = d
            #     'link' : url,
            #     'data' : d
            # }
            
            print(url,D[url])
            
    #         dtn = datetime.now().strftime("%Y%m%d")
            if dtn in C.keys():
                C[dtn][page] = url
            else:
                C[dtn] = {
                    page : url
                }
            #--------------------
            #write data
            with open(f"data/{province}_led.json", "w") as outfile:
                outfile.write(json.dumps(D, indent=4))
            with open(f"data/{province}_currentlink.json", "w") as outfile:
                outfile.write(json.dumps(C, indent=4))
            
    except Exception as  e: 
        print('Error',e)
        
        

        
        
        