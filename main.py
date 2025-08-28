from flask import Flask, render_template
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
    
@app.route('/webpages')
def render_webpages():
    query = "SELECT Name, Album, SongStreams, ReleaseDate FROM top_songs"
    con = create_connection(DATABASE)
    cur = con.cursor

    #Query the database
    cur.execute(query)
    songs_list = cur.fetchall
    con.close()
    print(songs_list)
    return render_template("webpages.html", top_songs = songs_list)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=81)