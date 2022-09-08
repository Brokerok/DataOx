from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import math
from datetime import datetime, timedelta, date
from googlesheetswrite import sheets_write
from postgresql import write_in_sql


def update_date_for_postgres(date_ads):
    if '-' in date_ads:
        r = date_ads.split('-')
        date_ads = r[1] + '-' + r[2] + '-' + r[0]
    elif '/' in date_ads:
        r = date_ads.split('/')
        date_ads = r[1] + '-' + r[0] + '-' + r[2]
    return date_ads


def get_integer(string):
    res = []
    for t in string.split():
        try:
            res.append(int(t))
        except ValueError:
            pass
    return res


data_sheets = []


def main():
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.maximize_window()
    driver.get('https://www.kijiji.ca/b-apartments-condos/city-of-toronto/c37l1700273')
    resultsShowing = driver.find_element(By.CLASS_NAME, 'resultsShowingCount-1707762110')
    resultsShowingCount = int(resultsShowing.text.split(' of ')[1].split(' ')[0])
    pagination = resultsShowingCount / 40
    pagination_max = math.ceil(pagination)
    print(f'Pages {pagination_max}')
    print(resultsShowingCount)
    for i in range(pagination_max):
        driver.get(f'https://www.kijiji.ca/b-apartments-condos/city-of-toronto/page-{i+1}/c37l1700273')
        ads = driver.find_elements(By.CLASS_NAME, 'clearfix')
        for ad in ads:
            try:
                try:
                    price = ad.find_element(By.CLASS_NAME, 'price').text[1:]
                    if ',' in price:
                        price = price.replace(',', '')
                    if 'Contact' in price:
                        price = None
                    print(price)
                except:
                    print('Price NOT')

                try:
                    image = ad.find_element(
                        By.CLASS_NAME, 'image').find_element(By.TAG_NAME, 'source').get_attribute('data-srcset')
                except:
                    image = 'https://ca.classistatic.com/static/V/11155/img/placeholder-large.png'
                print(image)
                try:
                    name = ad.find_element(By.CLASS_NAME, 'title ').text
                    print(name)
                except:
                    print('name NOT')

                try:
                    description = ad.find_element(By.CLASS_NAME, 'description').text
                    print(description)
                except:
                    print('description NOT')
                try:
                    beds = ad.find_element(By.CLASS_NAME, 'bedrooms').text
                    print(beds)
                except:
                    print('beds NOT')

                try:
                    location = ad.find_element(By.CLASS_NAME, 'location').text
                    if '<' in location:
                        city = location.split('<')[0].strip()
                    elif '/' in location:
                        city = location[:-11]
                    else:
                        city = location[:-10]
                    print(city)
                except:
                    print('city NOT')

                try:
                    date_ads = ad.find_element(By.CLASS_NAME, 'location').find_element(By.CLASS_NAME, 'date-posted').text
                    if 'hours' in date_ads:
                        hours = get_integer(date_ads)[0]
                        datetime_now = str(datetime.now())
                        time_now = int(datetime_now.split(' ')[1].split(':')[0])
                        if hours > time_now:
                            date_ads = date.today() - timedelta(days=1)
                        else:
                            date_ads = date.today()
                    elif 'minute' in date_ads:
                        date_ads = date.today()
                    elif 'Yesterday' in date_ads:
                        date_ads = date.today() - timedelta(days=1)
                    date_ads = update_date_for_postgres(str(date_ads))
                    print(date_ads)
                except:
                    print('date_ads NOT')
                try:
                    data_sheets.append([image, name, date_ads, city, beds, description, price])
                except:
                    print('Error sheets')
                try:
                    write_in_sql(name, price, image, description, city, beds, date_ads)
                except:
                    print('Error sql')
            except:
                print('!!!!!!!!!!')
                pass


if __name__ == '__main__':
    main()
    time.sleep(5)
    sheets_write(data_sheets)
    print('END PARSE!')
    time.sleep(30)
