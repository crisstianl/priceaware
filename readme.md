### Priceaware 
Web application developed Django and Python that help users search for a product in different online stores with one click.       
The application uses a windowless browser, called PhantomJS, to make GET requests on the web stores, but more importantly to execute the javascript code that renders Html elements.   
Then using beautifulsoup library the application parses the Html page and extracts elements containing product data.   
The above process is executed for every registered shop, but in a separate thread to flatten performance.  

### Usage:
Type a product name, code, model, manufacturer into the search form and press enter.        
The application returns the full name and description of the product, the price, and a link to the product.  
The results are ordered by the rating of each store.  
If you find a result that interests you, then you can save it in the cart and review it later.  
If you fancy a certain store, then you can tweak the algorithm to prioritise the search and return results from this store firstly or return more products.

### Instalation:
- create virtual environment, "virtualenv . -p python3"
- install django, "pip install django=2.2.4"
- install beautifulsoup, "pip install bs4"
- install url library, "pip install urllib3==1.25"
- install seleniun framework, "pip install selenium==3.11cd"
- copy the phantomJS executable into bin directory
- active virtual environment, "source bin/activate"
- start local server, "python src/manage.py runserver 8080"
- go to http://localhost:8080/priceaware

### Frameworks and libraries:
- python 3.7
- django 2.2
- beautifulsoup 4.8
- selenium 3.1
- urllib3 1.2
- phantomJS
