# Amazon_Products_DataScraping
---
This project is a web scraper that collects product details from Amazon India using Python. Users can choose a product category (Electronics, Fashion, Food, or Beauty) and enter a product name. The script then searches Amazon, goes through multiple pages, and extracts details like product name, features, current price, original price, and discount percentage.

The project uses requests to send website requests and BeautifulSoup to read and extract useful information from the webpage. To avoid getting blocked by Amazon, it also includes a fake user agent that makes the script look like a real browser. If the website blocks the request, the script can also read saved data from previous runs.

After collecting the data, the project uses Pandas to organize and display it in a table format. It also calculates the price difference and discount percentage for each product. Users can see the results on the screen or save them in an Excel file for later use.
