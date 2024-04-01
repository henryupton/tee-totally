from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

driver.get("https://www.golf.co.nz/club-detail?clubid=100")

description = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[1]/div/div')
print(description.text)
phone = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[2]/div/div[1]/div/p/span')
print(phone.text)

email = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[2]/div/div[1]/div/p/a[1]')
print(email.text)

address1 = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[1]/div/p[1]/span[1]')
address2 = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[1]/div/p[1]/span[2]')
address3 = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[1]/div/p[1]/span[3]')
postcode = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[1]/div/p[1]/span[4]')

total_men = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[2]/div/div[2]/div/p/span[4]')
total_women = driver.find_element(By.XPATH, '//*[@id="ctl55"]/section/div[1]/div/div[2]/div[2]/div/div[2]/div/p/span[5]')

location = driver.find_element(By.XPATH, '//*[@id="courseMap"]/div/div[3]/div[1]/div[2]/div/div[4]/div/div/div/div[1]/div[2]/div/div/a')

print(address1.text)
print(address2.text)
print(address3.text)
print(postcode.text)

print(total_men.text)
print(total_women.text)
