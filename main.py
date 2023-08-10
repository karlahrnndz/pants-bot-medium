# Import packages
from bs4 import BeautifulSoup
import requests
import datetime
import smtplib
import time
import os

# Define Constants
URL = "https://www.rei.com/product/206977/the-north-face-summit-soft-shell-pants-womens"
MY_SIZE = os.environ.get("MY_SIZE")
SENDER = os.environ.get("SENDER")
RECIPIENT = os.environ.get("RECIPIENT")
APP_PWD = os.environ.get("APP_PWD")


# Key functions
USER_AGENT = " ".join(["Mozilla/5.0 (Macintosh;",
                       "Intel Mac OS X 10_15_5)",
                       "AppleWebKit/537.36",
                       "(KHTML, like Gecko)",
                       "Chrome/84.0.4147.125",
                       "Safari/537.36"])
HEADER = {
    "User-Agent": USER_AGENT,
    "Accept-Language": "en-GB, en-US; q=0.9, en; q=0.8"
}


def scrape_sizes():
    response = requests.get(URL, headers=HEADER)
    soup = BeautifulSoup(response.content, "html.parser")
    selection = " ".join(["#product-color-size-component",
                          ".size-selector.size-color__size",
                          "button[data-ui='size-selector-button:available']",
                          "span[aria-hidden]"])

    return [ele.getText() for ele in soup.select(selection)]


def send_email():
    connection = smtplib.SMTP("smtp.gmail.com", port=587)
    connection.starttls()
    connection.login(user=SENDER, password=APP_PWD)
    connection.sendmail(from_addr=SENDER,
                        to_addrs=RECIPIENT,
                        msg=f"Subject:Pants Available!\n\n Pants: {URL}")
    connection.close()


# Execution
if __name__ == "__main__":  # Good practice
    while True:
        now = datetime.datetime.now()

        if now.hour in {10, 19} and now.minute in {0}:
            sizes = scrape_sizes()

            if MY_SIZE in sizes:
                send_email()

            time.sleep(60)  # For checking at most once per minute
