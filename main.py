from flask import Flask, request
import sqlite3
from bs4 import BeautifulSoup
import requests
import os
from twilio.rest import Client

account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
client = Client(account_sid, auth_token)

app = Flask(__name__)

conn = sqlite3.connect("apis-collection.db")
cursor = conn.cursor()


# cursor.execute(""" CREATE TABLE api_info(id integer, api text, desc text, url text)""") #Create Table
# conn.execute(""" CREATE VIRTUAL TABLE api_info_virtual USING fts5(api, desc, url)""") #Create Virtual Table
# conn.commit()

def scrape_api_data():
    URL = "https://github.com/public-apis/public-apis/blob/master/README.md"
    api_page = requests.get(URL)
    soup = BeautifulSoup(api_page.content, "html.parser")
    tables = soup.find_all("table")
    for table in tables:
        tbody = table.find_all("tbody")
        for body in tbody:
            tr = body.find_all("tr")
            for row in tr:
                url = row.find("a").get("href")
                text = row.getText().split('\n')
                api = text[1]
                desc = text[2]
                cursor.execute("INSERT INTO api_info_virtual VALUES (?, ?, ?)", (api, desc, url))
                conn.commit()


# scrape_api_data()


@app.route("/request_apis", methods=['POST'])
def request_apis():
    query = request.values.get('Body')
    from_wa = request.values.get('From')
    to_wa = request.values.get('To')
    list_apis = search_in_db(query)
    if len(list_apis) > 0:
        message = "\n".join(list_apis)
        send_message = client.messages.create(
            body=f"Following are your suggested APIs: \n{message}",
            from_=f'whatsapp:{to_wa}',
            to=f'whatsapp:{from_wa}'
        )
        return "Success", 200
    else:
        send_message = client.messages.create(
            body=f"Sorry couldn't find the APIs for provided idea. 😔",
            from_=f'whatsapp:{to_wa}',
            to=f'whatsapp:{from_wa}'
        )
        return "Not Found", 404


def search_in_db(search_query: str) -> list:
    list_searches = conn.execute('''SELECT * FROM api_info_virtual WHERE desc MATCH ? ORDER BY rank''',
                                 [search_query.replace(" ", " OR ")])
    list_searches = list(list_searches)
    return list_searches


if __name__ == '__main__':
    app.run(debug=True)
