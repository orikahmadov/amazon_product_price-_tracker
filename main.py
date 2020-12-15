import requests, os, time, smtplib
from bs4 import BeautifulSoup
from email.message import EmailMessage

"""THIS IS A PYTHON SCRIPT TO TRACK THE CHANGES OF PRICE OF THE  GIVEN AMAZON PRODUCT, IN ORDER TO GET THIS SCRIPT WORK JUST GET THE PORT AND SMTP EMAIL OF YOUR EMAIL PROVIDER 
IN THIS CASE MINE IS GMAIL SO I USE 465 PORT WHICH IS SECURED TSL AND I RECOMMEND YOU TO SAVE YOUR SMTP PASSWORD IN USER VARIABLE ENVIRONMENT DO NOT INCLUDE YOUR PASSWORD IN YOUR SCRIPT
"""


def automate_price_checking():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"}
    request = requests.get(
        "https://www.amazon.de/Razer-Externes-Grafikkarten-Geh%C3%A4use-Thunderbolt/dp/B07D4NBPBC/ref=sr_1_2?__mk_de_DE=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=2DNC57HKEXRQS&dchild=1&keywords=egpu+mit+grafikkarte&qid=1608071653&sprefix=egpu+mit+%2Caps%2C172&sr=8-2",
        headers=headers)

    soup = BeautifulSoup(request.content, "html.parser")
    product_title = soup.find("span", id="productTitle").text.strip()
    product_price = soup.find("span", id="priceblock_ourprice").text.strip()
    characters_filter = ["€", " "]
    a = set(characters_filter)
    filtered_price = "".join([c.replace(",", ".") for c in product_price if not c in a])
    final_price =  float(filtered_price)
    message_subject = product_title
    product_link =  request.url
    message_content =  f" New price for {product_title} is {final_price}€ \n\n Click the link to get the product {product_link}"
    to_email = "orkhan_ahmadov47@hotmail.com" 
    if round(final_price) < 290: #Setting the expected price of the product here to compare with the current price number
        print(f"Checked the given price and sending email to {to_email}")
        send_mail(to_email, message_subject, message_content)
    else:
        print("No changes in the price")

#Second Function which is logging to email to send a message
def send_mail(To, Subject, Content):
    try:
        with smtplib.SMTP_SSL(host =  "smtp.gmail.com", port =  465) as server:
            LOGIN =  os.getenv("EMAIL_ADDRESS")
            PASSWORD  =  os.getenv("PASSWORD")
            server.login(user =  LOGIN, password= PASSWORD)
            message =  EmailMessage()
            message["FROM"] =  LOGIN
            message["TO"] =  To
            message["Subject"] =  Subject
            message.set_content(Content)
            server.send_message(message)
    except:
        print("Message could not be sent sorry :(")
    else:
        print(f"Auto generated Message has been sent to {To}")


"""ADDING TIME TO RUN THE SCRIPT EVERY 24 HOURS """
while (True):
    automate_price_checking()
    time.sleep(86400) # 24 hours in seconds  to wait to run the script again















