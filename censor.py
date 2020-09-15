#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -*- Coded by Almir Kvakic -*-
# +*+ fb.com/almir.kvakic.10 +*+
# -*- Version: 1.0 beta -*-

from selenium import webdriver
from time import sleep
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


email="yourmail@gmail.com"
pwd="yourpassword"
blacklists = ['Novak', 'Pomoci cu', "This content isn't available right now", 'Dwayne Johnson', 'Giveaway']
  
driver = webdriver.Chrome(r"C:\chromedriver.exe")
driver.maximize_window()
driver.get('https://www.facebook.com/')
print("Facebook otvoren slijedi logovanje...")
sleep(1) 

#UNOS EMAIL I PASSWORDA, LOGOVANJE
username_box = driver.find_element_by_id('email')
username_box.send_keys(email)
sleep(1)

password_box = driver.find_element_by_id('pass')
password_box.send_keys(pwd)
  
login_box = driver.find_element_by_xpath("//button[text()='Log In']")
login_box.click()

#REDIREKT U GRUPU
sleep(1)
driver.get('https://m.facebook.com/groups/YOUR_GROUP_ID')

#SCROLANJE ( https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python )
for scroll in range(3):
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    sleep(2)

#BROJ UCITANIH POSTOVA
posts = driver.find_elements_by_class_name("story_body_container")
#UZIMANJE IMENA OSOBE KOJA JE OBJAVILA POST
posterNames = driver.find_element_by_xpath("//h3[@data-gt='{\"tn\":\"C\"}']//strong[1]")

for i in range(0, len(posts)):
    #PROVJERA DA LI SE U POSTU NALAZI BL RIJEC
    if any(word in posts[i].text for word in blacklists):
        print("pronadjen")

        main_window = driver.current_window_handle
        link = driver.find_element_by_xpath("(//div[@data-sigil='m-feed-voice-subtitle']//a[contains(@href, 'groups')])[%s]" % str(i)).get_attribute("href")
        driver.execute_script("window.open('');")
        driver.switch_to.window(driver.window_handles[1])
        driver.get(link)
        driver.switch_to.window(main_window)
        
        driver.find_element_by_xpath("(//a[@class='_4s19 sec'])[%s]" % str(i)).click()
        sleep(1)
        try:
            #MUTE NA 28DANA
            driver.find_element_by_xpath("//a[@class='_56bz _54k8 _55i1 _58a0 touchable _53n6 _4ob2']").click()
            sleep(2)
            driver.find_element_by_xpath("//input[@value='twenty_eight_days']").click()
            driver.find_element_by_xpath("//button[@value='Confirm']").click()
            
            #BRISANJE POSTA
            driver.switch_to.window(driver.window_handles[1])
            driver.find_elements_by_xpath("//a[@class='_4s19 sec']")[0].click()
            sleep(2)
            driver.find_elements_by_xpath("//a[contains(@data-sigil, 'moreOptions')]")[0].click()
            sleep(1)
            driver.find_elements_by_xpath("//a[contains(@data-sigil, 'removeStoryButton')]")[0].click()
            sleep(1)
            driver.find_elements_by_xpath("//a[@aria-label='Delete']")[0].click()
            
            #VRACANJE NA MAIN TAB
            driver.close()
            driver.switch_to.window(main_window)

        except NoSuchElementException:
            continue
    else:
        print("nop")

#driver.quit() 
