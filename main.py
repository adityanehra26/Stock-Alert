import smtplib
import requests
import html

STOCK = "TSLA"  # checking stock of tesla inc.
COMPANY_NAME = "Tesla Inc"

# ==================================================================================================================== #

# STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_api = " "    # api from https://www.alphavantage.co/
url = "https://www.alphavantage.co/query"
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "outputsize": "compact",
    "apikey": "---api key0-----"
}

response = requests.get(url=url, params=parameters)
response.raise_for_status()   # incase of exception

daily_stock = response.json()["Time Series (Daily)"]
daily_stock_list = [value for (key, value) in daily_stock.items()]

yesterday_price = daily_stock_list[0]['4. close']
day_before_yesterday_price =daily_stock_list[1]['4. close']

fluctuation = (float(yesterday_price) - float(day_before_yesterday_price))

# ==================================================================================================================== #

# STEP 3: Use https://www.twilio.com OR send mail
# Send a seperate message with the percentage change and each article's title and description to your phone number. 
def send_mail(fluctuation="", message=''):
    my_email = " " #"---sender mail---"
    send_to = " " #"---receiver mail---"
    password = " "  #"---type sender password---"
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()  # transport layer security
        connection.login(user=my_email, password=password)
        connection.sendmail(from_addr=my_email, to_addrs=send_to, msg=f"Subject: TSLA: {fluctuation}\n\n"
                                                                      f"{message}\n")

# ==================================================================================================================== #

# --------------------- Checking Fluctuation For sending Mail ------------------- #

if abs(fluctuation) > 5:
    fluctuation_per = f"{round((fluctuation*100)/float(yesterday_price))}%"
    print(fluctuation_per)

    # ================================================================================================================ #
    # STEP 2: Use https://newsapi.org
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.
    news_api = "apikey"
    news_url = "https://newsapi.org/v2/everything"
    news_params = {
        'language': 'en',
        'qInTitle': COMPANY_NAME,
        "apiKey": " "  #"---api key for newsapi---"
    }
    news_response = requests.get(url=news_url, params=news_params)
    news_article = html.unescape(news_response.json())['articles'][:3]

    msg = f"Article 1\nHeadline: {news_article[0]['title']}\nBrief: {news_article[0]['description']}\n\n" \
          f"Article 2\nHeadline: {news_article[1]['title']}\nBrief: {news_article[1]['description']}\n\n" \
          f"Article 3\nHeadline: {news_article[2]['title']}\nBrief: {news_article[2]['description']}\n\n"
    send_mail(fluctuation_per, msg)


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

