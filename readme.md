# Welcome to SVwho! 
## SVwho is a simple Law & Order: SVU look-up app

I set out on this project to accomplish two simple goals:  First, I wanted to get some practice working with relational databases within a web application.  Second, I wanted to create a more streamlined experience for a task that I do regularly: figuring out where I know the special guest stars in Law & Order; SVU from. 

I got my data for this app via IMDB.  You can find that here: 
https://www.imdb.com/interfaces/

SVwho was built using Flask. The current version of the code is using the sqlite3 library to handle queries but I will likely need to refactor that to something else before I can host it somewhere. However, for my own personal use, sqlite3 is working just fine after I set up an index on one of the larger tables. 

On the front end, I utilized (and personalized) various components from uiverse.io to give the application a little bit of personality. 