import json
import time
import sys
import pandas as pd

from bs4 import BeautifulSoup
from seleniumwire import webdriver
from seleniumwire.utils import decode
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options


restarunt_final_data = [["Restaurant Name", "Latitude", "Longitude"]]

path = Service("C:\\Users\\Jasvinder Singh\\Downloads\\chromedriver.exe")
#driver = webdriver.Chrome(service = path)
chrome_opts = webdriver.ChromeOptions()
chrome_opts.headless = True  # In headless mode, it’s possible to run large scale web application tests, navigate from page to page without human intervention
user_agent = ('Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) ' + 
              'Chrome/60.0.3112.50 Safari/537.36') # Set the user agent
chrome_opts.add_argument(f'user-agent={user_agent}') # Add the user agent
chrome_opts.add_argument('--no-sandbox') # Disable sandbox
chrome_opts.add_argument("--disable-extensions") # Disable extensions
chrome_opts.add_argument('--disable-dev-shm-usage') # Disable shared memory

options = { # Set the options for the browser to use the chrome driver and the options
    'exclude_hosts': [
        'google-analytics.com',
        'analytics.google.com',
        'google.com',
        'facebook.com',
        'stats.g.doubleclick.net',
    ],
}
#A list of addresses for which Selenium Wire should be bypassed entirely. Note that if you have configured an upstream proxy then requests to excluded hosts will also bypass that proxy.

driver = webdriver.Chrome(service=path,
                                desired_capabilities=chrome_opts.to_capabilities(),
                                seleniumwire_options=options)  # Create the browser and open the url in it and wait for the page to load completely






location = input("Enter location to search for  ")
location_url = location.replace(',',"%2C")
location_url = location.replace(' ',"%20")

# driver.get('https://food.grab.com/sg/en/restaurants?search=The%20Stamford%2C%20Raffles%20City%20Robinsons%2C%202%20Stamford%20Rd&lng=en')

driver.get('https://food.grab.com/sg/en/restaurants?search='+location_url+'&lng=en')
time.sleep(15)

WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="page-content"]/div[4]/div/div/div[2]/div/button'))).click()
print("First Click successful")

clicks = 0
while True:
    print("Entered While loop")
    try:
        time.sleep(12)
        p=driver.find_element(By.CLASS_NAME,'ant-btn.ant-btn-block')
        time.sleep(3)
        p.click()
        time.sleep(8)
        clicks = clicks + 1
        

    except:
        break
        print("Number of pages loaded is ",clicks)

print("While loop Exit")
    

for request in driver.requests:
    print("Reached Requests ")
    if request.response:
        if (request.url.startswith("https://portal.grab.com/foodweb/v2/search")) :
            print(
                request.url,
                request.response.status_code,
                request.response.headers['Content-Type']
            )
            response = request.response
            body = decode(response.body, response.headers.get('Content-Encoding', 'identity'))
            decoded_body = body.decode('utf-8')
            json_data = json.loads(decoded_body)
            
            restaurant_data3 = json_data["searchResult"]["searchMerchants"]

            for value in restaurant_data3:
                restarunt_final_data.append([value["address"]["name"], value["latlng"]["latitude"],
                                   value["latlng"]["longitude"]])
                print(value["address"]["name"], value["latlng"]["latitude"],
                      value["latlng"]["longitude"])

            print()
# saving the final data to a csv file
df = pd.DataFrame(restarunt_final_data)
df.to_csv(location + '.csv', index=True)


