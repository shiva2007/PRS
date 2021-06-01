# import requests
import urllib.request,urllib.parse,urllib.error
from bs4 import BeautifulSoup
import ssl
class Query():
    def __init__(self):
        self.n =[]
        self.p = []
        self.r = []
        self.im = []
        self.u = []
    def display(self,names, prices, ratings,images,urls,site):
        flag = 1
        
        for name,price,rating, image,url in zip(names,prices,ratings,images,urls):
            
            self.n.append(name.text)
            self.p.append(price.text)
            self.r.append(rating.text)
            self.im.append(image.get('src'))
            if(site=="amazon"):
                self.u.append('https://www.amazon.in/'+url.get("href"))
            else:
                self.u.append('https://www.flipkart.in/'+url.get("href"))
            
            flag=0
        
        
        if flag:
            print("No results found")
        return self.n,self.p,self.r,self.im
    
    def amazon(self,item):
        print("amazon")
    
        #ignore ssl certificates error
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Amazon.............

        
        item = "+".join(item.split(" "))
        url = "https://www.amazon.in/s?k="+item+"&ref=nb_sb_noss_2"


        opener = urllib.request.Request(url)
        opener.add_header('User-agent', 'Mozilla/5.0')
        fhand = urllib.request.urlopen(opener,context = ctx).read()


        soup = BeautifulSoup(fhand,'html.parser') 
        names = soup.find_all(class_="a-size-medium a-color-base a-text-normal")
        prices = soup.find_all(class_="a-price-whole")
        ratings = soup.find_all(class_="a-icon a-icon-star-small a-star-small-4 aok-align-bottom")
        images = soup.find_all(class_="s-image")
        uri = soup.find_all(class_="a-link-normal a-text-normal")
        # print(uri)
        if(not names):
            names = soup.find_all(class_="a-size-base-plus a-color-base a-text-normal")
        self.display(names,prices,ratings,images,uri,site="amazon")
        print("amazon")
    
    def flipkart(self,item):
        print("flipkart")
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        url = "https://www.flipkart.com/search?q="+item+"&&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=on&as=off"
        # print(url)

        opener = urllib.request.Request(url)
        opener.add_header('User-agent', 'Mozilla/5.0')
        fhand = urllib.request.urlopen(opener,context = ctx).read()


        soup = BeautifulSoup(fhand,'html.parser') 
        self.names = soup.find_all(class_="_4rR01T")
        self.prices = soup.find_all(class_="_30jeq3")
        self.ratings = soup.find_all(class_="_3LWZlK")
        self.images = soup.find_all(class_="_396cs4 _3exPp9")
        self.uri = soup.find_all(class_="_1fQZEK")
        
        if(not self.names): 
            self.names = soup.find_all(class_="s1Q9rs")
          
        if(not self.names): 
            self.names = soup.find_all(class_="_2B099V")    

        if(not self.uri): 
            self.uri = soup.find_all(class_="s1Q9rs")

        if(not self.uri): 
            self.uri = soup.find_all(class_="_2UzuFa")

        if(not self.images): 
            self.images = soup.find_all(class_="_2r_T1I")
        # print(self.images)
        
        self.display(self.names,self.prices,self.ratings,self.images,self.uri,site="flipkart")

        
def filter_prices(names,prices,ratings,images,urls,item):
    filtered_p=[]
    filtered_r = []

    for name,price,rating, image,url in zip(names,prices,ratings,images,urls):
        if(price[0].isdigit()):
            k = float("".join(price.split(',')))
            filtered_p.append(k)
        else:
            filtered_p.append(float("".join(price[1:].split(','))))
        filtered_r.append(float(rating[:3]))
    # print(filtered_p,filtered_r)
    max_value = max(filtered_p)
    max_rating = max(filtered_r)
    overall_max=0
    # name=names[0]
    # price = prices[0]
    # rating = ratings[0]
    # url=urls[0]
    # image=images[0]
    for i in range(len(filtered_p)):
        filtered_p[i]=abs(100-(filtered_p[i]*100/max_value))
        filtered_r[i]=filtered_r[i]*100/max_rating
        if(filtered_r[i]+filtered_p[i]>overall_max and names[i].lower().startswith(item)):
            overall_max=filtered_p[i]+filtered_r[i]
            name=names[i]
            price = prices[i]
            rating = ratings[i]
            url=urls[i]
            image=images[i]
    return [name,price,rating,image,url]