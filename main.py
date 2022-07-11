from flask import Flask, redirect, render_template, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///poll.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)


class Poll(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    first_site_url = db.Column(db.String(2048), nullable=False)
    first_site_developer = db.Column(db.String(250), nullable=False)
    first_site_votes = db.Column(db.Integer, default=0, nullable=False)
    first_site_img_url = db.Column(db.String(2048), nullable=False)
    first_site_about = db.Column(db.String, nullable=False)

    second_site_url = db.Column(db.String(2048), nullable=False)
    second_site_developer = db.Column(db.String(250), nullable=False)
    second_site_votes = db.Column(db.Integer, default=0, nullable=False)
    second_site_img_url = db.Column(db.String(2048), nullable=False)
    second_site_about = db.Column(db.String, nullable=False)


db.create_all()


@app.route("/")
def home():
    polls = Poll.query.all()
    return render_template("index.html", polls=polls)


@app.route("/add-new-poll")
def add_poll():
    new_poll = Poll(
        first_site_url="https://john-doe-site.com",
        first_site_developer="John Doe",
        first_site_img_url="https://john-doe-site-screenshot.jpg",
        first_site_about="Lorem Ipsum",

        second_site_url="https://jane-doe-site.com",
        second_site_developer="Jane Doe",
        second_site_img_url="https://jane-doe-site-screenshot.jpg",
        second_site_about="Lorem Ipsum"
    )
    db.session.add(new_poll)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/poll-<poll_id>")
def show_poll(poll_id):
    poll_to_show = Poll.query.get(poll_id)
    return render_template("poll.html", poll=poll_to_show)


@app.route("/poll-<poll_id>/site-1")
def show_first_site_info(poll_id):
    poll = Poll.query.get(poll_id)
    return render_template("site_info.html", poll=poll, first_site=True)


@app.route("/poll-<poll_id>/site-2")
def show_second_site_info(poll_id):
    poll = Poll.query.get(poll_id)
    return render_template("site_info.html", poll=poll)


@app.route("/poll-<poll_id>/vote-for/site-1")
def increase_first_site_votes(poll_id):
    poll = Poll.query.get(poll_id)
    poll.first_site_votes += 1
    db.session.commit()
    return redirect(url_for("show_poll", poll_id=poll_id))


@app.route("/poll-<poll_id>/vote-for/site-2")
def increase_second_site_votes(poll_id):
    poll = Poll.query.get(poll_id)
    poll.second_site_votes += 1
    db.session.commit()
    return redirect(url_for("show_poll", poll_id=poll_id))


if __name__ == "__main__":
    app.run(debug=True)
