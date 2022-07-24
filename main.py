from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
import sqlite3
from bs4 import BeautifulSoup
import requests
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap(app)
conn = sqlite3.connect("apis-collection.db", check_same_thread=False)
cursor = conn.cursor()


# cursor.execute(""" CREATE TABLE api_info(id integer, api text, desc text, url text)""") #Create Table
# conn.execute(""" CREATE VIRTUAL TABLE api_info_virtual USING fts5(api, desc, url)""") #Create Virtual Table
# conn.commit()

class SearchForm(FlaskForm):
    query = StringField(label="Your Idea: ", validators=[DataRequired()])
    search = SubmitField(label="Search")


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

@app.route("/", methods=['GET', 'POST'])
def request_apis():
    form = SearchForm()
    if form.validate_on_submit():
        query = request.values.get("query")
        list_apis = search_in_db(query)
        if len(list_apis) > 0:
            for api in list_apis:
                api_name = api[0]
                api_desc = api[1]
                api_website = api[2]
                api = f"API - {api_name} \n Description - {api_desc} \n Website - {api_website}"
            return "Success", 200
        else:
            return "Not Found", 404
    return render_template("index.html", form=form)


def search_in_db(search_query: str) -> list:
    list_searches = conn.execute('''SELECT * FROM api_info_virtual WHERE desc MATCH ? ORDER BY rank''',
                                 [search_query.replace(" ", " OR ")])
    list_searches = list(list_searches)
    return list_searches


if __name__ == '__main__':
    app.run(debug=True, port=8000)
