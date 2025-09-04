from flask import Flask, render_template, request
import sqlite3
from sqlite3 import Error

app = Flask(__name__)
# Connect my database file into my code
DATABASE = "bts_songs.db"

@app.route('/')
def render_home():
    return render_template("index.html")

def create_connection(db_file):
    """
    Creates a connection to the database file
    """
    try:
        connection = sqlite3.connect(db_file)
        return connection
    except Error as e:
        print(e)
        return None
    
@app.route('/catalouge')
def render_catalouge():
    query = "SELECT Name, Album, SongStreams, ReleaseDate FROM top_songs"
    con = create_connection(DATABASE)
    cur = con.cursor()

    #Query the database
    cur.execute(query)
    songs_list = cur.fetchall()
    con.close()
    return render_template("catalouge.html", song=songs_list)

@app.route('/album')
def render_album():
    con = create_connection(DATABASE)
    cur = con.cursor()
    songs_list = cur.fetchall()
    print(songs_list)

    album_dict = {}
    for name, album in songs_list:
        if album not in album_dict:
            album_dict[album] = []
        album_dict[album].append(name)
    print(album_dict)
    con.close()
    return render_template("album.html", album_dict = album_dict)

def get_tags(song_type):
    title = song_type.upper()
    query = "SELECT Name, Album, SongStreams, ReleaseDate FROM top_songs WHERE type=?"
    con = create_connection(DATABASE)
    cur = con.cursor()

    cur.execute(query, (title,))
    songs_list = cur.fetchall()
    con.close()
    return songs_list

@app.route('/tags/<song_type>')
def render_tags(song_type):
    songs_list = get_tags(song_type)
    return render_template("tags.html", song=songs_list, tag=song_type)

@app.route('/search', methods=['GET', 'POST'])
def render_search():
    search = request.form['search']
    title = "Search for" + search
    query = "SELECT Name, Album, SongStreams, ReleaseDate FROM top_songs WHERE Name LIKE ?" \
            "OR Album LIKE ? OR ReleaseDate LIKE ?"
    search = "%" + search + "%"
    con = create_connection(DATABASE)
    cur = con.cursor()
    cur.execute(query, (search, search, search))
    songs_list = cur.fetchall()
    con.close()
    
    return render_template("catalouge.html", song=songs_list, tag=title)



if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)
