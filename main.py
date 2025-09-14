"""A website to display information about BTS's top songs."""
from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
# Connect my database file into my code
DATABASE = "bts_songs.db"


@app.route('/')  # Create a route for the home page
def render_home():
    """Render the home page."""
    return render_template("index.html")  # Render the index.html template


def create_connection(db_file):
    """Create a connection to the database file."""
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        return None


@app.route('/catalouge')  # Create a route for the catalouge page
def render_catalouge():
    """Render the catalouge page with all songs."""
    # Create a query to select relevant columns from the database
    query = "SELECT Ranking, Name, Album, SongStreams,\
          ReleaseDate, SongCover FROM top_songs"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # Execute the query
    cur.execute(query)
    songs_list = cur.fetchall()
    con.close()
    # Render the catalouge.html template with the list of songs
    return render_template("catalouge.html", song=songs_list)


@app.route('/song')  # Create a route for the song page
def render_song():
    """Render the song page with all songs."""
    # Create a query to select all songs from the database
    query = "SELECT Ranking, Name, ReleaseDate, SongCover FROM top_songs"
    con = create_connection(DATABASE)
    cur = con.cursor()

    # Execute the query
    cur.execute(query)
    songs_list = cur.fetchall()
    con.close()
    return render_template("song.html", song=songs_list)


@app.route('/album')  # Create a route for the album page
def render_album():
    """Render the album page with all albums and their songs."""
    con = create_connection(DATABASE)
    cur = con.cursor()
    # Create a query to select album names and their corresponding song names
    query = "SELECT Name, Album FROM top_songs"
    cur.execute(query)  # Execute the query
    album_list = cur.fetchall()

    album_dict = {}  # Dictionary to hold albums and their songs
    for name, album in album_list:
        if album not in album_dict:
            album_dict[album] = []
        # Append song names to the corresponding album
        album_dict[album].append(name)
    con.close()
    # Render the album.html template with the album dictionary
    return render_template("album.html", album_dict=album_dict)


def get_songs(song_type):
    """Get songs based on their type."""
    title = song_type.upper()
    # Create a query to select songs of a specific type
    query = "SELECT Name, Album, SongStreams, \
        ReleaseDate FROM top_songs WHERE type=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query, (title,))
    songs_list = cur.fetchall()
    con.close()
    return songs_list


# Create a route for the search results page
@app.route('/search', methods=['GET', 'POST'])
def render_search():
    """Render the search results page."""
    search = request.form['search']
    title = "Search for" + search
    # Create a query to search for songs by name, album, or release date
    query = "SELECT Ranking, Name, Album, SongStreams, ReleaseDate, \
        SongCover FROM top_songs WHERE Name LIKE ? \
            OR Album LIKE ? OR ReleaseDate LIKE ?"
    search = "%" + search + "%"  # Wildcards for partial matching
    con = create_connection(DATABASE)
    cur = con.cursor()
    # Execute the query with search parameters
    cur.execute(query, (search, search, search))
    songs_list = cur.fetchall()
    con.close()
    # Render the catalouge.html template with the search results
    return render_template("catalouge.html", song=songs_list, tag=title)


@app.route('/sort')  # Create a route for the sorted catalouge page
def render_sortpage():
    """Render the sorted catalouge page."""
    sort = request.args.get('sort')
    order = request.args.get('order', 'asc')  # Default order is ascending

    if order == 'asc':
        new_order = 'desc'  # Reverse the order for the next click
    else:
        new_order = 'asc'  # Reverse the order for the next click

    query = "SELECT Ranking, Name, Album, SongStreams, \
        ReleaseDate, SongCover FROM top_songs ORDER BY " + sort + " " + order
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query)
    songs_list = cur.fetchall()
    con.close()
    # Render the catalouge.html template with the sorted list of songs
    return render_template("catalouge.html",
                           song=songs_list, sort=sort, order=new_order)


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)
