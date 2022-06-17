from flask import Flask,flash,url_for,redirect,render_template,request,session,abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# database path
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize a connection to the database
db = SQLAlchemy(app)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))

class Frame(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(20))
    game_id=db.Column(db.Integer)
    pins_knocked_down=db.Column(db.Integer)


@app.route('/')
def root_page():
    return render_template("hello.html")

@app.route('/api/games')
def get_games():
    games = Game.query.all()
    return render_template("index.html", games=games)

@app.route("/api/games/create", methods=["POST"])
def create():
    name = request.form.get("name")
    new_game = Game(name=name)
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for("get_games"))

@app.route("/api/games/update/<int:id>",methods = ['GET','POST'])
def update(id):
    game = Game.query.filter_by(id=id).first()
    name=request.form.get("name")
    game.name=name
    db.session.commit()
    return redirect(url_for("get_games"))

@app.route("/api/games/delete/<int:id>")
def delete(id):
    game = Game.query.filter_by(id=id).first()
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for("get_games"))
###############################################
#Frames
@app.route('/api/games/frames')
def get_frames():
    frames = Frame.query.all()
    return render_template("frame.html", frames=frames)

@app.route("/api/games/frames/create", methods=["POST"])
def create_frame():
    name = request.form.get("name")
    pins_knocked_down=request.form.get("pins_knocked_down")
    game_id=request.form.get("gameid")
    new_frame = Frame(name=name,game_id=game_id,pins_knocked_down=pins_knocked_down)
    db.session.add(new_frame)
    db.session.commit()
    return redirect(url_for("get_frames"))

@app.route("/api/games/frames/update/<int:id>",methods = ['GET','POST'])
def update_frame(id):
    frame = Frame.query.filter_by(id=id).first()
    name=request.form.get("name")
    pins_knocked_down=request.form.get("pins_knocked_down")
    if name!="":
        frame.name=name
    if pins_knocked_down!="":
        frame.pins_knocked_down=pins_knocked_down

    db.session.commit()
    return redirect(url_for("get_frames"))

@app.route("/api/games/frames/delete/<int:id>")
def delete_frame(id):
    frame = Frame.query.filter_by(id=id).first()
    db.session.delete(frame)
    db.session.commit()
    return redirect(url_for("get_frames"))

if __name__ == "__main__":
    app.run(debug=True)
