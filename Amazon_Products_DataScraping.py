# Importing important libraries.
import requests as re    # To send and get http requests.
from fake_useragent import UserAgent   # To set headers in http requests to prevent scrap block or IP ban by mimicing a browser
from bs4 import BeautifulSoup as bs   # To convert get response to scrapable format
import pandas as pd   # To convert scrap data to dataframe
import time



# Ask Product Category & Name from user
while True:
    print("Select category: "
        "\n1. Electronics "
        "\n2. Fashion "
        "\n3. Food"
        "\n4. Beauty"
        "\nYour Choice: ",end="")
    ask=input().strip()
    if ask in ["1","2","3","4"]:        
        category=ask
        if ask=="1":
            product=input("\nEnter Electronics product name: ").lower()
            cat="Electronics"
            break
        if ask=="2":
            product=input("\nEnter Fashion product name: ").lower()
            cat="Fashion"
            break
        if ask=="3":
            product=input("\nEnter Food product name: ").lower()
            cat="Food"
            break
        if ask=="4":
            product=input("\nEnter Beauty product name: ").lower()
            cat="Beauty"
            break
    else:
        print("---Invalid input---\n\n")
        time.sleep(1)
time.sleep(1)



headers = {'User-Agent': UserAgent().random}   # Random User-Agent
response = ""
code=0

for i in range(1,6):
    print(f"Reading page {i}")
    time.sleep(1)
    url=f"https://www.amazon.in/s?k={product}&page={i}"
    resp = re.get(url, headers=headers)   # Send http Get request
    code=resp.status_code
    if resp.status_code == 200:
        response += resp.text  #Append the page HTML content
    else:
        print(f"Failed to fetch page {i}")
print("All pages read!")



# Checkpoint 1
if code==200:
    # Create a .html file in the name of the product and write the response for future use.
    with open(f"F:/Visual Studio/Webscraping/Amazon Products/Data/{cat}/{product}.html","w",encoding="utf-8") as f:   # Use your sys path
        f.write(response)
        print(f"{product} data from Amazon.in extract and write successful!\n")

    with open(f"F:/Visual Studio/Webscraping/Amazon Products/Data/{cat}/{product}.html","r",encoding="utf-8") as f:   # Use your sys path
        soup=bs(f.read(),'html.parser')   # Read and parse the data in html format. Create a soup object.
        time.sleep(3)
        print("Data parsed successful!\n", flush=True)



    # -+-+-+ MayDay +-+-+-
    #      .__(*)< (MEOW)
    #       \___)
    # ~~~~~~~~~~~~~~~~~~-->
    # If error in above code(Checkpoint 1),
    # Mark it as comment and use the below code(Checkpoint 2) to scrap from data saved offline
    # Do not change the identation
    # Amazon's data is/maybe dynamic
    # Incase of error with Amazon.in web result's backend code modified, I've provided some data of products
    # saved during testing of this code, that perfectly works.
    # Available offline data for "chocolate" "dryfruit" "iphone" "laptop" "namkeen" "pant" "realme phones" "shirt" "shoe"

  
# Checkpoint 2
#if True:
#    category="4"
#    cat="Beauty"
#    product="facewash"
#    with open(f"F:/Visual Studio/Webscraping/Amazon Products/Data/{cat}/{product}.html","r",encoding="utf-8") as f:   # Use your sys path
#            soup=bs(f.read(),'html.parser')   # Read and parse the data in html format. Create a soup object.
#            #time.sleep(3)
#            print("Data parsed successful!\n", flush=True)



    time.sleep(1)
    print("Scraping Data from search",end="", flush=True)
    for _ in range(5):
        time.sleep(0.5)
        print(".", end="", flush=True)
    time.sleep(1)



    def find_price(data):
        prices=data
        
        def get_price(pd):
            price=pd            
            # Checks if price section is available for each item fetched
            if price.find("div", class_="a-row a-size-base a-color-base"):
                price_details=price.find("div", class_="a-row a-size-base a-color-base")
            else:
                price_details=price.find("div", class_="a-row a-size-mini a-color-base")
            if price_details.find("span", class_="a-price-whole"):
                c_p=float(price_details.find("span", class_="a-price-whole").get_text().replace("₹","").replace(",",""))
                
                # Checks if original price is found for each item fetched
                org_p=price_details.find("span", {"data-a-strike": True})
                if org_p:
                    o_p=float(org_p.find("span", {"aria-hidden": True}).get_text().replace("₹","").replace(",",""))
                else:
                    # If not found, Current price is the Original price
                    o_p=float(price_details.find("span", class_="a-price-whole").get_text().replace("₹","").replace(",",""))
                    
            else:
                # If no price found
                c_p=0
                o_p=0
            return c_p,o_p

        if category=="1":
            return get_price(prices)
        else:
            c_p=[]
            o_p=[]
            for price in prices:
                c,o=get_price(price)
                c_p.append(c)
                o_p.append(o)
            return c_p,o_p



    # Extract data of Electronic Products
    if category=="1":
        # Dictionary to store data fetched
        data={"Product Name":[],"Details":[],"Current Price":[], "Original Price":[]}

        details=soup.find_all("div",class_="puisg-col-inner")
        for detail in details:
            # Extract Brand Name and Product Details
            if detail.find("div",{"data-cy":"title-recipe"}):
                title=(detail.find("div",{"data-cy":"title-recipe"})).find("h2").span.get_text().split()
                p=[]   # Store product name
                d=[]   # Store product details
                marker=1000   # Marks the loc of name-details divider
                for i in range(0,len(title)):
                    if i<marker:
                        if "(Refur" in title[i]: # Track the word (Refurbished)
                            p.append(title[i])
                        elif "," in title[i][len(title[i])-1] or ":" in title[i][len(title[i])-1]:   # replace char, store name and mark loc
                            p.append(title[i].replace(":", "").replace(",", ""))
                            marker=i
                        elif "(" in title[i][0] or "(" in title[i]:   # Store the word in details and mark loc
                            d.append(title[i])
                            marker=i
                        elif "|" in title[i] or "-" in title[i]:   # Skip this character and mark loc
                            marker=i
                        else:
                            p.append(title[i])
                    else:
                        d.append(title[i])

                data["Product Name"].append(" ".join(p))   # Append the product name to dictionary
                data["Details"].append(" ".join(d if d else "-"))   # Append the product details to dictionary

                # Extract Current Prices and Original Prices
                if detail.find("div",{"data-cy":"price-recipe"}):
                    data["Current Price"],data["Original Price"]=find_price(detail)
                else:
                    data["Current Price"].append(0)
                    data["Original Price"].append(0)



    # Extract data of Fashion Products
    if category=="2":
        # Dictionary to store data fetched
        data={"Brand":[],"Product Details":[],"Current Price":[], "Original Price":[]}
        # Extract Brand Name and Product Details
        details=soup.find_all("div",{"data-cy":"title-recipe"})
        for detail in details:
            data["Brand"].append(" ".join(i for i in detail.find("span", class_="a-size-base a-color-base puis-medium-weight-text").get_text().split()))
            data["Product Details"].append(detail.find("h2", {"aria-label": True})["aria-label"])
        
        # Extract Current Prices and Original Prices
        prices=soup.find_all("div",{"data-cy":"price-recipe"})
        data["Current Price"],data["Original Price"]=find_price(prices)



    # Extract data of Food Products
    if category=="3":
        # Dictionary to store data fetched
        data={"Product Name":[],"Details":[],"Current Price":[], "Original Price":[]}
        # Extract Product Name and Product Details
        details=soup.find_all("div",{"data-cy":"title-recipe"})
        for detail in details:
            title=(detail.find("h2")).span.get_text().split()
            p=[]
            d=[]
            marker=7
            for i in range(0,len(title)):
                if i<marker:
                    if "," in title[i][len(title[i])-1]:
                        p.append(title[i].replace(":", "").replace(",", ""))
                        marker=i
                    elif ")" in title[i][len(title[i])-1]:
                        p.append(title[i])
                        marker=i
                    elif "|" in title[i] or "-" in title[i]:
                        marker=i
                    else:
                        p.append(title[i])
                else:
                    d.append(title[i])
            
            data["Product Name"].append(" ".join(i for i in p))
            if d:
                data["Details"].append(" ".join(i for i in d))
            else:
                data["Details"].append("na")

        # Extract Current Prices and Original Prices
        prices=soup.find_all("div",{"data-cy":"price-recipe"})
        data["Current Price"],data["Original Price"]=find_price(prices)



    # Extract data of Beauty Products
    if category=="4":
        # Dictionary to store data fetched
        data={"Product Name":[],"Details":[],"Current Price":[], "Original Price":[]}
        # Extract Product Name and Product Details
        details=soup.find_all("div",{"data-cy":"title-recipe"})
        for detail in details:
            title=detail.find("h2",{"aria-label":True}).span.get_text(separator=" ").split()
            p=[]
            d=[]
            marker=1000
            for i in range(0,len(title)):
                if i<marker:
                    if "," in title[i][len(title[i])-1]:
                        p.append(title[i].replace(",", ""))
                        marker=i
                    elif ")" in title[i][len(title[i])-1]:
                        p.append(title[i])
                        marker=i
                    elif "|" in title[i]:
                        marker=i
                    else:
                        p.append(title[i])
                else:
                    d.append(title[i])
            
            data["Product Name"].append(" ".join(p))
            data["Details"].append(" ".join(d if d else "-"))

        # Extract Current Prices and Original Prices
        prices=soup.find_all("div",{"data-cy":"price-recipe"})
        data["Current Price"],data["Original Price"]=find_price(prices)



    print("\nData Scrapped!", flush=True)
    time.sleep(2)
    df=pd.DataFrame.from_dict(data)   # Transform data to pandas dataframe

    # Calculate the difference in price
    df["Less Amount"]=df["Original Price"] - df["Current Price"]

    # Calculate the discount
    df["Discount %"]=round(((df["Original Price"] - df["Current Price"]) / df["Original Price"]) * 100)

    # Show dataframe
    print(df)

    # Extract data in desired format
    df.to_excel(f"F:/Visual Studio/Webscraping/Amazon Products/Output/{cat}/Amazon-{product}.xlsx",index=False)   # Use your sys path

else:
    print("Couldn't fetch data from web due to scrap blocker or IP ban.\n")
