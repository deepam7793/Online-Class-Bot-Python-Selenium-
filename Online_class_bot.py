import requests,os
import urllib
from selenium.webdriver.common.keys import Keys
from seleniumwire import webdriver
import json,requests,os
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.common.by import By

os.chdir(r'C:\Users\Administrator\Desktop')

userid = "" #Reg No
password = "" #pass
botid = -1

def read_option():
    return requests.get("https://api.telegram.org/bot1482106123:AAFm9Y14TYoX6hmCRibBAvWM/getUpdates").json()['result'][-1]['channel_post']['text'].upper()



def send_mess(text):
    url = "https://api.telegram.org/bot1482106123:AAFmzqoX6hmCRibBAvWM/"
    params = {'chat_id':-12, 'text': text}
    response = requests.post(url + 'sendMessage', data=params)

def sendImage():
    url = "https://api.telegram.org/bot1482106123:AAFm9Y14TYUqoX6hmCRibBAvWM/sendPhoto";
    os.chdir(r'C:\Users\Administrator\Desktop')
    files = {'photo': open('class.png', 'rb')}
    data = {'chat_id' : -botid}
    r= requests.post(url, files=files, data=data)
    return r.status_code

import datetime

def get_class():
    url = "https://lovelyprofessionaluniversity.codetantra.com/r/l/p"
    payload = {'i':userid,'p':password}
    payload = urllib.parse.urlencode(payload)
    headers = {
      'Referer': 'https://myclass.lpu.in/',
      'Content-Type': 'application/x-www-form-urlencoded',
    }
    response = requests.post( url, headers=headers, data=payload).cookies.get_dict()
    token = response['_wtj']
    dt = datetime.datetime.today()
    tm = datetime.time(0, 0)
    combined = dt.combine(dt, tm)
    prv = int(combined.timestamp())
    net = dt+datetime.timedelta(days=1)
    ntday = int(net.combine(net,tm).timestamp())

    d = '{"minDate":'+str(prv)+'000,"maxDate":'+str(ntday)+'000,"filters":{"showSelf":true,"status":"started"},"smr":false}'
    #d = '{"minDate":1610908200000,"maxDate":1610994600000,"filters":{"showSelf":true,"status":"started"},"smr":false}'    
    url2 = "https://lovelyprofessionaluniversity.codetantra.com/secure/rest/dd/mf"
    headers = {
    "Content-Type": "application/json",
    "Cookie":"_wtj="+token,
    "Referer": "https://lovelyprofessionaluniversity.codetantra.com/secure/tla/m.jsp",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36",
    "X-Requested-With": "XMLHttpRequest"
    }
    ref = requests.post(url2,headers=headers,data=d).json()['ref']
    return ref

attended = []

def join_class(ref):
    #ref =ref[0]
    url_class = 'https://lovelyprofessionaluniversity.codetantra.com/secure/tla/jnr.jsp?m='+ref['_id']
    #print(ref)
    options = Options()
    os.chdir(r'C:\Program Files\Google\Chrome\Application')
    #Boptions.binary_location = r'C:\Program Files\Google\Chrome\Application'
    options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
    #options.add_argument('--headless')
    #options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(executable_path=r"C:\chromedriver.exe",chrome_options=options)
    driver.get("https:/myclass.lpu.in/")
    time.sleep(5)
    driver.find_element_by_xpath("/html/body/div[2]/div/form/div[6]/input[1]").send_keys(userid)
    driver.find_element_by_xpath("/html/body/div[2]/div/form/div[6]/input[2]").send_keys(password)
    driver.find_element_by_xpath("/html/body/div[2]/div/form/div[7]/button").click()
    driver.get(url_class)
    wait = WebDriverWait(driver, 100000)
    wait.until(ec.visibility_of_element_located((By.ID, 'frame')))
    iframe = driver.find_element_by_id("frame")    
    driver.switch_to.frame(iframe)
    wait = WebDriverWait(driver, 100000)
    wait.until(ec.visibility_of_element_located((By.XPATH, "/html/body/div[2]/div/div/div[1]/div/div/span/button[2]/span[1]")))
    driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div/span/button[2]/span[1]").click()
    
    send_mess('Class Joined For User 119xxxxx '+ref['title']+ ' status: '+ref['status'])
    os.chdir(r'C:\Users\Administrator\Desktop')
    time.sleep(15)
    driver.save_screenshot("class.png")
    sendImage()
    current_class = True
    while current_class:
        try:
            poll = driver.find_element_by_class_name('pollingContainer--1xRnAH')
            if poll.is_displayed():
                send_mess('Poll Avilable')
                driver.save_screenshot("class.png")
                sendImage()
                poll_option = {'A':1,'B':2,'C':3,'D':4,'E':5,'F':6,'G':7}

                poll_wait_count = 0

                while poll_wait_count<300:
                    p_op = read_option()
                    if p_op in list(poll_option.keys()):
                        try:
                            driver.find_element_by_xpath("/html/body/div/main/div[1]/div/div[2]/div["+str(poll_option[p_op])+"]/button").click()  #clicking poll option
                            send_mess("Poll Successfully Given")
                            driver.save_screenshot("class.png")
                            sendImage()
                            break
                        except Exception as e:
                            
                            #send_mess('Poll Option Clicking Failed '+str(e))
                            pass
                    poll_wait_count+=1
                    time.sleep(1)

        except Exception as err:
            print(err)
            pass
        temp_rf=get_class()
        if len(temp_rf)==0 or temp_rf[0]['_id'] not in attended:
            driver.close()
            current_class = False
            break
        time.sleep(30)
    return 0
         
timestamp = datetime.datetime.now()
currTime = timestamp.time()
print('running')
while datetime.time(currTime.hour,currTime.minute)>=datetime.time(8,50):
    rf = get_class()
    if len(rf)>0:
        rf = rf[0]
        if rf['_id'] not in attended:
            attended.append(rf['_id'])
            try:
                join_class(rf)
            except Exception as e:
                print('Error',e)
                join_class(rf)

    time.sleep(200)      
            
            
# try:
#   os.system('cmd /k "taskkill /f /IM chromedriver.exe /T"')
# except:
#   pass
# try:
#   os.system('cmd /k "taskkill /f /IM chrome.exe /T"')
# except:
#   pass  
