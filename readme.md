Overview:
Priceaware is web application developed in Python and Django that allow users to search for a product 
in different online stores and collect all results into a nice table view.

Description:
The user types the product name, code, model, manufacturer into form input then posts a request to the webserver. 
On the server I use a windowless browser called PhantomJS to invoke GET search requests on the web stores and
to process javascript content. 
After the page containing the store results was loaded by PhantomJS, I pass the source html to the Beautifulsoup library
and start scrapping the divs, tables, hrefs for prices, names, links of the product.
The above process repeats for every registered store, after which the results are rendered nicely to the end user.

Frameworks and libraries:
- python 3.7
- django 2.2
- beautifulsoup 4.8
- selenium 3.1
- urllib3 1.2
- phantomJS

Instalation:
- create a virtual environment
- pip install django 2.2
- pip install bs4
- pip install urllib
- pip install selenium 3.1
- copy the phantomJS executable into bin directory.
- start your server.
- go to http://server_ip/priceaware
