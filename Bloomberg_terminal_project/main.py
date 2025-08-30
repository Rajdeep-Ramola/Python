import requests
import emoji
from twilio.rest import Client
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY= "Your api key"
NEWS_API_KEY="Your api key"
TWILIO_SID="Your account sid"
TWILIO_AUTH_TOKEN="Your authorization token"

# Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print news related to that company

# Getting yesterday's closing stock price.
stock_params={
"function":"TIME_SERIES_DAILY",
"symbol" : STOCK_NAME,
"apikey":STOCK_API_KEY,
}
response=requests.get(STOCK_ENDPOINT,params=stock_params)
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yesterday_closing_price=yesterday_data["4. close"]


# Getting the day before yesterday's closing stock price
day_before_yesterday_data=data_list[1]
day_before_yesterday_closing_data=day_before_yesterday_data["4. close"]


# Find the positive difference between 1 and 2
difference=(float(yesterday_closing_price)-float(day_before_yesterday_closing_data))
up_down=None
if difference>0:
    up_down="⬆️"
else:
    up_down="🔻"



# Find the percentage difference in price between closing price yesterday and closing price the day before yesterday.
diff_percent=round((difference/float(yesterday_closing_price))*100)




# Using the News API to get articles related to the COMPANY_NAME
if abs(diff_percent)>1:
    news_params={
        "apiKey":NEWS_API_KEY,
        "qInTitle":COMPANY_NAME,
    }
    news_response=requests.get(NEWS_ENDPOINT,params=news_params)
    articles=news_response.json()["articles"]

    three_articles=articles[:3]

    #Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number.

    formatted_articles=[f"{STOCK_NAME}: {up_down}{diff_percent}% Headline:{articles['title']}. \n Brief:{articles['description']}" for articles in three_articles]

    #Send each article as a separate message via Twilio.
    client=Client(TWILIO_SID,TWILIO_AUTH_TOKEN)
    for article in formatted_articles:
        message=client.messages.create(
            body=article,
            from_="phone_no",
            to="My phone number"

    )


