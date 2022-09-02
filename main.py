import os

from bs4 import BeautifulSoup
import requests
import smtplib

DESIRED_PRICE = 150.00
ITEM_LINK = "https://www.amazon.com/Logitech-Tenkeyless-Lightspeed-Mechanical-LIGHTSYNC/dp/B085RFFC9Q/ref"

# Setting up smtplib to send emails
my_email = os.environ.get('EMAIL')
password = os.environ.get('PASSWORD')

# Setting Up Beautiful Soup API request
response = requests.get(ITEM_LINK,
                        "=sr_1_13?crid=22AOXYMHS9SPY&keywords=logitech+g&qid=1662104958&sprefix=logitech+g%2Caps%2C91"
                        "&sr=8-13",
                        headers={"User-Agent": "en-US,en;q=0.9",
                                 "Accept-Language": "text"})

# Parsing Beutiful Soup Data
yc_web_page = response.text

soup = BeautifulSoup(yc_web_page, "html.parser")

# The Product you are trying to buy
item = soup.title.text

# The Price of the Item
price_tag = soup.find_all(name="span", class_="a-offscreen")

# takes the first result, get's it's text, removes the $ sign
price = float(price_tag[0].getText()[1:])
print(price)


def send_email(amazon_item, amazon_price):
    global my_email, password

    connection = smtplib.SMTP("smtp.gmail.com")
    connection.starttls()

    message = f"Your item on {amazon_item} is on sale at {amazon_price}. Hurry now before it changes!"

    connection.login(user=my_email, password=password)
    connection.sendmail(from_addr=my_email, to_addrs=my_email,
                        msg=f"Subject:Amazon Price Tracker\n\n{message}")
    connection.close()


if price < DESIRED_PRICE:
    send_email(item, price)
