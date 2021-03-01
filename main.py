import requests
from twilio.rest import Client

from api_keys import ApiKeys

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

keys = ApiKeys()

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": keys.stockapi
}
news_parameters = {
    "q": COMPANY_NAME,
    "apikey": keys.newsorgapi
}
response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stocks_data = response.json()

stock_dict_list = [value for (key, value) in stocks_data.items()]
stock_dict_list = stock_dict_list[1]

dates = [key for (key, value) in stock_dict_list.items()]  # list of dates

yesterday_closing_price = float(stock_dict_list[dates[0]]["4. close"])

day_before_yesterday_closing_price = float(stock_dict_list[dates[1]]["4. close"])

closing_diff = abs(yesterday_closing_price - day_before_yesterday_closing_price)

diff_percent = round((closing_diff / float(yesterday_closing_price)) * 100)
up_down = None
if diff_percent > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

# diff_percent = 7  # for testing remove it after testing
if diff_percent > 5:
    response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    response.raise_for_status()
    news_data = response.json()["articles"]
    # news_filter_data = [item[:3] for item in news_data]
    first_three_news = news_data[0:3]
    print(first_three_news)

    headlines = [title["title"] for title in first_three_news]
    description = [description["description"] for description in first_three_news]
    client = Client(keys.twilioaccountsid, keys.twilioauthtoken)
    for i in range(0, 3):
        message = client.messages.create(
            body=f"{COMPANY_NAME}{up_down}{diff_percent}% Headline:{headlines[i]}?. Brief: {description[i]}",
            from_=keys.twiliophonenumber, to=keys.twiliotophonenumber)




