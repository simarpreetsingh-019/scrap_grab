<div align="center" id="top"> 
  <img src="./.github/app.gif" alt="Scrapping_FoodGrab" />
   
  &#xa0;

</div>

<h1 align="center">Scrapping_FoodGrab</h1>

<p align="center">
  <img alt="Github top language" src="https://img.shields.io/github/languages/top/simarpreetsingh-019/scrap_grab?color=56BEB8">

  <img alt="Github language count" src="https://img.shields.io/github/languages/count/simarpreetsingh-019/scrap_grab?color=56BEB8">

  <img alt="Repository size" src="https://img.shields.io/github/repo-size/simarpreetsingh-019/scrap_grab?color=56BEB8">

  <img alt="License" src="https://img.shields.io/github/license/simarpreetsingh-019/scrap_grab?color=56BEB8">

  <!-- <img alt="Github issues" src="https://img.shields.io/github/issues/simarpreetsingh-019/scrap_grab?color=56BEB8" /> -->

  <!-- <img alt="Github forks" src="https://img.shields.io/github/forks/simarpreetsingh-019/scrap_grab?color=56BEB8" /> -->

  <!-- <img alt="Github stars" src="https://img.shields.io/github/stars/simarpreetsingh-019/scrap_grab?color=56BEB8" /> -->
</p>

<!-- Status -->

<!-- <h4 align="center"> 
	🚧  Scrapping Food Grab 🚀 Under construction...  🚧
</h4> 

<hr> -->

<p align="center">
  <a href="#dart-about">About</a> &#xa0; | &#xa0; 
  <a href="#sparkles-approach">Approach</a> &#xa0; | &#xa0;
  <a href="#desert_island-plan-1">Plan 1</a> &#xa0; | &#xa0;	
  <a href="#stop_sign-difficulty-faced-during-doing-this">Difficulties Faced</a> &#xa0; | &#xa0;
  <a href="#stop_sign-difficulty-faced-during-doing-this">Idea for new approach</a> &#xa0; | &#xa0;
  <a href="#sparkles-approach-2--implementing-new-things">Plan 2</a> &#xa0; | &#xa0;
  <a href="#dart-golf-results-">Results </a> &#xa0; | &#xa0;	
  <a href="#rocket-technologies">Technologies</a> &#xa0; | &#xa0;
  <a href="#white_check_mark-requirements">Requirements</a> &#xa0; | &#xa0;
  <a href="#checkered_flag-starting">Starting</a> &#xa0; | &#xa0;
  <a href="#memo-license">License</a> &#xa0; | &#xa0;
  <a href="https://github.com/simarpreetsingh-019" target="_blank">Author</a>
</p>

<br>

## :dart: About ##
Web scraping of Food Grab website using XHR requests

## :sparkles: Approach ##

### Exploring website and networking tab
- I visited the website, checked through html elements, founded only about calculated distance between the 2 location , but no geolocation, opened devtools, checked all the api calls and requests made through the website, got one request, name starting from collect, which initiated the call to search for the given location. Nothing about restaurants.
- so when i click loadmore button in the lower portion of the page [Food Grab](https://food.grab.com/sg/en/restaurants) we can see a request named search, from this, request was sent to "https://portal.grab.com/foodweb/v2/search"

- so if we go to response section you can see in preview, one response 
```
{searchResult: {searchID: "09df6af6b3a148de8deea8d12c10dedb", totalCount: 283,…}}"
```

- clicking on it gave us some more values and details in form of json object,
- under searchResult, one object named searchMerchant was there , having 8 sub objects

where 4-C2MUTVCJJAEKGT is ‍restaurant_id‍
```
searchMerchants: [{id: "4-C2MUTVCJJAEKGT", address: {name: "Kok Sen Restaurant - Keong Saik Road"},…},…]
0: {id: "4-C2MUTVCJJAEKGT", address: {name: "Kok Sen Restaurant - Keong Saik Road"},…}
1: {id: "4-C2KTCBVKE8BYG2", address: {name: "Kaffe & Toast - Outram"},…}
2: {id: "4-CY3KNAKEPE4XEX", address: {name: "Pizza Hut - Kreta Ayer Road"},…}
3: {id: "4-CZDXJJMZBB61N2", address: {name: "Little Elephant SG Thai Bistro - Tiong Bahru Estate"},…}
4: {id: "4-C3NJVU2EC7WWVN", address: {name: "Unagi Tei - 1 Keong Saik Road"},…}
5: {id: "4-C3A3MAWVLU2JHE", address: {name: "Wildfire Burgers - Keppel Road"},…}
6: {id: "4-C2U1JTCHDEK2LE",…}
7: {id: "4-C3KHMBTTNTEHUA", address: {name: "Let's KINN Thai - Tanjong Pagar Plaza"},…}
```

Opening any of this gave us a detailed overview of all details of restaurants that appeared in the load more request :
```
0: {id: "4-C2MUTVCJJAEKGT", address: {name: "Kok Sen Restaurant - Keong Saik Road"},…}
address: {name: "Kok Sen Restaurant - Keong Saik Road"}
businessType: "FOOD"
chainID: "01_Kok_Sen"
chainName: "Kok Sen"
estimatedDeliveryTime: 30
id: "4-C2MUTVCJJAEKGT"
latlng: {latitude: 1.28032191, longitude: 103.8415906}
merchantBrief: {cuisine: ["Chinese", "Seafood", "Noodles", "MICHELIN Bib Gourmand"],…}
merchantStatusInfo: {status: "CLOSED_SCHEDULE_AVALIABLE", statusText: "Closed.", tipText: "Order for later."}
metadata: {origin: ["NonKeyword::", "Search"],…}
```

so 
    - ["searchResults"]["searchMerchant"]["address"]["name"] will give us name of restaurant
    - ["searchResults"]["searchMerchant"]["latlng"]["latitude"] will give us latitude of restaurant
    - ["searchResults"]["searchMerchant"]["latlng"]["longitude"] will give us longitude of restaurant


- we can get name, address, latitude and longitude from here, by saving all responses from the search request triggered whenever we click loadmore button, with python, but insure all of the http headers must be same with http headers that in the chrome dev tools


### :desert_island: Plan 1 
- So since i have to find data from the search request, i have used selenium wire for this for capturing the XHR request, i have used chrome driver as browser.
- Solution Desgin 
```
1. Load the python libraries needed
2. get location from user where we want to get details of nearby restaurants
3. define a function load_more - Load the food.grab.com page and automatically activate the "Load More"  button in loop until the page contains all the restaurants in the given area
4. define check response - Use driver to fetch all request made while loading the website,  check for request on "portal.grab.com/foodweb/v2/search" and then decode the data and store it in json format in json_data.
5. define function to  get details of restaurant - remove all the extra and keep name, address and location only, then store it in a dictionaries.
```
- Given a base_url, capture all restaurants (based on user's submitted location, e.g., singapore) name, address, latitude & longitude
by intercepting grab-foods food-web Post request. portal.grab.com/foodweb/v2/search was founded by manually inspecting all XHR made by grab-foods, using chrome dev tools.

### :stop_sign: Difficulty faced during doing this 
- I found it difficult to pass the location to search bar and then press enter so as to make a request for given location,
   reason being late response of the autocomplete search api.
- Had to take the other path of generating custom request for each location which was made after clicking search button :
                - https://food.grab.com/sg/en/restaurants?search=<location name>  

- Searching for random locations might give few or 0 restaurants as ans because it wont find any nearby location, 
- Slow internet can result in failure of the load more button to load on time, so script will skip it. We have to re run the script in that case
- making a new request in less than 5 minutes can result in requests getting blocked and give Error 403 
  

- I have taken help for various resources and documentation since i have to use selenium wire for this and get data from XHR request.

### :trophy: Using obstacle as a power
- Since i mentioned autocompelete search api was an obstacle in start, i tried to understand its response generated from this post request : 
  "https://food.grab.com/v1/autocomplete?component=country:SG&language=en&transportType=0&keyword=" +location + "&limit=10"
  gives the details of top 8 locations as per suggested by the api and their details.

- These suggestions will counter the random location search while making the requests.
- Request to precise or suggested location resulted in More details of restaurants.
- So Upgradation in approach 1 will give more and better results : 

## :sparkles: Approach 2 : implementing new things

- Solution Design
  
```
  1. Load the driver
  2. Get location input from user
  3. make request to autocomplete search api, fetch name and address of top 8 suggested places and save them in a list :  suggested_location
  4. Loop over all the locations in this suggested_location list :
                  - For each location in this list, make a call to (https://food.grab.com/sg/en/restaurants?search=<location name>)
  5. Same work as approach 1, but now over 8 places instead of 1.
  6 saving response from each request in <location name>.csv file

```
  
## :dart: :golf: Results :
  Shockingly,
  - Precise or accurate locations give more restaurants data
  - Now we have data of 8 suggested places from one keyword only, in one run only.
  Data from **approach 1** could give sometimes 400-500 restaurants,
  Data from **approach 2** can give atleast 1500-2000+ locations at once.
  
  We have details of all locations individually, with the last file saved having details of all restaurants from the 1 search itself,
  so all scraped data in one run can be found in the file named with the last location searched.
  
  we can find data of individual locations also by subtracting the common entries in the currenmt file and the previos name saved file
  
 This script will take time to make a complete one run successfully because we have to wait for atleast 5 mins before making a new request for new location, 
  or else the request will be blocked.
  Sometimes slow internet, or few locations in that search can also be reason of few or no entries in file. just rerun to check for it.
  
## Demo : 
  check difference in the output of
  - [Approach 1 result : 520 entries ](https://github.com/simarpreetsingh-019/scrap_grab/blob/main/The%20Stamford%2C%20Raffles%20City.csv)
  - [Approach 2 results : 3010+ entries](https://github.com/simarpreetsingh-019/scrap_grab/blob/main/Capitol%20Singapore%2C%2013%20Stamford%20Road%2C%20Singapore%2C%20178905.csv)
  
## :rocket: Technologies ##

The following tools were used in this project:

- [Python](https://www.python.org/)
- [Selenium](https://pypi.org/project/selenium-wire/)
- [Chromedriver](https://chromedriver.chromium.org/)

## :white_check_mark: Requirements ##

Before starting :checkered_flag:, you need to have [Git](https://git-scm.com) and [python](https://python.org/) installed.

## :checkered_flag: Starting ##

```bash
# Clone this project
$ git clone https://github.com/{{YOUR_GITHUB_USERNAME}}/scrap_grab

# Access
$ cd scrap_grab

# Setup virtual environment
$ python3 -m venv venv

# Install dependencies
$ pip install -r requirements.txt

# Run the project
$ run main.py file 

```

## :memo: License ##

This project is under license from MIT. For more details, see the [LICENSE](LICENSE.md) file.


Made with :heart: by <a href="https://github.com/simarpreetsingh-019" target="_blank">Simarpreet Singh</a>

&#xa0;

<a href="#top">Back to top</a>
