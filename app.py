import urllib.request
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, session, redirect, url_for, session
from flask_session import Session
import sqlite3
import datetime
import time

# comment for testing

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


"""def goodreads_description(soup):
    
    :param soup: 
    :return: 
    """"""
    Scrape info about book
    :param soup:
    :return: 
    

    description = soup.find('div', class_="DetailsLayoutRightParagraph__widthConstrained").get_text()
    return description
"""


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
    if request.method == 'POST':
        try:
            book_input = request.form["book-name"]
            session["book_input"] = book_input
            url = book_page(book_input)
            r = urllib.request.urlopen(url).read()
            soup = BeautifulSoup(r, 'html.parser')

            titleNauthor = (soup.title.contents[0]).split('by')  # can consistently get title and author from this
            author = titleNauthor[1].strip() #author name
            session["author"] = author

            # ------------- generate smaller subsets of html to look through ------------ #
            b_tag = soup.body
            span_tag = soup.body.span
            a_tag = soup.body.a
            # ------------------------ get genre -------------------------------- #
            for b in b_tag.children:
                try:
                    genre = soup.find('a', class_="actionLinkLite bookPageGenreLink").get_text()
                except AttributeError as err:
                    genre = soup.find('span', class_="u-visuallyHidden").get_text()
                session["genre"] = genre

            """
            -- desc -- not working but AHHHHHHHH help 
            for b in b_tag.children:

                description = soup.find('div', class_="TruncatedContent").get_text()
                session["description"] = description
                print(session["description"])
               
            """
            # get rating
            # ------------------------ get rating -------------------------------- #
            for s in span_tag.children:
                rating = soup.find('span', {'itemprop': 'ratingValue'}).text.strip()
                session["rating"] = rating
                # get cover
            # ------------------------ get cover -------------------------------- #
            for a in a_tag:
                image = soup.find('img', {'id': 'coverImage'})
                cover = image['src']
                session["cover"] = cover
            #for b in b_tag:
            #    description = soup.find('span', class_="Formatted").get_text()
            #    print(description)
            # ------------------ get Giveaway titles-----------------------------#
            for b in b_tag.children:
                u = soup.find('a', class_="actionLinkLite bookPageGenreLink").get('href')
            page = urllib.request.urlopen(f'https://www.goodreads.com/{u}').read()
            poup = BeautifulSoup(page, 'html.parser')  # poup, not to be mistaken with their prettier sister, soup who is the html of the first page

            titles = poup.find_all('a', class_='bookTitle')
            titles_give = []
            for i in titles:
                titles_give.append(i.get_text())
            session["titles_give"] = titles_give
            #----------------- Get giveaway covers start ---------------------------#

            book = poup.find_all("img", class_="bookCover")

            books_give = []
            for element in book:
                books_give.append(element.attrs['src'])
            session["books_give"] = books_give
            # ----------------- Get giveaway covers start ---------------------------#

            #description = goodreads_description(soup)
            # session["description"] = description
            #print(description)

        except:
            error.append("Book not Found")

        conn = get_db_connection()
        if book_input not in (conn.execute("Select Title from Book")):
            conn.execute('INSERT INTO book (Title, Author, Genre, Cover) VALUES (?, ?, ?, ?)',
                         (book_input, author, genre, cover))
            conn.commit()
            conn.close()
        else:
            print("In Book DB")
        return redirect("/result")

@app.route("/result", methods=('Get', 'POST'))
def result():
    if request.method == 'POST':
        print("button clicked?????")
        session["tbr"].append(session["book_input"])
        mask = session["tbr"]
        session["tbr"] = mask
        print(session["tbr"])

    return render_template("result.html", book_input=session["book_input"], authors=session["author"], image=session["cover"],
                           ratings=session["rating"], books=session["books_give"], words=session["titles_give"], tbr=session["tbr"])
# tbr=session["tbr"]


@app.route("/logout")
def logout():
    session["tbr"] = []
    session["name"] = None
    return redirect("/")


@app.route('/shelf', methods=('GET', 'POST'))
def shelf():
    conn = get_db_connection()
    users = conn.execute('Select * FROM user').fetchall()
    TBRs= conn.execute('Select * FROM TBR').fetchall()
    Books = conn.execute('Select * FROM book').fetchall()
    conn.close()
    #users = users, TBRs = TBRs,
    return render_template('shelf.html', Books=Books)

if __name__ == '__main__':

    app.run(debug=True, port=5000)

