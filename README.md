# Book-Scraper Website

# Overview
A flask-based web application that webscrapes [Goodreads](https://www.goodreads.com/) to find tags that contains information such as author, current giveaways for related genre, and ratings. The user enters the title of the book they want to search for, and the corresponding results are displayed. 

## Purpose
Goodreads can be overwhelming for some so we created this project allows user to search through based off the book of their choosing, which will display only essential information, as well as current book giveaways based on the genre of selected book. It also allows users to easily add the books to their cart, where they can choose to export as a CSV. 


# Built With
<img width="100" src="https://user-images.githubusercontent.com/68759170/206540118-bf6354fb-87b4-4fda-802d-9f8b9a223f07.svg">  <img width="100" src="https://user-images.githubusercontent.com/68759170/206544782-ce9dd16f-73ce-4624-b62e-16b38f40eb3b.png"><img width="150" src="https://user-images.githubusercontent.com/68759170/206543551-37190acc-0850-4f9b-a568-466a492ba27e.png">


# Demo

![Dec-08-2022 14-47-53](https://user-images.githubusercontent.com/68759170/206553182-fd24c39b-804f-404e-ad56-52bfe5df884c.gif)

# How to use

### Login
Built with Flask sessions, the user is able to login so that book search and cart is stored for that session.

### Search
User will search the book of their choosing and click enter to load the results.

### Main Page Display
Once the requests have successfully gone through, the page will load with results respctive to the books searched in which the user can view. Scrolling will allow user to view the current giveaways. 

### TBR Cart
If user wants to read the searched book in the future, they can easily had to their TBR cart. Once satisified with cart, they can download as a CSV for their own future use. 

### History
User can view history of their viewed books (this still needs to be styled accordingly)

&nbsp; 

# Project Issues
- Race conditions (requests not going through each time)
- Git (branching, merge conflicts, etc)
- Database issues
- Responsive design

&nbsp;

# Contributions

| Name               | Role                                       |
| ------------------ | ---------------------------------------------- |
| Alessandra Guerra Delgado | DDL Schema, Flask sessions|
| Patricia Andreica       | Requests, Frontend development        |
| Grace Erickson        | Requests & fixing race conditions, building database       |     


&nbsp;

# MVP Requirements:

1.	Create a backend with enough tables to hold shopping cart information for user – json-flat file, SQLite- flat files tables
2.	Have main page where user can search for book recommendations. Recommendations gathered from Goodreads. 
3.	Have “add to cart” button that will push information to backend and hold for shopping cart 
4.	Have “Download Shopping Cart” button for user to download xml of shopping cart information
5.	Aesthetically pleasing front end design
6.  Add error checking (eg user enters non-existing book title)

&nbsp;

# Potential Features/Upgrades:

1. Host website
2. Implement data analysis:
    - Most popular books, Most added to tbr, Least popular
3. Connect to Goodreads API to allow user to connect to their account
4. Ability to share books on social media
5. Improve interface
6. Style the history page to shows the book covers
7. Add breadcrumbs (links to previous pages) 


