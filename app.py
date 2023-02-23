from flask import Flask, render_template, request
from helpers import wildcard
import sqlite3

app = Flask(__name__)



connection = sqlite3.connect("./svwho.db", check_same_thread=False)
cursor = connection.cursor()

@app.route('/')
def index():
    return render_template("index.html")


@app.route('/actor', methods=["GET","POST"])
def actor():
    if request.method == "POST":
       name = request.form.get("name")
       episode = cursor.execute("SELECT primaryTitle, seasonNumber, episodeNumber FROM episodes JOIN titles ON episodes.tconst = titles.tconst WHERE episodes.tconst IN (SELECT tconst FROM principals WHERE nconst = (SELECT nconst FROM names WHERE upper(primaryName) = upper(?)))", [name]).fetchall()
       plural = "this episode:"
       
       if not episode: 
            sorry = "Sorry! According to our records, no one by that name has been in an episode of Law & Order: SVU."
            guesses = cursor.execute("SELECT DISTINCT primaryName FROM names JOIN principals ON names.nconst = principals.nconst WHERE upper(primaryName) LIKE upper(?) LIMIT 7", [wildcard(name)]).fetchall()
            return render_template("sorry.html", sorry=sorry, guesses=guesses)
       
       elif len(episode) > 10:
            plural = "many episodes!  Including..."
            return render_template("actor_results.html", data=episode[0 : 10], name=name, plural=plural)
    
       elif len(episode) > 1:
            plural = "these episodes:"
       
       return render_template("actor_results.html", data=episode, plural=plural, name=name)
       
    else:
        if request.args.get("name"):
            name = request.args.get("name")
            episode = cursor.execute("SELECT primaryTitle, seasonNumber, episodeNumber FROM episodes JOIN titles ON episodes.tconst = titles.tconst WHERE episodes.tconst IN (SELECT tconst FROM principals WHERE nconst = (SELECT nconst FROM names WHERE upper(primaryName) = upper(?)))", [name]).fetchall()
            plural = "this episode:"
       
            if not episode: 
                sorry = "Sorry! According to our records, no one by that name has been in an episode of Law & Order: SVU."
                guesses = cursor.execute("SELECT primaryName FROM names WHERE upper(primaryName) LIKE upper(?) LIMIT 7", [(name[0:-2] + '%')]).fetchall()
                return render_template("sorry.html", sorry=sorry, guesses=guesses)
       
            elif len(episode) > 10:
                plural = "many episodes!  Including..."
                return render_template("actor_results.html", data=episode[0 : 10], name=name, plural=plural)
    
            elif len(episode) > 1:
                plural = "these episodes:"
       
            return render_template("actor_results.html", data=episode, plural=plural, name=name)
       

        else: 
            return render_template("actor.html")

@app.route('/episode', methods=["GET", "POST"])
def episode():
    if request.method == "POST":
        season = request.form.get("season")
        episode = request.form.get("episode")

        if not season or not episode:
            sorry = "Uh oh! Something was wrong with your input... try again?"
            return render_template("sorry.html", sorry=sorry)
 
        cast = cursor.execute("SELECT primaryName, characters, tconst FROM names JOIN principals ON names.nconst = principals.nconst WHERE principals.tconst IN (SELECT tconst FROM episodes WHERE seasonNumber = ? AND episodeNumber = ?) AND characters != '\\N'", [season, episode]).fetchall()
        
        if not cast:
            sorry = "Sorry!  That episode doesn't exist... Probably"
            return render_template("sorry.html", sorry=sorry)
        
        tconst = cast[0][2]
        title = cursor.execute("SELECT primaryTitle FROM titles WHERE tconst = ?", [tconst]).fetchone()
        return render_template("episode_results.html", data=cast, title=title, season=season, episode=episode)


    else:
        if request.args:
            season = request.args.get("season")
            episode = request.args.get("episode")
            cast = cursor.execute("SELECT primaryName, characters, tconst FROM names JOIN principals ON names.nconst = principals.nconst WHERE principals.tconst IN (SELECT tconst FROM episodes WHERE seasonNumber = ? AND episodeNumber = ?) AND characters != '\\N'", [season, episode]).fetchall()
            tconst = cast[0][2]
            title = cursor.execute("SELECT primaryTitle FROM titles WHERE tconst = ?", [tconst]).fetchone()
            return render_template("episode_results.html", data=cast, title=title, season=season, episode=episode)

        else:   
            return render_template("episode.html")
       

if __name__ == "__main__":
    app.run(debug=True)