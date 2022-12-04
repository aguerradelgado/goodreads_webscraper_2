import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, session, redirect, url_for, session
from flask_session import Session
import sqlite3
import datetime
import time



app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

#for db
app.secret_key = "secret key"

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# Dictionary of Headers to send with the Request.
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'}

#headers = {
 #       'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) Gecko/20100101 Firefox/78.0',
  #      'Accept-Language': 'en-US,en;q=0.5'}

# Defining at the module level
books = ""
giveaway_titles = ""

# Lists to pass to html
error = []
books_give = []
titles_give = []

def book_page(searchterms):
    """
    Load main page based on book title entered
    :param searchterms:
    :return: url of book page
    """
    searchterms = "+".join(searchterms.split())
    url =  f'https://www.goodreads.com/search?q={searchterms}'
    r = urllib.request.urlopen(url).read()
    soup = BeautifulSoup(r, 'html.parser')
    link = soup.find('a', class_='bookTitle').get('href')
    url = f'https://www.goodreads.com/{link}'
    return url


@app.route('/')
def home():
    # check if the users exist or not
    if not session.get("name"):
        # if not there in the session then redirect to the login page
        return redirect("/login")
    return render_template('index.html')

@app.route("/login", methods=["POST", "GET"])
def login():
    # if form is submited
    if request.method == "POST":
        # record the user name
        session["name"] = request.form.get("name")
        # redirect to the main page
        return redirect("/")
    return render_template("login.html")


@app.route('/index', methods=["POST"])
def index2():
    author = ""
    genre = ""
    cover = ""
    description = " "
    title = " "
    if request.method == 'POST':
        try:
            book_input = request.form["book-name"]
            session["book_input"] = book_input
            url = book_page(book_input)
            r = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(r, 'html.parser')

            titleNauthor = (soup.title.contents[0]).split('by')  # can consistently get title and author from this
            author = titleNauthor[1].strip() #author name
            title = titleNauthor[0].strip()
            session['title'] = title #we need this so the book titles are consistent and there is no redundancy
            session["author"] = author

            # ------------- generate smaller subsets of html to look through ------------------------ #
            b_tag = soup.body
            span_tag = soup.body.span
            a_tag = soup.body.a
            #-------------------------get description ---------- -------------------------------------#
            description = soup.find('div', {'id': 'description'}).get_text().split("\n")
            description = description[2]
            session["description"] = description
            # ------------------------------- get genre --------------------------------------------- #
            for b in b_tag.children:
                try:
                    genre = soup.find('a', class_="actionLinkLite bookPageGenreLink").get_text()
                except AttributeError as err:
                    genre = soup.find('span', class_="u-visuallyHidden").get_text()
                session["genre"] = genre
            # ------------------------------------ get rating --------------------------------------- #
            for s in span_tag.children:
                rating = soup.find('span', {'itemprop': 'ratingValue'}).text.strip()
                session["rating"] = rating
            # ---------------------------------- get cover ------------------------------------------ #
            for a in a_tag:
                image = soup.find('img', {'id': 'coverImage'})
                cover = image['src']
                session["cover"] = cover
            # ----------------------------- get Giveaway titles--------------------------------------#
            for b in b_tag.children:
                u = soup.find('a', class_="actionLinkLite bookPageGenreLink").get('href')
            page = urllib.request.urlopen(f'https://www.goodreads.com/{u}').read()
            poup = BeautifulSoup(page, 'html.parser')  # poup, not to be mistaken with their prettier sister, soup who is the html of the first page

            titles = poup.find_all('a', class_='bookTitle')
            titles_give = []
            for i in titles:
                titles_give.append(i.get_text())
            session["titles_give"] = titles_give
            #---------------------------------- Get giveaway covers ----------------------------------#
            book = poup.find_all("img", class_="bookCover")
            books_give = []
            for element in book:
                books_give.append(element.attrs['src'])
            session["books_give"] = books_give

        except:
            error.append("Book not Found")
        #------------------------------- Put new search result in DB ---------------------------------#
        conn = get_db_connection()
        try:
            if session["title"] not in (conn.execute("Select Title from BookTable")):
                conn.execute('INSERT INTO BookTable (Title, Author, Genre, Cover) VALUES (?, ?, ?, ?)',
                             (title, author, genre, cover))
                conn.commit()
                conn.close()
        except sqlite3.IntegrityError as bookexists:
            return redirect("/result")
        return redirect("/result")

@app.route("/result", methods=('Get', 'POST'))
def result():
    if request.method == 'POST':
        print("button clicked?????")
        session["tbr"].append(session["title"])
        print(session["tbr"])

    return render_template("result.html", book_input=session["title"], authors=session["author"], image=session["cover"],
                           ratings=session["rating"], books=session["books_give"], words=session["titles_give"], description=session["description"], tbr=session["tbr"])

@app.route("/logout")
def logout():
    if request.method == 'POST':
        session["name"] = None
        session["tbr"] = []
        return redirect("/")


@app.route('/shelf', methods=('GET', 'POST'))
def shelf():
    conn = get_db_connection()
    users = conn.execute('Select * FROM user').fetchall()
    TBRs= conn.execute('Select * FROM TBR').fetchall()
    Books = conn.execute('Select * FROM BookTable').fetchall()
    conn.close()
    return render_template('shelf.html', Books=Books)

if __name__ == '__main__':

    app.run(debug=True, port=5011)

