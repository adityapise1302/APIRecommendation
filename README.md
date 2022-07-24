## Inspiration
Every time I have an idea for a project I like to check whether there are APIs available to reduce my effort and the timeline for completion of the project. I realized that all my fellow hackers would be facing the same problem of navigating on the web endlessly to find the perfect API for their project. To solve this problem I designed a web application to help my fellow hackers find the perfect API and save their time and in-turn allow them focus on their projects' other aspects.
## What it does
Provided the right query for the description of the API you need for your project it lists all the available APIs satisfying the provided description. For example if you want to create a weather forecast app and you search "weather" it will provide you with a list of APIs related to weather.
## How we built it
I used SQLite to create a database of the api name, description and the website url. With the help of BeautifulSoup I scraped a github repository, listing all the useful APIs, for the api name, description and website url. The website was built using HTML, CSS, BootStrap and Flask. The full text search queries were performed using fts5 virtual table module of SQLite for providing the best results for the given search query.
## Challenges we ran into
1. Figuring out how to use Full Text Search Queries of SQLite.
2. Creating SQLite database and querying.
3.  Ordering the APIs relevant to the search query.
## Accomplishments that we're proud of
1. The website is able to perform various search queries and provide relevant results based upon the provided search query.
2. Using all the functionalities of SQLite efficiently to provide relevant results.
## What we learned
1. How to use SQLite for full text search.
2. WebScraping with BeautifulSoup.
## What's next for API On The Go
1. Improve the search results based on semantic analysis of the search query.
2. Improve the UI of the website.
