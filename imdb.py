from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

driver = webdriver.Chrome()
url = 'https://www.imdb.com/chart/top/'
driver.get(url)

title = []
year = []
genre = []
rating = []
missing_rows = []

row_count = len(driver.find_elements(By.XPATH, '//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr'))
for row in range(1, row_count + 1):
    try:
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[' + str(row) + ']/td[2]/a')))
        driver.find_element(By.XPATH, '//*[@id="main"]/div/span/div/div/div[3]/table/tbody/tr[' + str(row) + ']/td[2]/a').click()

        title.append(driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/h1').text)

        year.append(driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[1]/div[2]/ul/li[1]/a').text)
        
        num_of_genre = len(driver.find_elements(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div'))
        thisGenre = []
        for i in range(1, num_of_genre + 1):
            thisGenre.append(driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/div[1]/div/a[' + str(i) + ']/span').text)
        genre.append(thisGenre)

        rating.append(driver.find_element(By.XPATH, '//*[@id="__next"]/main/div/section[1]/section/div[3]/section/section/div[1]/div[2]/div/div[1]/a/div/div/div[2]/div[1]/span[1]').text)
    except:
        missing_rows.append(row)

    time.sleep(2)
    driver.back()

    movies = [{
    'Title': a, 
    'Year': b, 
    'Genre': c, 
    'Rating': d
} for a, b, c, d in zip(title, year, genre, rating)]

print( 'missing rows: ',  missing_rows)

df = pd.DataFrame(movies)
df.to_csv('imdb.csv')

time.sleep(2)
driver.quit()