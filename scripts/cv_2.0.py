from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import re
import pandas as pd
import numpy as np 



for p in range(0,600,50):
    tg=[]
    a_tags=[]
    resume_links=[] 
    resume_datas=[]
    # LOADING THE PAGE
    driver = webdriver.Chrome(r"C:\chromedriver\chromedriver.exe",)
    driver.get('https://resumes.indeed.com/search?l=&q=data%20science&searchFields=&start={}'.format(p))
    print('https://resumes.indeed.com/search?l=&q=data%20science&searchFields=&start={}'.format(p))    
    #driver.get('chrome://settings/passwords')
    delay = 10 # seconds
    try:
        myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'rezemp-ResumeSearchCard')))
        print ("Page is ready!")
    except TimeoutException:
        print ("Loading took too much time!")

    def get_resume_url(driver,resume_links):
        # GETTING ALL LINKS IN PAGE
        a_tag=driver.find_elements_by_tag_name("a")
        for tag in a_tag:
            a_tags.append(tag.get_attribute('href'))
        # EXTRACTING RESUME LINKS
        for link in a_tags:
                if link != None:
                    cmp_url = re.search("/resume/.+", link)
                    if cmp_url:
                        resume_links.append(link.strip())
    def get_resume_info(driver,resume_links):
        nb_war = 0
        for link in resume_links:
            print("scraping:",link)
            driver.get(link)
            delay = 15 # seconds
            try:
                myElem = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.CLASS_NAME, 'rezemp-ResumeDisplay')))
                print ("Page is ready!")
            except TimeoutException:
                print ("Loading took too much time!")
            try:
                rs=bs(driver.page_source,'lxml')
                title=rs.find('div','rezemp-u-h2').get_text()
                location=rs.find('div','icl-u-textColor--secondary icl-Heading4').get_text()
                description=str(rs.find('div','icl-Grid-col icl-u-xs-span12 icl-u-md-span8 rezemp-ResumeViewPage-resumedisplay'))
                resume_datas.append(title)
                resume_datas.append(location)
                resume_datas.append(description) 
                print('len resume dataset : ',len(resume_datas))
            except:
                print('warning')
                nb_war+=1
        print('len resum links: ',len(resume_links)-nb_war)
        print('len resum datas: ',len(resume_datas))
        x = np.array(resume_datas).reshape((len(resume_links)-nb_war,3))
        df = pd.DataFrame(data=x, columns=['Title', 'Location','Description'])   
        return df        


    get_resume_url(driver,resume_links)
    df=get_resume_info(driver,resume_links)
    df.to_json('C:\\Users\\Ayoub BOUCHACHIAY\\Desktop\\resumeNETWORKADMIN{}.json'.format(p+1300))
    driver.close()
    # GETTING RESUME INFORMATIONS 


