from flask import Flask, render_template
from blueprints.users import users_bp
from blueprints.movies import movies_bp
from blueprints.reviews import reviews_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'a_very_secret_key'

app.register_blueprint(users_bp)
app.register_blueprint(movies_bp)
app.register_blueprint(reviews_bp)


@app.route('/')
def home():
    return render_template("home.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=True)
