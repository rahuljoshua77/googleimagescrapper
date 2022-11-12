#Author: Tech_Hexor
#Requirements: PANDAS, SELENIUM, WGET
#Contact: https://www.fiverr.com/techhexor

from selenium import webdriver
import os
import pandas as pd
import time
from selenium.webdriver.common.by import By
import base64
import traceback
import requests
import shutil
import wget

project_path = os.path.dirname(os.path.abspath(__file__))

chrome_options = webdriver.ChromeOptions()
chrome_options.headless = True
chrome_options.add_argument('log-level=3')
prefs = {"profile.managed_default_content_settings.images": 2}
driver = webdriver.Chrome(options=chrome_options)

tab_link = []

base_url = 'https://www.google.com/search?tbm=isch&q='
with open(project_path+"\\keyword.txt", 'r') as temp_file:
  keyword = [line.rstrip('\n') for line in temp_file]

with open(project_path+"\\filename.txt", 'r') as temp_file:
  filename = [line.rstrip('\n') for line in temp_file]

all_images =""

for j in range(0, len(keyword)):

    driver.get(base_url+keyword[j])
    try:
        image_container = driver.find_element(By.CLASS_NAME, 'islrc') 
        all_images = image_container.find_elements(By.CSS_SELECTOR, 'div.PNCib')
        a = 1
        for single_img in all_images:
            img_tab_link = single_img.get_attribute('data-id')
            tab_link.append(img_tab_link)
            if a==10:
                break
            a = a+1
        for i in range(0, len(tab_link)):
            filename_final = filename[j]+"-"+str(i+1)+".jpg"
            driver.get(base_url+keyword[j]+'#imgrc='+tab_link[i])
            time.sleep(0.5)
            img_org_link = driver.find_element(By.CSS_SELECTOR, '#Sva75c > div > div > div.pxAole > div.tvh9oe.BIB1wf > c-wiz > div > div.OUZ5W > div.zjoqD > div.qdnLaf.isv-id > div > a > img').get_attribute('src')
            if 'data:image/png;base64,' in img_org_link:
                img_org_link = img_org_link.replace('data:image/png;base64,', "")
                with open(project_path+"\\img\\"+filename_final, "wb") as fh:
                    fh.write(base64.urlsafe_b64decode(img_org_link))
            elif 'data:image/jpeg;base64' in img_org_link:
                img_org_link = img_org_link.replace('data:image/jpeg;base64,', "")
                with open(project_path+"\\img\\"+filename_final, "wb") as fh:
                    fh.write(base64.urlsafe_b64decode(img_org_link))
            
            else:
                try:
                    wget.download(img_org_link, project_path+"\\img\\"+filename_final)
                except:
                    try:
                        r = requests.get(img_org_link, stream=True,timeout=10)
                        if r.status_code == 200:
                            with open(project_path+"\\img\\"+filename_final, 'wb') as f:
                                r.raw.decode_content = True
                                shutil.copyfileobj(r.raw, f)
                    except:
                        pass
            print("\n["+str(j)+"]"+" => Keyword: "+keyword[j]+" Filename: => "+filename_final)
            

        data = {
            "Keyword":[keyword[j]],
            "Filename_1":[filename[j]+"-1.jpg"],
            "Filename_2":[filename[j]+"-2.jpg"],
            "Filename_3":[filename[j]+"-3.jpg"],
            "Filename_4":[filename[j]+"-4.jpg"],
            "Filename_5":[filename[j]+"-5.jpg"],
            "Filename_6":[filename[j]+"-6.jpg"],
            "Filename_7":[filename[j]+"-7.jpg"],
            "Filename_8":[filename[j]+"-8.jpg"],
            "Filename_9":[filename[j]+"-9.jpg"],
            "Filename_10":[filename[j]+"-10.jpg"],
            "Image URL":[base_url+keyword[j]+'#imgrc='+tab_link[i]]
        }
        df = pd.DataFrame(data)
        if os.path.exists(project_path+'\\filename.csv'):
            with open(project_path+'\\filename.csv', 'a', newline="", encoding='utf-8') as f:
                df.to_csv(f, header=False, index=False)
        else:
            with open(project_path+'\\filename.csv', 'a', newline="", encoding='utf-8') as f:
                df.to_csv(f, header=True, index=False)
        tab_link.clear()
        all_images = ""

    except Exception as e:
        print(e)

driver.quit()