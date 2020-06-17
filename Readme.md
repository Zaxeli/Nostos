# Nostos

Nostos is a web application that allows users to manage their interests and activities. It provides the user with different lists which hold the items for each type of activity or interest of theirs.

## Inspiration:

The idea to have a web-app for this purpose originated from a problem I myself faced in managing items I was interested in such as video games, movies, shows, books and tasks-to-do. For example, a video game would be available on Epic Game Store, PlayStation or XBox and not on Steam, the platform where I would maintain my gaming wishlist. This left room for me to forget about some interesting upcoming games and overlook them &mdash; a problem that could be solved my maintaining a single list for such things in an easily accessible way. Having a web-app for this purpose provides a single list which can be easily accessed from anywhere using the internet. 

## Running:

The web-app can be easily run by simply executing the run.sh file to run the Flask server. 

## Design:

The web-app is designed using a Database, a Flask server (back-end) and a front-end.

The front-end is designed using HTML, CSS, JS and Jinja templates. The pages are rendered and served by the Flask server upon accessing the correct web-app route.

The Flask server handles the different web-app routes and ensures the proper pages are served to the user as well as the proper data. 

The Database holds the records for the following:

- **User data:** The information about the users registered on the web-app. When a new user registers, their user data (username and password-hash) is stored and when a user logs in to the app, the credentials are verified using this data.

- **Activity data:** Each of the items that get added by the user is stored in the Database. The data about the item itself is stored in a seperate table and the data linking an the users to their respective items is stored in a separate table. For example, a user's books are stored in the following manner: The book name and reference links are stored in the 'Readables' table; whereas the User_ID (Foreign Key), the Read_ID (Foreign Key), its description and whether it is marked 'done' is stored in the 'Read' table.

### Database Schema:

The following tables are present in the Database.

**User:** 
- ID
- Username
- Hash_pwd (hash of the user's password)

**Readables:** 
- ID
- Name
- reference

**Read:** 
- User_ID
- Read_ID
- note (user-provided description for the item)
- done (whether the item is completed)

**Playables:** 
- ID
- Name
- reference

**Play:** 
- User_ID
- Play_ID
- note (user-provided description for the item)
- done (whether the item is completed)

**Watchables:** 
- ID
- Name
- reference

**Watch:** 
- User_ID
- Watch_ID
- note (user-provided description for the item)
- done (whether the item is completed)

**Doables:** 
- ID
- User_ID
- Name
- note (user-provided description for the item)
- reference
- done (whether the item is completed)

>The reason for splitting the data for every activity except the tasks ('Doables' table) is that initially, the intent was to store each item, such as a book or a movie, uniquely and not have repeats for the same item for each user. Each user to add that item could be recorded by simply referencing that item for the User using Foreign Keys.
>
>This feature can be included in later improvements.

## Implementation:

The web-app has been implemented using [app.py](app.py), Jinja templates and an SQLite DB.

### [app.py](app.py)

This file implements the Flask server which handles the back-end tasks such as interfacing with the DB to insert/delete/add data. It also handles rendering the Jinja template files and serving them to the user as needed. The [app.py](app.py) file also makes use of some supplementary code that is available in [helpers.py](helpers.py) such as for accessing DB and executing queries.

### Jinja templates

The html files have been made using Jinja templates for easier implementation.

### SQLite DB

The SQLite DB holds the records for the Users registered with the application as well as all the data of the items that they have entered.


## Layout:

The web-app, after logging in, provides the user with two sections wherein the various lists are maintained: the Study section, where reading and tasks are maintained; and the Leisure section, where games and movies are maintained. There is also the main home page called 'Fireplace' which is shown after logging in.

- Fireplace
- Study 
    - Library
    - Tasks
- Leisure
    - Play
    - Watch

### Page Naming

The different pages have also been given names for the purpose of taste. These names are have been concocted using different actual words from languages such as Arabic, Latin and Greek.

The etymology for these neologistic words are explained below:

- Nostos:
    
    From Ancient Greek *nóstos*, meaning 'returning home'.

- Nostos Estrea:
    
    Slightly transfigured form of Greek *εστία*, meaning 'hearth'. 

- Nostos Erudire:

    Modified from original *erudite*, meaning 'learned'.

- Nostos Erreiha:

    From Arabic راحة ( /raː.ħa/) meaning rest, recreation or leisure. Slightly modified form of the Arabic word.

- Nostos Ergon:

    Modification of Greek έργο, meaning task.

- Nostos Lectus:

    From Latin *lectus*, meaning 'read'.

- Nostos Ludens:

    From Latin *ludens*, meaning 'playing'.

- Nostos Videre:

    From Latin *videre*, meaning 'see'.



## Further improvements:

Further imporvements which could be done at a later time include the following features.

### Socialisation

In a later iteration of this web-app the feature to allow for messaging between Users and adding people as 'friends'.

### Edit item

Currently, once an item has been added by a User in any of their lists, its information cannot be modified. Although it is not a very complex thing to implement, it has been left out of the current implementation. It may be added at a later time.

### Multiple lists for an activity

The User has only one list for each type of activity available in the current implementation. A possible improvement could allow for multiple lists under a single activiity.

### Tags for items

The User would be able to add tags to their items and even create custom tags in this possible improvement.
