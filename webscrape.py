from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
driver = webdriver.Chrome()
driver.get("YOUR_POWERSCHOOL_PORTAL_URL")
# assert "Python" in driver.title
elem = driver.find_element(By.NAME, "account")
elem.clear()
elem.send_keys("YOUR_USERNAME")

elem = driver.find_element(By.NAME, "pw")
elem.clear()
elem.send_keys("YOUR_PASSWORD")
elem.send_keys(Keys.RETURN)
# assert "No results found." not in driver.page_source
#driver.close()
elems = driver.find_elements(By.XPATH, "/html/body/div[2]/div[4]/div[2]/div[3]/div[1]/table[1]/tbody/*")
# for r in range(2,3):
for r in range(2, len(elems) - 1):
    elem = driver.find_elements(By.XPATH, "/html/body/div[2]/div[4]/div[2]/div[3]/div[1]/table[1]/tbody/*")[r]
    tds = elem.find_elements(By.TAG_NAME, "td")
    for i in range(len(tds) - 3, -1, -1):
        if tds[i].get_attribute("class") != "notInSession":
            a = tds[i].find_element(By.TAG_NAME, "a")
            a.click()
            time.sleep(1.5)
            trs = driver.find_elements(By.TAG_NAME, "tr")
            course_data = trs[1]
            tds = course_data.find_elements(By.TAG_NAME, "td")
            if len(tds) >= 4:
                course_name = tds[0].text
                course_term = tds[3].text
                print(f'Course: {course_name}\nTerm: {course_term}') 
            
            total_points = earned_points = 0
            for tr in trs:
                if tr.get_attribute("role") == "row":
                    if tr.find_elements(By.CLASS_NAME, "tt-excluded") == []:
                        tds = tr.find_elements(By.TAG_NAME, "td")
                        for td in tds:
                            if td.get_attribute("class") == "score":
                                try:
                                    score = td.text.split("/")
                                    earned_points += float(score[0])
                                    total_points += float(score[1])
                                except:
                                    pass
            if total_points == 0:
                print("No Grades Posted\n")
            else:
                print(f'Grade By Raw Points: {earned_points}/{total_points} = {earned_points / total_points * 100}%\n')

            break
    driver.back()
#print(elems)
while True:
    pass