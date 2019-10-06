### Priceaware 
is web application developed in Python and Django that facilitates users to search for a product in different online stores with one click and have quick access to prices, details, stores.

### Usage:
The user types the product name, code, model, manufacturer into the search form whichs posts a request to the backend.    
The application uses a windowless browser, called PhantomJS, to make GET search requests on the web stores, but also to process dynamic javascript content.     
After the page source was loaded by PhantomJS, the application passes the source html to the Beautifulsoup library
and starts scrapping the divs, tables, hrefs for prices, names, links of the product. 
The above process repeats for every registered store, after which the results are rendered nicely to the end user.

### Instalation:
- create a virtual environment, virtualenv . -p python3
- install django, pip install django=2.2.4
- install beautifulsoup, pip install bs4
- install url library, pip install urllib3==1.25
- install seleniun framework, pip install selenium==3.11cd
- copy the phantomJS executable into bin directory.
- start your server.
- go to http://localhost:8000/priceaware

### Frameworks and libraries:
- python 3.7
- django 2.2
- beautifulsoup 4.8
- selenium 3.1
- urllib3 1.2
- phantomJS
