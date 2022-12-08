# Book-Scraper Website

# Overview
A flask-based web application that webscrapes [Goodreads](https://www.goodreads.com/) to find tags that contains information such as author, current giveaways for related genre, and ratings. The user enters the title of the book they want to search for, and the corresponding results are displayed. 

# Built With
<img width="100" src="https://user-images.githubusercontent.com/68759170/206540118-bf6354fb-87b4-4fda-802d-9f8b9a223f07.svg">  <img width="100" src="https://user-images.githubusercontent.com/68759170/206544782-ce9dd16f-73ce-4624-b62e-16b38f40eb3b.png"><img width="150" src="https://user-images.githubusercontent.com/68759170/206543551-37190acc-0850-4f9b-a568-466a492ba27e.png">


# Demo

![Dec-08-2022 14-45-06](https://user-images.githubusercontent.com/68759170/206552647-d7cad65f-81a8-4a27-ab7e-55e7d4b21cb0.gif)




# Purpose:
Allows user to search through Goodreads for book recommendations based off the book of their choosing. User will be able to add the books to their cart, where they can choose to export, as am xml file. This will provide the user with the list of books they want, along with the link to purchase the book at Barnes and Noble. 

# MVP Requirements:

1.	Create a backend with enough tables to hold shopping cart information for user – json-flat file, SQLite- flat files tables
2.	Have main page where user can search for book recommendations. Recommendations gathered from Goodreads. 
3.	Have “add to cart” button that will push information to backend and hold for shopping cart 
4.	Have “Download Shopping Cart” button for user to download xml of shopping cart information
5.	Aesthetically pleasing front end design
6.  Add error checking (eg user enters non-existing book title)

# Potential Features/Upgrades:

1.	Adding sorting (eg, sort books by author, genre, ratings)
2.	Create own recommendations using Affinity or Market Basket analysis 
3.	Incorporate better scrapping methods 
4.	Use Goodreads API to allow users to synch to their Goodreads account
5.	Use Product API to allows users to add to carts on Amazon
6.	STMP

