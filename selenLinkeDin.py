import csv
import parameters
from parsel import Selector
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys
from time import sleep

def validate_field(field):
    if field:
        pass
    else:
        field = ''
    return field

writer = csv.writer(open(parameters.file_name,'wb'))
writer.writerow(['name','job_title','school','location','linkedin_url'])

driver = webdriver.Chrome('/home/up/chromedriver')
driver.get('https://www.linkedin.com') 
username = driver.find_element_by_id(parameters.linkedin_username)    
password = driver.find_element_by_id(parameters.linkedin_password) 
submit = driver.find_element_by_id('login-submit') 

username.send_keys('ayoub1996.am2@gmail.com')
sleep(0.5)
password.send_keys('ayoubcom1996')
sleep(0.5)
submit.click()
sleep(5)

driver.get('https://www.google.com') 
sleep(3)

search_query = driver.find_element_by_name('q')  
search_query.send_keys(parameters.search_query)
sleep(0.5)

search_query.send_keys(Keys.RETURN)

linkedin_urls = driver.find_elements_by_tag_name('cite')  

linkedin_urls = [url.text for url in linkedin_urls ]

for url in linkedin_urls:
    if 'linkedin' in url.split('.'):
        driver.get(url)
        sleep(5)
        sel = Selector(text=driver.page_source)
        name = sel.xpath('//ha/text()').extract_first()
        job_title = sel.xpath('//h2/text()').extract_first()
        school = sel.xpath('//*[starts-with(@class, "pv-top-card-section__school")]/text()').extract_first()
        if school:
            school = school.strip()
        
        location = sel.xpath('//*[starts-with(@class, "pv-top-card-section__location")]/text()').extract_first()
        linkedin_url = driver.current_url

        name=validate_field(name)
        job_title=validate_field(job_title)
        school=validate_field(school)
        location=validate_field(location)
        linkedin_url=validate_field(linkedin_url)

        writer.writerow([name.encode('utf-8'),job_title.encode('utf-8'),school.encode('utf-8'),location.encode('utf-8'),linkedin_url.encode('utf-8')])
        try:
            driver.find_element_by_xpath('//snap[text()="Connect"]').click
            sleep(3)
            driver.find_element_by_xpath('//*[@class="button-primary-large ml3"]').click
            sleep(3)
        except :
            pass
        

driver.quit()