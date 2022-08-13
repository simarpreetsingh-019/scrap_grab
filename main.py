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

path = Service("C:\\Users\\Jasvinder Singh\\Downloads\\chromedriver.exe")

def initialise_driver():

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
    print("Driver initialised")
    return driver

def time_stamp():
    curr = time.ctime(time.time())
    return curr
    
def autocomplete_response_data(driver, url): 
    suggested_locations = []
    print("time of entering autocomplete func = ", time_stamp())
    print("Request and responses coming for : ", url)
    driver.get(url) 
    time.sleep(5)
    for request in driver.requests:
        #print("Reached Requests ")
        if request.response:
            if (request.url.startswith("https://food.grab.com/v1/autocomplete?")) :
                print(
                    request.url,
                    request.response.status_code,
                    request.response.headers['Content-Type']
                )
                response = request.response
                body = decode(response.body, response.headers.get('Content-Encoding', 'identity'))
                decoded_body = body.decode('utf-8')
                json_data = json.loads(decoded_body)

    restaurant_data3 = json_data["places"]
    for value in restaurant_data3:
        name = value["name"]
        address = value["address"]
        whole = name+" - "+address
        suggested_locations.append(whole)
        
    print("Suggested location sent ")
    print("Exit time = ", time_stamp())
    time.sleep(5)
    return suggested_locations
        
def scrap_location_data(driver, locations):
    print("Time at the locations {} data fetching = {}".format(locations, time_stamp()))
    print("Location : {}  request in progress ".format(locations))
    response_time_delay = 20
    location_url = locations.replace(",","%2C")
    location_url = location_url.replace(" ","%20")

    
    time.sleep(response_time_delay)
    driver.get('https://food.grab.com/sg/en/restaurants?search='+location_url+'&lng=en')
    time.sleep(2 * response_time_delay)
    
    while True:
        try:
            WebDriverWait(driver,40).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="page-content"]/div[4]/div/div/div[2]/div/button'))).click()
            print("First Click successful")

            clicks = 0
            while True:
                if clicks == 0:
                    print("Entered While loop")
                try:
                    time.sleep(15)
                    p=driver.find_element(By.CLASS_NAME,'ant-btn.ant-btn-block')
                    time.sleep(3)
                    p.click()
                    time.sleep(10)
                    clicks = clicks + 1
                    print("loading page no : ", clicks)


                except:
                    break
                    print("Number of pages loaded is ",clicks)

            print("While loop Exit")

            time.sleep(10)
            for request in driver.requests:
                #print("Reached Requests ")
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
                df.to_csv(locations + '.csv', index=True)
    
        except:
            for request in driver.requests:
                if(request.response.status_code == 403):
                    print("Get request Blocked for {} , will generate next request in 5 mins for next location ".format(locations))
            
            print("Load button disabled or no locations left. generating next request")
            break   
    
    print(" {} 's request completed at {} ".format(locations, time_stamp()))


def get_url(driver):
    response_time_delay = 20
    new_request_time_delay =360 
    
    countries = ["id", "ph", "th","vn", "sg", "my"]
    print("Choose country code to search in :")
    choice = int(input("\n 1. Indonesia  \n 2. Phillippines  \n 3. Thailand  \n 4. Vietnam  \n 5. Singapore  \n 6. Malaysia \n"))
    country_code = countries[choice-1]
    
    location = input("Enter location to search for  ")
    location = location.replace(",","%2C")
    location = location.replace(" ","%20")
    
    time.sleep(5)
    
    first_request = "https://food.grab.com/v1/autocomplete?component=country:"+country_code.upper()+"&language=en&transportType=0&keyword="+location + "&limit=10"
    print(first_request)
    
    print("\n Time at starting of this program = ", time_stamp())
    
    suggested_locations = autocomplete_response_data(driver, first_request)
    count = 0
    print("\n locations we got in auto complete search =  ", suggested_locations)
    time.sleep(10)
    
    for locations in suggested_locations : 
        count = count+1
        # driver.get('https://food.grab.com/sg/en/restaurants?search=The%20Stamford%2C%20Raffles%20City%20Robinsons%2C%202%20Stamford%20Rd&lng=en')
        print("\n Sending {} 's request ".format(locations))
        print("request sent at : ", time_stamp())
        if count == 1  or count == 5: 
            time.sleep(response_time_delay)
        scrap_location_data(driver, locations)
        print(" \n \n \n ")
        time.sleep(new_request_time_delay)
        print("New location sent at time  : ", time_stamp())
        print("{} locations done , starting {} ".format(count, count+1))
        time.sleep(5)

    print("Exiting at time : ", time_stamp())    


if __name__ == "__main__":
    
    driver = initialise_driver()
    print('driver initialised')
    
    get_url(driver)